/* Sound sensor */
#define D0_PIN 15

/* Oled */
#define SDA_PIN 21
#define SCL_PIN 22
#define ssd1306 // Oled 0.96"
//#define sh1106 // Oled 1.3"
#if defined(ssd1306)
  #include <SSD1306.h> // ref: https://github.com/ThingPulse/esp8266-oled-ssd1306
  SSD1306 oled(0x3C, SDA_PIN, SCL_PIN); // from 'I2C_scanner.ino' sketch
#elif defined(sh1106)
  #include <SH1106.h> // ref: https://github.com/ThingPulse/esp8266-oled-ssd1306
  SH1106 oled(0x3C, SDA_PIN, SCL_PIN); // from 'I2C_scanner.ino' sketch
#endif

// setup to run only once
void setup() {
  Serial.begin(115200);
  initSensor();
  initOled();
}

// loop to run repeatedly
void loop() {
  readD0();
}

/* Sound sensor */
void initSensor() {
  pinMode(D0_PIN, INPUT);
}

int clap = 0;
long detection_range_start = 0, detection_range = 0;
void readD0() {
  int dValue = digitalRead(D0_PIN); // 0:sound; 1:no-sound
  if (dValue == 0) {
    if (clap == 0) {
      clap++;
      detection_range_start = detection_range = millis();
    } else {
      if (millis() - detection_range >= 100) {
        clap++;
        detection_range = millis();
      }
    }
  }
  if (millis() - detection_range_start >= 300) {
    if (clap == 1) {
      printOled("CLAP", "1 time");
    } else if (clap == 2) {
      printOled("CLAP", "2 times");
    }
    clap = 0;
  }
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
  oled.drawString(0, 36, line2);
  oled.display();
}