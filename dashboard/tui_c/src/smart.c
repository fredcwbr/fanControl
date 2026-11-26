#define _DEFAULT_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <glob.h>
#include <unistd.h>
#include <ctype.h>
#include "smart.h"

static void read_str(const char *path, char *out, size_t max_len) {
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

static void query_smartctl(disk_smart_t *d) {
    char cmd[256];
    // Try smartctl -j -a, if failure try with -d sat
    snprintf(cmd, sizeof(cmd), "smartctl -j -a %s 2>/dev/null", d->dev);
    FILE *fp = popen(cmd, "r");
    if (!fp) {
        d->has_access = false;
        return;
    }

    char *buf = malloc(65536);
    if (!buf) {
        pclose(fp);
        d->has_access = false;
        return;
    }

    size_t total = 0;
    while (!feof(fp) && total < 65530) {
        size_t n = fread(buf + total, 1, 4096, fp);
        if (n == 0) break;
        total += n;
    }
    buf[total] = '\0';
    pclose(fp);

    // If sat layer error occurred, retry with -d sat
    if (strstr(buf, "SAT layer") || (total < 50 && !strstr(buf, "smart_status"))) {
        snprintf(cmd, sizeof(cmd), "smartctl -j -a -d sat %s 2>/dev/null", d->dev);
        fp = popen(cmd, "r");
        if (fp) {
            total = 0;
            while (!feof(fp) && total < 65530) {
                size_t n = fread(buf + total, 1, 4096, fp);
                if (n == 0) break;
                total += n;
            }
            buf[total] = '\0';
            pclose(fp);
        }
    }

    // Check if we got valid smart status
    char *status_pos = strstr(buf, "\"passed\":");
    if (status_pos) {
        d->has_access = true;
        if (strstr(status_pos, "true")) {
            snprintf(d->status, sizeof(d->status), "PASSED");
            d->health_pct = 100;
        } else {
            snprintf(d->status, sizeof(d->status), "FAILED");
            d->health_pct = 0;
        }

        // Temperature
        char *temp_pos = strstr(buf, "\"current\":");
        if (temp_pos) {
            int t = 0;
            if (sscanf(temp_pos, "\"current\": %d", &t) == 1) {
                d->temp_c = t;
            }
        }

        // Search attribute tables for Reallocated, Pending, Uncorrectable, CRC
        char *p = buf;
        while ((p = strstr(p, "\"name\":")) != NULL) {
            char attr_name[64] = {0};
            if (sscanf(p, "\"name\": \"%63[^\"]\"", attr_name) == 1) {
                // Find "value": inside "raw"
                char *raw_pos = strstr(p, "\"raw\":");
                if (raw_pos && (raw_pos - p) < 300) {
                    char *val_pos = strstr(raw_pos, "\"value\":");
                    if (val_pos) {
                        int rval = 0;
                        if (sscanf(val_pos, "\"value\": %d", &rval) == 1) {
                            if (strcmp(attr_name, "Reallocated_Sector_Ct") == 0) {
                                d->reallocated_sectors = rval;
                                if (rval > 0) d->health_pct = (rval > 10) ? 50 : 85;
                            } else if (strcmp(attr_name, "Current_Pending_Sector") == 0) {
                                d->pending_sectors = rval;
                            } else if (strcmp(attr_name, "Offline_Uncorrectable") == 0) {
                                d->uncorrectable_sectors = rval;
                            } else if (strcmp(attr_name, "UDMA_CRC_Error_Count") == 0) {
                                d->crc_errors = rval;
                            } else if ((strcmp(attr_name, "Temperature_Celsius") == 0 ||
                                        strcmp(attr_name, "Airflow_Temperature_Cel") == 0) && d->temp_c == 0) {
                                d->temp_c = rval;
                            }
                        }
                    }
                }
            }
            p += 7;
        }
    } else {
        d->has_access = false;
        snprintf(d->status, sizeof(d->status), "UNKNOWN");
    }

    free(buf);
}

void smart_read_all(disks_info_t *info, bool demo_mode) {
    if (!info) return;
    memset(info, 0, sizeof(disks_info_t));

    glob_t g;
    if (glob("/sys/block/*", 0, NULL, &g) != 0) {
        return;
    }

    for (size_t i = 0; i < g.gl_pathc && info->count < MAX_DISKS; i++) {
        const char *bpath = g.gl_pathv[i];
        const char *slash = strrchr(bpath, '/');
        const char *devname = slash ? slash + 1 : bpath;

        if (strncmp(devname, "sd", 2) != 0 && strncmp(devname, "nvme", 4) != 0 && strncmp(devname, "vd", 2) != 0) {
            continue;
        }

        char size_path[256];
        snprintf(size_path, sizeof(size_path), "%s/size", bpath);
        FILE *sf = fopen(size_path, "r");
        if (!sf) continue;
        long blocks = 0;
        if (fscanf(sf, "%ld", &blocks) != 1 || blocks <= 0) {
            fclose(sf);
            continue;
        }
        fclose(sf);

        disk_smart_t *d = &info->disks[info->count];
        snprintf(d->name, sizeof(d->name), "%s", devname);
        snprintf(d->dev, sizeof(d->dev), "/dev/%s", devname);
        d->size_gb = (double)blocks * 512.0 / (1024.0 * 1024.0 * 1024.0);

        char model_path[256];
        snprintf(model_path, sizeof(model_path), "%s/device/model", bpath);
        read_str(model_path, d->model, sizeof(d->model));
        if (d->model[0] == '\0') {
            snprintf(d->model, sizeof(d->model), "Desconhecido");
        }

        char rot_path[256];
        snprintf(rot_path, sizeof(rot_path), "%s/queue/rotational", bpath);
        char rot_str[8] = {0};
        read_str(rot_path, rot_str, sizeof(rot_str));
        if (strncmp(devname, "nvme", 4) == 0) {
            snprintf(d->type, sizeof(d->type), "NVMe");
        } else if (rot_str[0] == '1') {
            snprintf(d->type, sizeof(d->type), "HDD");
        } else {
            snprintf(d->type, sizeof(d->type), "SSD");
        }

        if (demo_mode) {
            d->has_access = true;
            int seed = 0;
            for (const char *c = devname; *c; c++) seed += *c;
            d->temp_c = 32 + (seed % 14);
            snprintf(d->status, sizeof(d->status), "PASSED");
            d->health_pct = 100 - (seed % 7);
            d->reallocated_sectors = (seed % 3 == 0) ? (seed % 4) : 0;
            d->pending_sectors = 0;
            d->uncorrectable_sectors = 0;
            d->crc_errors = 0;
            d->ata_errors = 0;
        } else {
            query_smartctl(d);
        }

        info->count++;
    }
    globfree(&g);
}
