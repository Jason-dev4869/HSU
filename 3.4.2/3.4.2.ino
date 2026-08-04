/* Active buzzer */
#define BUZZER_PIN 13

/* Wifi */
#include <WiFi.h>
#define AP_SSID "HSU_Students"
#define AP_PASSWORD "tontrongsukhacbiet"

/* Google Firebase */
#include <FirebaseESP32.h> // ref: https://github.com/mobizt/Firebase-ESP32
#define DB_URL "https://buzzer-4d438-default-rtdb.asia-southeast1.firebasedatabase.app/" // Realtime Database >> Data >> URL
#define DB_SECRET "fSpHhE33P1AA5eKrHAom3RDcHxj8Yf7I9nQILCnD" // Project settings >> Service accounts >> Database secrets
FirebaseConfig config; FirebaseAuth auth; FirebaseData fbdo; // firebase data object

// setup to run only once
void setup() {
  Serial.begin(115200);
  initBuzzer();
  initWifi();
  initFirebase();
}

// loop to run repeatedly
void loop() {
  int value = getValueFromFirebase();
  if (value) {
    sosBuzzer();
  } else {
    offBuzzer();
  }
  delay(500);
}

/* Active buzzer */
void initBuzzer() {
  pinMode(BUZZER_PIN, OUTPUT);
  offBuzzer();
}
void sosBuzzer() {
  for (int i = 1; i <= 3; i++) {
    digitalWrite(BUZZER_PIN, LOW); delay(50); // turn on
    digitalWrite(BUZZER_PIN, HIGH); delay(100); // turn off
  }
  delay(100);
  for (int i = 1; i <= 3; i++) {
    digitalWrite(BUZZER_PIN, LOW); delay(200);
    digitalWrite(BUZZER_PIN, HIGH); delay(100);
  }
  delay(100);
  for (int i = 1; i <= 3; i++) {
    digitalWrite(BUZZER_PIN, LOW); delay(50);
    digitalWrite(BUZZER_PIN, HIGH); delay(100);
  }
}

void offBuzzer() {
  digitalWrite(BUZZER_PIN, HIGH);
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
    if (Firebase.getInt(fbdo, "BUZZER/value")) value = fbdo.intData();
    Serial.println("value: " + String(value)); // for DEBUG
  }
  return value;
}