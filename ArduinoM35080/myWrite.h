/* Copyright (c) 2019, Radek Sebela (r.sebela@gmail.com) */

void myWrite(uint16_t myAddress, uint8_t myValue)
{
    SPI.beginTransaction(spiSettings);
    digitalWrite(SS, LOW);
    SPI.transfer(WRITE);
    SPI.transfer16(myAddress);
    SPI.transfer(myValue);
    digitalWrite(SS, HIGH);
    SPI.endTransaction();
}
