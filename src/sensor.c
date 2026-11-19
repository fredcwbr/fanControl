#define _DEFAULT_SOURCE
#include "sensor.h"
#include "fancontrol.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <unistd.h>

bool sensor_read_temp(const char *temp_path, double *out_temp_c) {
    if (!temp_path || !out_temp_c) {
        return false;
    }

    FILE *fp = fopen(temp_path, "r");
    if (!fp) {
        return false;
    }

    long raw_val = 0;
    if (fscanf(fp, "%ld", &raw_val) != 1) {
        fclose(fp);
        return false;
    }
    fclose(fp);

    // hwmon temp*_input reports millidegrees Celsius
    *out_temp_c = (double)raw_val / 1000.0;
    return true;
}

void sensor_discover(void) {
    const char *hwmon_base = "/sys/class/hwmon";
    DIR *dir = opendir(hwmon_base);
    if (!dir) {
        LOG_WARN("Could not open %s for device discovery", hwmon_base);
        return;
    }

    LOG_INFO("Discovered hwmon devices:");
    struct dirent *entry;
    while ((entry = readdir(dir)) != NULL) {
        if (entry->d_name[0] == '.') {
            continue;
        }

        char name_path[512];
        snprintf(name_path, sizeof(name_path), "%s/%s/name", hwmon_base, entry->d_name);

        char dev_name[128] = "unknown";
        FILE *fp = fopen(name_path, "r");
        if (fp) {
            if (fgets(dev_name, sizeof(dev_name), fp)) {
                dev_name[strcspn(dev_name, "\r\n")] = '\0';
            }
            fclose(fp);
        }

        LOG_INFO("  - %s (%s): %s/%s", entry->d_name, dev_name, hwmon_base, entry->d_name);
    }
    closedir(dir);
}
