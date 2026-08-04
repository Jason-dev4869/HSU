/* MFRC522 */
#define RFID_SDA_PIN 5
#define RFID_RST_PIN 4
#include <MFRC522.h> // ref: https://github.com/miguelbalboa/rfid
MFRC522 mfrc522(RFID_SDA_PIN, RFID_RST_PIN);

/* Servo */
#include <ESP32Servo.h> // ref: https://madhephaestus.github.io/ESP32Servo/annotated.html
#define SERVO_PIN 15
Servo servo;

// setup to run only once
void setup() {
  Serial.begin(115200);
  initMFRC522();
  initServo();
}
// loop to run repeatedly
int oldValue = 0;
void loop() {
  String uid = getCardUID();
  Serial.println(uid); // for DEBUG
  if (uid == "6925324505" && oldValue == 0) {
    Serial.println("blue card"); // for DEBUG
    upServo(); oldValue = 1;
  } else if (uid == "1318714705" && oldValue == 1) {
    Serial.println("white card"); // for DEBUG
    downServo(); oldValue = 0;
  }
  delay(100);
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

String getCardUIDinDEC(byte* buffer, byte bufferSize) {
  String result = "";
  for (byte i = 0; i < bufferSize; i++) {
    result += (buffer[i] < 0x10) ? "0" : "";
    result += String(buffer[i]);
  }
  return result;
}

/* Servo */
void initServo() {
  servo.attach(SERVO_PIN);
  servo.write(0);
}
void upServo() {
  for (int pos = 0; pos <= 180; pos += 1) { // from 0-180 degrees in steps of 1 degree
    servo.write(pos); delay(20);
  }
}
void downServo() {
  for (int pos = 180; pos >= 0; pos -= 1) { // from 180-0 degrees in steps of -1 degree
    servo.write(pos); delay(20);
  }
}