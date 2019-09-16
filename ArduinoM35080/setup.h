/* Copyright (c) 2019, Radek Sebela (r.sebela@gmail.com) */

void setup() {
    Serial.print("M35080 - Copyright (c) 2019, Radek Sebela (r.sebela@gmail.com)\n");
    pinMode(WRITE_ENABLE, OUTPUT);
    digitalWrite(WRITE_ENABLE, WRITE_ENABLE_VALUE);
    Serial.begin(9600);
    //Serial.println();
    digitalWrite(SS, HIGH);
    SPI.begin();
    SPI.setClockDivider(SPI_CLOCK_DIV32);
    Serial.flush();
    Serial.print("BOARD SPI PINS DEFINITIONS -> SS: ");
    Serial.print(SS);
    Serial.print(", MOSI: ");
    Serial.print(MOSI);
    Serial.print(", MISO: ");
    Serial.print(MISO);
    Serial.print(", SCK: ");
    Serial.print(SCK);
    Serial.print("\nDONE\nTEST COMMANDS:\nCMD:INFO;\nCMD:ALL;\n");
}
