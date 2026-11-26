#define _DEFAULT_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <glob.h>
#include <unistd.h>
#include "lvm.h"

static void read_str_f(const char *path, char *out, size_t max_len) {
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

static long read_long_f(const char *path, long def_val) {
    FILE *f = fopen(path, "r");
    if (!f) return def_val;
    long val = def_val;
    if (fscanf(f, "%ld", &val) != 1) {
        val = def_val;
    }
    fclose(f);
    return val;
}

void lvm_read_all(lvm_info_t *info) {
    if (!info) return;
    memset(info, 0, sizeof(lvm_info_t));

    glob_t g;
    if (glob("/sys/block/dm-*", 0, NULL, &g) != 0) {
        return;
    }

    for (size_t i = 0; i < g.gl_pathc && info->lv_count < MAX_LVS; i++) {
        const char *dm_path = g.gl_pathv[i];
        const char *slash = strrchr(dm_path, '/');
        const char *dm_name = slash ? slash + 1 : dm_path;

        char p[512];
        char uuid[128] = {0};
        snprintf(p, sizeof(p), "%s/dm/uuid", dm_path);
        read_str_f(p, uuid, sizeof(uuid));

        char raw_name[128] = {0};
        snprintf(p, sizeof(p), "%s/dm/name", dm_path);
        read_str_f(p, raw_name, sizeof(raw_name));

        if (strncmp(uuid, "LVM-", 4) != 0 && strchr(raw_name, '-') == NULL) {
            continue;
        }

        snprintf(p, sizeof(p), "%s/size", dm_path);
        long sz = read_long_f(p, 0);
        double size_gb = (double)sz * 512.0 / (1024.0 * 1024.0 * 1024.0);

        // Parse VG and LV from raw_name: e.g. "vgSDD-W8" -> vg="vgSDD", lv="W8"
        char vg_buf[32] = {0};
        char lv_buf[32] = {0};

        char *hyphen = strchr(raw_name, '-');
        if (hyphen) {
            size_t vg_len = hyphen - raw_name;
            if (vg_len >= sizeof(vg_buf)) vg_len = sizeof(vg_buf) - 1;
            strncpy(vg_buf, raw_name, vg_len);
            vg_buf[vg_len] = '\0';
            snprintf(lv_buf, sizeof(lv_buf), "%s", hyphen + 1);
        } else {
            snprintf(vg_buf, sizeof(vg_buf), "Outros");
            snprintf(lv_buf, sizeof(lv_buf), "%s", raw_name);
        }

        lvm_lv_t *lv = &info->lvs[info->lv_count++];
        snprintf(lv->vg_name, sizeof(lv->vg_name), "%s", vg_buf);
        snprintf(lv->lv_name, sizeof(lv->lv_name), "%s", lv_buf);
        snprintf(lv->dm_name, sizeof(lv->dm_name), "%s", dm_name);
        lv->size_gb = size_gb;

        // Group into VG
        int found_vg = -1;
        for (int v = 0; v < info->vg_count; v++) {
            if (strcmp(info->vgs[v].name, vg_buf) == 0) {
                found_vg = v;
                break;
            }
        }
        if (found_vg >= 0) {
            info->vgs[found_vg].lv_count++;
            info->vgs[found_vg].allocated_gb += size_gb;
        } else if (info->vg_count < MAX_VGS) {
            lvm_vg_t *vg = &info->vgs[info->vg_count++];
            snprintf(vg->name, sizeof(vg->name), "%s", vg_buf);
            vg->lv_count = 1;
            vg->allocated_gb = size_gb;
        }
    }
    globfree(&g);
}
