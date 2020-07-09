#include "Arduino.h"
#include <SPI.h>
#include <RF24.h>

RF24 radio(7, 8);
byte addresses[][6] = {"1Node", "2Node"};

void setup() {
  Serial.begin(9600);
  Serial.println("TRANSMITTERDE CODE");
  radio.begin();
  radio.setPALevel(RF24_PA_MIN);
  radio.setDataRate(RF24_2MBPS);
  radio.setChannel(122);
  radio.openWritingPipe(addresses[1]);
  radio.openReadingPipe(1, addresses[0]);
  randomSeed(analogRead(A0));
}

void loop() {
 
  char data = "REQ";
  radio.stopListening();
   
  unsigned long previousMillis=0;
  unsigned long currentMillis;
  currentMillis = micros();
  
  
  if (!radio.write( &data, sizeof(unsigned char) )) {
    Serial.println("No acknowledgement of transmission - receiving radio device connected?");    
  }
  radio.startListening();
  unsigned long started_waiting_at = millis();
  while ( ! radio.available() ) {
    if (millis() - started_waiting_at > 200 ) {
      Serial.println("No response received - timeout!");
      return;
    }
  }
  unsigned char dataRx;
  radio.read( &dataRx, sizeof(unsigned char) );

  Serial.print(micros()- currentMillis);
  Serial.println(" mus");


}
