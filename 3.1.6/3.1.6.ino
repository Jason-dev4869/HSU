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

/* RGB led */
#define RED_LED_PIN 14
#define GREEN_LED_PIN 12
#define BLUE_LED_PIN 13

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  initRGBLed();
}

String cmd = "";
void loop() {
  // put your main code here, to run repeatedly:
  char key = keypad.getKey();
  if ('0' <= key && key <= '9') {
    Serial.print(key); // for DEBUG
    cmd += key;
  } else if (key == '*' || key == '#') {
    Serial.println(key); // for DEBUG
    if (cmd == "1") onRGBLed(1, 0, 0);
    if (cmd == "2") onRGBLed(0, 1, 0);
    if (cmd == "3") onRGBLed(0, 0, 1);
    if (cmd == "4") onRGBLed(1, 1, 1);
    if (cmd == "5") onRGBLed(0, 0, 0);
    cmd = "";
  }
  delay(100);
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