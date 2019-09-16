/* Copyright (c) 2019, Radek Sebela (r.sebela@gmail.com) */

#include "definitions.h"
#include "setup.h"
#include "command.h"

#include "m35080Read.h"
//#include "myRead.h"
#include "myWrite.h"
#include "printHex.h"

#include "printAll.h"
#include "writeTest.h"

String command = "";

void loop() {
    if (Serial.available() > 0) {
        if (cmdAdd(command, Serial.read())) {
            if (cmdEqual(command, "CMD:ALL"))
                printAll();
            else if (cmdEqual(command, "CMD:INFO"))
                cmdInfo();
            else if (cmdEqual(command, "CMD:READ"))
                cmdRead(command, spiSettings);
            // writeTest();
            cmdRemove(command);
        }
    }
}
