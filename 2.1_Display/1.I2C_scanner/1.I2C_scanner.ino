#include <Wire.h> // ref: https://randomnerdtutorials.com/esp32-esp8266-i2c-lcd-arduino-ide

// setup to run only once
void setup() {
  Serial.begin(115200);
  Serial.println("I2C scanning...");
  Wire.begin();
}

// loop to run repeatedly
void loop() {
  for (byte addr = 1; addr < 127; addr++) {
    Wire.beginTransmission(addr);
    if (Wire.endTransmission() == 0) {
      Serial.print("I2C device found at address 0x");
      Serial.println(addr, HEX);
    }
  }
  delay(3000);
}