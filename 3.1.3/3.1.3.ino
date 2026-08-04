/* RGB led */
#define RED_LED_PIN 14
#define GREEN_LED_PIN 12
#define BLUE_LED_PIN 13

/* Wifi */
#include <WiFi.h>
#define AP_SSID "HSU_Students"
#define AP_PASSWORD "tontrongsukhacbiet"

/* MQTT broker */
#include <PubSubClient.h> // ref: http://pubsubclient.knolleary.net
#define MQTT_SERVER "broker.hivemq.com" // HiveMQ broker
#define MQTT_PORT 1883
#define MQTT_NAME "Led_MTTQ"
WiFiClient client;
PubSubClient mqttClient(client);

// setup to run only once
void setup() {
  Serial.begin(115200);
  initRGBLed();
  initWifi();
  initMQTT();
  subscribeRGBfromMQTT();
}

// loop to run repeatedly
int red = 0, green = 0, blue = 0;
void loop() {
  mqttClient.loop(); // keep the connection to the server
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

/* MQTT broker */
void initMQTT() {
  mqttClient.setServer(MQTT_SERVER, MQTT_PORT);
  Serial.print("Connecting to "); Serial.print(MQTT_SERVER);
  String clientId = WiFi.macAddress();
  while (!mqttClient.connected()) {
    Serial.print(".");
    if (mqttClient.connect(clientId.c_str())) {
      Serial.println("\nMQTT connected");
    } else {
      Serial.println("\nMQTT error, state: " + String(mqttClient.state()));
      delay(1000);
    }
  }
}

String topicR = String(MQTT_NAME) + "/LEDs/R";
String topicG = String(MQTT_NAME) + "/LEDs/G";
String topicB = String(MQTT_NAME) + "/LEDs/B";
void subscribeRGBfromMQTT() {
  mqttClient.subscribe(topicR.c_str());
  mqttClient.subscribe(topicG.c_str());
  mqttClient.subscribe(topicB.c_str());
  mqttClient.setCallback(callbackMQTT);
}

void callbackMQTT(char* topic, byte* message, unsigned int length) {
  String payload = "";
  for (int i = 0; i < length; i++) payload += (char)message[i];
  payload.trim();
  if (String(topic) == topicR) red = payload.toInt();
  if (String(topic) == topicG) green = payload.toInt();
  if (String(topic) == topicB) blue = payload.toInt();
  Serial.println("RGB: " + String(red) + String(green) + String(blue)); // for DEBUG
}