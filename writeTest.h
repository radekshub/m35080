void writeTest()
{
    WRITE_ENABLE_VALUE = HIGH;
    digitalWrite(WRITE_ENABLE, WRITE_ENABLE_VALUE);
    Serial.print("Write 0x66 to 0x20, 0x30, 0x40, 0x50, 0x60, 0x70, 0x80, 0x90. Enable: ");
    Serial.println(WRITE_ENABLE_VALUE);
    myWrite(0x20, 0x66);
    myWrite(0x30, 0x66);
    myWrite(0x40, 0x66);
    myWrite(0x50, 0x66);
    myWrite(0x60, 0x66);
    myWrite(0x70, 0x66);
    myWrite(0x80, 0x66);
    myWrite(0x90, 0x66);
    WRITE_ENABLE_VALUE = LOW;
    digitalWrite(WRITE_ENABLE, WRITE_ENABLE_VALUE);
    Serial.print("Write 0x66 to 0x20, 0x30, 0x40, 0x50, 0x60, 0x70, 0x80, 0x90. Enable: ");
    Serial.println(WRITE_ENABLE_VALUE);
    myWrite(0x20, 0x66);
    myWrite(0x30, 0x66);
    myWrite(0x40, 0x66);
    myWrite(0x50, 0x66);
    myWrite(0x60, 0x66);
    myWrite(0x70, 0x66);
    myWrite(0x80, 0x66);
    myWrite(0x90, 0x66);
    Serial.println("DONE");
}
