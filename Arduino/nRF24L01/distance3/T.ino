/*The following is code for the transponder. This is the device carried on your person. It's 
purpose is to configure the transceiver and keep the receive buffer (RX FIFO) empty. It can 
also be used for power management, although that ability has not been coded yet.*/
#include <SPI.h> //include the SPI library to use for communicating with the transceiver
//Sensor's memory register addresses:
#define WRITE 0b00100000   // nRF24L01+'s write command
// pins used for the connection with the sensor
// the other you need are controlled by the SPI library):

#define chipEnablePin 10
#define chipSelectPin 4
#define chipInterruptPin 3
#define DATAOUT 11//MOSI
#define DATAIN  12//MISO 
#define SPICLOCK  13//sck
#define SLAVESELECT 10//ss

volatile byte stat = 0;
void setup() {
  Serial.begin(9600);
  // start the SPI library:
  SPI.begin();
  SPI.setDataMode(SPI_MODE0); //clock polarity is 0, phase is 0
  SPI.setBitOrder(MSBFIRST); //set bit order
  SPI.setClockDivider(SPI_CLOCK_DIV2); //set SPI for max speed
  // initalize the  data ready and chip select pins:
  pinMode(chipEnablePin, OUTPUT);
  pinMode(chipSelectPin, OUTPUT);
  pinMode(DATAOUT, OUTPUT);
  pinMode(DATAIN, INPUT);
  pinMode(SPICLOCK,OUTPUT);
  pinMode(SLAVESELECT,OUTPUT);
  pinMode(chipInterruptPin, INPUT);
  digitalWrite(chipSelectPin, HIGH);
  digitalWrite(chipEnablePin, LOW);
  //Configure nRF24L01+:
  writeRegister(0x04, 0b00010011); //enable auto-retransmit:address, value
  writeRegister(0x06, 0b00100110); //set for 250 kbps data rate and high power transmit
  writeRegister(0x05, 1); //change channel
  //writeRegister(0x0A, 0x02); //set receive address of pipe0 (only writing LSByte, otherwise address is 5 bytes)
  //writeRegister(0x10, 0x02); //set transmit address (only writing LSByte, otherwise address is 5 bytes) receive pipe0 needs to be changed to this address for auto acknowledge to work
  writeRegister(0x11, 0b00000010); //set payload width for pipe 0, default is 0 (pipe not used)
  writeRegister(0x1C, 0b00000001); //use dynamic payload length
  writeRegister(0x1D, 0b00000100); //use dynamic payload length
  
  writeRegister(0x00,0b00111011); //CRC enabled, power-up, RX mode, mask TX interrupts
  delay(100); // give the transceiver time to set up
  attachInterrupt(1, checkStatus, FALLING); //attach interrupt to #1 when it is pulled low
  digitalWrite(chipEnablePin, HIGH); //chip enable needs to be high for transceiver to receive
}
void loop() {
    
  delay(60);
    if(stat = 1) {
      if((readRegister(0x17,1) & 0b00000001) == 0) { //check that there is data in the RX FIFO, continue to read and clear IRQ until RX FIFO is empty
        readRegister(0b01100001, 1); //read RF FIFO to clear it out
        writeRegister(0x07, 0b01110000); //clear interrupt status once RX FIFO has been read out
       }
      if((readRegister(0x17,1) & 0b00000010)>>1 == 1) { //check if the RX_FIFO is full, sometimes this causes a hang-up and it needs to be cleared to resume receiving
        sendCommand(0b11100010); //flush RX_FIFO
       }
       stat = 0;
    }
    
}
//interrupt for checking and clearing the status register of the nRF24L01+:
void checkStatus()
{
  stat = 1;
}
//read the Status register of the nRF24L01+. We could use readRegister, but the transceiver automatically
//sends the status register on the first 8 bits of SPI so there's no need to send it a specific address:
byte readStatus() {
  byte result = 0; // result to return
  result = SPI.transfer(0xFF); // send a NOP value to read the status register
  return(result);
}
//Read from or write to register from the nRF24L01+:
unsigned long readRegister(byte thisRegister, int bytesToRead ) {
  unsigned long inByte = 0; // incoming byte from the SPI
  byte bytesRead = 0; //# of bytes to read from register
  unsigned long result = 0; // result to return
  digitalWrite(chipSelectPin, LOW); // bring the chip select low to select the device
  SPI.transfer(thisRegister); // send the device the register you want to read
  result = SPI.transfer(0xFF); // send a NOP value to read the first byte returned
  bytesRead++; // increment the number of bytes left to read
  while (bytesToRead > bytesRead) { // if you still have another byte to read
    inByte = SPI.transfer(0xFF); // continue to send a NOP value to read further bytes
    inByte = inByte << (8*bytesRead); // Bytes are loaded in least significant first. Take data in, shift it 8, 16, 24, etc bits over and add it to result
    result = result + inByte;
    bytesRead++; // increment the number of bytes left to read
  }
  digitalWrite(chipSelectPin, HIGH); // bring the chip select high to de-select the device
  return(result); // return the result
}
//Writes to register on nRF24L01+. Register addresses are handled by last five bits of command.
void writeRegister(byte thisRegister, byte thisValue) {
  byte addressToSend = thisRegister | WRITE; //combine write command and address to form one byte. 
  digitalWrite(chipSelectPin, LOW); // bring the chip select low to select the device
  SPI.transfer(addressToSend); //Send register location
  SPI.transfer(thisValue);  //Send value to record into register
  digitalWrite(chipSelectPin, HIGH); // bring the chip select high to de-select the device
}
//Sends a command to nRF24L01+; can be done with write command, but this is slightly faster when a return isn't necessary
void sendCommand(byte theRegister) {
  digitalWrite(chipSelectPin, LOW); // bring the chip select low to select the device
  SPI.transfer(theRegister); //Send register location
  digitalWrite(chipSelectPin, HIGH); // bring the chip select high to de-select the device
}d