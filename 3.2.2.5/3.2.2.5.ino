/* Relay */
#define RELAY_PIN 13

/* Water sensor */
#define D0_PIN 15

// setup to run only once
void setup() {
  Serial.begin(115200);
  initRelay();
}

// loop to run repeatedly
void loop() {
  bool water = readD0();
  if (water) {
    Serial.println("Water: +"); // for DEBUG
    offRelay();
  } else {
    Serial.println("Water: -"); // for DEBUG
    onRelay();
  }
  delay(100);
}

/* Water sensor */
void initSensor() {
  pinMode(D0_PIN, INPUT);
}

bool readD0() {
  int dValue = digitalRead(D0_PIN); // 0: water/rain detected; 1: no water/dry
  if (dValue) return false;         // Nếu là 1 (mức HIGH) -> Không có nước (false)
  else return true;                 // Nếu là 0 (mức LOW)  -> Có nước (true)
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