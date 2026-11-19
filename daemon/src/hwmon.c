#define _DEFAULT_SOURCE
#include "hwmon.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>

bool hwmon_read_temp(const char *path, double *out_temp_c) {
    if (!path || !out_temp_c) return false;

    FILE *fp = fopen(path, "r");
    if (!fp) return false;

    long millidegrees = 0;
    if (fscanf(fp, "%ld", &millidegrees) != 1) {
        fclose(fp);
        return false;
    }
    fclose(fp);

    *out_temp_c = (double)millidegrees / 1000.0;
    return true;
}

double hwmon_get_max_temp(const char *primary_path, const char *secondary_path) {
    double temp1 = -100.0;
    double temp2 = -100.0;

    bool ok1 = hwmon_read_temp(primary_path, &temp1);
    bool ok2 = hwmon_read_temp(secondary_path, &temp2);

    if (ok1 && ok2) {
        return (temp1 > temp2) ? temp1 : temp2;
    } else if (ok1) {
        return temp1;
    } else if (ok2) {
        return temp2;
    }

    return 45.0; // Safe fallback temperature if sensors cannot be read
}

void hwmon_list_devices(void) {
    const char *base = "/sys/class/hwmon";
    DIR *dir = opendir(base);
    if (!dir) return;

    printf("Available hwmon devices on this Linux PC:\n");
    struct dirent *entry;
    while ((entry = readdir(dir)) != NULL) {
        if (entry->d_name[0] == '.') continue;

        char path[512];
        snprintf(path, sizeof(path), "%s/%s/name", base, entry->d_name);

        char name[128] = "unknown";
        FILE *fp = fopen(path, "r");
        if (fp) {
            if (fgets(name, sizeof(name), fp)) {
                name[strcspn(name, "\r\n")] = '\0';
            }
            fclose(fp);
        }

        printf("  - %s: %s (%s/%s)\n", entry->d_name, name, base, entry->d_name);
    }
    closedir(dir);
}
