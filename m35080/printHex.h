/* Copyright (c) 2019, Radek Sebela (r.sebela@gmail.com) */

void printHex(int num, int precision) {
    char tmp[16];
    char format[128];
    sprintf(format, "%%.%dX ", precision);
    sprintf(tmp, format, num);
    Serial.print(tmp);
}
