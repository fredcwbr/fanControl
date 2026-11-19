#ifndef FAN_H
#define FAN_H

#include <stdbool.h>

/**
 * Read current fan speed (RPM) from a sysfs fan*_input file.
 */
bool fan_read_rpm(const char *fan_input_path, int *out_rpm);

/**
 * Write target PWM value (typically 0-255) to a sysfs pwm* file.
 */
bool fan_write_pwm(const char *pwm_path, int pwm_value);

/**
 * Enable manual PWM control mode (e.g. write 1 to pwm*_enable).
 */
bool fan_set_manual_mode(const char *pwm_enable_path);

/**
 * Restore automatic fan control mode (e.g. write 2 or 0 to pwm*_enable).
 */
bool fan_restore_auto_mode(const char *pwm_enable_path);

#endif /* FAN_H */
