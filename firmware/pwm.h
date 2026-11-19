#ifndef PWM_H
#define PWM_H

#include <stdint.h>
#include <stdbool.h>

#define NUM_CHANNELS 4

typedef enum {
    PWM_MODE_3PIN_LOWFREQ, // ~61Hz for 3-pin low-side ULN driving
    PWM_MODE_4PIN_25KHZ    // 25kHz for 4-pin PWM fans
} pwm_mode_t;

typedef enum {
    FAN_BEHAVIOR_INDEPENDENT = 0,
    FAN_BEHAVIOR_SYMMETRIC,   // Ch2 mirrors Ch1
    FAN_BEHAVIOR_ASYMMETRIC,  // Ch2 runs at programmed offset
    FAN_BEHAVIOR_HOT_STANDBY  // Ch2 kicks in at 100% if Ch1 stalls
} fan_behavior_t;

void pwm_init(pwm_mode_t mode);
void pwm_set_channel(uint8_t channel, uint8_t duty);
uint8_t pwm_get_channel(uint8_t channel);
void pwm_set_all(uint8_t duty);
void pwm_set_behavior(fan_behavior_t behavior);
fan_behavior_t pwm_get_behavior(void);
void pwm_update_behavior(uint16_t rpm1, uint16_t rpm2);

#endif /* PWM_H */
