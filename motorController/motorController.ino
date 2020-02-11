#include <Servo.h> 
#include <Wire.h>
#define I2CAddress 9
Servo motor0;
Servo motor1;
Servo motor2;
Servo motor3;
Servo motor4;
Servo motor5;
Servo motor6;
Servo motor7;
Servo motors[8] = {motor0,motor1,motor2,motor3,motor4,motor5,motor6,motor7};

int minPulseRate = 1000;
int maxPulseRate = 2000;
int throttleChangeDelay = 100;

int readThrottle(int i) {
  int throttle = motor2.read();
  
  Serial.print("Current throttle at ");
  Serial.print(i);
  Serial.print(" is: ");
  Serial.println(throttle);
  
  return throttle;
}

// Ensure the throttle value is between 0 - 180
int normalizeThrottle(int value) {
  if( value < 0 )
    return 0;
  if( value > 180 )
    return 180;
  return value;
}
void setup() {
  motor0.attach(6, minPulseRate, maxPulseRate); 
  motor0.write(0);
  motor1.attach(7, minPulseRate, maxPulseRate); 
  motor1.write(0);
  motor2.attach(8, minPulseRate, maxPulseRate); 
  motor2.write(0);
  motor3.attach(9, minPulseRate, maxPulseRate); 
  motor3.write(0);
  motor4.attach(10, minPulseRate, maxPulseRate); 
  motor4.write(0);
  motor5.attach(11, minPulseRate, maxPulseRate); 
  motor5.write(0);
  motor6.attach(12, minPulseRate, maxPulseRate); 
  motor6.write(0);
  motor7.attach(13, minPulseRate, maxPulseRate); 
  motor7.write(0);
  Serial.begin(9600);
  Serial.setTimeout(500);
  Serial.println("Slave here");
  Wire.begin(I2CAddress);
  Wire.onReceive(receiveString);
}
void receiveString(int bytes) {
  int motorVals[9];
  int i=0;
  for(i=0;i<9;i++){
    motorVals[i]=-1;
  }
  i=0;
  Serial.print("[");
  while (Wire.available()) {
    int c =(int) Wire.read(); // receive a byte as character
    Serial.print(c,DEC);
    Serial.print(", ");
    motorVals[i]= c;
    i++;
  }
  Serial.println("]");
  for(i=1;i<9;i++){
    motors[i].write(motorVals[i]);
  }
}
//increments throttle of motor at index to designated throttle
void changeThrottle(int index, int throttle) {
  throttle = normalizeThrottle(throttle);
  int currentThrottle = readThrottle(index);
  
  // Are we going up or down
  int step = 1;
  if( throttle < currentThrottle )
    step = -1;
  
  // Slowly move to the new throttle value 
  while( currentThrottle != throttle ) {
    motors[index].write(currentThrottle + step);
    currentThrottle = readThrottle(index);
    delay(throttleChangeDelay);
  }
  
}
void loop() {
    /*
    //Wire.requestFrom(0x8,8);
    int i=0;
    //Serial.println("[");
    while(Wire.available()){
      byte b = Wire.read();
      Serial.println((int) b);
      changeThrottle(i,(int) b);
    }
    //Serial.println("]");

    */
    delay(100);  
  }
