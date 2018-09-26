#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// called this way, it uses the default address 0x40
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();


// calibrations
int SERVO_MIN[] = {450, 435,  90, 90};
int SERVO_MAX[] = { 90,  120, 450, 450};
int limit_low[] = {-45, -90, -90, -90};
int limit_high[]= { 45,  90,  90,  90};

// dimensions:
float pen_h   =  8.4;
float joint_0 = 12.8;
float joint_1 = 10.4;
float joint_2 = 10.7;

float float_map(float x, float in_min, float in_max, float out_min, float out_max)
{
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

// current angles of servos
float current_angles[] = {0, 0, 0, 0};

void go_to_angle(int pin, float angle) {
    if(angle < limit_low[pin] || angle > limit_high[pin]){
        digitalWrite(LED_BUILTIN, HIGH);
        delay(100);
        return;
    }
    current_angles[pin] = angle;
    digitalWrite(LED_BUILTIN, LOW);
    // int pulse = map(angle, -90, 90, SERVO_MIN[pin], SERVO_MAX[pin]);
    float pulse = float_map(angle, -90, 90, SERVO_MIN[pin], SERVO_MAX[pin]);

    pwm.setPWM(pin, 0, pulse);
}

void set_all_angles(float a0, float a1, float a2, float a3){
    go_to_angle(0, a0);
    go_to_angle(1, a1);
    go_to_angle(2, a2);
    go_to_angle(3, a3);
}

void move_to_smooth(float a0_target, float a1_target, float a2_target, float a3_target, float duration){
    // this function doesn't work with delays and instead sets the angles by
    // continuously linearly interpolating between the start and end angles
    if(duration < 100){
        duration = 100;
    }

    float original[] = {current_angles[0], current_angles[1], current_angles[2], current_angles[3]};
    int t0 = millis();
    int t = 0;
    do {
        t = millis();
        // d is a value between 0 and 1 that tells us how far along
        // the duration we are: 0 -> start, 1-> end
        float d = (float)(t - t0) / (float) duration;
        // linear interpolations
        float a0 = (1-d) * original[0] + d * a0_target;
        float a1 = (1-d) * original[1] + d * a1_target;
        float a2 = (1-d) * original[2] + d * a2_target;
        float a3 = (1-d) * original[3] + d * a3_target;
        // and set all the angles
        set_all_angles(a0, a1, a2, a3);
    } while((t - t0) < duration);
    set_all_angles(a0_target, a1_target, a2_target, a3_target);
}

void move_pen(float target_h, float a1, float a0){
    float a2 = acos((target_h-cos(-a1*PI/180)*joint_2) / joint_1)*180/PI - a1;
    float a3 = 90 - (a2+a1);
    Serial.println("--");
    Serial.println(a2);
    Serial.println(a3);

    //  go_to_angle(0, -a0);
    //  go_to_angle(1, -a1);
    //  go_to_angle(2, -a2);
    //  go_to_angle(3, -a3);
    move_to_smooth(a0, a1, a2, a3, 1000);
    delay(200);
}

void read_commands(){
    if(!Serial.available())
        return;

    String command = Serial.readStringUntil('\n');
    String substrings[16];
    for (size_t i = 0; i < 16; i++) {
        substrings[i] = "";
    }

    // split up the command into substrings delimited by spaces
    int pos = command.indexOf(' ', 0);
    int i = 0;
    substrings[i++] = command.substring(0, pos);
    while(pos < command.length()){
        // find next delimiter
        int next_space = command.indexOf(' ', pos+1); // pos+1 to skip over the previous space
        if(next_space == -1)
            next_space = command.indexOf('\n', pos);
        // and chop the command up some more
        substrings[i++] = command.substring(pos, next_space); // pos+1 to skip over the space
        Serial.println(command.substring(pos+1, next_space));
        pos = next_space;
    }

    // and execute the appropriate command
    if (substrings[0] == "reset") {
        Serial.println("arm reset");
        set_all_angles(0, 0, 0, 0);

    } else if (substrings[0] == "set") {
        int pin = substrings[1].toInt();
        int angle = substrings[2].toInt();
        Serial.println("servo set");
        go_to_angle(pin, angle);

    } else if (substrings[0] == "set_all") {
        int a0 = substrings[1].toInt();
        int a1 = substrings[2].toInt();
        int a2 = substrings[3].toInt();
        int a3 = substrings[4].toInt();
        Serial.println("all servos set");
        set_all_angles(a0, a1, a2, a3);

    } else if (substrings[0] == "move_to") {
        int a0 = substrings[1].toInt();
        int a1 = substrings[2].toInt();
        int a2 = substrings[3].toInt();
        int a3 = substrings[4].toInt();
        int duration = substrings[5].toInt();
        Serial.println("started movement...");
        move_to_smooth(a0, a1, a2, a3, duration);

    }
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

    // read and execute commands that are coming in
    read_commands();

    /* * * * * * * * *
    * This moves the arm and draws a sort of 'square'
    * * * * * * * * */

    // int a0f = 20;
    // int a0t = -20;
    // int a1f = 45;
    // int a1t = 20;
    //
    // int h = pen_h + 1;
    //
    // move_pen(h, a1f, a0f);
    // move_pen(h, a1f, a0t);
    // move_pen(h, a1t, a0t);
    // move_pen(h, a1t, a0f);
    //
    // if (Serial.available() > 0) {
    //     String s = Serial.readStringUntil('\n');
    //     // Serial.print("response: ");
    //     Serial.println(s);
    // }


    /* * * * * * * * *
    * This looks at the serial monitor and waits for a command to change the position of a servo
    * format: <servo number (0 -> 3)> <angle (-90 -> 90)>
    * * * * * * * * */

    // go_to_angle(3, 0);
    // go_to_angle(2, 0);
    // go_to_angle(1, 0);
    // go_to_angle(0, 0);
    // int angles[4];
    // while(1){
    //     if(Serial.available() > 0){
    //         int pin = Serial.parseInt();
    //         int angle = Serial.parseInt();
    //         angles[0] = current_angles[0]; angles[0] = current_angles[1]; angles[2] = current_angles[2]; angles[3] = current_angles[3];
    //         angles[pin] = angle;
    //         go_to_angle(pin, angle);
    //         // move_to_smooth(angles[0], angles[1], angles[2], angles[3]);
    //         Serial.print(pin);
    //         Serial.print(" set to ");
    //         Serial.println(angle);
    //     }
    //     delay(100);
    // }


    /* * * * * * * * *
    * This moves one servo back and forth, used for calibration only
    * * * * * * * * */

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
