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
int SERVO_MIN[] = {450, 435,  90, 90};
int SERVO_MAX[] = { 90,  120, 450, 450};
int limit_low[] = {-80, -80, -80, -45};
int limit_high[]= { 80,  80,  80,  45};

// dimensions:
 float pen_h   =  8.4;
 float joint_0 = 12.8;
 float joint_1 = 10.4;
 float joint_2 = 10.7;


// current angles of servos
int current_angles[] = {0, 0, 0, 0};

void go_to_angle(int pin, int angle) {
  if(angle < limit_low[pin] || angle > limit_high[pin]){
    digitalWrite(LED_BUILTIN, HIGH);
    delay(100);
    return;
  }
  current_angles[pin] = angle;
  digitalWrite(LED_BUILTIN, LOW);
  int pulse = map(angle, -90, 90, SERVO_MIN[pin], SERVO_MAX[pin]);
  pwm.setPWM(pin, 0, pulse);
}

void set_all_angles(int a0, int a1, int a2, int a3){
  go_to_angle(0, a0);
  go_to_angle(1, a1);
  go_to_angle(2, a2);
  go_to_angle(3, a3);
}

void move_to_slow(int a0_to, int a1_to, int a2_to, int a3_to){
  float increments[] = {
    a0_to - current_angles[0],
    a1_to - current_angles[1],
    a2_to - current_angles[2],
    a3_to - current_angles[3]
  };

  float max_inc = max(abs(increments[0]), max(abs(increments[1]), max(abs(increments[2]), abs(increments[3]))));
  int steps = max_inc;

  float original[] = {current_angles[0], current_angles[1], current_angles[2], current_angles[3]};

  int i = 0;
  while(i < steps){
    set_all_angles(
      original[0] + increments[0] / steps * i, 
      original[1] + increments[1] / steps * i, 
      original[2] + increments[2] / steps * i, 
      original[3] + increments[3] / steps * i
    );
    delay(100);
    i++;
  }

  set_all_angles(a0_to, a1_to, a2_to, a3_to);
  delay(100);
}

void move_pen(float target_h, int a1, int a0){
  float a2 = acos((target_h-cos(-a1*PI/180)*joint_2) / joint_1)*180/PI - a1;
  float a3 = 90 - (a2+a1);
  Serial.println("--");
  Serial.println(a2);
  Serial.println(a3);
  
//  go_to_angle(0, -a0);
//  go_to_angle(1, -a1);
//  go_to_angle(2, -a2);
//  go_to_angle(3, -a3);
  move_to_slow(a0, a1, a2, a3);
  delay(200);
}


void setup() {
  Serial.begin(9600);
  
  pinMode(LED_BUILTIN, OUTPUT);
  
  pwm.begin();
  pwm.setPWMFreq(50);
  delay(10);

  
  set_all_angles(0,0,0,0);
}

void loop() {
  int a0f = 20;
  int a0t = -20;
  int a1f = 45;
  int a1t = 20;

  int h = pen_h + 1;

  move_pen(h, a1f, a0f); 
  move_pen(h, a1f, a0t);
  move_pen(h, a1t, a0t);
  move_pen(h, a1t, a0f);


//  move_pen(h, -45, 0);
  


//  set_all_angles(0,0,0,0);
//  move_to_slow(0, 45, 45, -45);
//  delay(2000);
//  move_to_slow(0, 0, 0, 0);
  
  
//  go_to_angle(3, 0);
//  go_to_angle(2, 0);
//  go_to_angle(1, 0);
//  go_to_angle(0, 0);
//  int angles[4];
//  while(1){
//    if(Serial.available() > 0){
//      int pin = Serial.parseInt();
//      int angle = Serial.parseInt();
//      angles[0] = current_angles[0]; angles[0] = current_angles[1]; angles[2] = current_angles[2]; angles[3] = current_angles[3];
//      angles[pin] = angle;
////      go_to_angle(pin, angle);
//      move_to_slow(angles[0], angles[1], angles[2], angles[3]);
//      Serial.print(pin);
//      Serial.print(" set to ");
//      Serial.println(angle);
//    }
//    delay(100);
//  }

//  int servonum = 1;
//  int minangle = -45;
//  int maxangle = 45;
//  uint16_t pulse;
//  for (uint16_t angle = minangle; angle < maxangle; angle += 1) {
//    pulse = map(angle, -90, 90, SERVO_MIN[servonum], SERVO_MAX[servonum]);
//    pwm.setPWM(servonum, 0, pulse);
//    if(angle == 0){
////      delay(1000);
//    }
//    delay(20);
//  }
//
//  delay(1000);
//  for (uint16_t angle = maxangle; angle > minangle; angle -= 1) {
//    pulse = map(angle, -90, 90, SERVO_MIN[servonum], SERVO_MAX[servonum]);
//    pwm.setPWM(servonum, 0, pulse);
//    if(angle == 0){
////      delay(1000);
//    }
//    delay(20);
//  }
//  delay(1000);
}
