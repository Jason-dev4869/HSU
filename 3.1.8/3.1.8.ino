/* Sound sensor */
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
  readD0();
}

/* Sound sensor */
void initSensor() {
  pinMode(D0_PIN, INPUT);
}
int clap = 0;
long detection_range_start = 0, detection_range = 0;
void readD0() {
  int dValue = digitalRead(D0_PIN); // 0:sound; 1:no-sound
  if (dValue == 0) {
    if (clap == 0) {
      detection_range_start = detection_range = millis();
      clap++;
    } else if (clap > 0 && millis() - detection_range >= 100) {
      detection_range = millis();
      clap++;
    }
  }
  if (millis() - detection_range_start >= 300) {
    if (clap == 1) {
      Serial.println("CLAP 1 times"); // for DEBUG
      digitalWrite(LED_PIN, HIGH);
    } else if (clap == 2) {
      Serial.println("CLAP 2 times"); // for DEBUG
      digitalWrite(LED_PIN, LOW);
    }
    clap = 0;
  }
}

/* RGB led */
void initRGBLed() {
  pinMode(LED_PIN, OUTPUT);
}