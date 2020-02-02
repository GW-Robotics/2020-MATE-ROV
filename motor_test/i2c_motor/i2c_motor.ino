#include <Wire.h>
#include <Servo.h> 
#define I2CAddress 9
#define ledPin 13
Servo motor1;
String s = "";


int minPulseRate = 1000;
int maxPulseRate = 2000;
int throttleChangeDelay = 100;

int readThrottle() {
  int throttle = motor1.read();
  
  Serial.print("Current throttle at 1");
  Serial.print(" is: ");
  Serial.println(throttle);
  
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
  throttle = normalizeThrottle(throttle);
  int currentThrottle = readThrottle();
  
  // Are we going up or down
  int step = 1;
  if( throttle < currentThrottle )
    step = -1;
  
  // Slowly move to the new throttle value 
  while( currentThrottle != throttle ) {
    motor1.write(currentThrottle + step);
    currentThrottle = readThrottle();
    delay(throttleChangeDelay);
  }
  
}

void receiveString(int bytes) {
  String text = "";
  s = "";
  while (Wire.available()) {
    char c = Wire.read(); // receive a byte as character
    s += c;
  }
  Serial.print("Printing: ");
  Serial.println(s);

  manageLed();
}

int StringToInt(){
  int len = s.length();
  char chars[len];
  s.toCharArray(chars,len);
  int ret = 0;
  for (int i = 0; i < len; i++){
    Serial.println(chars[i] + " " + i);
    ret += (int(s[i]));
    Serial.println(ret);
  }
  return ret;
}

void manageLed() {
  Serial.println(s);
  int t = atoi(s.c_str());
  Serial.println(t);
  int i = readThrottle();
  changeThrottle(t);
}

void setup() {
  motor1.attach(9, minPulseRate, maxPulseRate); 
  motor1.write(0);
  Serial.begin(9600);
  Serial.println("Slave here");
 
  // Start the I2C Bus as Slave on address 9
  Wire.begin(I2CAddress);

   // Attach a function to trigger when something is received.
  Wire.onReceive(receiveString);

  // LED
  pinMode(ledPin,OUTPUT);
  digitalWrite(ledPin,LOW);
}

void loop() {
  delay(10);
}
