#define _DEFAULT_SOURCE
#include "serial.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <termios.h>
#include <sys/select.h>

static speed_t get_baud_constant(int baud) {
    switch (baud) {
        case 9600:   return B9600;
        case 19200:  return B19200;
        case 38400:  return B38400;
        case 57600:  return B57600;
        case 115200: return B115200;
        default:     return B115200;
    }
}

int serial_open(const char *port, int baud_rate) {
    int fd = open(port, O_RDWR | O_NOCTTY | O_NONBLOCK);
    if (fd < 0) {
        return -1;
    }

    struct termios tty;
    if (tcgetattr(fd, &tty) != 0) {
        close(fd);
        return -1;
    }

    speed_t baud = get_baud_constant(baud_rate);
    cfsetospeed(&tty, baud);
    cfsetispeed(&tty, baud);

    // 8N1 raw mode
    tty.c_cflag &= ~PARENB;        // No parity
    tty.c_cflag &= ~CSTOPB;        // 1 stop bit
    tty.c_cflag &= ~CSIZE;
    tty.c_cflag |= CS8;            // 8 data bits
    tty.c_cflag &= ~CRTSCTS;       // No hardware flow control
    tty.c_cflag |= CREAD | CLOCAL; // Turn on READ & ignore ctrl lines

    tty.c_lflag &= ~(ICANON | ECHO | ECHOE | ISIG); // Raw input
    tty.c_iflag &= ~(IXON | IXOFF | IXANY);         // Disable software flow control
    tty.c_iflag &= ~(IGNBRK | BRKINT | PARMRK | ISTRIP | INLCR | IGNCR | ICRNL);
    tty.c_oflag &= ~OPOST;                          // Raw output

    tty.c_cc[VMIN]  = 0;
    tty.c_cc[VTIME] = 5; // 0.5s inter-byte timeout

    if (tcsetattr(fd, TCSANOW, &tty) != 0) {
        close(fd);
        return -1;
    }

    // Give Arduino/ch340 time to reset after DTR toggle
    usleep(1500000);
    tcflush(fd, TCIOFLUSH);

    return fd;
}

void serial_close(int fd) {
    if (fd >= 0) {
        close(fd);
    }
}

bool serial_write_line(int fd, const char *line) {
    if (fd < 0 || !line) return false;

    size_t len = strlen(line);
    ssize_t written = write(fd, line, len);
    if (written != (ssize_t)len) {
        return false;
    }

    if (line[len - 1] != '\n') {
        if (write(fd, "\n", 1) != 1) return false;
    }

    tcdrain(fd);
    return true;
}

bool serial_read_line(int fd, char *buffer, size_t max_len, int timeout_ms) {
    if (fd < 0 || !buffer || max_len == 0) return false;

    size_t idx = 0;
    while (idx < max_len - 1) {
        fd_set read_fds;
        FD_ZERO(&read_fds);
        FD_SET(fd, &read_fds);

        struct timeval tv;
        tv.tv_sec = timeout_ms / 1000;
        tv.tv_usec = (timeout_ms % 1000) * 1000;

        int res = select(fd + 1, &read_fds, NULL, NULL, &tv);
        if (res <= 0) {
            // Timeout or error
            break;
        }

        char c;
        ssize_t n = read(fd, &c, 1);
        if (n <= 0) break;

        if (c == '\r') continue;
        if (c == '\n') {
            if (idx > 0) break;
            continue;
        }

        buffer[idx++] = c;
    }

    buffer[idx] = '\0';
    return (idx > 0);
}

bool serial_ping(int fd) {
    if (!serial_write_line(fd, "PING")) {
        return false;
    }

    char reply[64];
    if (serial_read_line(fd, reply, sizeof(reply), 1000)) {
        return (strncmp(reply, "PONG", 4) == 0);
    }

    return false;
}
