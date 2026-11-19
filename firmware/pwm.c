#include "pwm.h"
#include <avr/io.h>

static uint8_t g_duties[NUM_CHANNELS] = {0, 0, 0, 0};
static pwm_mode_t g_mode = PWM_MODE_3PIN_LOWFREQ;

void pwm_init(pwm_mode_t mode) {
    g_mode = mode;

    // Configure pins as outputs:
    // Pin 9 (PB1) = OC1A, Pin 10 (PB2) = OC1B, Pin 11 (PB3) = OC2A
    DDRB |= (1 << DDB1) | (1 << DDB2) | (1 << DDB3);
    // Pin 3 (PD3) = OC2B
    DDRD |= (1 << DDD3);

    if (mode == PWM_MODE_4PIN_25KHZ) {
        // Timer 1: 16-bit Phase Correct PWM with ICR1 as TOP = 320 -> 25 kHz at 16MHz
        // TCCR1A: COM1A1, COM1B1, WGM11
        // TCCR1B: WGM13, CS10 (no prescaler)
        TCCR1A = (1 << COM1A1) | (1 << COM1B1) | (1 << WGM11);
        TCCR1B = (1 << WGM13) | (1 << CS10);
        ICR1 = 320;

        // Timer 2: Phase Correct PWM, Prescaler 8 -> 16MHz / (510 * 8) ~= 3.9kHz
        TCCR2A = (1 << COM2A1) | (1 << COM2B1) | (1 << WGM20);
        TCCR2B = (1 << CS21);
    } else {
        // 3-Pin Low-Side ULN Mode:
        // Timer 1: Fast PWM 8-bit (TOP = 255), Prescaler 1024 -> 16MHz / (256 * 1024) ~= 61 Hz
        TCCR1A = (1 << COM1A1) | (1 << COM1B1) | (1 << WGM10);
        TCCR1B = (1 << WGM12) | (1 << CS12) | (1 << CS10);

        // Timer 2: Fast PWM 8-bit (TOP = 255), Prescaler 1024 -> 16MHz / (256 * 1024) ~= 61 Hz
        TCCR2A = (1 << COM2A1) | (1 << COM2B1) | (1 << WGM20) | (1 << WGM21);
        TCCR2B = (1 << CS22) | (1 << CS21) | (1 << CS20);
    }

    pwm_set_all(0);
}

void pwm_set_channel(uint8_t channel, uint8_t duty) {
    if (channel < 1 || channel > NUM_CHANNELS) return;
    g_duties[channel - 1] = duty;

    if (g_mode == PWM_MODE_4PIN_25KHZ) {
        // Scale 0-255 to 0-320 for Timer 1
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

uint8_t pwm_get_channel(uint8_t channel) {
    if (channel < 1 || channel > NUM_CHANNELS) return 0;
    return g_duties[channel - 1];
}

void pwm_set_all(uint8_t duty) {
    for (uint8_t i = 1; i <= NUM_CHANNELS; i++) {
        pwm_set_channel(i, duty);
    }
}
