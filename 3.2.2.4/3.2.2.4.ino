/* Relay */
#define RELAY_PIN 13

/* Moisture sensor */
#define D0_PIN 15

// setup to run only once
void setup() {
  Serial.begin(115200);
  initSensor();
  initRelay();
}

// loop to run repeatedly
void loop() {
  bool moisture = readD0();
  if (moisture) {
    Serial.println("Moisture: +"); // for DEBUG
    offRelay();
  } else {
    Serial.println("Moisture: -"); // for DEBUG
    onRelay();
  }
  delay(100);
}

/* Moisture sensor */
void initSensor() {
  pinMode(D0_PIN, INPUT);
}

bool readD0() {
  int dValue = digitalRead(D0_PIN); // 0:moisture; 1:no-moisture
  if (dValue) return false;
  else return true;
}

/* Relay */
void initRelay() {
  pinMode(RELAY_PIN, OUTPUT);
}
void onRelay() {
  digitalWrite(RELAY_PIN, HIGH);
}
void offRelay() {
  digitalWrite(RELAY_PIN, LOW);
}