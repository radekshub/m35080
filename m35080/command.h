/* Copyright (c) 2019, Radek Sebela (r.sebela@gmail.com) */

bool cmdAdd(String &cmd, char newChar) {
    if (newChar >= 32)
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

void cmdRemove(String &cmd) {
    int index = cmd.indexOf(';');
    if (index > cmd.length()) {
        cmd = cmd.substring(index + 1);
    } else {
        cmd = "";
    }
}
