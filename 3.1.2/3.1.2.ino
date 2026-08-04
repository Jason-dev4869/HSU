/* RGB led */
#define RED_LED_PIN 14
#define GREEN_LED_PIN 12
#define BLUE_LED_PIN 13

/* Wifi */
#include <WiFi.h>
#define AP_SSID "HSU_Students"
#define AP_PASSWORD "tontrongsukhacbiet"

/* Google Firebase */
#include <FirebaseESP32.h> // ref: https://github.com/mobizt/Firebase-ESP32
#define DB_URL "https://rgb-led-5ffce-default-rtdb.asia-southeast1.firebasedatabase.app/" // Realtime Database >> Data >> URL
#define DB_SECRET "4PrY4W7tpfoVz7iiq2iwrLces0F9zrrCGPQQaJVb" // Project settings >> Service accounts >> Database secrets
FirebaseConfig config; FirebaseAuth auth; FirebaseData fbdo; // firebase data object

// setup to run only once
void setup() {
  Serial.begin(115200);
  initRGBLed();
  initWifi();
  initFirebase();
}

// loop to run repeatedly
int red = 0, green = 0, blue = 0;
void loop() {
  getRGBfromFirebase(red, green, blue);
  onRGBLed(red, green, blue);
  delay(100);
}

/* RGB led */
void initRGBLed() {
  pinMode(RED_LED_PIN, OUTPUT);
  pinMode(GREEN_LED_PIN, OUTPUT);
  pinMode(BLUE_LED_PIN, OUTPUT);
}

void onRGBLed(int red, int green, int blue) {
  if (red == 1) digitalWrite(RED_LED_PIN, HIGH);
  else digitalWrite(RED_LED_PIN, LOW);
  if (green == 1) digitalWrite(GREEN_LED_PIN, HIGH);
  else digitalWrite(GREEN_LED_PIN, LOW);
  if (blue == 1) digitalWrite(BLUE_LED_PIN, HIGH);
  else digitalWrite(BLUE_LED_PIN, LOW);
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

void getRGBfromFirebase(int& red, int& green, int& blue) {
  if (Firebase.ready()) {
    if (Firebase.getInt(fbdo, "LEDs/R")) red = fbdo.intData();
    if (Firebase.getInt(fbdo, "LEDs/G")) green = fbdo.intData();
    if (Firebase.getInt(fbdo, "LEDs/B")) blue = fbdo.intData();
    Serial.println("RGB: " + String(red) + String(green) + String(blue)); // for DEBUG
  }
}