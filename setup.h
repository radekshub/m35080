void setup() {
    Serial.print("BOOT");
    pinMode(WRITE_ENABLE, OUTPUT);
    digitalWrite(WRITE_ENABLE, WRITE_ENABLE_VALUE);
    Serial.begin(9600);
    Serial.println();
digitalWrite(SS,HIGH);
SPI.begin();
SPI.setClockDivider(SPI_CLOCK_DIV32);
    Serial.flush();
    Serial.println("DONE");
}
