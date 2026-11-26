CC ?= gcc
CFLAGS ?= -Wall -Wextra -O2 -I../../include -Isrc -std=c99
LDFLAGS ?= -lncursesw

SRC = src/main.c src/hwmon.c src/smart.c src/raid.c src/lvm.c
TARGET = ../fancontrol-tui

.PHONY: all clean

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) $(SRC) -o $(TARGET) $(LDFLAGS)

clean:
	rm -f $(TARGET)
