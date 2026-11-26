#ifndef HWMON_H
#define HWMON_H

#define MAX_SENSORS 16
#define MAX_TEMPS   16
#define MAX_FANS    8
#define MAX_PWMS    8

typedef struct {
    char label[32];
    double temp_c;
    double crit_c;
} temp_sensor_t;

typedef struct {
    char label[32];
    int rpm;
} fan_sensor_t;

typedef struct {
    char name[16];
    int value;
    double duty_pct;
} pwm_sensor_t;

typedef struct {
    char id[16];
    char name[32];
    int temp_count;
    temp_sensor_t temps[MAX_TEMPS];
    int fan_count;
    fan_sensor_t fans[MAX_FANS];
    int pwm_count;
    pwm_sensor_t pwms[MAX_PWMS];
} hwmon_device_t;

typedef struct {
    int count;
    hwmon_device_t devices[MAX_SENSORS];
} hwmon_info_t;

void hwmon_read_all(hwmon_info_t *info);

#endif /* HWMON_H */
