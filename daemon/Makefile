CC ?= gcc
CFLAGS ?= -Wall -Wextra -pedantic -std=c11 -O2 -Isrc

TARGET = fancontrold
SRCS = src/main.c src/serial.c src/hwmon.c src/curve.c
OBJS = $(SRCS:.c=.o)

.PHONY: all clean install

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) $(TARGET)

install: $(TARGET)
	install -d /usr/local/bin
	install -m 755 $(TARGET) /usr/local/bin/
	install -d /etc/fancontrol
	install -m 644 fancontrol.conf /etc/fancontrol/
	install -m 644 fancontrol.service /etc/systemd/system/
	install -m 644 99-fancontrol.rules /etc/udev/rules.d/
	udevadm control --reload-rules && udevadm trigger
	systemctl daemon-reload
