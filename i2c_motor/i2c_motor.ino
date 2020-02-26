#include <Wire.h>
#include <Servo.h> 
#include <LiquidCrystal.h>
#define I2CAddress 9

#define ESC_0 6
#define ESC_1 7
#define ESC_2 8
#define ESC_3 9
#define ESC_4 10
#define ESC_5 11
#define ESC_6 12
#define ESC_7 13

Servo esc0;
Servo esc1;
Servo esc2;
Servo esc3;
Servo esc4;
Servo esc5;
Servo esc6;
Servo esc7;

LiquidCrystal lcd(12,11,5,4,3,2);

int minPulseRate = 1000;
int maxPulseRate = 2000;
int throttleChangeDelay = 100;

int readThrottle() {
  int throttle = esc0.read();
  
  //Serial.print("Current throttle is: ");
  //Serial.println(throttle);
  
  return throttle;
}

int normalizeThrottle(int value) {
  if( value < 0 )
    return 0;
  if( value > 180 )
    return 180;
  return value;
}

void changeThrottle(int throttle) {
  // Read the current throttle value
  int currentThrottle = readThrottle();
  
  // Are we going up or down?
  int step = 1;
  if( throttle < currentThrottle )
    step = -1;
  
  // Slowly move to the new throttle value 
  while( currentThrottle != throttle ) {
    esc0.write(currentThrottle + step);
    esc1.write(currentThrottle + step);
    esc2.write(currentThrottle + step);
    esc3.write(currentThrottle + step);
    esc4.write(currentThrottle + step);
    //esc5.write(currentThrottle + step);
    //esc6.write(currentThrottle + step);
    esc7.write(currentThrottle + step);
    currentThrottle = readThrottle();
    delay(throttleChangeDelay);
  }
  
}
int motorVals[9];
bool readData = 1;
String s = "";
bool writeS = 0;
void requestData(int bytes){
  Serial.println("Data Write");
  for(int i=0;i<5;i++){
  Wire.write(1);
  }
}
void receiveData(int bytes) {
    int i = 0;
    s = "[";
    for(i=0; i<9; i++){
      motorVals[i]=-1;
    }
    i=0;
    while(Wire.available()) {
      int c = (int) Wire.read();
      s+=c;
      s+=", ";
      motorVals[i] = c;
      i++;
    }
    s+="]";
    writeS = 1;
  
    changeThrottle(motorVals[1]);
    //Wire.flush();
}

void setup() {
  lcd.begin(16,2);
  
  // Attach the the servo to the correct pin and set the pulse range
  esc0.attach(ESC_0, minPulseRate, maxPulseRate);
  esc1.attach(ESC_1, minPulseRate, maxPulseRate);
  esc2.attach(ESC_2, minPulseRate, maxPulseRate);
  esc3.attach(ESC_3, minPulseRate, maxPulseRate);
  esc4.attach(ESC_4, minPulseRate, maxPulseRate);
  //esc5.attach(ESC_5, minPulseRate, maxPulseRate);
  //esc6.attach(ESC_6, minPulseRate, maxPulseRate);
  esc7.attach(ESC_7, minPulseRate, maxPulseRate);
  
  // Write a minimum value (most ESCs require this correct startup)
  esc0.write(0);
  esc1.write(0);
  esc2.write(0);
  esc3.write(0);
  esc4.write(0);
  //esc5.write(0);
  //esc6.write(0);
  esc7.write(0);
  Serial.begin(9600);
  lcd.setCursor(0,0);
  lcd.print("Slave here");
 
  // Start the I2C Bus as Slave on address 9
  Wire.begin(I2CAddress);

  // Attach a function to trigger when something is received.
  Wire.onReceive(receiveData);
  //Wire.onRequest(requestData);
}

void loop() {
  if(writeS){
    lcd.setCursor(0,1);
    lcd.print(s);
    writeS = 0;
  }
  
}
