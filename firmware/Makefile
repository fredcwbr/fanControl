MCU ?= atmega328p
F_CPU ?= 16000000UL
BAUD ?= 115200
PORT ?= /dev/ttyUSB0
PROGRAMMER ?= arduino

CC = avr-gcc
OBJCOPY = avr-objcopy
AVRDUDE = avrdude
SIZE = avr-size

CFLAGS = -Wall -Wextra -Os -std=gnu99 -DF_CPU=$(F_CPU) -mmcu=$(MCU) -I.

SRCS = main.c uart.c pwm.c tach.c
OBJS = $(SRCS:.c=.o)
TARGET = fancontroller

.PHONY: all clean flash size

all: $(TARGET).hex size

$(TARGET).elf: $(OBJS)
	$(CC) $(CFLAGS) -o $@ $^

$(TARGET).hex: $(TARGET).elf
	$(OBJCOPY) -O ihex -R .eeprom $< $@

size: $(TARGET).elf
	$(SIZE) --format=avr --mcu=$(MCU) $<

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f *.o *.elf *.hex

flash: $(TARGET).hex
	$(AVRDUDE) -c $(PROGRAMMER) -p $(MCU) -P $(PORT) -b $(BAUD) -U flash:w:$<:i
