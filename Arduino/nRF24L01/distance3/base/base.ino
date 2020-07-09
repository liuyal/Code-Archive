/*The following is code for the base station. This is the device that is left stationary and 
serves as the point for collecting data and performing calculations. It configures the 
transceiver, loads the transmit buffer (TX FIFO) and repeatedly sends a packet to the 
transponder, measuring how much time (in clock cycles)elapses between the transmission of 
the packet and the reception of the acknowledge packet from the transponder.The results are 
filtered out using standard deviation and transmitted over serial.*/

#include <SPI.h> //include the SPI library to use for communicating with the transceiver
#define WRITE 0b00100000   // nRF24L01+'s write command
#define CLR(x,y) (x&=(~(1<<y))) //direct port manipulation: bring pin low (x= port y = pin# for the PORT!, not the board)
#define SET(x,y) (x|=(1<<y)) //direct port manipulation: bring pin high

// pins used for the connection with the sensor
// the other you need are controlled by the SPI library):
#define chipEnablePin A5 //PF0
#define chipSelectPin A4 //PF1
#define chipInterruptPin 6
#define DATAOUT 11//MOSI
#define DATAIN  12//MISO 
#define SPICLOCK  13//sck
#define SLAVESELECT 8//ss

//code configuration variables
#define samples 600 //define how many samples we will take before performing calculations
#define minValue 13560 //smallest aloowable raw result from the test; serves as the minimum measured time
#define maxValue 13650 //smallest allowable raw result
#define sdFactor 100 //% to adjust standard deviant factor. Lower percentage results in tighter filtering
#define serialBaud 9600 //baud rate for serial connection
unsigned long starttime=0;
volatile unsigned long endtime=0; //cycles of timer1
unsigned long average = 0;
unsigned long stDeviation = 0;
unsigned long sum = 0;
unsigned int lowResultRejections=0; //log how many results were discarded that fell below the minimum
unsigned int highResultRejections=0; //log how many results were discarded that fell above the maximum
unsigned int numPoints = 0;
volatile byte stat = 0;
byte testResults[samples];
byte timercache = 0;

