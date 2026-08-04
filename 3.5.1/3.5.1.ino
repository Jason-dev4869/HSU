/* Bluetooth A2DP */
#include <AudioTools.h> // ref: https://github.com/pschatzmann/arduino-audio-tools
#include <BluetoothA2DPSink.h> // ref: https://github.com/pschatzmann/ESP32-A2DP
I2SStream i2s;
BluetoothA2DPSink a2dp(i2s);
#define LRC_PIN  25
#define BCLK_PIN 26
#define DIN_PIN  27
#define DEVICE_NAME "<device_name>"

// setup to run only once
void setup() {
  Serial.begin(115200);
  initA2DP();
}

// loop to run repeatedly
void loop() {}

/* Bluetooth A2DP */
void initA2DP() {
  I2SConfig cfg = i2s.defaultConfig();
  cfg.pin_bck = BCLK_PIN;
  cfg.pin_ws = LRC_PIN;
  cfg.pin_data = DIN_PIN;
  i2s.begin(cfg);
  a2dp.start(DEVICE_NAME);
  Serial.println("Bluetooth Speaker is ready to pair");
}