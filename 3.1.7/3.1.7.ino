/* Light sensor */
#define D0_PIN 15

/* RGB led */
#define LED_PIN 13

// setup to run only once
void setup() {
  Serial.begin(115200);
  initSensor();
  initRGBLed();
}

// loop to run repeatedly
void loop() {
  bool light = readD0();
  if (light) {
    Serial.println("Light: +"); // for DEBUG
    digitalWrite(LED_PIN, LOW);
  } else {
    Serial.println("Light: -"); // for DEBUG
    digitalWrite(LED_PIN, HIGH);
  }
  delay(100);
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

/* RGB led */
void initRGBLed() {
  pinMode(LED_PIN, OUTPUT);
}