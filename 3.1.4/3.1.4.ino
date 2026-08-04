/* RGB led */
#define RED_LED_PIN 14
#define GREEN_LED_PIN 12
#define BLUE_LED_PIN 13

/* Wifi */
#include <WiFi.h>
#define AP_SSID "HSU_Students"
#define AP_PASSWORD "tontrongsukhacbiet"

/* Blynk cloud */
#define BLYNK_TEMPLATE_ID "TMPL6uOHwto0N"
#define BLYNK_TEMPLATE_NAME "LED RGB"
#define BLYNK_AUTH_TOKEN "Plz0SexZuc3MALC2xlTighUtUGE9lOZQ"
#include <BlynkSimpleEsp32.h>

// setup to run only once
void setup() {
  Serial.begin(115200);
  initRGBLed();
  initWifi();
  initBlynk();
}
// loop to run repeatedly
int red = 0, green = 0, blue = 0;
void loop() {
  Blynk.run(); // keep the connection to the server
  onRGBLed(red, green, blue);
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

/* Blynk cloud */
void initBlynk() {
  Blynk.config(BLYNK_AUTH_TOKEN);
  if (Blynk.connect()) Serial.println("Blynk connected");
}
BLYNK_WRITE(V1) {
  red = param.asInt();
  Serial.println("RGB: " + String(red) + String(green) + String(blue)); // for DEBUG
}
BLYNK_WRITE(V0) {
  green = param.asInt();
  Serial.println("RGB: " + String(red) + String(green) + String(blue)); // for DEBUG
}
BLYNK_WRITE(V2) {
  blue = param.asInt();
  Serial.println("RGB: " + String(red) + String(green) + String(blue)); // for DEBUG
}