#include "Arduino.h"
#include <SPI.h>
#include <RF24.h>

RF24 radio(7, 8);
byte addresses[][6] = {"1Node","2Node"};

void setup() {
  Serial.begin(9600);
  Serial.println("RECEIVER CODE");
  radio.begin();
  radio.setPALevel(RF24_PA_MIN);
  radio.setDataRate(RF24_2MBPS);
  radio.setChannel(122);
  radio.openWritingPipe(addresses[0]);
  radio.openReadingPipe(1, addresses[1]);
  radio.startListening();
}

void loop() {

  char data;
  
  if ( radio.available()) {
   
    while (radio.available()) {
      radio.read( &data, sizeof(char));
    }

    radio.stopListening();
    radio.write( "ACK", sizeof(char) );
    radio.startListening();

    Serial.print("Recieved: ");
    Serial.println(&data);
    Serial.println("Sent response: ACK");
  }

}
