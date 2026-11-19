#ifndef CONFIG_H
#define CONFIG_H

#include <stdbool.h>

#define MAX_PATH_LEN 256

typedef struct {
    char temp_input_path[MAX_PATH_LEN];
    char fan_input_path[MAX_PATH_LEN];
    char pwm_path[MAX_PATH_LEN];
    char pwm_enable_path[MAX_PATH_LEN];

    double temp_min;      // Temperature below which fan is at min_pwm (°C)
    double temp_max;      // Temperature above which fan is at max_pwm (°C)
    int pwm_min;          // Minimum PWM (0-255)
    int pwm_max;          // Maximum PWM (0-255)

    int poll_interval_ms; // Poll interval in milliseconds
} fan_config_t;

void config_set_defaults(fan_config_t *cfg);
bool config_load_file(const char *filepath, fan_config_t *cfg);
int config_calculate_pwm(const fan_config_t *cfg, double current_temp);

#endif /* CONFIG_H */
