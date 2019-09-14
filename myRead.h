uint8_t myRead(uint16_t myAddress)
{
    SPI.beginTransaction(sPISettings);
    digitalWrite(SS, LOW);
    SPI.transfer(READ);
    SPI.transfer16(myAddress);
    uint8_t re = SPI.transfer(0xFF);
    digitalWrite(SS, HIGH);
    SPI.endTransaction();
    return re;
}
