/* Keypad */
#include <Keypad.h> // ref: https://github.com/Chris--A/Keypad
#define ROWS 4 // four rows
#define COLS 4 // four columns
byte rowPins[ROWS] = {5, 18, 19, 23}; // connect to the row pinouts of the keypad
byte colPins[COLS] = {0, 4, 16, 17}; // connect to the column pinouts of the keypad

char keys[ROWS][COLS] = {
  {'1','2','3','A'},
  {'4','5','6','B'},
  {'7','8','9','C'},
  {'*','0','#','D'}
};

Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

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

// setup to run only once
void setup() {
  Serial.begin(115200);
  initOled();
}

// loop to run repeatedly
void loop() {
  char key = keypad.getKey();
  if (key) {
    printOled("Keypad", String(key));
  }
  delay(100);
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