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

// current angles of servos
float current_angles[] = {0, 0, 0, 0};

float target_angles[] = {0, 0, 90, -20}; //this is also the initial position when the robot is turned on
float start_angles[] = {0, 0, 0, 0};
float duration = 0;
int t0 = 0;
int t = 0;

void new_target(float a0, float a1, float a2, float a3, int d){
    start_angles[0] = current_angles[0];
    start_angles[1] = current_angles[1];
    start_angles[2] = current_angles[2];
    start_angles[3] = current_angles[3];

    target_angles[0] = a0;
    target_angles[1] = a1;
    target_angles[2] = a2;
    target_angles[3] = a3;

    duration = max(10, d);
    t0 = millis();
    t = t0;
}


void setup() {
    Serial.begin(19200);

    pinMode(LED_BUILTIN, OUTPUT);

    pwm.begin();
    pwm.setPWMFreq(50);
    delay(10);

    // set_all_angles(0, 0, 0, 0);
}

void loop() {

    // read and execute commands that are coming in
    read_commands();

    // move towards target position
    t = millis();
    // d is a value between 0 and 1 that tells us how far along
    // the duration we are: 0 -> start, 1-> end
    float d = (float)(t - t0) / (float) duration;
    d = min(1.0, d);
    // linear interpolations
    float a0 = (1-d) * start_angles[0] + d * target_angles[0];
    float a1 = (1-d) * start_angles[1] + d * target_angles[1];
    float a2 = (1-d) * start_angles[2] + d * target_angles[2];
    float a3 = (1-d) * start_angles[3] + d * target_angles[3];
    // and set all the angles
    set_all_angles(a0, a1, a2, a3);

    // if(d >= 1){
    //     Serial.println("done");
    // }
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
        // Serial.println(command.substring(pos+1, next_space));
        pos = next_space;
    }

    // and execute the appropriate command
    if (substrings[0] == "reset") {
        set_all_angles(0, 0, 0, 0);
        Serial.println("done");

    // } else if (substrings[0] == "set") {
    //     int pin = substrings[1].toInt();
    //     int angle = substrings[2].toInt();
    //     go_to_angle(pin, angle);
    //
    // } else if (substrings[0] == "set_all") {
    //     int a0 = substrings[1].toInt();
    //     int a1 = substrings[2].toInt();
    //     int a2 = substrings[3].toInt();
    //     int a3 = substrings[4].toInt();
    //     set_all_angles(a0, a1, a2, a3);

    } else if (substrings[0] == "move_to") {
        float a0 = substrings[1].toFloat();
        float a1 = substrings[2].toFloat();
        float a2 = substrings[3].toFloat();
        float a3 = substrings[4].toFloat();
        int duration = substrings[5].toInt();
        // move_to_smooth(a0, a1, a2, a3, duration);
        new_target(a0, a1, a2, a3, duration);
        Serial.println("done");

    } else if (substrings[0] == "is_done") {
        float d = (float)(t - t0) / (float) duration;
        d = min(1.0, d);
        Serial.println(d);
    }
}

float float_map(float x, float in_min, float in_max, float out_min, float out_max)
{
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

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
