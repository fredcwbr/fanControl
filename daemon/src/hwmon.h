#ifndef HWMON_H
#define HWMON_H

#include <stdbool.h>

bool hwmon_read_temp(const char *path, double *out_temp_c);
double hwmon_get_max_temp(const char *primary_path, const char *secondary_path);
void hwmon_list_devices(void);

#endif /* HWMON_H */
