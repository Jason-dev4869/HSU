/* LCD */
#include <LiquidCrystal_I2C.h>
#define LCD_COLS 16
#define LCD_ROWS 2
LiquidCrystal_I2C lcd(0x27, LCD_COLS, LCD_ROWS);

void setup() {
  // put your setup code here, to run once:
  initLcd();
}

void loop() {
  // put your main code here, to run repeatedly:
  String line1 = "Chau + Khoi";
  String line2 = "CK_IoT";
  printLcd(line1, ""); delay(2000);
  printLcd(line1, line2); delay(2000);
}

void initLcd(){
  lcd.init();
  lcd.backlight();
}

void printLcd(String line1, String line2){
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(line1);
  lcd.setCursor(0, 1);
  lcd.print(line2);
}