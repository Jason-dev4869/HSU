/* WiFi */
#include <WiFi.h>
#define AP_SSID "HieuChau1"
#define AP_PASSWORD "alochau2003"

/* Epoch Time */
#include <time.h>
#define NTP_SERVER "sg.pool.ntp.org"

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  initWifi();
  initEpochTime();
}

void loop() {
  // put your main code here, to run repeatedly:
  long now = getEpochTime();
  Serial.println(now);
  delay(100);
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