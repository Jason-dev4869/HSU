/* Wifi */
#include <WiFi.h>

#define AP_SSID "HSU_Students"
#define AP_PASSWORD "tontrongsukhacbiet"

/* CoinGecko API */
#if defined(ESP8266)
  #include <ESP8266HTTPClient.h>
#elif defined(ESP32)
  #include <HTTPClient.h>
#endif
#include <WiFiClientSecure.h>
#include <ArduinoJson.h>
String COINS = "bitcoin,ethereum,cardano"; // from https://api.coingecko.com/api/v3/coins/list
String CURRENCY = "usd"; // from https://api.coingecko.com/api/v3/simple/supported_vs_currencies
int MAX_COINS = 10;

/* Oled */
#define OLED_SDA_PIN 21
#define OLED_SCL_PIN 22
#define ssd1306 // Oled 0.96"
//#define sh1106 // Oled 1.3"
#if defined(ssd1306)
  #include <SSD1306.h> // ref: https://github.com/ThingPulse/esp8266-oled-ssd1306
  SSD1306 oled(0x3C, OLED_SDA_PIN, OLED_SCL_PIN); // from 'I2C_scanner.ino' sketch
#elif defined(sh1106)
  #include <SH1106.h> // ref: https://github.com/ThingPulse/esp8266-oled-ssd1306
  SH1106 oled(0x3C, OLED_SDA_PIN, OLED_SCL_PIN); // from 'I2C_scanner.ino' sketch
#endif

void setup() {
    Serial.begin(115200);
    initWifi();
    initOled();
}

void loop() {
  getPrices();
  delay(2000);
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

/* Oled */
void initOled() {
  oled.init();
  oled.flipScreenVertically();
}

void printOled(String line1, String line2) {
  oled.clear();
  oled.setTextAlignment(TEXT_ALIGN_LEFT);
  oled.setFont(ArialMT_Plain_24);
  oled.drawString(0, 0, line1);
  oled.setFont(ArialMT_Plain_16);
  oled.drawString(0, 36, line2);
  oled.display();
}

/* CoinGecko API */
void getPrices() {
  String url = "https://api.coingecko.com/api/v3/simple/price?ids=" + COINS + "&vs_currencies="+ CURRENCY;

  HTTPClient https;
  WiFiClientSecure client;
  client.setInsecure();

  https.begin(client, url);

  int httpCode = https.GET();

  if (httpCode == HTTP_CODE_OK) {
    String payload = https.getString();

    Serial.println(payload);

    JsonDocument data;
    DeserializationError error = deserializeJson(data, payload);

    if (!error) {
      String coins[MAX_COINS];

      int numCoins = splitString(COINS, ',', coins, MAX_COINS);

      for (int i = 0; i < numCoins; i++) {
        String coin = coins[i];
        double price = data[coin][CURRENCY];

        if (data.containsKey(coin)) {
          printOled("1 " + coin, String(price) + " " + CURRENCY);delay(2000);
        }
      }
    } else {
      printOled("JSON error: " , String(error.c_str()));
    }
  } else {
    printOled("HTTP error: " , String(httpCode));
  }

  https.end();
}

int splitString(String input, char separator, String output[], int maxItems) {
  int count = 0;

  while (input.length() > 0 && count < maxItems) {
    int index = input.indexOf(separator);

    if (index == -1) {
      output[count++] = input;
      break;
    } else {
      output[count++] = input.substring(0, index);
      input = input.substring(index + 1);
    }
  }

  return count;
}