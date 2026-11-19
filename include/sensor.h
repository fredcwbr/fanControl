#ifndef SENSOR_H
#define SENSOR_H

#include <stdbool.h>

/**
 * Read temperature in degrees Celsius from a sysfs temperature file.
 * Returns true on success, false on failure.
 */
bool sensor_read_temp(const char *temp_path, double *out_temp_c);

/**
 * Autodetect available hwmon sensors and print their paths/names.
 */
void sensor_discover(void);

#endif /* SENSOR_H */
