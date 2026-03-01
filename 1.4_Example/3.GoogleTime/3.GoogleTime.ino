/* WiFi */
#include <WiFi.h>
#define AP_SSID "HieuChau1"
#define AP_PASSWORD "alochau2003"

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  initWifi();
}

void loop() {
  // put your main code here, to run repeatedly:
  String now = googleTime();
  Serial.println(now);
  delay(1000);
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

/* Google time */
String googleTime() { // ref: http://www.esp8266.com/viewtopic.php?f=29&t=6007
  WiFiClient client;
  while (!client.connect("google.com", 80)) { Serial.println("Connecting to GOOGLE failed, retrying ..."); }
  client.print("HEAD / HTTP/1.1\r\n\r\n");
  while(!client.available()) { yield(); }
  while(client.available()) {
    if (client.read() == '\n') {
      if (client.read() == 'D') {
        if (client.read() == 'a') {
          if (client.read() == 't') {
            if (client.read() == 'e') {
              if (client.read() == ':') {
                client.read();
                String theDate = client.readStringUntil('\r');
                client.stop();
                return theDate;
              }
            }
          }
        }
      }
    }
  }
  return "ERROR";
}