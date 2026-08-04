/* Light sensor */
#define D0_PIN 15

/* Wifi */
#include <WiFi.h>
#define AP_SSID "HSU_Students"
#define AP_PASSWORD "tontrongsukhacbiet"

/* Telegram bot */
#include <UniversalTelegramBot.h> // ref: https://github.com/witnessmenow/Universal-Arduino-Telegram-Bot
#define BOTtoken "8824232804:AAG5aQ29-24E-5-9DHG5whEUUgzNbTVcEZA" // from BotFather
#define CHAT_ID "8833200606" // from IDBot
#include <WiFiClientSecure.h>
WiFiClientSecure client;
UniversalTelegramBot bot(BOTtoken, client);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  initSensor();
  initWifi();
  initTelegram();
}

void loop() {
  // put your main code here, to run repeatedly:
  bool light = readD0();
  if (light) {
    //Serial.println("Light: +");
    bot.sendMessage(CHAT_ID, "Light: +", "");
  } else {
    //Serial.println("Light: -");
    bot.sendMessage(CHAT_ID, "Light: -", "");
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

void initTelegram() {
  client.setCACert(TELEGRAM_CERTIFICATE_ROOT); // add root certificate for api.telegram.org
  bot.sendMessage(CHAT_ID, "Bot started up", "");
}