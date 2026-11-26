#define _DEFAULT_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <glob.h>
#include <unistd.h>
#include "hwmon.h"

static void read_str_file(const char *path, char *out, size_t max_len) {
    FILE *f = fopen(path, "r");
    if (!f) return;
    if (fgets(out, max_len, f)) {
        size_t len = strlen(out);
        while (len > 0 && (out[len - 1] == '\n' || out[len - 1] == '\r')) {
            out[--len] = '\0';
        }
    }
    fclose(f);
}

static long read_long_file(const char *path, long default_val) {
    FILE *f = fopen(path, "r");
    if (!f) return default_val;
    long val = default_val;
    if (fscanf(f, "%ld", &val) != 1) {
        val = default_val;
    }
    fclose(f);
    return val;
}

void hwmon_read_all(hwmon_info_t *info) {
    if (!info) return;
    memset(info, 0, sizeof(hwmon_info_t));

    glob_t g;
    if (glob("/sys/class/hwmon/hwmon*", 0, NULL, &g) != 0) {
        return;
    }

    for (size_t i = 0; i < g.gl_pathc && info->count < MAX_SENSORS; i++) {
        const char *dir = g.gl_pathv[i];
        hwmon_device_t *dev = &info->devices[info->count];

        const char *slash = strrchr(dir, '/');
        snprintf(dev->id, sizeof(dev->id), "%s", slash ? slash + 1 : dir);

        char name_path[256];
        snprintf(name_path, sizeof(name_path), "%s/name", dir);
        read_str_file(name_path, dev->name, sizeof(dev->name));
        if (dev->name[0] == '\0') {
            snprintf(dev->name, sizeof(dev->name), "unknown");
        }

        // Temperatures
        glob_t tg;
        char temp_pattern[256];
        snprintf(temp_pattern, sizeof(temp_pattern), "%s/temp*_input", dir);
        if (glob(temp_pattern, 0, NULL, &tg) == 0) {
            for (size_t j = 0; j < tg.gl_pathc && dev->temp_count < MAX_TEMPS; j++) {
                temp_sensor_t *t = &dev->temps[dev->temp_count];
                long raw_temp = read_long_file(tg.gl_pathv[j], -1);
                if (raw_temp >= 0) {
                    t->temp_c = raw_temp / 1000.0;

                    // Label
                    char label_path[1024];
                    char base_path[256];
                    strncpy(base_path, tg.gl_pathv[j], sizeof(base_path) - 1);
                    base_path[sizeof(base_path) - 1] = '\0';
                    char *input_pos = strstr(base_path, "_input");
                    if (input_pos) *input_pos = '\0';

                    snprintf(label_path, sizeof(label_path), "%s_label", base_path);
                    read_str_file(label_path, t->label, sizeof(t->label));
                    if (t->label[0] == '\0') {
                        const char *b_slash = strrchr(base_path, '/');
                        snprintf(t->label, sizeof(t->label), "%.31s", b_slash ? b_slash + 1 : base_path);
                    }

                    // Crit
                    char crit_path[512];
                    snprintf(crit_path, sizeof(crit_path), "%s_crit", base_path);
                    long raw_crit = read_long_file(crit_path, -1);
                    t->crit_c = (raw_crit > 0) ? (raw_crit / 1000.0) : 0.0;

                    dev->temp_count++;
                }
            }
            globfree(&tg);
        }

        // Fans
        glob_t fg;
        char fan_pattern[256];
        snprintf(fan_pattern, sizeof(fan_pattern), "%s/fan*_input", dir);
        if (glob(fan_pattern, 0, NULL, &fg) == 0) {
            for (size_t j = 0; j < fg.gl_pathc && dev->fan_count < MAX_FANS; j++) {
                fan_sensor_t *fn = &dev->fans[dev->fan_count];
                long rpm = read_long_file(fg.gl_pathv[j], -1);
                if (rpm >= 0) {
                    fn->rpm = (int)rpm;
                    char label_path[1024];
                    char base_path[256];
                    strncpy(base_path, fg.gl_pathv[j], sizeof(base_path) - 1);
                    base_path[sizeof(base_path) - 1] = '\0';
                    char *input_pos = strstr(base_path, "_input");
                    if (input_pos) *input_pos = '\0';

                    snprintf(label_path, sizeof(label_path), "%s_label", base_path);
                    read_str_file(label_path, fn->label, sizeof(fn->label));
                    if (fn->label[0] == '\0') {
                        const char *b_slash = strrchr(base_path, '/');
                        snprintf(fn->label, sizeof(fn->label), "%.31s", b_slash ? b_slash + 1 : base_path);
                    }
                    dev->fan_count++;
                }
            }
            globfree(&fg);
        }

        // PWMs
        glob_t pg;
        char pwm_pattern[256];
        snprintf(pwm_pattern, sizeof(pwm_pattern), "%s/pwm[0-9]*", dir);
        if (glob(pwm_pattern, 0, NULL, &pg) == 0) {
            for (size_t j = 0; j < pg.gl_pathc && dev->pwm_count < MAX_PWMS; j++) {
                const char *p_file = pg.gl_pathv[j];
                if (strstr(p_file, "_enable") || strstr(p_file, "_mode")) {
                    continue;
                }
                pwm_sensor_t *pwm = &dev->pwms[dev->pwm_count];
                long val = read_long_file(p_file, -1);
                if (val >= 0) {
                    const char *b_slash = strrchr(p_file, '/');
                    snprintf(pwm->name, sizeof(pwm->name), "%s", b_slash ? b_slash + 1 : p_file);
                    pwm->value = (int)val;
                    pwm->duty_pct = (pwm->value / 255.0) * 100.0;
                    dev->pwm_count++;
                }
            }
            globfree(&pg);
        }

        if (dev->temp_count > 0 || dev->fan_count > 0 || dev->pwm_count > 0) {
            info->count++;
        }
    }
    globfree(&g);
}
