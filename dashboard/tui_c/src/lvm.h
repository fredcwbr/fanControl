#ifndef LVM_H
#define LVM_H

#define MAX_VGS 8
#define MAX_LVS 32

typedef struct {
    char vg_name[32];
    char lv_name[32];
    char dm_name[16];
    double size_gb;
} lvm_lv_t;

typedef struct {
    char name[32];
    int lv_count;
    double allocated_gb;
} lvm_vg_t;

typedef struct {
    int vg_count;
    lvm_vg_t vgs[MAX_VGS];
    int lv_count;
    lvm_lv_t lvs[MAX_LVS];
} lvm_info_t;

void lvm_read_all(lvm_info_t *info);

#endif /* LVM_H */
