/* Active buzzer */
#define BUZZER_PIN 13

// setup to run only once
void setup() {
  initBuzzer();
}
// loop to run repeatedly
void loop() {
  sosBuzzer();
  delay(500);
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