#ifndef SMART_H
#define SMART_H

#include <stdbool.h>

#define MAX_DISKS 16

typedef struct {
    char dev[32];
    char name[16];
    char model[32];
    char type[8];
    double size_gb;
    int temp_c;
    char status[16]; // PASSED, FAILED, UNKNOWN
    int health_pct;
    int reallocated_sectors;
    int pending_sectors;
    int uncorrectable_sectors;
    int crc_errors;
    int ata_errors;
    bool has_access;
} disk_smart_t;

typedef struct {
    int count;
    disk_smart_t disks[MAX_DISKS];
} disks_info_t;

void smart_read_all(disks_info_t *info, bool demo_mode);

#endif /* SMART_H */
