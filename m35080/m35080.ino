/* Copyright (c) 2019, Radek Sebela (r.sebela@gmail.com) */

#include "definitions.h"
#include "setup.h"

#include "myRead.h"
#include "myWrite.h"
#include "printHex.h"

#include "printAll.h"
#include "writeTest.h"

void loop() {
    while (Serial.available() <= 0) {}

    printAll();

    writeTest();

    while (Serial.available() > 0)
        Serial.read();
}
