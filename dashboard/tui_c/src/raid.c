#define _DEFAULT_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <glob.h>
#include <unistd.h>
#include "raid.h"

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

void raid_read_all(raid_info_t *info) {
    if (!info) return;
    memset(info, 0, sizeof(raid_info_t));

    glob_t g;
    if (glob("/sys/block/md*", 0, NULL, &g) != 0) {
        return;
    }

    for (size_t i = 0; i < g.gl_pathc && info->count < MAX_RAIDS; i++) {
        const char *md_path = g.gl_pathv[i];
        const char *slash = strrchr(md_path, '/');
        const char *md_name = slash ? slash + 1 : md_path;

        char md_dir[256];
        snprintf(md_dir, sizeof(md_dir), "%s/md", md_path);
        if (access(md_dir, F_OK) != 0) continue;

        raid_array_t *arr = &info->arrays[info->count];
        snprintf(arr->name, sizeof(arr->name), "%s", md_name);

        char p[512];
        snprintf(p, sizeof(p), "%s/level", md_dir);
        read_str_f(p, arr->level, sizeof(arr->level));

        snprintf(p, sizeof(p), "%s/array_state", md_dir);
        read_str_f(p, arr->state, sizeof(arr->state));

        snprintf(p, sizeof(p), "%s/sync_action", md_dir);
        read_str_f(p, arr->sync_action, sizeof(arr->sync_action));

        snprintf(p, sizeof(p), "%s/degraded", md_dir);
        long deg = read_long_f(p, 0);
        arr->degraded = (deg == 1);

        snprintf(p, sizeof(p), "%s/raid_disks", md_dir);
        arr->total_disks = (int)read_long_f(p, 0);

        snprintf(p, sizeof(p), "%s/size", md_path);
        long sz = read_long_f(p, 0);
        arr->size_gb = (double)sz * 512.0 / (1024.0 * 1024.0 * 1024.0);

        // Members
        glob_t mg;
        char member_pattern[512];
        snprintf(member_pattern, sizeof(member_pattern), "%s/dev-*", md_dir);
        if (glob(member_pattern, 0, NULL, &mg) == 0) {
            for (size_t m = 0; m < mg.gl_pathc && arr->member_count < MAX_MEMBERS; m++) {
                const char *dpath = mg.gl_pathv[m];
                const char *dslash = strrchr(dpath, '/');
                const char *dname = dslash ? dslash + 1 : dpath;
                if (strncmp(dname, "dev-", 4) == 0) dname += 4;

                raid_member_t *mem = &arr->members[arr->member_count];
                snprintf(mem->name, sizeof(mem->name), "%s", dname);

                char mp[512];
                snprintf(mp, sizeof(mp), "%s/state", dpath);
                read_str_f(mp, mem->state, sizeof(mem->state));

                snprintf(mp, sizeof(mp), "%s/slot", dpath);
                mem->slot = (int)read_long_f(mp, -1);

                snprintf(mp, sizeof(mp), "%s/errors", dpath);
                mem->errors = (int)read_long_f(mp, 0);

                if (strstr(mem->state, "in_sync")) {
                    arr->active_disks++;
                }

                arr->member_count++;
            }
            globfree(&mg);
        }

        // Read health mask from /proc/mdstat
        FILE *mf = fopen("/proc/mdstat", "r");
        if (mf) {
            char line[256];
            bool found_md = false;
            while (fgets(line, sizeof(line), mf)) {
                if (strncmp(line, md_name, strlen(md_name)) == 0 && (line[strlen(md_name)] == ' ' || line[strlen(md_name)] == ':')) {
                    found_md = true;
                    continue;
                }
                if (found_md) {
                    char *u_pos = strchr(line, '[');
                    while (u_pos) {
                        char *close_pos = strchr(u_pos, ']');
                        if (close_pos && (strstr(u_pos, "U") || strstr(u_pos, "_"))) {
                            size_t mlen = close_pos - u_pos + 1;
                            if (mlen < sizeof(arr->health_mask)) {
                                strncpy(arr->health_mask, u_pos, mlen);
                                arr->health_mask[mlen] = '\0';
                            }
                            break;
                        }
                        u_pos = strchr(close_pos + 1, '[');
                    }
                    break;
                }
            }
            fclose(mf);
        }

        info->count++;
    }
    globfree(&g);
}
