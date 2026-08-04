/* Light sensor */
#define D0_PIN 15

// setup to run only once
void setup() {
  Serial.begin(115200);
  initSensor();
}

// loop to run repeatedly
void loop() {
  bool light = readD0();
  if (light) {
    Serial.println("Light: +");
  } else {
    Serial.println("Light: -");
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

