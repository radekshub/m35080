/* Copyright (c) 2019, Radek Sebela (r.sebela@gmail.com) */

#include "definitions.h"
#include "setup.h"
#include "command.h"

#include "myRead.h"
#include "myWrite.h"
#include "printHex.h"

#include "printAll.h"
#include "writeTest.h"

String command = "";

void loop() {
    if (Serial.available() > 0) {
        if (cmdAdd(command, Serial.read())) {
            Serial.println(command);
            if (cmdEqual(command, "CMD:ALL"))
                printAll();
            if (cmdEqual(command, "CMD:TEST"))
                Serial.println("OK");
            // writeTest();
            cmdRemove(command);
        }
    }
}
