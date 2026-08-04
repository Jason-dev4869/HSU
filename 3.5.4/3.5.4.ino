/* Keypad */
#include <Keypad.h> // ref: https://github.com/Chris--A/Keypad
#define ROWS 4 // four rows
#define COLS 4 // four columns
byte rowPins[ROWS] = {5, 18, 19, 23}; // connect to the row pinouts of the keypad
byte colPins[COLS] = {0, 4, 16, 17}; // connect to the column pinouts of the keypad

char keys[ROWS][COLS] = {
  {'1','2','3','A'},
  {'4','5','6','B'},
  {'7','8','9','C'},
  {'*','0','#','D'}
};

Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

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
String text = "";
void loop() {
  audio.loop(); // required to keep audio playback running smoothly
  if (!audio.isRunning() && millis() - last >= 100) { // delay(100)
    char key = keypad.getKey();
    if ('0' <= key && key <= '9') {
      Serial.print(key); // for DEBUG
      text += key;
    } else if (key == '*' || key == '#') {
      Serial.println(key); // for DEBUG
      text2speech(text);
      text = "";
    }
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