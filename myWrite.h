void myWrite(uint16_t myAddress, uint8_t myValue)
{
    SPI.beginTransaction(sPISettings);
    digitalWrite(SS, LOW);
    SPI.transfer(WRITE);
    SPI.transfer16(myAddress);
    SPI.transfer(myValue);
    digitalWrite(SS, HIGH);
    SPI.endTransaction();
}
