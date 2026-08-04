/* Wifi */
#include <WiFi.h>

#define AP_SSID "HSU_Students"
#define AP_PASSWORD "tontrongsukhacbiet"

/* Weather API */
#if defined(ESP8266)
  #include <ESP8266HTTPClient.h>
#elif defined(ESP32)
  #include <HTTPClient.h>
#endif
#include <ArduinoJson.h>
String API_KEY = "c8e0c3bd214745619d681223251011"; // from https://www.weatherapi.com/my
String CITY = "Ho_Chi_Minh";

/* Oled */
#define OLED_SDA_PIN 21
#define OLED_SCL_PIN 22
#define ssd1306 // Oled 0.96"
//#define sh1106 // Oled 1.3"
#if defined(ssd1306)
  #include <SSD1306.h> // ref: https://github.com/ThingPulse/esp8266-oled-ssd1306
  SSD1306 oled(0x3C, OLED_SDA_PIN, OLED_SCL_PIN); // from 'I2C_scanner.ino' sketch
#elif defined(sh1106)
  #include <SH1106.h> // ref: https://github.com/ThingPulse/esp8266-oled-ssd1306
  SH1106 oled(0x3C, OLED_SDA_PIN, OLED_SCL_PIN); // from 'I2C_scanner.ino' sketch
#endif

void setup() {
    Serial.begin(115200);
    initOled();
    initWifi();
}

void loop() {
  getWeather();
  delay(10000);
}

/* Wifi */
void initWifi() {
  WiFi.setAutoReconnect(true); WiFi.persistent(true);
  WiFi.begin(AP_SSID, AP_PASSWORD);
  Serial.print("\nConnecting to "); Serial.print(AP_SSID);
  while (WiFi.status() != WL_CONNECTED) { delay(500); Serial.print("."); }
  Serial.print("\nWiFi connected, IP address: "); Serial.println(WiFi.localIP());
  Serial.print("MAC address: "); Serial.println(WiFi.macAddress());
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
  oled.setFont(ArialMT_Plain_10);
  oled.drawString(0, 0, line1);
  oled.drawString(0, 24, line2);
  oled.drawString(0, 48, line3);
  oled.display();
}

/* Weather API */
void getWeather() {
  String url = "http://api.weatherapi.com/v1/current.json?key=" + API_KEY + "&q=" + CITY;

  HTTPClient http;
  WiFiClient client;

  http.begin(client, url);

  int httpCode = http.GET();

  if (httpCode == HTTP_CODE_OK) {
    String payload = http.getString();
    Serial.println(payload); // for DEBUG

    JsonDocument data;
    DeserializationError error = deserializeJson(data, payload);

    if (!error) {
      float temp = data["current"]["temp_c"];
      int humidity = data["current"]["humidity"];
      String desc = data["current"]["condition"]["text"];

      printOled("Temperature: " + String(temp) + " C", 
                "Humidity: " + String(humidity) + " %",
                "Weather: " + desc);
    } else {
      printOled("JSON error: " , String(error.c_str()));
    }
  } else {
    printOled("HTTP error: " , String(httpCode));
  }

  http.end();
}