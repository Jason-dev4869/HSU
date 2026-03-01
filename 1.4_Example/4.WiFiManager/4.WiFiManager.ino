/* WiFi Manager */
#include <WiFiManager.h>
#define FLASH_BUTTON_PIN 0

/* Epoch Time */
#include <time.h>
#define NTP_SERVER "sg.pool.ntp.org"

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  initWiFiManager();
  initEpochTime();
}

void loop() {
  // put your main code here, to run repeatedly:
  long now = getEpochTime();
  Serial.println(now);
  delay(1000);
}

/* WiFiManager */
void initWiFiManager() {
  pinMode(FLASH_BUTTON_PIN, INPUT_PULLUP);
  Serial.println("\nPress and hold the FLASH/BOOT button for 3 seconds to erase WiFi configuration...");
  // check if the FLASH button is being held
  long pressedTime = 0;
  bool resetTriggered = false;
  // monitor for 5 seconds after boot
  for (int i = 0; i < 5000; i += 100) {
    if (digitalRead(FLASH_BUTTON_PIN) == LOW) {
      if (pressedTime == 0) pressedTime = millis();
      if (millis() - pressedTime >= 3000) {
        resetTriggered = true;
        break;
      }
    } else pressedTime = 0; // FLASH/BOOT button released, reset the counter
    delay(100);
  }
  if (resetTriggered) {
    Serial.println("Erasing WiFi configuration...");
    WiFiManager wm;
    wm.resetSettings(); // clear saved WiFi credentials
    ESP.restart();
  } else {
    WiFiManager wm;
    if (!wm.autoConnect("ESP-ConfigAP")) {
      Serial.println("Failed to connect via WiFiManager, restarting...");
      ESP.restart();
    }
    Serial.print("WiFi connected, IP address: "); Serial.println(WiFi.localIP());
    Serial.print("MAC address: "); Serial.println(WiFi.macAddress());
  }
}

/* Epoch time */
void initEpochTime() {
  configTime(0, 0, NTP_SERVER); // GMT time offset, daylight saving time, NTP server
  Serial.print("Connecting to "); Serial.print(NTP_SERVER);
  while (getEpochTime() == 0) Serial.print(".");
  Serial.print("\nEpoch time: "); Serial.println(getEpochTime());
}

long getEpochTime() {
  tm infoTime;
  if (!getLocalTime(&infoTime)) return 0;
  time_t epochTime;
  time(&epochTime);
  return epochTime;
}
