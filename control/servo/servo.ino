/*************************************************** 
  This is an example for our Adafruit 16-channel PWM & Servo driver
  Servo test - this will drive 8 servos, one after the other on the
  first 8 pins of the PCA9685

  Pick one up today in the adafruit shop!
  ------> http://www.adafruit.com/products/815
  
  These drivers use I2C to communicate, 2 pins are required to  
  interface.

  Adafruit invests time and resources providing this open source code, 
  please support Adafruit and open-source hardware by purchasing 
  products from Adafruit!

  Written by Limor Fried/Ladyada for Adafruit Industries.  
  BSD license, all text above must be included in any redistribution
 ****************************************************/

#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// called this way, it uses the default address 0x40
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();


// calibrations
int SERVO_MIN[] = {450, 435,  90,  90};
int SERVO_MAX[] = { 90,  75, 475, 450};
int limit_low[] = {-80, -80, -80, -45};
int limit_high[]= { 80,  80,  80,  45};

// dimensions:
 float pen_h   =  8.4;
 float joint_0 = 12.8;
 float joint_1 = 10.4;
 float joint_2 = 10.7;

void setup() {
  Serial.begin(9600);
  
  pinMode(LED_BUILTIN, OUTPUT);
  
  pwm.begin();
  pwm.setPWMFreq(50);  // Analog servos run at ~60 Hz updates
  delay(10);
}

void go_to_angle(int pin, int angle) {
  if(angle < limit_low[pin] || angle > limit_high[pin]){
    digitalWrite(LED_BUILTIN, HIGH);
    delay(100);
    return;
  }
  digitalWrite(LED_BUILTIN, LOW);
  int pulse = map(angle, -90, 90, SERVO_MIN[pin], SERVO_MAX[pin]);
  pwm.setPWM(pin, 0, pulse);
}

void move_pen(float target_h, int a2, int a3){
  float a1 = -acos((target_h-cos(a2*PI/180)*joint_2) / joint_1)*180/PI - a2;
  float a0 = -90 - (a1+a2);
  Serial.println("--");
  Serial.println(a1);
  Serial.println(a0);
  
  go_to_angle(3, a3);
  go_to_angle(2, a2);
  go_to_angle(1, a1);
  go_to_angle(0, a0);
  delay(200);
}

void loop() {
  int a3f = -10;
  int a3t = 10;
  int a2f = -45;
  int a2t = -22;

  int h = pen_h + 7;


//  for(int a3 = a3f; a3 < a3t; a3++){
//    move_pen(h, a2f, a3);
//  }
//  for(int a2 = a2f; a2 < a2t; a2++){
//    move_pen(h, a2, a3t); 
//  }
//  delay(2000);
//  for(int a3 = a3t; a3 > a3f; a3--){
//    move_pen(h, a2t, a3);
//  }
//  for(int a2 = a2t; a2 > a2f; a2--){
//    move_pen(h, a2, a3f); 
//  }
//  delay(2000);
  

  
  
  go_to_angle(3, 0);
  go_to_angle(2, 0);
  go_to_angle(1, 0);
  go_to_angle(0, 0);
  delay(100);

  int servonum = 1;
  int minangle = 0;
  int maxangle = 180;
  uint16_t pulse;
  for (uint16_t angle = minangle; angle < maxangle; angle += 1) {
    pulse = map(angle, 0, 180, SERVO_MIN[servonum], SERVO_MAX[servonum]);
    pwm.setPWM(servonum, 0, pulse);
    if(angle == 90){
      delay(1000);
    }
    delay(20);
  }

  delay(1000);
  for (uint16_t angle = maxangle; angle > minangle; angle -= 1) {
    pulse = map(angle, 0, 180, SERVO_MIN[servonum], SERVO_MAX[servonum]);
    pwm.setPWM(servonum, 0, pulse);
    if(angle == 90){
      delay(1000);
    }
    delay(20);
  }
  delay(1000);
}
