
bool system_on = false;
String input = "";

void setup() {
  Serial.begin(115200);
}

void loop() {
  
  int rssi = random(-90,-40);
  
  if (Serial.available() > 0) {
    input = Serial.readString();
    if (input.indexOf("start") >= 0) { Serial.println("ack"); system_on = true; }
    else if (input.indexOf("end") >= 0) { Serial.println("ack"); system_on = false; }
  }

  if (system_on) {
    Serial.print("Test1|b4:cf:84:6f:2b:e4|");
    Serial.println(rssi);
  }
  
  delay(1000);
}