void setup() {
  Serial.begin(serialBaud);
  
  // start the SPI library:
  SPI.begin();
  SPI.setDataMode(SPI_MODE0); //clock polarity is 0, phase is 0
  SPI.setBitOrder(MSBFIRST); //set bit order
  SPI.setClockDivider(SPI_CLOCK_DIV8); //set SPI for max speed
  
  // initalize the  data ready and chip select pins:
  pinMode(chipEnablePin, OUTPUT);
  pinMode(chipSelectPin, OUTPUT);
  pinMode(DATAOUT, OUTPUT);
  pinMode(DATAIN, INPUT);
  pinMode(SPICLOCK,OUTPUT);
  //pinMode(SLAVESELECT,OUTPUT);
  pinMode(chipInterruptPin, INPUT_PULLUP);
  
  digitalWrite(chipSelectPin, HIGH);
  digitalWrite(chipEnablePin, LOW);
  
  //Configure nRF24L01+:
  //writeRegister(0x04, 0b00101000); //enable retransmit: wait 750 us between retransmit, attempt up to 4 times
  writeRegister(0x06, 0b00100110); //set for 250 kbps data rate and high power transmit
  writeRegister(0x05, 1); //0b00000100); //change channel
  //writeRegister(0x0A, 0x02); //set receive address of pipe0 (only writing LSByte, otherwise address is 5 bytes)
  //writeRegister(0x10, 0x02); //set transmit address (only writing LSByte, otherwise address is 5 bytes) receive pipe0 needs to be changed to this address for auto acknowledge to work
  writeRegister(0x11, 0b00000001); //set payload width for pipe 0, default is 0 (pipe not used)
  writeRegister(0x1C, 0b00000001); //set dynamic payload length
  writeRegister(0x1D, 0b00000100); //set dynamic payload length
  writeRegister(0x00,0b01001010); //CRC enabled, power-up, TX mode, disable RX_DR interrupt

  
  // give the transceiver time to set up:
  //configure timer1
  TCCR1A = 0b00000000; //disable comparators and run in normal mode (16 bit)
  TCCR1B = 0b00000001; //run at a prescaler of 0 to stop timer
  TCCR1C = 0x00; //disable force output compare
  
  delay(5000);
  writeRegister(0x04, 0b11101000); //enable retransmit: wait 1250 us between retransmit, attempt up to 4 times. For some reason this has to be written despite being previously called
  sendCommand(0b11100001); //clear TX FIFO
  writeRegister(0x07, 0b00110000); //clear TX status 
  writeRegister(0b10100000, 0x00); //write blank value for pinging. Transponder will only change channel if value is over 0.
  digitalWrite(chipEnablePin, HIGH); //send enable signal to transmit
  digitalWrite(chipEnablePin, LOW);
  
  attachInterrupt(0, checkStatus, FALLING); //attach interrupt to #0 (pin 3) when it is pulled low
  Serial.println("Starting");
}
void loop() {
 
  delay(50);
  writeRegister(0x04, 0b10010000); //disable retransmit so we can accurately count dropped packets
  sendCommand(0b11100011); //reuse last transmitted payload
  lowResultRejections=0;
  highResultRejections=0;
 
  for(int x=0; x < samples; x++) {
    restart:
    delayMicroseconds(920); //helps stability of results, but needs to be a specific number, for some reason, to reduce outlier data
    stat = 0;
    timercache = TCCR0B; //store current state of timer register
    TCCR0B = 0x00; //pause timer 0 to prevent it's interrupt from triggering
    uint8_t oldSREG = SREG; //save results of interrupt register so they can be reinstated after global interrupts are re-enabled
    cli(); //disable global interrupts to make timing and trigger event as consistent as possible
    Serial.end(); //disable serial to marginally improve standard deviation (4%). Can be left out.
    GTCCR |= (1 << PSRSYNC); //reset general timer/counter control register to resync counters
    TCNT1 = 0; //reset timer 1 counter
    SET(PORTB, 0); //direct port manipulate the chip enable pin for more consistent results
    sei();
    SREG = oldSREG; //reinstate old interrupt register values
    while(stat < 1) { }//stat must be a voltatile variable, otherwise the while loop freezes
    CLR(PORTB, 0) ;//direct port manipulate the chip enable pin
    TCCR0B = timercache; //restore timer0
    Serial.begin(serialBaud); //restore serial
    
    if(stat==2) { 
        goto restart; //max_rt was triggered, restart measurement
      }
      
    if(endtime > maxValue) { //limit the window of results; otherwise we collect some stray data at higher values
      highResultRejections++;
      goto restart;
    }
    if(endtime < minValue) {
      lowResultRejections++;
      goto restart;
    }
    testResults[x] = (endtime-minValue); //collect results into an array, subtract the minimum expected value so we can keep the values under a byte each (IE 13575-13600= 75)
  }
  sum = 0;
  for(int x=0; x<samples; x++) { //sum the test values so they can be averaged
    testResults[x] = testResults[x]*10;
    sum += testResults[x];  
  }
  average = sum/samples;
  sum=0; //clear out sum so we can now use it to sum the squared difference from average, used for finding standard deviation
  for(int x=0; x<samples; x++) {
    sum += sq(testResults[x] - average);
  }
  stDeviation = sqrt(sum/samples); //find the standard deviation by finding the square root of the average of the squared difference from average (confused yet?)
  stDeviation = (stDeviation * sdFactor) / 100; //apply a factor to standard deviation, allows for tuning the filter
  sum=0;
  numPoints = 0;
  for(int x=0; x<samples; x++) {
    if(abs(testResults[x]-average) < stDeviation) { //sum the raw values that fall within standard deviation
      sum += testResults[x];
      numPoints++; //log the number of data points collected
    }
  }
  average = sum/numPoints; //find the standard deviation corrected average
  
  //serial string for PLX-DAQ
  Serial.print("DATA,");
  Serial.println(average);
  //Serial.print(",");
  //Serial.println(endtime);
  
  Serial.print(average);
  Serial.print(", ");
  Serial.print(numPoints);
  Serial.print(", ");
  Serial.print(lowResultRejections);
  Serial.print(", ");
  Serial.print(highResultRejections);
  Serial.print(", ");
  Serial.println(stDeviation);
}
void checkStatus()
{
  endtime=TCNT1; //read timer1 counter to find how many cycles have passed
  stat = readRegister(0x07,1);
  if(((stat & 0b00100000) >> 5) == 1) { //check for TX_DS interrupt
    writeRegister(0x07, 0b00100000); //clear TX_DS status
    stat = 1;
  } else if(((stat & 0b00010000) >> 4) == 1) { //check for MAX_RT interrupt
    stat=2;
    writeRegister(0x07, 0b00010000); //clear MAX_RT status
    sendCommand(0b11100001); //clear TX FIFO
    sendCommand(0b11100011); //reuse last transmitted payload
  }
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
}
