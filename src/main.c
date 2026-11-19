#define _DEFAULT_SOURCE
#include "fancontrol.h"
#include "sensor.h"
#include "fan.h"
#include "config.h"

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <signal.h>
#include <unistd.h>
#include <getopt.h>

static volatile sig_atomic_t g_running = 1;
static fan_config_t g_config;

static void handle_signal(int sig) {
    (void)sig;
    g_running = 0;
}

static void print_usage(const char *prog_name) {
    printf("Usage: %s [OPTIONS]\n\n", prog_name);
    printf("Options:\n");
    printf("  -c, --config <file>    Path to configuration file\n");
    printf("  -d, --discover         Scan and list available hwmon devices\n");
    printf("  -o, --once             Read temperature once and exit\n");
    printf("  -v, --version          Show version information\n");
    printf("  -h, --help             Display this help message\n\n");
}

int main(int argc, char *argv[]) {
    const char *config_file = "fancontrol.conf";
    bool discover_only = false;
    bool once_only = false;

    static struct option long_options[] = {
        {"config",   required_argument, 0, 'c'},
        {"discover", no_argument,       0, 'd'},
        {"once",     no_argument,       0, 'o'},
        {"version",  no_argument,       0, 'v'},
        {"help",     no_argument,       0, 'h'},
        {0, 0, 0, 0}
    };

    int opt;
    while ((opt = getopt_long(argc, argv, "c:dovh", long_options, NULL)) != -1) {
        switch (opt) {
            case 'c':
                config_file = optarg;
                break;
            case 'd':
                discover_only = true;
                break;
            case 'o':
                once_only = true;
                break;
            case 'v':
                printf("%s v%s\n", PROJECT_NAME, PROJECT_VERSION);
                return EXIT_SUCCESS;
            case 'h':
                print_usage(argv[0]);
                return EXIT_SUCCESS;
            default:
                print_usage(argv[0]);
                return EXIT_FAILURE;
        }
    }

    if (discover_only) {
        sensor_discover();
        return EXIT_SUCCESS;
    }

    config_set_defaults(&g_config);
    if (access(config_file, F_OK) == 0) {
        LOG_INFO("Loading config from %s", config_file);
        config_load_file(config_file, &g_config);
    } else {
        LOG_INFO("Config file '%s' not found, running with defaults", config_file);
    }

    // Set up signal handlers for graceful shutdown
    struct sigaction sa;
    sa.sa_handler = handle_signal;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = 0;
    sigaction(SIGINT, &sa, NULL);
    sigaction(SIGTERM, &sa, NULL);

    LOG_INFO("Starting %s v%s...", PROJECT_NAME, PROJECT_VERSION);
    LOG_INFO("Sensor: %s, PWM: %s", g_config.temp_input_path, g_config.pwm_path);
    LOG_INFO("Temp range: %.1fC - %.1fC => PWM: %d - %d",
             g_config.temp_min, g_config.temp_max, g_config.pwm_min, g_config.pwm_max);

    // Try setting manual control mode
    if (g_config.pwm_enable_path[0] != '\0' && access(g_config.pwm_enable_path, W_OK) == 0) {
        fan_set_manual_mode(g_config.pwm_enable_path);
    }

    while (g_running) {
        double current_temp = 0.0;
        if (!sensor_read_temp(g_config.temp_input_path, &current_temp)) {
            LOG_WARN("Failed to read temperature from %s", g_config.temp_input_path);
        } else {
            int target_pwm = config_calculate_pwm(&g_config, current_temp);
            int rpm = -1;
            if (g_config.fan_input_path[0] != '\0') {
                fan_read_rpm(g_config.fan_input_path, &rpm);
            }

            if (rpm >= 0) {
                LOG_INFO("Temp: %.1f°C | Target PWM: %d/255 (%.0f%%) | Fan Speed: %d RPM",
                         current_temp, target_pwm, (target_pwm / 255.0) * 100.0, rpm);
            } else {
                LOG_INFO("Temp: %.1f°C | Target PWM: %d/255 (%.0f%%)",
                         current_temp, target_pwm, (target_pwm / 255.0) * 100.0);
            }

            // Write PWM if target is writable
            if (access(g_config.pwm_path, W_OK) == 0) {
                fan_write_pwm(g_config.pwm_path, target_pwm);
            }
        }

        if (once_only) {
            break;
        }

        usleep(g_config.poll_interval_ms * 1000);
    }

    LOG_INFO("Stopping %s. Restoring auto mode...", PROJECT_NAME);
    if (g_config.pwm_enable_path[0] != '\0' && access(g_config.pwm_enable_path, W_OK) == 0) {
        fan_restore_auto_mode(g_config.pwm_enable_path);
    }

    return EXIT_SUCCESS;
}
