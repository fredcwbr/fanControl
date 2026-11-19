#ifndef FANCONTROL_H
#define FANCONTROL_H

#include <stdio.h>
#include <stdbool.h>

#define PROJECT_NAME "fancontrol"
#define PROJECT_VERSION "0.1.0"

#define LOG_INFO(...)  do { fprintf(stdout, "[INFO]  " __VA_ARGS__); fputc('\n', stdout); } while (0)
#define LOG_WARN(...)  do { fprintf(stderr, "[WARN]  " __VA_ARGS__); fputc('\n', stderr); } while (0)
#define LOG_ERROR(...) do { fprintf(stderr, "[ERROR] " __VA_ARGS__); fputc('\n', stderr); } while (0)

#endif /* FANCONTROL_H */
