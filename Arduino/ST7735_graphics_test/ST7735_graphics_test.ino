
#include <Adafruit_GFX.h>    // Core graphics library
#include <Adafruit_ST7735.h> // Hardware-specific library for ST7735
#include <SPI.h>

#define sclk 4  // SainSmart: SCL
#define mosi 5  // SainSmart: SDA
#define cs   6  // SainSmart: CS
#define dc   7  // SainSmart: RS/DC
#define rst  8  // SainSmart: RES

Adafruit_ST7735 tft = Adafruit_ST7735(cs, dc, mosi, sclk, rst);

void setup(void) {
  Serial.begin(9600);
  Serial.print(F("Hello! ST77xx TFT Test"));
  tft.initR(INITR_BLACKTAB); 
  Serial.println(F("Initialized"));
  tft.fillScreen(ST77XX_BLACK);
  delay(1000);

  tft.drawFastHLine(0, 30,  tft.width(), ST7735_WHITE);   // draw horizontal white line at position (0, 30)
  tft.setTextColor(ST7735_WHITE, ST7735_BLACK);           // set text color to white and black background
  tft.setTextSize(1);                                     // text size = 1
  tft.setCursor(19, 1);                                   // move cursor to position (19, 15) pixel
  tft.print("WEATHER STATION");
  
  tft.drawFastHLine(0, 76,  tft.width(), ST7735_WHITE);   // draw horizontal white line at position (0, 76)
  tft.drawFastHLine(0, 122,  tft.width(), ST7735_WHITE);  // draw horizontal white line at position (0, 122)
  tft.setTextColor(ST7735_RED, ST7735_BLACK);     // set text color to red and black background
  tft.setCursor(5, 39);                          // move cursor to position (25, 39) pixel
  tft.print("TIME");
  tft.setTextColor(ST7735_CYAN, ST7735_BLACK);    // set text color to cyan and black background
  tft.setCursor(5, 85);                          // move cursor to position (34, 85) pixel
  tft.print("TEMPERATURE");
  tft.setTextColor(ST7735_GREEN, ST7735_BLACK);   // set text color to green and black background
  tft.setCursor(5, 131);                         // move cursor to position (34, 131) pixel
  tft.print("HUMIDITY");
           
  delay(1000);
}

void loop() {
  
  tft.setTextSize(1);

  tft.setTextColor(0xFD00, ST7735_BLACK);
  tft.setCursor(10, 54);
  tft.print("10:30AM");
  
  tft.setTextColor(ST7735_YELLOW, ST7735_BLACK);  
  tft.setCursor(10, 100);
  tft.print("25.00");
  tft.drawCircle(10+35, 102, 2, ST7735_YELLOW);
  tft.setCursor(10+35+5, 100);
  tft.print("C");

  tft.setTextColor(ST7735_MAGENTA, ST7735_BLACK); 
  tft.setCursor(10, 146);
  tft.print("50.00");
  tft.setCursor(10+30+4, 146);
  tft.print("%");

  
  delay(1000);

}
