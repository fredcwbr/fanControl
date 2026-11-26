#define _DEFAULT_SOURCE
#define _XOPEN_SOURCE_EXTENDED 1
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <ncursesw/ncurses.h>
#include <locale.h>

#include "hwmon.h"
#include "smart.h"
#include "raid.h"
#include "lvm.h"

#define PAIR_HEADER  1
#define PAIR_OK      2
#define PAIR_WARN    3
#define PAIR_ALERT   4
#define PAIR_CYAN    5
#define PAIR_FOOTER  6
#define PAIR_MAGENTA 7

static void init_colors(void) {
    start_color();
    use_default_colors();
    init_pair(PAIR_HEADER,  COLOR_WHITE, COLOR_BLUE);
    init_pair(PAIR_OK,      COLOR_GREEN, -1);
    init_pair(PAIR_WARN,    COLOR_YELLOW, -1);
    init_pair(PAIR_ALERT,   COLOR_RED, -1);
    init_pair(PAIR_CYAN,    COLOR_CYAN, -1);
    init_pair(PAIR_FOOTER,  COLOR_BLACK, COLOR_CYAN);
    init_pair(PAIR_MAGENTA, COLOR_MAGENTA, -1);
}

static void draw_temp_bar(WINDOW *win, int y, int x, double temp, double max_temp, int bar_width) {
    if (temp <= 0) {
        mvwprintw(win, y, x, "  --.- C [          ]");
        return;
    }
    int pair = PAIR_OK;
    if (temp >= 80.0) pair = PAIR_ALERT;
    else if (temp >= 55.0) pair = PAIR_WARN;

    wattron(win, COLOR_PAIR(pair) | A_BOLD);
    mvwprintw(win, y, x, "%5.1f C ", temp);
    wattroff(win, COLOR_PAIR(pair) | A_BOLD);

    int filled = (int)((temp / max_temp) * bar_width);
    if (filled < 0) filled = 0;
    if (filled > bar_width) filled = bar_width;

    waddch(win, '[');
    wattron(win, COLOR_PAIR(pair));
    for (int i = 0; i < filled; i++) waddch(win, '|');
    wattroff(win, COLOR_PAIR(pair));
    for (int i = filled; i < bar_width; i++) waddch(win, '.');
    waddch(win, ']');
}

