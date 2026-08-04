/* Light sensor */
#define A0_PIN 34

// setup to run only once
void setup() {
  Serial.begin(115200);
}

// loop to run repeatedly
void loop() {
  int light = readA0();
  Serial.println("Light: " + String(light));
  delay(1000);
}

/* Light sensor */
int readA0() {
  int aValue = analogRead(A0_PIN); // from 0 to 1024 or 4095
  int light = map(aValue, 0, 4095, 0, 100); // map aValue from 0-4095 to 0-100 (percentage)
  return light;
}