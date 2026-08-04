/* Relay */
#define RELAY_PIN 13

/* Wifi */
#include <WiFi.h>
#define AP_SSID "HSU_Students"
#define AP_PASSWORD "tontrongsukhacbiet"

/* Google Firebase */
#include <FirebaseESP32.h> // ref: https://github.com/mobizt/Firebase-ESP32
#define DB_URL "https://relay-motor-default-rtdb.asia-southeast1.firebasedatabase.app/" // Realtime Database >> Data >> URL
#define DB_SECRET "HRCsh3Z5MtMrrr19F1bDcho9YeqxFyna2vI4yNAp" // Project settings >> Service accounts >> Database secrets
FirebaseConfig config; FirebaseAuth auth; FirebaseData fbdo; // firebase data object

// setup to run only once
void setup() {
  Serial.begin(115200);
  initRelay();
  initWifi();
  initFirebase();
}
// loop to run repeatedly
void loop() {
  int value = getValueFromFirebase();
  if (value){
    onRelay();
  } else {
    offRelay();
  } 
  delay(100);
}

/* Relay */
void initRelay() {
  pinMode(RELAY_PIN, OUTPUT);
}
void onRelay() {
  digitalWrite(RELAY_PIN, HIGH);
}
void offRelay() {
  digitalWrite(RELAY_PIN, LOW);
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

/* Google Firebase */
void initFirebase() {
  config.database_url = DB_URL;
  config.signer.tokens.legacy_token = DB_SECRET;
  Firebase.begin(&config, &auth);
  Firebase.reconnectNetwork(true);
}

int getValueFromFirebase() {
  int value = -1;
  if (Firebase.ready()) {
    if (Firebase.getInt(fbdo, "MOTOR/value")) value = fbdo.intData();
    Serial.println("value: " + String(value)); // for DEBUG
  }
  return value;
}