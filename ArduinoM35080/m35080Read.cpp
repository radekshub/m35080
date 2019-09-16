/* Copyright (c) 2019, Radek Sebela (r.sebela@gmail.com) */

#include "m35080Read.h"

static const uint8_t READ = 0b00000011;  // TODO
//static const int SS = 10; // TODO

uint8_t m35080Read(uint16_t address, const SPISettings &spiSettings)
{
    SPI.beginTransaction(spiSettings);
    digitalWrite(SS, LOW);
    SPI.transfer(READ);
    SPI.transfer16(address);
    uint8_t re = SPI.transfer(0x00);
    digitalWrite(SS, HIGH);
    SPI.endTransaction();
    return re;
}
