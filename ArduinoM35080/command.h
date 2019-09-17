/* Copyright (c) 2019, Radek Sebela (r.sebela@gmail.com) */

#include "m35080Read.h"

bool cmdAdd(String &cmd, const char newChar) {
    if (newChar >= ' ')
        cmd += newChar;
    if (cmd.length() > 64)
        cmd = "";
    if (newChar == ';')
        return true;
    return false;
}

bool cmdEqual(const String &cmd, const String &pattern) {
    if (cmd.length() >= pattern.length() && cmd.substring(0, pattern.length()).equalsIgnoreCase(pattern))
        return true;
    return false;
}

void cmdParameters(const String &cmd, String &firstParameter, String &secondParameter)
{
//"AAA:BBB,XXXX,YYzz";
    firstParameter = "";
    secondParameter = "";
    int index = cmd.indexOf(',');
    if (index >= 0)
        firstParameter = cmd.substring(index + 1, cmd.length() - 1);
    index = firstParameter.indexOf(',');
    if (index >= 0) {
        secondParameter = firstParameter.substring(index + 1);
        firstParameter = firstParameter.substring(0, index);
    }
}

void cmdRemove(String &cmd) {
    int index = cmd.indexOf(';');
    if (index > cmd.length()) {
        cmd = cmd.substring(index + 1);
    } else {
        cmd = "";
    }
}

void cmdInfo() {
    Serial.print("M35080\nCopyright (c) 2019 Radek Sebela\n");
    Serial.print("BOARD PINS DEFINITIONS:\n* SS: ");
    Serial.print(SS);
    Serial.print("\n* MOSI: ");
    Serial.print(MOSI);
    Serial.print("\n* MISO: ");
    Serial.print(MISO);
    Serial.print("\n* SCK: ");
    Serial.print(SCK);
    Serial.print("\nM35080 PINS DEFINITIONS:\n");
    Serial.print("* 1 - GND\n");
    Serial.print("* 2 - SS\n");
    Serial.print("* 3 - W\n");
    Serial.print("* 4 - MISO\n");
    Serial.print("* 5 - NC\n");
    Serial.print("* 6 - SCK\n");
    Serial.print("* 7 - MISO\n");
    Serial.print("* 8 - VCC 5V\n");
}

String getHex(const int value, const uint8_t precision, const bool prefix)
{
    String hexValue = String(value, HEX);
    while (hexValue.length() < precision)
        hexValue = "0" + hexValue;
    if (prefix == true)
        hexValue = "0x" + hexValue;
    return hexValue;
}

void cmdRead1(const String &cmd, const SPISettings &spiSettings) {
    String firstParameter;
    String secondParameter;
    cmdParameters(cmd, firstParameter, secondParameter);
    if (firstParameter.length() == 6 && secondParameter.length() == 0) {
        const int address = strtol(firstParameter.c_str(), 0, 16);
        uint8_t data = m35080Read(address, spiSettings);
        Serial.print("VALUE:" + getHex(address, 4, true) + "=" + getHex(data, 2, true) + ";\n");
        return;
    }
    Serial.print("ERROR:PARAMETERS," + firstParameter + "," + secondParameter + ";\n");
}

void cmdRead(const String &cmd, const SPISettings &spiSettings) {
    String addressString;
    String countString;
    cmdParameters(cmd, addressString, countString);
    if (addressString.length() == 6 && countString.length() == 4) {
        const int address = strtol(addressString.c_str(), 0, 16);
        const int count = strtol(countString.c_str(), 0, 16);
        String dataOut = "DATA:" + getHex(count, 2, true);
        for (size_t index = address; index < address + count; index++) {
            const uint16_t itemAddress = index;
            const uint8_t itemData = m35080Read(itemAddress, spiSettings);
            dataOut += "," + getHex(itemAddress, 4, true) + "=" + getHex(itemData, 2, true);
        }
        dataOut += ";\n";
        Serial.print(dataOut);
        return;
    }
    Serial.print("ERROR:PARAMETERS," + addressString + "," + countString + ";\n");
}