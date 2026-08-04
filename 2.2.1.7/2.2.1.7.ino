/* Light sensor */
#define D0_PIN 15

/* Wifi */
#include <WiFi.h>
#define AP_SSID "HSU_Students"
#define AP_PASSWORD "tontrongsukhacbiet"

/* Epoch time */
#include <time.h>
#define NTP_SERVER "sg.pool.ntp.org"

/* Blynk cloud */
#define BLYNK_TEMPLATE_ID "TMPL6oN7XlSAy"
#define BLYNK_TEMPLATE_NAME "LightSensor"
#define BLYNK_AUTH_TOKEN "fZjz3Vw7OMM-CwQG0A6IDh7QrSFNzUu-"
#include <BlynkSimpleEsp32.h>

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  initSensor();
  initWifi();
  initEpochTime();
  initBlynk();
}

void loop() {
  // put your main code here, to run repeatedly:
  Blynk.run();
  bool light = readD0();
  if (light) {
  //Serial.println("Light: +");
    setLightToBlynk(light);
  } else {
    //Serial.println("Light: -");
    setLightToBlynk(light);
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

/* Blynk cloud */
void initBlynk() {
  Blynk.config(BLYNK_AUTH_TOKEN);
  if (Blynk.connect()) Serial.println("Blynk connected");
}

void setLightToBlynk(int light) {
  long now = getEpochTime();
  Serial.println(String(light) + ":" + String(now)); // for DEBUG
  if (Blynk.connected()) {
    Blynk.virtualWrite(V0, light);
    Blynk.virtualWrite(V1, now);
  }
}