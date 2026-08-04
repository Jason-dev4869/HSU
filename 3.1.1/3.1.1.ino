/* RGB led */
#define RED_LED_PIN 14
#define GREEN_LED_PIN 12
#define BLUE_LED_PIN 13

// setup to run only once
void setup() {
  Serial.begin(115200);
  initRGBLed();
}

// loop to run repeatedly
void loop() {
  // red blinks 10 times
  for (int i = 1; i <= 10; i++) {
    onRGBLed(1, 0, 0); delay(500);
    onRGBLed(0, 0, 0); delay(500);
  }
  // green blinks 7 times
  for (int i = 1; i <= 7; i++) {
    onRGBLed(0, 1, 0); delay(500);
    onRGBLed(0, 0, 0); delay(500);
  }
  // blue blinks 3 times
  for (int i = 1; i <= 3; i++) {
    onRGBLed(0, 0, 1); delay(500);
    onRGBLed(0, 0, 0); delay(500);
  }
}

/* RGB led */
void initRGBLed() {
  pinMode(RED_LED_PIN, OUTPUT);
  pinMode(GREEN_LED_PIN, OUTPUT);
  pinMode(BLUE_LED_PIN, OUTPUT);
}

void onRGBLed(int red, int green, int blue) {
  if (red == 1) digitalWrite(RED_LED_PIN, HIGH);
  else digitalWrite(RED_LED_PIN, LOW);
  if (green == 1) digitalWrite(GREEN_LED_PIN, HIGH);
  else digitalWrite(GREEN_LED_PIN, LOW);
  if (blue == 1) digitalWrite(BLUE_LED_PIN, HIGH);
  else digitalWrite(BLUE_LED_PIN, LOW);
}