int main(int argc, char *argv[]) {
    bool demo_mode = false;
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "-d") == 0 || strcmp(argv[i], "--demo") == 0) {
            demo_mode = true;
        }
    }

    setlocale(LC_ALL, "");
    initscr();
    cbreak();
    noecho();
    keypad(stdscr, TRUE);
    curs_set(0);
    timeout(1000); // 1s refresh

    if (has_colors()) {
        init_colors();
    }

    hwmon_info_t hw;
    disks_info_t disks;
    raid_info_t raids;
    lvm_info_t lvm;

    int view_mode = 0; // 0 = COMPLETO, 1 = STORAGE (SMART+RAID+LVM), 2 = SENSORES (Hwmon)
    const char *view_names[] = {"COMPLETO", "STORAGE (RAID & LVM)", "SENSORES (Hwmon)"};

    bool running = true;
    while (running) {
        hwmon_read_all(&hw);
        smart_read_all(&disks, demo_mode);
        raid_read_all(&raids);
        lvm_read_all(&lvm);

        int max_y, max_x;
        getmaxyx(stdscr, max_y, max_x);
        erase();

        // 1. Header
        attron(COLOR_PAIR(PAIR_HEADER) | A_BOLD);
        for (int i = 0; i < max_x; i++) mvaddch(0, i, ' ');
        mvprintw(0, 1, " FanControl TUI (Hardware, SMART, RAID, LVM) ");
        mvprintw(0, 48, "[Visao: %s]", view_names[view_mode]);
        if (demo_mode) {
            attron(COLOR_PAIR(PAIR_ALERT) | A_BOLD);
            mvprintw(0, 78, "[DEMO]");
            attroff(COLOR_PAIR(PAIR_ALERT) | A_BOLD);
            attron(COLOR_PAIR(PAIR_HEADER) | A_BOLD);
        }

        time_t now = time(NULL);
        char time_str[32];
        strftime(time_str, sizeof(time_str), "%H:%M:%S", localtime(&now));
        mvprintw(0, max_x - (int)strlen(time_str) - 2, "%s", time_str);
        attroff(COLOR_PAIR(PAIR_HEADER) | A_BOLD);

        int row = 2;

        // --- SECTION HWMON ---
        if (view_mode == 0 || view_mode == 2) {
            attron(COLOR_PAIR(PAIR_CYAN) | A_BOLD);
            mvprintw(row++, 1, "--- SENSORES TERMICOS E VENTOINHAS (hwmon) ---");
            attroff(COLOR_PAIR(PAIR_CYAN) | A_BOLD);

            for (int i = 0; i < hw.count && row < max_y - 14; i++) {
                hwmon_device_t *dev = &hw.devices[i];
                mvprintw(row++, 2, "[%s: %s]", dev->id, dev->name);

                for (int t = 0; t < dev->temp_count && row < max_y - 12; t++) {
                    temp_sensor_t *ts = &dev->temps[t];
                    mvprintw(row, 4, "%-16s: ", ts->label);
                    draw_temp_bar(stdscr, row, 22, ts->temp_c, 100.0, 15);
                    row++;
                }

                for (int f = 0; f < dev->fan_count && row < max_y - 12; f++) {
                    fan_sensor_t *fn = &dev->fans[f];
                    attron(COLOR_PAIR(PAIR_CYAN));
                    mvprintw(row++, 4, "%-16s: %d RPM", fn->label, fn->rpm);
                    attroff(COLOR_PAIR(PAIR_CYAN));
                }

                for (int p = 0; p < dev->pwm_count && row < max_y - 12; p++) {
                    pwm_sensor_t *pwm = &dev->pwms[p];
                    mvprintw(row++, 4, "%-16s: %d (%.1f%%)", pwm->name, pwm->value, pwm->duty_pct);
                }
            }
            row++;
        }

        // --- SECTION SMART ---
        if (view_mode == 0 || view_mode == 1) {
            attron(COLOR_PAIR(PAIR_CYAN) | A_BOLD);
            mvprintw(row++, 1, "--- METRICAS DE SMART & SAUDE DOS DISCOS ---");
            attroff(COLOR_PAIR(PAIR_CYAN) | A_BOLD);

            attron(A_UNDERLINE | A_BOLD);
            mvprintw(row++, 1, "%-8s %-16s %-5s %-7s %-8s %-9s %-7s %-10s %-8s %-8s %-8s",
                     "DISCO", "MODELO", "TIPO", "TAM", "TEMP", "STATUS", "SAUDE", "REALOC", "PEND", "UNCORR", "CRC");
            attroff(A_UNDERLINE | A_BOLD);

            for (int i = 0; i < disks.count && row < max_y - 10; i++) {
                disk_smart_t *d = &disks.disks[i];
                char size_str[16];
                snprintf(size_str, sizeof(size_str), "%.0fG", d->size_gb);

                mvprintw(row, 1, "%-8s %-16.16s %-5s %-7s", d->name, d->model, d->type, size_str);

                if (!d->has_access) {
                    attron(COLOR_PAIR(PAIR_WARN));
                    mvprintw(row, 39, "Sem permissao ioctl (use sudo)");
                    attroff(COLOR_PAIR(PAIR_WARN));
                } else {
                    if (d->temp_c > 0) {
                        int tpair = (d->temp_c > 50) ? PAIR_ALERT : ((d->temp_c > 42) ? PAIR_WARN : PAIR_OK);
                        attron(COLOR_PAIR(tpair));
                        mvprintw(row, 39, "%3d C   ", d->temp_c);
                        attroff(COLOR_PAIR(tpair));
                    } else {
                        mvprintw(row, 39, "  --    ");
                    }

                    int spair = strcmp(d->status, "PASSED") == 0 ? PAIR_OK : PAIR_ALERT;
                    attron(COLOR_PAIR(spair) | A_BOLD);
                    mvprintw(row, 48, "%-9s", d->status);
                    attroff(COLOR_PAIR(spair) | A_BOLD);

                    mvprintw(row, 58, "%3d%%  ", d->health_pct);

                    int rpair = (d->reallocated_sectors > 0) ? (PAIR_ALERT | A_BOLD) : PAIR_OK;
                    attron(COLOR_PAIR(rpair));
                    mvprintw(row, 66, "%-10d", d->reallocated_sectors);
                    attroff(COLOR_PAIR(rpair));

                    int ppair = (d->pending_sectors > 0) ? (PAIR_ALERT | A_BOLD) : PAIR_OK;
                    attron(COLOR_PAIR(ppair));
                    mvprintw(row, 77, "%-8d", d->pending_sectors);
                    attroff(COLOR_PAIR(ppair));

                    int upair = (d->uncorrectable_sectors > 0) ? (PAIR_ALERT | A_BOLD) : PAIR_OK;
                    attron(COLOR_PAIR(upair));
                    mvprintw(row, 86, "%-8d", d->uncorrectable_sectors);
                    attroff(COLOR_PAIR(upair));

                    int cpair = (d->crc_errors > 0) ? (PAIR_ALERT | A_BOLD) : PAIR_OK;
                    attron(COLOR_PAIR(cpair));
                    mvprintw(row, 95, "%-8d", d->crc_errors);
                    attroff(COLOR_PAIR(cpair));
                }
                row++;
            }
            row++;
        }

        // --- SECTION RAID & LVM ---
        if (view_mode == 0 || view_mode == 1) {
            // RAID
            attron(COLOR_PAIR(PAIR_MAGENTA) | A_BOLD);
            mvprintw(row++, 1, "--- LINUX SOFTWARE RAID (md) ---");
            attroff(COLOR_PAIR(PAIR_MAGENTA) | A_BOLD);

            for (int r = 0; r < raids.count && row < max_y - 6; r++) {
                raid_array_t *arr = &raids.arrays[r];
                int rcolor = arr->degraded ? (PAIR_ALERT | A_BOLD) : (PAIR_OK | A_BOLD);
                attron(COLOR_PAIR(rcolor));
                mvprintw(row, 2, "[%s] %-6s (%.1fG) - %s %s - Discos: %d/%d",
                         arr->name, arr->level, arr->size_gb,
                         arr->degraded ? "DEGRADADO" : "SAUDAVEL",
                         arr->health_mask, arr->active_disks, arr->total_disks);
                attroff(COLOR_PAIR(rcolor));

                // Print members
                char mbuf[256] = {0};
                for (int m = 0; m < arr->member_count; m++) {
                    char item[64];
                    snprintf(item, sizeof(item), "%s(%s,err:%d) ", arr->members[m].name, arr->members[m].state, arr->members[m].errors);
                    strncat(mbuf, item, sizeof(mbuf) - strlen(mbuf) - 1);
                }
                mvprintw(row + 1, 4, "Membros: %s", mbuf);
                row += 2;
            }
            row++;

            // LVM
            attron(COLOR_PAIR(PAIR_WARN) | A_BOLD);
            mvprintw(row++, 1, "--- LVM VOLUME GROUPS (VG) & LOGICAL VOLUMES (LV) ---");
            attroff(COLOR_PAIR(PAIR_WARN) | A_BOLD);

            for (int v = 0; v < lvm.vg_count && row < max_y - 2; v++) {
                lvm_vg_t *vg = &lvm.vgs[v];
                mvprintw(row++, 2, "VG [%s]: %d LVs mapeados | Alocado: %.1f GB",
                         vg->name, vg->lv_count, vg->allocated_gb);
            }
        }

        // 4. Footer
        attron(COLOR_PAIR(PAIR_FOOTER) | A_BOLD);
        for (int i = 0; i < max_x; i++) mvaddch(max_y - 1, i, ' ');
        mvprintw(max_y - 1, 1, " [v/Tab] Alternar Visao | [d] Modo Demo | [q] Sair | [r] Atualizar ");
        attroff(COLOR_PAIR(PAIR_FOOTER) | A_BOLD);

        refresh();

        int ch = getch();
        if (ch == 'q' || ch == 'Q') {
            running = false;
        } else if (ch == 'd' || ch == 'D') {
            demo_mode = !demo_mode;
        } else if (ch == 'v' || ch == 'V' || ch == '\t') {
            view_mode = (view_mode + 1) % 3;
        } else if (ch == '1') {
            view_mode = 0;
        } else if (ch == '2') {
            view_mode = 1;
        } else if (ch == '3') {
            view_mode = 2;
        }
    }

    endwin();
    return 0;
}
