#include <math.h> 
#define tempPin 0

int val;

void setup() 
{ 
  Serial.begin(9600); 
} 

void loop() 
{ 
  val = analogRead(tempPin);
  float mv = (val/1024.0)*3300;
  float cel = mv/10;
  Serial.print("TEMPRATURE = ");
  Serial.print(cel);
  Serial.print("*C");
  Serial.println();

  delay(1000); 
} 
