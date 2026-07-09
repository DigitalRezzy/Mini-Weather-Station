#include <LiquidCrystal.h>
#include <DHT.h>

#define DHTPIN 7
#define DHTTYPE DHT11
#define GREEN_LED 8
#define YELLOW1 9
#define YELLOW2 10
#define YELLOW3 13
#define RED_LED 6
#define BUZZER A0

DHT dht(DHTPIN, DHTTYPE);
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

//BUZZER STATE MEMORY
bool redAlertActive = false;


//LED RESET
void clearLEDs() {
  digitalWrite(GREEN_LED, LOW);
  digitalWrite(YELLOW1, LOW);
  digitalWrite(YELLOW2, LOW);
  digitalWrite(YELLOW3, LOW);
  digitalWrite(RED_LED, LOW);
}
//BUZZER FUNCTION
void beepFiveTimes() {
  for(int i = 0; i < 5; i++) {
    digitalWrite(BUZZER, HIGH);
    delay(120);
    digitalWrite(BUZZER, LOW);
    delay(120);
  }
}
//SETUP
void setup() {
  lcd.begin(16, 2);
  dht.begin();
  Serial.begin(9600);

  pinMode(GREEN_LED, OUTPUT);
  pinMode(YELLOW1, OUTPUT);
  pinMode(YELLOW2, OUTPUT);
  pinMode(YELLOW3, OUTPUT);
  pinMode(RED_LED, OUTPUT);
  pinMode(BUZZER, OUTPUT);
}
//LOOP
void loop() {

  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Sensor error");
    return;
  }

  //HEAT INDEX CALCULATION
  float heatIndex = dht.computeHeatIndex(temperature, humidity, false);

  //SERIAL OUTPUT
  Serial.print(temperature);
  Serial.print(",");
  Serial.print(humidity);
  Serial.print(",");
  Serial.println(heatIndex);

  //LCD DISPLAY
  lcd.clear();

  lcd.setCursor(0,0);
  lcd.print("T:");
  lcd.print(temperature,1);
  lcd.print("C F:");
  lcd.print(heatIndex,1);
  lcd.print("C");

  lcd.setCursor(0,1);
  lcd.print("H:");
  lcd.print(humidity,0);
  lcd.print("%");

  //LED LOGIC
  clearLEDs();

  if (humidity <= 30) {
    digitalWrite(GREEN_LED, HIGH);
    redAlertActive = false;
  }
  else if (humidity < 45) {
    digitalWrite(YELLOW1, HIGH);
    redAlertActive = false;
  }
  else if (humidity < 60) {
    digitalWrite(YELLOW2, HIGH);
    redAlertActive = false;
  }
  else if (humidity < 80) {
    digitalWrite(YELLOW3, HIGH);
    redAlertActive = false;
  }
  else {
    digitalWrite(RED_LED, HIGH);

    //BUZZ ONLY 5 TIMES
    if (!redAlertActive) {
      beepFiveTimes();
      redAlertActive = true;
    }
  }

  delay(2000);
}
