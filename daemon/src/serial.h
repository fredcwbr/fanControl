#ifndef SERIAL_H
#define SERIAL_H

#include <stdbool.h>
#include <stdint.h>
#include <stddef.h>

int serial_open(const char *port, int baud_rate);
void serial_close(int fd);
bool serial_write_line(int fd, const char *line);
bool serial_read_line(int fd, char *buffer, size_t max_len, int timeout_ms);
bool serial_ping(int fd);

#endif /* SERIAL_H */
