/* Light sensor */
#define D0_PIN 15

/* Wifi */
#include <WiFi.h>
#define AP_SSID "HSU_Students"
#define AP_PASSWORD "tontrongsukhacbiet"

/* Epoch time */
#include <time.h>
#define NTP_SERVER "sg.pool.ntp.org"

/* MQTT broker */
#include <PubSubClient.h> // ref: http://pubsubclient.knolleary.net
#define MQTT_SERVER "broker.hivemq.com" // HiveMQ broker
#define MQTT_PORT 1883
#define MQTT_NAME "LightSensor_MTTQ"
WiFiClient client;
PubSubClient mqttClient(client);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  initSensor();
  initWifi();
  initEpochTime();
  initMQTT();
}

void loop() {
  // put your main code here, to run repeatedly:
  mqttClient.loop();
  bool light = readD0();
  if (light) {
  //Serial.println("Light: +");
    publishLightToMQTT(light);
  } else {
    //Serial.println("Light: -");
    publishLightToMQTT(light);
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

void publishLightToMQTT(int light) {
  long now = getEpochTime();
  Serial.println(String(light) + ":" + String(now)); // for DEBUG
  if (mqttClient.connected()) {
    String topicValue = String(MQTT_NAME) + "/LIGHT/value";
    String topicUpdated = String(MQTT_NAME) + "/LIGHT/updated";
    mqttClient.publish(topicValue.c_str(), String(light).c_str());
    mqttClient.publish(topicUpdated.c_str(), String(now).c_str());
  }
}