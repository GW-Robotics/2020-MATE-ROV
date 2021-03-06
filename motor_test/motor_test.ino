#include <Servo.h> 

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

int minPulseRate = 1000;
int maxPulseRate = 2000;
int throttleChangeDelay = 100;

void setup() {
  
  Serial.begin(9600);
  Serial.setTimeout(500);
  
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
  
}

void loop() {

  // Wait for some input
  if (Serial.available() > 0) {
    
    // Read the new throttle value
    int throttle = normalizeThrottle( Serial.parseInt() );
    
    // Print it out
    Serial.print("Setting throttle to: ");
    Serial.println(throttle);
    
    // Change throttle to the new value
    changeThrottle(throttle);
    
  }

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
    esc5.write(currentThrottle + step);
    esc6.write(currentThrottle + step);
    esc7.write(currentThrottle + step);
    currentThrottle = readThrottle();
    delay(throttleChangeDelay);
  }
  
}

int readThrottle() {
  int throttle = esc0.read();
  
  Serial.print("Current throttle is: ");
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
