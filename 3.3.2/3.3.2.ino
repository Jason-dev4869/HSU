/* Servo */
#include <ESP32Servo.h> // ref: https://madhephaestus.github.io/ESP32Servo/annotated.html
#define SERVO_PIN 15
Servo servo;

/* Wifi */
#include <WiFi.h>
#define AP_SSID "HSU_Students"
#define AP_PASSWORD "tontrongsukhacbiet"

/* Google Firebase */
#include <FirebaseESP32.h> // ref: https://github.com/mobizt/Firebase-ESP32
#define DB_URL "https://servo-f0e85-default-rtdb.asia-southeast1.firebasedatabase.app/" // Realtime Database >> Data >> URL
#define DB_SECRET "Lm8xwSClecqbBBIFSz3tcSJ4xk8zqCrMXnNUzKb3" // Project settings >> Service accounts >> Database secrets
FirebaseConfig config; FirebaseAuth auth; FirebaseData fbdo; // firebase data object

// setup to run only once
void setup() {
  Serial.begin(115200);
  initServo();
  initWifi();
  initFirebase();
  setValueToFirebase(0);
}
// loop to run repeatedly
int oldValue = 0;
void loop() {
  int newValue = getValueFromFirebase(); // 0:down, 1:up
  if (newValue == 1 && oldValue == 0) {
    upServo();
    oldValue = 1;
  } else if (newValue == 0 && oldValue == 1) {
    downServo();
    oldValue = 0;
  }
  delay(100);
}

/* Servo */
void initServo() {
  servo.attach(SERVO_PIN);
  servo.write(0);
}
void upServo() {
  for (int pos = 0; pos <= 180; pos += 1) { // from 0-180 degrees in steps of 1 degree
    servo.write(pos); delay(20);
  }
}
void downServo() {
  for (int pos = 180; pos >= 0; pos -= 1) { // from 180-0 degrees in steps of -1 degree
    servo.write(pos); delay(20);
  }
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

void setValueToFirebase(int value) {
  if (Firebase.ready()) {
    Firebase.setInt(fbdo, "SERVO/value", value);
  }
}
int getValueFromFirebase() {
  int value = -1;
  if (Firebase.ready()) {
    if (Firebase.getInt(fbdo, "SERVO/value")) value = fbdo.intData();
    Serial.println("value: " + String(value)); // for DEBUG
  }
  return value;
}