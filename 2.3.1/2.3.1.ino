/* DHT11 */
#define DHT_PIN 15
#include <DHT11.h> // ref: https://github.com/dhrubasaha08/DHT11
DHT11 dht11(DHT_PIN);

/* Oled */
#define SDA_PIN 21
#define SCL_PIN 22
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
  Serial.begin(115200);
  initOled();
}

// loop to run repeatedly
void loop() {
  int temp = 0, humi = 0;
  readDHT11(temp, humi);
  printOled("Temp: " + String(temp), "Humi: " + String(humi));
  delay(1000);
}

/* DHT11 */
void readDHT11(int& temp, int& humi) {
  int temperature = dht11.readTemperature(); delay(10);
  int humidity = dht11.readHumidity();
  if (temperature != DHT11::ERROR_CHECKSUM && temperature != DHT11::ERROR_TIMEOUT &&
      humidity != DHT11::ERROR_CHECKSUM && humidity != DHT11::ERROR_TIMEOUT) {
    temp = temperature;
    humi = humidity;
  }
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