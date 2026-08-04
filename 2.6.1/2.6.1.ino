/* Reed switch */
#define DO_PIN 15

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
  bool state = readDO();
  if (state) {
    printOled("MC38", "State: open");
  } else {
    printOled("MC38", "State: close");
  }
  delay(100);
}

/* Reed switch */
void initSensor() {
  pinMode(DO_PIN, INPUT_PULLUP);
}

bool readDO() {
  int dValue = digitalRead(DO_PIN); // 0:close; 1:open
  if (dValue) return true;
  else return false;
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