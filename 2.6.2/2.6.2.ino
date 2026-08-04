/* MFRC522 */
#define RFID_SDA_PIN 5
#define RFID_RST_PIN 4

#include <MFRC522.h> // ref: https://github.com/miguelbalboa/rfid
MFRC522 mfrc522(RFID_SDA_PIN, RFID_RST_PIN);

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
  //printOled("Ready", "Scan card"); 
  initMFRC522();
}

// loop to run repeatedly
void loop() {
  String uid = getCardUID();
  if (uid != "") {
    Serial.println("UID: " + uid);
  }

  if (uid == "6925324505") {
    printOled("MFRC522", "blue card");
  } else if (uid == "1318714705") {
    printOled("MFRC522","white card");
  }
  delay(500);
}

/* MFRC522 */
void initMFRC522() {
  SPI.begin();
  mfrc522.PCD_Init();
}

String getCardUID() {
  String uid = "";
  if (mfrc522.PICC_IsNewCardPresent()) { // look for new cards
    if (mfrc522.PICC_ReadCardSerial()) { // select one of the cards
      uid = getCardUIDinDEC(mfrc522.uid.uidByte, mfrc522.uid.size);
    }
  }
  return uid;
}

/*String getCardUIDinHEX(byte* buffer, byte bufferSize) {
  String result = "";
  for (byte i = 0; i < bufferSize; i++) {
    result += (buffer[i] < 0x10) ? "0" : "";
    result += String(buffer[i], HEX);
    if (i < bufferSize - 1) result += "-";
  }
  result.toUpperCase();
  return result;
}*/

String getCardUIDinDEC(byte* buffer, byte bufferSize) {
  String result = "";
  for (byte i = 0; i < bufferSize; i++) {
    result += (buffer[i] < 0x10) ? "0" : "";
    result += String(buffer[i]);
  }
  return result;
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