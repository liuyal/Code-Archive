
#define PIN 7

void setup() {
  pinMode(PIN, OUTPUT);     // Initialize the BUILTIN_LED pin as an output
}

// the loop function runs over and over again forever
void loop() {
  digitalWrite(PIN, LOW); 
  delay(1000);                     
  digitalWrite(PIN, HIGH);
  delay(1000);
}
