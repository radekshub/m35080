/* Copyright (c) 2019, Radek Sebela (r.sebela@gmail.com) */

void printAll()
{
    Serial.print("======================================================\n0000 : ");
    for (uint16_t index = 0x00; index < 0x10; index++)
        printHex(myRead(index), 2);
    Serial.print("\n0010 : ");
    for (uint16_t index = 0x10; index < 0x20; index++)
        printHex(myRead(index), 2);
    Serial.print("\n======================================================");
    int cnt = -1 ;
    for (uint16_t index = 0x20; index <= 0x3FF; index++) {
        cnt++;
        if (cnt % 8 == 0) {
            Serial.print("\n");
            printHex(index, 4);
            Serial.print(": ");
        }
        printHex(myRead(index), 2);
    }
    Serial.println("\n==============================");
}
