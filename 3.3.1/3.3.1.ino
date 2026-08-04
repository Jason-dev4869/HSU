/* Servo */
#include <ESP32Servo.h> // ref: https://madhephaestus.github.io/ESP32Servo/annotated.html
#define SERVO_PIN 15
Servo servo;

// setup to run only once
void setup() {
  Serial.begin(115200);
  initServo();
}

// loop to run repeatedly
void loop() {
  upServo();
  downServo();
}

/* Servo */
void initServo() {
  servo.attach(SERVO_PIN);
  servo.write(0);
}
void upServo() {
  for (int pos = 0; pos <= 180; pos += 1) { // from 0-180 degrees in steps of 1 degree
    servo.write(pos); delay(20);
  }
}
void downServo() {
  for (int pos = 180; pos >= 0; pos -= 1) { // from 180-0 degrees in steps of -1 degree
    servo.write(pos); delay(20);
  }
}