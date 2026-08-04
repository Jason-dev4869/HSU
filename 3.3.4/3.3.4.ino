/* Keypad */
#include <Keypad.h> // ref: https://github.com/Chris--A/Keypad
#define ROWS 4 // four rows
#define COLS 4 // four columns
byte rowPins[ROWS] = {5, 18, 19, 23}; // connect to the row pinouts of the keypad
byte colPins[COLS] = {0, 4, 16, 17}; // connect to the column pinouts of the keypad

char keys[ROWS][COLS] = {
  {'1','2','3','A'},
  {'4','5','6','B'},
  {'7','8','9','C'},
  {'*','0','#','D'}
};

Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

/* Servo */
#include <ESP32Servo.h> // ref: https://madhephaestus.github.io/ESP32Servo/annotated.html
#define SERVO_PIN 15
Servo servo;

void setup() {
  Serial.begin(115200);
  initServo();
}

// loop to run repeatedly
String pwd = "159"; int pos = 0;
void loop() {
  char key = keypad.getKey(); // '*'|'#':down, 'pwd':up
  if (key == '*' || key == '#') {
    Serial.println(key); // for DEBUG
    downServo();
    pos = 0;
  } else if (key == pwd[pos]) {
    Serial.print(key); // for DEBUG
    pos++;
    if (pos == pwd.length()) { // correct password
      upServo();
      pos = 0;
    }
  }
  delay(100);
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