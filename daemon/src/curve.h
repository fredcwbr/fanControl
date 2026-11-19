#ifndef CURVE_H
#define CURVE_H

#include <stdint.h>

typedef struct {
    double temp_min;     // Temperature (°C) at which fans start at min_pwm
    double temp_max;     // Temperature (°C) at which fans reach max_pwm
    uint8_t pwm_min;     // Minimum PWM (0-255)
    uint8_t pwm_max;     // Maximum PWM (0-255)
} fan_curve_t;

uint8_t curve_calculate_pwm(const fan_curve_t *curve, double current_temp);

#endif /* CURVE_H */
