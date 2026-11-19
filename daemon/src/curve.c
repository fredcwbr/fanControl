#include "curve.h"

uint8_t curve_calculate_pwm(const fan_curve_t *curve, double current_temp) {
    if (!curve) return 128;

    if (current_temp <= curve->temp_min) {
        return curve->pwm_min;
    }
    if (current_temp >= curve->temp_max) {
        return curve->pwm_max;
    }

    double ratio = (current_temp - curve->temp_min) / (curve->temp_max - curve->temp_min);
    int target = (int)(curve->pwm_min + ratio * (curve->pwm_max - curve->pwm_min));

    if (target < curve->pwm_min) target = curve->pwm_min;
    if (target > curve->pwm_max) target = curve->pwm_max;

    return (uint8_t)target;
}
