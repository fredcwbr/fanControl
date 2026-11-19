#define _DEFAULT_SOURCE
#include "fan.h"
#include "fancontrol.h"

#include <stdio.h>
#include <stdlib.h>

bool fan_read_rpm(const char *fan_input_path, int *out_rpm) {
    if (!fan_input_path || !out_rpm) {
        return false;
    }

    FILE *fp = fopen(fan_input_path, "r");
    if (!fp) {
        return false;
    }

    int rpm = 0;
    if (fscanf(fp, "%d", &rpm) != 1) {
        fclose(fp);
        return false;
    }
    fclose(fp);

    *out_rpm = rpm;
    return true;
}

bool fan_write_pwm(const char *pwm_path, int pwm_value) {
    if (!pwm_path) {
        return false;
    }

    if (pwm_value < 0) pwm_value = 0;
    if (pwm_value > 255) pwm_value = 255;

    FILE *fp = fopen(pwm_path, "w");
    if (!fp) {
        return false;
    }

    int written = fprintf(fp, "%d\n", pwm_value);
    fclose(fp);

    return written > 0;
}

bool fan_set_manual_mode(const char *pwm_enable_path) {
    if (!pwm_enable_path) {
        return true; // Optional
    }

    FILE *fp = fopen(pwm_enable_path, "w");
    if (!fp) {
        return false;
    }

    // Usually '1' represents manual control in hwmon
    int written = fprintf(fp, "1\n");
    fclose(fp);
    return written > 0;
}

bool fan_restore_auto_mode(const char *pwm_enable_path) {
    if (!pwm_enable_path) {
        return true; // Optional
    }

    FILE *fp = fopen(pwm_enable_path, "w");
    if (!fp) {
        return false;
    }

    // Usually '2' or '0' represents automatic BIOS/hardware control
    int written = fprintf(fp, "2\n");
    fclose(fp);
    return written > 0;
}
