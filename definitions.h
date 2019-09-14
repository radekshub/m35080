#include <SPI.h>
int WRITE_ENABLE = 9;
int WRITE_ENABLE_VALUE = HIGH;
SPISettings sPISettings(3000000, MSBFIRST, SPI_MODE0);

//Instruction Set
byte WREN = 0b00000110; //Set Write Enable Latch
byte WRDI = 0b00000100; //Reset Write Enable Latch
byte RDSR = 0b00000101; //Read Status Register
byte WRSR = 0b00000001; //Write Status Register
byte READ = 0b00000011; //Read Data from Memory Array
byte WRITE = 0b00000010; //Write Data to Memory Array
byte WRINC = 0b00000111; //Write Data to Secure Array
