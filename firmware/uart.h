#ifndef UART_H
#define UART_H

#include <stdint.h>
#include <stdbool.h>

void uart_init(uint32_t baud_rate);
void uart_putc(char c);
void uart_puts(const char *str);
bool uart_available(void);
char uart_getc(void);
void uart_read_line(char *buffer, uint8_t max_len);

#endif /* UART_H */
