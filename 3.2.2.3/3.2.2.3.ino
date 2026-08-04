/* DHT11 */
#define DHT_PIN 15
#include <DHT11.h> // ref: https://github.com/dhrubasaha08/DHT11
DHT11 dht11(DHT_PIN);

/* Relay */
#define RELAY_PIN 13

void setup() {
  Serial.begin(115200);
  initRelay();

}
// loop to run repeatedly
int temp = 0, humi = 0;
void loop() {
  readDHT11(temp, humi);
  Serial.println("Temperature: " + String(temp)); // for DEBUG
  Serial.println("Humidity: " + String(humi)); // for DEBUG
  if (temp > 29) {
    onRelay();
  } else {
    offRelay();
  }
  delay(100);
}

/* DHT11 */
void readDHT11(int& temp, int& humi) {
  int temperature = dht11.readTemperature(); delay(10);
  int humidity = dht11.readHumidity();
  if (temperature != DHT11::ERROR_CHECKSUM && temperature != DHT11::ERROR_TIMEOUT &&
      humidity != DHT11::ERROR_CHECKSUM && humidity != DHT11::ERROR_TIMEOUT) {
    temp = temperature;
    humi = humidity;
  }
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