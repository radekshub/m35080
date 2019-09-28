/* Copyright (c) 2019, Radek Sebela (r.sebela@gmail.com) */

void setup() {
    pinMode(WRITE_ENABLE, OUTPUT);
    digitalWrite(WRITE_ENABLE, WRITE_ENABLE_VALUE);
    Serial.begin(115200);
    digitalWrite(SS, HIGH);
    SPI.begin();
    SPI.setClockDivider(SPI_CLOCK_DIV32);
    Serial.flush();
}
