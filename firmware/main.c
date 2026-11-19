#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "uart.h"
#include "pwm.h"
#include "tach.h"

#define DEFAULT_FAILSAFE_PWM 180 // ~70% duty cycle
#define DEFAULT_TIMEOUT_MS 5000  // 5 seconds

static volatile uint32_t g_uptime_ms = 0;
static volatile uint32_t g_last_cmd_ms = 0;
static uint32_t g_timeout_ms = DEFAULT_TIMEOUT_MS;
static uint8_t g_failsafe_pwm = DEFAULT_FAILSAFE_PWM;
static bool g_failsafe_active = false;

// Timer 0 for 1ms system tick
static void timer0_tick_init(void) {
    // CTC Mode (WGM01 = 1)
    TCCR0A = (1 << WGM01);
    // Prescaler 64: 16MHz / 64 = 250 kHz -> 250 ticks = 1 ms
    TCCR0B = (1 << CS01) | (1 << CS00);
    OCR0A = 249;
    TIMSK0 |= (1 << OCIE0A);
}

ISR(TIMER0_COMPA_vect) {
    g_uptime_ms++;
    tach_tick_1ms();
}

static void process_command(char *cmd) {
    char resp[128];

    // Reset failsafe timer on valid received packet
    g_last_cmd_ms = g_uptime_ms;
    if (g_failsafe_active) {
        g_failsafe_active = false;
    }

    if (strncmp(cmd, "PING", 4) == 0) {
        uart_puts("PONG\n");
    } else if (strncmp(cmd, "VERSION", 7) == 0) {
        uart_puts("FAN_CONTROLLER_V1.0\n");
    } else if (strncmp(cmd, "SETALL ", 7) == 0) {
        int duty = atoi(cmd + 7);
        if (duty < 0) duty = 0;
        if (duty > 255) duty = 255;
        pwm_set_all((uint8_t)duty);
        uart_puts("OK\n");
    } else if (strncmp(cmd, "SET ", 4) == 0) {
        int ch = 0, duty = 0;
        if (sscanf(cmd + 4, "%d %d", &ch, &duty) == 2) {
            if (ch >= 1 && ch <= 4) {
                if (duty < 0) duty = 0;
                if (duty > 255) duty = 255;
                pwm_set_channel((uint8_t)ch, (uint8_t)duty);
                uart_puts("OK\n");
                return;
            }
        }
        uart_puts("ERR: INVALID_PARAMS\n");
    } else if (strncmp(cmd, "GET ", 4) == 0) {
        int ch = atoi(cmd + 4);
        if (ch >= 1 && ch <= 4) {
            snprintf(resp, sizeof(resp), "FAN %d PWM:%u RPM:%u\n",
                     ch, pwm_get_channel((uint8_t)ch), tach_get_rpm((uint8_t)ch));
            uart_puts(resp);
        } else {
            uart_puts("ERR: INVALID_CHANNEL\n");
        }
    } else if (strncmp(cmd, "STATUS", 6) == 0) {
        snprintf(resp, sizeof(resp), "STATUS CH1:%u,%u CH2:%u,%u CH3:%u,%u CH4:%u,%u\n",
                 pwm_get_channel(1), tach_get_rpm(1),
                 pwm_get_channel(2), tach_get_rpm(2),
                 pwm_get_channel(3), tach_get_rpm(3),
                 pwm_get_channel(4), tach_get_rpm(4));
        uart_puts(resp);
    } else if (strncmp(cmd, "MODE ", 5) == 0) {
        if (strncmp(cmd + 5, "4PIN", 4) == 0) {
            pwm_init(PWM_MODE_4PIN_25KHZ);
            uart_puts("OK: MODE_4PIN_25KHZ\n");
        } else {
            pwm_init(PWM_MODE_3PIN_LOWFREQ);
            uart_puts("OK: MODE_3PIN_LOWFREQ\n");
        }
    } else if (strncmp(cmd, "BEHAVIOR ", 9) == 0) {
        if (strncmp(cmd + 9, "SYMM", 4) == 0) {
            pwm_set_behavior(FAN_BEHAVIOR_SYMMETRIC);
            uart_puts("OK: SYMMETRIC\n");
        } else if (strncmp(cmd + 9, "ASYMM", 5) == 0) {
            pwm_set_behavior(FAN_BEHAVIOR_ASYMMETRIC);
            uart_puts("OK: ASYMMETRIC\n");
        } else if (strncmp(cmd + 9, "HOT_STANDBY", 11) == 0) {
            pwm_set_behavior(FAN_BEHAVIOR_HOT_STANDBY);
            uart_puts("OK: HOT_STANDBY\n");
        } else {
            pwm_set_behavior(FAN_BEHAVIOR_INDEPENDENT);
            uart_puts("OK: INDEPENDENT\n");
        }
    } else if (strncmp(cmd, "TIMEOUT ", 8) == 0) {
        int sec = atoi(cmd + 8);
        if (sec > 0 && sec <= 60) {
            g_timeout_ms = (uint32_t)sec * 1000UL;
            uart_puts("OK\n");
        } else {
            uart_puts("ERR: INVALID_TIMEOUT\n");
        }
    } else {
        uart_puts("ERR: UNKNOWN_COMMAND\n");
    }
}

int main(void) {
    // Initialize hardware peripherals
    timer0_tick_init();
    uart_init(115200);
    pwm_init(PWM_MODE_3PIN_LOWFREQ);
    tach_init();

    // Enable global interrupts
    sei();

    // Initial safe spin-up test
    pwm_set_all(100);
    _delay_ms(500);

    char cmd_buffer[64];
    uint8_t cmd_idx = 0;

    g_last_cmd_ms = g_uptime_ms;

    while (1) {
        // Check for incoming UART command characters
        while (uart_available()) {
            char c = uart_getc();
            if (c == '\r' || c == '\n') {
                if (cmd_idx > 0) {
                    cmd_buffer[cmd_idx] = '\0';
                    process_command(cmd_buffer);
                    cmd_idx = 0;
                }
            } else if (cmd_idx < sizeof(cmd_buffer) - 1) {
                cmd_buffer[cmd_idx++] = c;
            }
        }

        // Check fan behaviors (such as Hot-Standby monitoring)
        pwm_update_behavior(tach_get_rpm(1), tach_get_rpm(2));

        // Failsafe watchdog check:
        // If Linux host freezes or serial cable disconnects, ramp fans to failsafe PWM
        if (!g_failsafe_active && (g_uptime_ms - g_last_cmd_ms > g_timeout_ms)) {
            g_failsafe_active = true;
            pwm_set_all(g_failsafe_pwm);
        }
    }

    return 0;
}
