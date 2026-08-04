/* Oled */
#if defined(ESP8266)
  #define SDA_PIN D2
  #define SCL_PIN D1
#elif defined(ESP32)
  #define SDA_PIN 21
  #define SCL_PIN 22
#endif
#define ssd1306 // Oled 0.96"
//#define sh1106 // Oled 1.3"
#if defined(ssd1306)
  #include <SSD1306.h> // ref: https://github.com/ThingPulse/esp8266-oled-ssd1306
  SSD1306 oled(0x3C, SDA_PIN, SCL_PIN); // from 'I2C_scanner.ino' sketch
#elif defined(sh1106)
  #include <SH1106.h> // ref: https://github.com/ThingPulse/esp8266-oled-ssd1306
  SH1106 oled(0x3C, SDA_PIN, SCL_PIN); // from 'I2C_scanner.ino' sketch
#endif

// setup to run only once
void setup() {
  initOled();
}

// loop to run repeatedly
void loop() {
  String line1 = "* Chau";
  String line2 = "* Khoi";
  String line3 = ">> C_IoT";
  String line4 = ">> K_IoT";
  printOled(line1, line2); delay(2000);
  printOled(line1, line2, line3); delay(2000);
  printOled(line1, line2, line3, line4); delay(2000);
}

/* Oled */
void initOled() {
  oled.init();
  oled.flipScreenVertically();
}

void printOled(String line1, String line2) {
  oled.clear();
  oled.setTextAlignment(TEXT_ALIGN_LEFT);
  oled.setFont(ArialMT_Plain_24);
  oled.drawString(0, 0, line1);
  oled.drawString(0, 36, line2);
  oled.display();
}

void printOled(String line1, String line2, String line3) {
  oled.clear();
  oled.setTextAlignment(TEXT_ALIGN_LEFT);
  oled.setFont(ArialMT_Plain_16);
  oled.drawString(0, 0, line1);
  oled.drawString(0, 24, line2);
  oled.drawString(0, 48, line3);
  oled.display();
}

void printOled(String line1, String line2, String line3, String line4) {
  oled.clear();
  oled.setTextAlignment(TEXT_ALIGN_LEFT);
  oled.setFont(ArialMT_Plain_10);
  oled.drawString(0, 0, line1);
  oled.drawString(0, 16, line2);
  oled.drawString(0, 32, line3);
  oled.drawString(0, 48, line4);
  oled.display();
}