/* Copyright (c) 2019, Radek Sebela (r.sebela@gmail.com) */

uint8_t myRead(uint16_t myAddress)
{
    SPI.beginTransaction(spiSettings);
    digitalWrite(SS, LOW);
    SPI.transfer(READ);
    SPI.transfer16(myAddress);
    uint8_t re = SPI.transfer(0x00);
    digitalWrite(SS, HIGH);
    SPI.endTransaction();
    return re;
}