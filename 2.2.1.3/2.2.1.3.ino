/* Light sensor */
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

void setup() {
  // put your setup code here, to run once:
  initSensor();
  initOled();
}

void loop() {
  // put your main code here, to run repeatedly:
  bool light = readD0();
  if (light) {
  //Serial.println("Light: +");
    printOled("Light sensor", "Light: +");
  } else {
    //Serial.println("Light: -");
    printOled("Light sensor", "Light: -");
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