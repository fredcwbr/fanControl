#include "uart.h"
#include <avr/io.h>
#include <avr/interrupt.h>

#ifndef F_CPU
#define F_CPU 16000000UL
#endif

#define RX_BUFFER_SIZE 64
static volatile char rx_buffer[RX_BUFFER_SIZE];
static volatile uint8_t rx_head = 0;
static volatile uint8_t rx_tail = 0;

ISR(USART_RX_vect) {
    char c = UDR0;
    uint8_t next_head = (rx_head + 1) % RX_BUFFER_SIZE;
    if (next_head != rx_tail) {
        rx_buffer[rx_head] = c;
        rx_head = next_head;
    }
}

void uart_init(uint32_t baud_rate) {
    uint16_t ubrr = (F_CPU / (16UL * baud_rate)) - 1;
    UBRR0H = (uint8_t)(ubrr >> 8);
    UBRR0L = (uint8_t)(ubrr);

    // Enable receiver, transmitter, and RX interrupt
    UCSR0B = (1 << RXEN0) | (1 << TXEN0) | (1 << RXCIE0);
    // 8 data bits, 1 stop bit, no parity
    UCSR0C = (1 << UCSZ01) | (1 << UCSZ00);
}

void uart_putc(char c) {
    while (!(UCSR0A & (1 << UDRE0))) {
        // Wait for transmit buffer to be empty
    }
    UDR0 = c;
}

void uart_puts(const char *str) {
    while (*str) {
        if (*str == '\n') {
            uart_putc('\r');
        }
        uart_putc(*str++);
    }
}

bool uart_available(void) {
    return (rx_head != rx_tail);
}

char uart_getc(void) {
    if (rx_head == rx_tail) {
        return '\0';
    }
    char c = rx_buffer[rx_tail];
    rx_tail = (rx_tail + 1) % RX_BUFFER_SIZE;
    return c;
}

void uart_read_line(char *buffer, uint8_t max_len) {
    uint8_t idx = 0;
    while (idx < max_len - 1) {
        if (!uart_available()) {
            continue;
        }
        char c = uart_getc();
        if (c == '\r' || c == '\n') {
            if (idx > 0) {
                break;
            }
            continue;
        }
        buffer[idx++] = c;
    }
    buffer[idx] = '\0';
}
