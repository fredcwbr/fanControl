#define _DEFAULT_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <signal.h>
#include <unistd.h>
#include <getopt.h>

#include "serial.h"
#include "hwmon.h"
#include "curve.h"

static volatile sig_atomic_t g_running = 1;

static void handle_signal(int sig) {
    (void)sig;
    g_running = 0;
}

static void print_usage(const char *prog) {
    printf("Custom PC Fan Controller - Linux Host Daemon\n");
    printf("Usage: %s [OPTIONS]\n\n", prog);
    printf("Options:\n");
    printf("  -p, --port <device>     Serial port (default: /dev/ttyUSB0 or /dev/fancontrol)\n");
    printf("  -b, --baud <rate>       Baud rate (default: 115200)\n");
    printf("  -s, --sensor <path>     Primary hwmon temp path (CPU)\n");
    printf("  -g, --gpu-sensor <path> Secondary hwmon temp path (GPU)\n");
    printf("  -i, --interval <sec>    Poll interval in seconds (default: 1)\n");
    printf("  --status                Query controller and print RPM/PWM status once\n");
    printf("  --set <ch> <val>        Set specific fan channel PWM (1-4, 0-255)\n");
    printf("  --setall <val>          Set all fans to specified PWM (0-255)\n");
    printf("  --list-hwmon            List available Linux temperature sensors\n");
    printf("  -h, --help              Display this help message\n\n");
}

int main(int argc, char *argv[]) {
    const char *port = "/dev/fancontrol";
    if (access(port, F_OK) != 0) {
        port = "/dev/ttyUSB0";
    }

    int baud = 115200;
    const char *sensor_cpu = "/sys/class/hwmon/hwmon1/temp1_input";
    const char *sensor_gpu = "/sys/class/hwmon/hwmon2/temp1_input";
    int interval_sec = 1;

    bool query_status = false;
    bool set_single = false;
    int set_ch = 1, set_val = 128;
    bool set_all = false;
    int setall_val = 128;

    fan_curve_t curve = {
        .temp_min = 38.0,
        .temp_max = 75.0,
        .pwm_min = 60,    // ~24% duty cycle (silent threshold)
        .pwm_max = 255    // 100% duty cycle
    };

    static struct option long_opts[] = {
        {"port",        required_argument, 0, 'p'},
        {"baud",        required_argument, 0, 'b'},
        {"sensor",      required_argument, 0, 's'},
        {"gpu-sensor",  required_argument, 0, 'g'},
        {"interval",    required_argument, 0, 'i'},
        {"status",      no_argument,       0, 1001},
        {"set",         required_argument, 0, 1002},
        {"setall",      required_argument, 0, 1003},
        {"list-hwmon",  no_argument,       0, 1004},
        {"help",        no_argument,       0, 'h'},
        {0, 0, 0, 0}
    };

    int opt;
    while ((opt = getopt_long(argc, argv, "p:b:s:g:i:h", long_opts, NULL)) != -1) {
        switch (opt) {
            case 'p': port = optarg; break;
            case 'b': baud = atoi(optarg); break;
            case 's': sensor_cpu = optarg; break;
            case 'g': sensor_gpu = optarg; break;
            case 'i': interval_sec = atoi(optarg); break;
            case 1001: query_status = true; break;
            case 1002: {
                set_single = true;
                if (optind < argc) {
                    set_ch = atoi(optarg);
                    set_val = atoi(argv[optind++]);
                } else {
                    set_val = atoi(optarg);
                }
                break;
            }
            case 1003: {
                set_all = true;
                setall_val = atoi(optarg);
                break;
            }
            case 1004:
                hwmon_list_devices();
                return EXIT_SUCCESS;
            case 'h':
                print_usage(argv[0]);
                return EXIT_SUCCESS;
            default:
                print_usage(argv[0]);
                return EXIT_FAILURE;
        }
    }

    // Connect to serial port
    int fd = serial_open(port, baud);
    if (fd < 0) {
        fprintf(stderr, "[ERROR] Unable to open serial port '%s'. Check permissions or udev rule.\n", port);
        return EXIT_FAILURE;
    }

    if (!serial_ping(fd)) {
        fprintf(stderr, "[WARN] Controller did not respond to PING on '%s'. Continuing anyway...\n", port);
    } else {
        printf("[INFO] Connected to Custom PC Fan Controller on %s\n", port);
    }

    // Single-action CLI modes
    if (set_all) {
        char cmd[32];
        snprintf(cmd, sizeof(cmd), "SETALL %d", setall_val);
        serial_write_line(fd, cmd);
        printf("[OK] Sent %s to controller.\n", cmd);
        serial_close(fd);
        return EXIT_SUCCESS;
    }

    if (set_single) {
        char cmd[32];
        snprintf(cmd, sizeof(cmd), "SET %d %d", set_ch, set_val);
        serial_write_line(fd, cmd);
        printf("[OK] Sent %s to controller.\n", cmd);
        serial_close(fd);
        return EXIT_SUCCESS;
    }

    if (query_status) {
        serial_write_line(fd, "STATUS");
        char resp[128];
        if (serial_read_line(fd, resp, sizeof(resp), 1000)) {
            printf("[STATUS] %s\n", resp);
        } else {
            printf("[WARN] No response received for STATUS.\n");
        }
        serial_close(fd);
        return EXIT_SUCCESS;
    }

    // Continuous Daemon Mode
    struct sigaction sa;
    sa.sa_handler = handle_signal;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = 0;
    sigaction(SIGINT, &sa, NULL);
    sigaction(SIGTERM, &sa, NULL);

    printf("[INFO] Starting FanControl Daemon (Poll interval: %ds)\n", interval_sec);
    printf("[INFO] Curve: %.1fC - %.1fC => PWM: %u - %u\n",
           curve.temp_min, curve.temp_max, curve.pwm_min, curve.pwm_max);

    while (g_running) {
        double max_temp = hwmon_get_max_temp(sensor_cpu, sensor_gpu);
        uint8_t target_pwm = curve_calculate_pwm(&curve, max_temp);

        char cmd[32];
        snprintf(cmd, sizeof(cmd), "SETALL %u", target_pwm);
        if (!serial_write_line(fd, cmd)) {
            fprintf(stderr, "[WARN] Failed to write to serial port. Attempting reconnect...\n");
            serial_close(fd);
            sleep(2);
            fd = serial_open(port, baud);
            continue;
        }

        // Query telemetry
        serial_write_line(fd, "STATUS");
        char status_resp[128];
        if (serial_read_line(fd, status_resp, sizeof(status_resp), 500)) {
            printf("[MONITOR] Max Temp: %.1f°C | Target PWM: %u/255 (%.0f%%) | %s\n",
                   max_temp, target_pwm, (target_pwm / 255.0) * 100.0, status_resp);
        } else {
            printf("[MONITOR] Max Temp: %.1f°C | Target PWM: %u/255 (%.0f%%)\n",
                   max_temp, target_pwm, (target_pwm / 255.0) * 100.0);
        }

        sleep(interval_sec);
    }

    printf("[INFO] Shutting down. Setting safe fan speed (180/255)...\n");
    serial_write_line(fd, "SETALL 180");
    serial_close(fd);

    return EXIT_SUCCESS;
}
