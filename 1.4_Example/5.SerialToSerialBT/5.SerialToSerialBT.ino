/* BLUETOOTH */
#include <BluetoothSerial.h>
BluetoothSerial SerialBT;
#define DEVICE_NAME "ESP32"

// setup to run only once
void setup() {
  Serial.begin(115200);
  initBluetooth();
}

// loop to run repeatedly
void loop() {
  if (SerialBT.available()) {
    String msg = SerialBT.readString();
    Serial.println("Received message: " + msg);
    String rev = reverse(msg);
    SerialBT.println("Reversed message: " + rev);
  }
}

/* BLUETOOTH */
void initBluetooth() {
  SerialBT.begin(DEVICE_NAME);
  Serial.println(DEVICE_NAME + String(" started, now you can pair it!"));
}

/* Helpers */
String reverse(String msg) {
  String result = "";
  for (int i = msg.length() - 1; i >= 0; i--) {
    result += msg[i];
  }
  return result;
}