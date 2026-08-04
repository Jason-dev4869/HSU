/* RGB led */
#define LED_PIN 13

/* Reed switch */
#define DO_PIN 15

// setup to run only once
void setup() {
  initRGBLed();
  initSensor();
}
// loop to run repeatedly
void loop() {
  bool state = readDO();
  if (state) {
    Serial.println("Gate: Open"); // for DEBUG
    digitalWrite(LED_PIN, LOW);
  } else {
    Serial.println("Gate: Close"); // for DEBUG
    digitalWrite(LED_PIN, HIGH);
  }
  delay(100);
}

/* RGB led */
void initRGBLed() {
  pinMode(LED_PIN, OUTPUT);
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