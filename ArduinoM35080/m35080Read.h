/* Copyright (c) 2019, Radek Sebela (r.sebela@gmail.com) */

#ifndef M35080_READ_H
#define M35080_READ_H

#include <stdint.h>
#include <SPI.h>

uint8_t m35080Read(uint16_t address, const SPISettings &spiSettings);

#endif /* M35080_READ_H */
