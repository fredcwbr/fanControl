#ifndef PWM_H
#define PWM_H

#include <stdint.h>

#define NUM_CHANNELS 4

typedef enum {
    PWM_MODE_3PIN_LOWFREQ, // ~61Hz - 122Hz for 3-pin low-side ULN driving
    PWM_MODE_4PIN_25KHZ    // 25kHz standard for 4-pin PWM fans
} pwm_mode_t;

void pwm_init(pwm_mode_t mode);
void pwm_set_channel(uint8_t channel, uint8_t duty);
uint8_t pwm_get_channel(uint8_t channel);
void pwm_set_all(uint8_t duty);

#endif /* PWM_H */
