CC ?= gcc
CFLAGS ?= -Wall -Wextra -pedantic -std=c11 -O2 -Iinclude
DEBUG_CFLAGS = -Wall -Wextra -pedantic -std=c11 -g -O0 -fsanitize=address,undefined -Iinclude

TARGET = fancontrol
SRC_DIR = src
INC_DIR = include
BUILD_DIR = build

SRCS = $(wildcard $(SRC_DIR)/*.c)
OBJS = $(patsubst $(SRC_DIR)/%.c, $(BUILD_DIR)/%.o, $(SRCS))

.PHONY: all clean debug run

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $^

$(BUILD_DIR)/%.o: $(SRC_DIR)/%.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

debug: CFLAGS = $(DEBUG_CFLAGS)
debug: clean $(TARGET)

clean:
	rm -rf $(BUILD_DIR) $(TARGET)

run: $(TARGET)
	./$(TARGET) -o
