/* MQ2: requires a warm-up period before it can be used effectively, during this time, the
   sensor may initially provide high readings */
#define D0_PIN 15

/* Active buzzer */
#define BUZZER_PIN 13

// setup to run only once
void setup() {
  Serial.begin(115200);
  initSensor();
  initBuzzer();
}
// loop to run repeatedly
void loop() {
  bool smoke = readMQ2();
  if (smoke) {
    Serial.println("Smoke: +"); // for DEBUG
    sosBuzzer();
  } else {
    Serial.println("Smoke: -"); // for DEBUG
    offBuzzer();
  }
  delay(500);
}

/* MQ2 */
void initSensor() {
  pinMode(D0_PIN, INPUT);
}
bool readMQ2() {
  int dValue = digitalRead(D0_PIN); // 0:smoke; 1:no-smoke
  if (dValue) return false;
  else return true;
}

/* Active buzzer */
void initBuzzer() {
  pinMode(BUZZER_PIN, OUTPUT);
  offBuzzer();
}

void sosBuzzer() {
  for (int i = 1; i <= 3; i++) {
    digitalWrite(BUZZER_PIN, LOW); delay(50); // turn on
    digitalWrite(BUZZER_PIN, HIGH); delay(100); // turn off
  }
  delay(100);
  for (int i = 1; i <= 3; i++) {
    digitalWrite(BUZZER_PIN, LOW); delay(200);
    digitalWrite(BUZZER_PIN, HIGH); delay(100);
  }
  delay(100);
  for (int i = 1; i <= 3; i++) {
    digitalWrite(BUZZER_PIN, LOW); delay(50);
    digitalWrite(BUZZER_PIN, HIGH); delay(100);
  }
}

void offBuzzer() {
  digitalWrite(BUZZER_PIN, HIGH);
}