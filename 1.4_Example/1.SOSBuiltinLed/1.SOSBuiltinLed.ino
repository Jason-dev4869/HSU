void setup() {
  // put your setup code here, to run once:
  initBILed();
}

void loop() {
  // put your main code here, to run repeatedly:
  sosBILed();
  delay(500);
}

void initBILed(){
  pinMode(BUILTIN_LED, OUTPUT);
}

void sosBILed(){
  for(int i = 1; i <=3; i++){
    digitalWrite(BUILTIN_LED, HIGH); delay(50);
    digitalWrite(BUILTIN_LED, LOW); delay(50);
  }
}