/* Light sensor */
#define D0_PIN 15

/* Wifi */
#include <WiFi.h>
#define AP_SSID "HSU_Students"
#define AP_PASSWORD "tontrongsukhacbiet"

/* Epoch time */
#include <time.h>
#define NTP_SERVER "sg.pool.ntp.org"

/* Google Firebase */
#include <FirebaseESP32.h> // ref: https://github.com/mobizt/Firebase-ESP32
#define DB_URL "https://lightsensor-ab9ca-default-rtdb.asia-southeast1.firebasedatabase.app/" // Realtime Database >> Data >> URL
#define DB_SECRET "x5UX80bEwfTGgaaOfJbxUvie38aUIC48p6liqwEt" // Project settings >> Service accounts >> Database secrets
FirebaseConfig config; FirebaseAuth auth; FirebaseData fbdo; // firebase data object

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  initSensor();
  initWifi();
  initEpochTime();
  initFirebase();
}

void loop() {
  // put your main code here, to run repeatedly:
  bool light = readD0();
  if (light) {
  //Serial.println("Light: +");
    setLightToFirebase(light);
  } else {
    //Serial.println("Light: -");
    setLightToFirebase(light);
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

/* Google Firebase */
void initFirebase() {
  config.database_url = DB_URL;
  config.signer.tokens.legacy_token = DB_SECRET;
  Firebase.begin(&config, &auth);
  Firebase.reconnectNetwork(true);
}

void setLightToFirebase(int light) {
  if (Firebase.ready()) {
    Firebase.setInt(fbdo, "LIGHT/value", light);
    Firebase.setInt(fbdo, "LIGHT/updated", getEpochTime());
  }
}