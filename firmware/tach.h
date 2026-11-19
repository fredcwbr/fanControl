#ifndef TACH_H
#define TACH_H

#include <stdint.h>

void tach_init(void);
void tach_tick_1ms(void);
uint16_t tach_get_rpm(uint8_t channel);

#endif /* TACH_H */
