/* Copyright (c) 2019, Radek Sebela (r.sebela@gmail.com) */

// SPI
#include <SPI.h>
static const SPISettings spiSettings(3000000, MSBFIRST, SPI_MODE0);

// M35080 Write Enable
int WRITE_ENABLE = 9;
int WRITE_ENABLE_VALUE = HIGH;

// M35080 Instructions
static const uint8_t WREN = 0b00000110;  // Set Write Enable Latch
static const uint8_t WRDI = 0b00000100;  // Reset Write Enable Latch
static const uint8_t RDSR = 0b00000101;  // Read Status Register
static const uint8_t WRSR = 0b00000001;  // Write Status Register
static const uint8_t READ = 0b00000011;  // Read Data from Memory Array
static const uint8_t WRITE = 0b00000010; // Write Data to Memory Array
static const uint8_t WRINC = 0b00000111; // Write Data to Secure Array
