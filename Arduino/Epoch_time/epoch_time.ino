#include <ESP8266WiFi.h>
#include <WiFiClientSecure.h>
#include <NTPClient.h>
#include <WiFiUdp.h> 

const char* ssid = "TELUS3854";
const char* password = "tsp5df7yfy";
unsigned long epoch;
const long utcOffsetInSeconds = 3600;

WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org", utcOffsetInSeconds);

void setup() {
  Serial.begin(9600);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
     delay(500);
     Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  
  timeClient.update();
  Serial.println(timeClient.getEpochTime());
  Serial.println(timeClient.getFormattedTime());
  delay(1000);
}
