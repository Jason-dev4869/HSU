/* DHT11 */
#define DHT_PIN 15
#include <DHT11.h> // ref: https://github.com/dhrubasaha08/DHT11
DHT11 dht11(DHT_PIN);

/* Wifi */
#include <WiFi.h>
#define AP_SSID "HSU_Students"
#define AP_PASSWORD "tontrongsukhacbiet"

/* AudioI2S */
#include <Audio.h> // ref: https://github.com/schreibfaul1/ESP32-audioI2S >> version 3.2.1
Audio audio;
#define LRC_PIN  25
#define BCLK_PIN 26
#define DIN_PIN  27

// setup to run only once
void setup() {
  Serial.begin(115200);
  initWifi();
  initAudio();
}

// loop to run repeatedly
long last = 0;
void loop() {
  audio.loop(); // required to keep audio playback running smoothly
  if (!audio.isRunning() && millis() - last >= 10000) { // delay(10000)
    int temp = 0, humi = 0;
    readDHT11(temp, humi);
    Serial.println("Temperature: " + String(temp) + " - Humidity: " + String(humi)); // for DEBUG
    String text = "nhiệt độ là " + String(temp) + " độ C và độ ẩm là " + String(humi) + " phần trăm";
    text2speech(text);
    last = millis();
  }
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

/* AudioI2S */
void initAudio() {
  audio.setPinout(BCLK_PIN, LRC_PIN, DIN_PIN);
  audio.setVolume(21); // max volume
}
void text2speech(String text) {
  Serial.println("Playing audio...");
  String url = "https://translate.google.com/translate_tts?client=tw-ob&tl=vi&q=" + urlEncode(text);
  audio.connecttohost(url.c_str());
}
String urlEncode(String text) {
  String encoded;
  for (char c : text) {
    if (isalnum(c) || strchr("-._~", c)) encoded += c;
    else {
      char hex[4];
      sprintf(hex, "%%%02X", (unsigned char)c);
      encoded += hex;
    }
  }
  return encoded;
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