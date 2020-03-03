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
Servo escs[] = {esc0,esc1,esc2,esc3,esc4,esc5,esc6,esc7};
int throttles[8];

int minPulseRate = 1000;
int maxPulseRate = 2000;
int throttleChangeDelay = 50;

int readThrottle(int i) {
  int throttle = escs[i].read();
  return throttle;
}

int normalizeThrottle(int value) {
  if( value < 0 )
    return 0;
  if( value > 180 )
    return 180;
  return value;
}
boolean checkThrottles(int throttles[]){
  for(int i=0;i<8;i++){
    if(throttles[i]!=readThrottle(i)){
      return true;
    }
  }
  return false;
}
void changeThrottle(int throttles[]) {
  // Read the current throttle value
  do{
    for(int i=0;i<8;i++){
      int throttle = throttles[i];
      int currentThrottle = readThrottle(i);
      
      // Are we going up or down?
      int step = 1;
      if( throttle < currentThrottle )
        step = -1;
      
      // Slowly move to the new throttle value 
      if( currentThrottle != throttle ) {
        escs[i].write(currentThrottle + step);
        currentThrottle = readThrottle(i);
      }
  }
  }while(checkThrottles(throttles));
  

}
void requestData(int bytes){
  Serial.println("Data Write");
  for(int i=0;i<5;i++){
  Wire.write(1);
  }
}
void receiveData(int bytes) {
    int i = 0;
    int motorVals[8];
    while(Wire.available()) {
      int c = (int) Wire.read();
      if(i!=0){
        motorVals[i-1] = max(0,min(c,180)); 
        //Serial.println(c);
      }
      i++;
    }
    for(int j=0;j<8;j++){
      escs[j].write(motorVals[j]);
    }
}

void setup() {

  
  // Attach the the servo to the correct pin and set the pulse range
  esc0.attach(ESC_0, minPulseRate, maxPulseRate);
  esc1.attach(ESC_1, minPulseRate, maxPulseRate);
  esc2.attach(ESC_2, minPulseRate, maxPulseRate);
  esc3.attach(ESC_3, minPulseRate, maxPulseRate);
  esc4.attach(ESC_4, minPulseRate, maxPulseRate);
  esc5.attach(ESC_5, minPulseRate, maxPulseRate);
  esc6.attach(ESC_6, minPulseRate, maxPulseRate);
  esc7.attach(ESC_7, minPulseRate, maxPulseRate);
  
  // Write a minimum value (most ESCs require this correct startup)
  esc0.write(0);
  esc1.write(0);
  esc2.write(0);
  esc3.write(0);
  esc4.write(0);
  esc5.write(0);
  esc6.write(0);
  esc7.write(0);
  // Start the I2C Bus as Slave on address 9
  Wire.begin(I2CAddress);

  // Attach a function to trigger when something is received.
  Wire.onReceive(receiveData);
  //Wire.onRequest(requestData);
}

void loop() {
  /*
  int throttle;
  int currentThrottle;
  for(int i=0;i<8;i++){
    throttle = throttles[i];
    currentThrottle = readThrottle(i);
    // Are we going up or down?
    int step = 1;
    if( throttle < currentThrottle )
      step = -1;
    
    // Slowly move to the new throttle value 
    if( currentThrottle != throttle ) {
      escs[i].write(currentThrottle + step);
    }
  }*/
  delay(throttleChangeDelay);
}
