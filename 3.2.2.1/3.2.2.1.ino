/* Relay */
#define RELAY_PIN 13

// setup to run only once
void setup() {
  initRelay();
}
// loop to run repeatedly
void loop() {
  onRelay(); delay(3000);
  offRelay(); delay(3000);
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