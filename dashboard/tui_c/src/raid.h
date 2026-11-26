#ifndef RAID_H
#define RAID_H

#include <stdbool.h>

#define MAX_RAIDS   8
#define MAX_MEMBERS 16

typedef struct {
    char name[32];
    char state[32];
    int slot;
    int errors;
} raid_member_t;

typedef struct {
    char name[16];
    char level[16];
    char state[16];
    char health_mask[16];
    bool degraded;
    int total_disks;
    int active_disks;
    double size_gb;
    char sync_action[16];
    int member_count;
    raid_member_t members[MAX_MEMBERS];
} raid_array_t;

typedef struct {
    int count;
    raid_array_t arrays[MAX_RAIDS];
} raid_info_t;

void raid_read_all(raid_info_t *info);

#endif /* RAID_H */
