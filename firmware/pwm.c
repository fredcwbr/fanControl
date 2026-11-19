#include "pwm.h"
#include <avr/io.h>

static uint8_t g_duties[NUM_CHANNELS] = {0, 0, 0, 0};
static pwm_mode_t g_mode = PWM_MODE_3PIN_LOWFREQ;
static fan_behavior_t g_behavior = FAN_BEHAVIOR_INDEPENDENT;
static bool g_hot_standby_tripped = false;

void pwm_init(pwm_mode_t mode) {
    g_mode = mode;

    // Output pins:
    // Pin 9 (PB1) = OC1A, Pin 10 (PB2) = OC1B, Pin 11 (PB3) = OC2A
    DDRB |= (1 << DDB1) | (1 << DDB2) | (1 << DDB3);
    // Pin 3 (PD3) = OC2B
    DDRD |= (1 << DDD3);

    if (mode == PWM_MODE_4PIN_25KHZ) {
        // Timer 1: Phase Correct PWM with ICR1 as TOP = 320 -> 25 kHz at 16MHz
        TCCR1A = (1 << COM1A1) | (1 << COM1B1) | (1 << WGM11);
        TCCR1B = (1 << WGM13) | (1 << CS10);
        ICR1 = 320;

        // Timer 2: Phase Correct PWM, Prescaler 8
        TCCR2A = (1 << COM2A1) | (1 << COM2B1) | (1 << WGM20);
        TCCR2B = (1 << CS21);
    } else {
        // 3-Pin Low-Side ULN Mode:
        // Timer 1: Fast PWM 8-bit (TOP = 255), Prescaler 1024 -> ~61 Hz
        TCCR1A = (1 << COM1A1) | (1 << COM1B1) | (1 << WGM10);
        TCCR1B = (1 << WGM12) | (1 << CS12) | (1 << CS10);

        // Timer 2: Fast PWM 8-bit (TOP = 255), Prescaler 1024 -> ~61 Hz
        TCCR2A = (1 << COM2A1) | (1 << COM2B1) | (1 << WGM20) | (1 << WGM21);
        TCCR2B = (1 << CS22) | (1 << CS21) | (1 << CS20);
    }

    pwm_set_all(0);
}

static void apply_hardware_pwm(uint8_t channel, uint8_t duty) {
    if (g_mode == PWM_MODE_4PIN_25KHZ) {
        uint16_t timer1_val = (uint16_t)(((uint32_t)duty * 320) / 255);
        switch (channel) {
            case 1: OCR1A = timer1_val; break;
            case 2: OCR1B = timer1_val; break;
            case 3: OCR2A = duty; break;
            case 4: OCR2B = duty; break;
        }
    } else {
        switch (channel) {
            case 1: OCR1A = duty; break;
            case 2: OCR1B = duty; break;
            case 3: OCR2A = duty; break;
            case 4: OCR2B = duty; break;
        }
    }
}

void pwm_set_channel(uint8_t channel, uint8_t duty) {
    if (channel < 1 || channel > NUM_CHANNELS) return;
    g_duties[channel - 1] = duty;
    apply_hardware_pwm(channel, duty);

    // If channel 1 is changed, update dependent channel 2 based on behavior mode
    if (channel == 1) {
        if (g_behavior == FAN_BEHAVIOR_SYMMETRIC) {
            g_duties[1] = duty;
            apply_hardware_pwm(2, duty);
        } else if (g_behavior == FAN_BEHAVIOR_ASYMMETRIC) {
            // Asymmetric: Ch2 runs at 75% of Ch1 duty
            uint8_t ch2_duty = (uint8_t)(((uint16_t)duty * 3) / 4);
            g_duties[1] = ch2_duty;
            apply_hardware_pwm(2, ch2_duty);
        } else if (g_behavior == FAN_BEHAVIOR_HOT_STANDBY) {
            if (!g_hot_standby_tripped) {
                g_duties[1] = 0; // Standby fan off while Ch1 healthy
                apply_hardware_pwm(2, 0);
            }
        }
    }
}

uint8_t pwm_get_channel(uint8_t channel) {
    if (channel < 1 || channel > NUM_CHANNELS) return 0;
    return g_duties[channel - 1];
}

void pwm_set_all(uint8_t duty) {
    for (uint8_t i = 1; i <= NUM_CHANNELS; i++) {
        g_duties[i - 1] = duty;
        apply_hardware_pwm(i, duty);
    }
}

void pwm_set_behavior(fan_behavior_t behavior) {
    g_behavior = behavior;
    g_hot_standby_tripped = false;
    pwm_set_channel(1, g_duties[0]);
}

fan_behavior_t pwm_get_behavior(void) {
    return g_behavior;
}

void pwm_update_behavior(uint16_t rpm1, uint16_t rpm2) {
    (void)rpm2;
    if (g_behavior == FAN_BEHAVIOR_HOT_STANDBY) {
        // If Fan 1 is commanded ON (> 50 PWM) but reports 0 RPM, trigger Hot Standby!
        if (g_duties[0] > 50 && rpm1 == 0) {
            if (!g_hot_standby_tripped) {
                g_hot_standby_tripped = true;
                g_duties[1] = 255; // Kick standby fan to 100%
                apply_hardware_pwm(2, 255);
            }
        } else if (g_hot_standby_tripped && rpm1 > 200) {
            // Fan 1 recovered
            g_hot_standby_tripped = false;
            g_duties[1] = 0;
            apply_hardware_pwm(2, 0);
        }
    }
}
