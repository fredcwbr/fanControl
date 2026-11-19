#define _DEFAULT_SOURCE
#include "config.h"
#include "fancontrol.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void safe_copy(char *dest, size_t dest_size, const char *src) {
    if (!dest || dest_size == 0 || !src) return;
    snprintf(dest, dest_size, "%s", src);
}

void config_set_defaults(fan_config_t *cfg) {
    if (!cfg) return;

    memset(cfg, 0, sizeof(*cfg));
    safe_copy(cfg->temp_input_path, sizeof(cfg->temp_input_path), "/sys/class/hwmon/hwmon1/temp1_input");
    safe_copy(cfg->pwm_path, sizeof(cfg->pwm_path), "/sys/class/hwmon/hwmon1/pwm1");
    safe_copy(cfg->pwm_enable_path, sizeof(cfg->pwm_enable_path), "/sys/class/hwmon/hwmon1/pwm1_enable");

    cfg->temp_min = 40.0;
    cfg->temp_max = 80.0;
    cfg->pwm_min = 64;   // ~25%
    cfg->pwm_max = 255;  // 100%
    cfg->poll_interval_ms = 1000;
}

bool config_load_file(const char *filepath, fan_config_t *cfg) {
    if (!filepath || !cfg) return false;

    FILE *fp = fopen(filepath, "r");
    if (!fp) {
        LOG_WARN("Could not open config file '%s'. Using defaults.", filepath);
        return false;
    }

    char line[512];
    while (fgets(line, sizeof(line), fp)) {
        char *comment = strchr(line, '#');
        if (comment) *comment = '\0';

        char key[128];
        char val[MAX_PATH_LEN];
        if (sscanf(line, " %127[^= ] = %255s", key, val) == 2) {
            if (strcmp(key, "temp_input_path") == 0) {
                safe_copy(cfg->temp_input_path, sizeof(cfg->temp_input_path), val);
            } else if (strcmp(key, "fan_input_path") == 0) {
                safe_copy(cfg->fan_input_path, sizeof(cfg->fan_input_path), val);
            } else if (strcmp(key, "pwm_path") == 0) {
                safe_copy(cfg->pwm_path, sizeof(cfg->pwm_path), val);
            } else if (strcmp(key, "pwm_enable_path") == 0) {
                safe_copy(cfg->pwm_enable_path, sizeof(cfg->pwm_enable_path), val);
            } else if (strcmp(key, "temp_min") == 0) {
                cfg->temp_min = atof(val);
            } else if (strcmp(key, "temp_max") == 0) {
                cfg->temp_max = atof(val);
            } else if (strcmp(key, "pwm_min") == 0) {
                cfg->pwm_min = atoi(val);
            } else if (strcmp(key, "pwm_max") == 0) {
                cfg->pwm_max = atoi(val);
            } else if (strcmp(key, "poll_interval_ms") == 0) {
                cfg->poll_interval_ms = atoi(val);
            }
        }
    }

    fclose(fp);
    return true;
}

int config_calculate_pwm(const fan_config_t *cfg, double current_temp) {
    if (!cfg) return 0;

    if (current_temp <= cfg->temp_min) {
        return cfg->pwm_min;
    }
    if (current_temp >= cfg->temp_max) {
        return cfg->pwm_max;
    }

    // Linear interpolation between temp_min and temp_max
    double ratio = (current_temp - cfg->temp_min) / (cfg->temp_max - cfg->temp_min);
    int target_pwm = (int)(cfg->pwm_min + ratio * (cfg->pwm_max - cfg->pwm_min));

    if (target_pwm < cfg->pwm_min) target_pwm = cfg->pwm_min;
    if (target_pwm > cfg->pwm_max) target_pwm = cfg->pwm_max;

    return target_pwm;
}
