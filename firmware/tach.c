#include "tach.h"
#include <avr/io.h>
#include <avr/interrupt.h>

static volatile uint16_t pulse_count[4] = {0, 0, 0, 0};
static volatile uint16_t rpm_values[4] = {0, 0, 0, 0};
static volatile uint16_t ms_counter = 0;
static uint8_t last_pind = 0;

void tach_init(void) {
    // Pin 2 (PD2) = Fan 1 Tach (INT0)
    // Pin 4 (PD4) = Fan 2 Tach (PCINT20)
    // Pin 5 (PD5) = Fan 3 Tach (PCINT21)
    // Pin 6 (PD6) = Fan 4 Tach (PCINT22)

    // Set as inputs with internal pull-ups enabled
    DDRD &= ~((1 << DDD2) | (1 << DDD4) | (1 << DDD5) | (1 << DDD6));
    PORTD |= (1 << PORTD2) | (1 << PORTD4) | (1 << PORTD5) | (1 << PORTD6);

    // INT0 on falling edge
    EICRA |= (1 << ISC01);
    EIMSK |= (1 << INT0);

    // Enable PCINT2 for pins 4, 5, 6
    PCICR |= (1 << PCIE2);
    PCMSK2 |= (1 << PCINT20) | (1 << PCINT21) | (1 << PCINT22);

    last_pind = PIND;
}

ISR(INT0_vect) {
    pulse_count[0]++;
}

ISR(PCINT2_vect) {
    uint8_t current = PIND;
    uint8_t changed = current ^ last_pind;
    last_pind = current;

    // Detect falling edges (transition from high to low)
    if ((changed & (1 << PIND4)) && !(current & (1 << PIND4))) {
        pulse_count[1]++;
    }
    if ((changed & (1 << PIND5)) && !(current & (1 << PIND5))) {
        pulse_count[2]++;
    }
    if ((changed & (1 << PIND6)) && !(current & (1 << PIND6))) {
        pulse_count[3]++;
    }
}

void tach_tick_1ms(void) {
    ms_counter++;
    if (ms_counter >= 1000) {
        ms_counter = 0;
        for (uint8_t i = 0; i < 4; i++) {
            // 2 pulses per revolution => RPM = (pulses / 2) * 60 = pulses * 30
            rpm_values[i] = pulse_count[i] * 30;
            pulse_count[i] = 0;
        }
    }
}

uint16_t tach_get_rpm(uint8_t channel) {
    if (channel < 1 || channel > 4) return 0;
    return rpm_values[channel - 1];
}
