/* Light sensor */
#define D0_PIN 15

/* Wifi */
#include <WiFi.h>
#define AP_SSID "HSU_Students"
#define AP_PASSWORD "tontrongsukhacbiet"

/* Epoch time */
#include <time.h>
#define NTP_SERVER "sg.pool.ntp.org"

/* Google script */
#include <HTTPClient.h>
#include <WiFiClientSecure.h>
String GSCRIPT_ID = "AKfycbzYLCe-u4Aa_K1z7p9q8E1vP8K2AtOP4fvUPx5LvfsRwaQsZPxXy-0-ustZpRCoRLHi";

// setup to run only once
void setup() {
  Serial.begin(115200);
  initSensor();
  initWifi();
  initEpochTime();
}
// loop to run repeatedly
void loop() {
  bool light = readD0();
  if (light) {
  //Serial.println("Light: +");
    setLightToGscript(light);
  } else {
    //Serial.println("Light: -");
    setLightToGscript(light);
  }
  delay(1000);
}

/* Light sensor */
void initSensor() {
  pinMode(D0_PIN, INPUT);
}

bool readD0() {
  int dValue = digitalRead(D0_PIN); // 0:light; 1:no-light
  if (dValue) return false;
  else return true;
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

/* Google script */
void setLightToGscript(int light) {
  long now = getEpochTime();
  Serial.println(String(light) + ":" + String(now)); // for DEBUG
  String url = "https://script.google.com/macros/s/" + GSCRIPT_ID + "/exec?" + "value=" + light
             + "&updated=" + now;
  HTTPClient https;
  WiFiClientSecure client; client.setInsecure();
  https.begin(client, url);
  int statusCode = https.GET();
  Serial.println("HTTP Status Code: " + String(statusCode)); // for DEBUG
  https.end();
}