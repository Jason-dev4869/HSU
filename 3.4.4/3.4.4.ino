/* Radar RCWL0516 */
#define DO_PIN 15

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
  bool motion = readDO();
  if (motion) {
    Serial.println("Motion: +"); // for DEBUG
    sosBuzzer();
  } else {
    Serial.println("Motion: -"); // for DEBUG
    offBuzzer();
  }
  delay(500);
}

/* Radar RCWL0516 */
void initSensor() {
  pinMode(DO_PIN, INPUT);
}

bool readDO() {
  int dValue = digitalRead(DO_PIN); // 0:no-motion; 1:motion
  if (dValue) return true;
  else return false;
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