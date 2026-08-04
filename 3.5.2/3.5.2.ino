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
    text2speech("Xin chào chúng tôi là Châu và Khôi");
    last = millis();
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