//this module handles interfacing to the motors

#include "arduino.h"
#include "melty_config.h"
#include "motor_driver.h"
#include "driver/ledc.h"
#include <ESP32Servo.h>

//motor_X_on functions are used for the powered phase of each rotation
//motor_X_coast functions are used for the unpowered phase of each rotation
//motor_X_off functions are used for when the robot is spun-down

void motor_on(float throttle_percent, int motor_pin) {

  if (THROTTLE_TYPE == BINARY_THROTTLE) {
    digitalWrite(motor_pin, HIGH);
  }

  if (THROTTLE_TYPE == FIXED_PWM_THROTTLE) {
    //ledcWrite(motor_pin, PWM_MOTOR_ON);
    escDictionary[motor_pin].writeMicroseconds(2000);
  }

//If DYNAMIC_PWM_THROTTLE - PWM is scaled between PWM_MOTOR_COAST and PWM_MOTOR_ON
//Applies over range defined by DYNAMIC_PWM_THROTTLE_PERCENT_MAX - maxed at PWM_MOTOR_ON above this
  if (THROTTLE_TYPE == DYNAMIC_PWM_THROTTLE) {
    float throttle_pwm = PWM_MOTOR_COAST + ((throttle_percent / DYNAMIC_PWM_THROTTLE_PERCENT_MAX) * (PWM_MOTOR_ON - PWM_MOTOR_COAST));
    if (throttle_pwm > PWM_MOTOR_ON) throttle_pwm = PWM_MOTOR_ON;
    ledcWrite(motor_pin, throttle_pwm);
  }
}

void motor_1_on(float throttle_percent) {
  motor_on(throttle_percent, MOTOR_PIN1);
}

void motor_2_on(float throttle_percent) {
  motor_on(throttle_percent, MOTOR_PIN2);
}

void motor_coast(int motor_pin) {
  if (THROTTLE_TYPE == FIXED_PWM_THROTTLE || THROTTLE_TYPE == DYNAMIC_PWM_THROTTLE) {
    escDictionary[motor_pin].writeMicroseconds(1000);
  }
  if (THROTTLE_TYPE == BINARY_THROTTLE) {
    digitalWrite(motor_pin, LOW);  //same as "off" for brushed motors
  }
}

void motor_1_coast() {
  motor_coast(MOTOR_PIN1);
}

void motor_2_coast() {
  motor_coast(MOTOR_PIN2);
}

void motor_off(int motor_pin) {
  if (THROTTLE_TYPE == FIXED_PWM_THROTTLE || THROTTLE_TYPE == DYNAMIC_PWM_THROTTLE) {
    escDictionary[motor_pin].writeMicroseconds(1000);
  }
  if (THROTTLE_TYPE == BINARY_THROTTLE) {
    digitalWrite(motor_pin, LOW);  //same as "off" for brushed motors
  }
}

void motor_1_off() {
  motor_off(MOTOR_PIN1);
}

void motor_2_off() {
  motor_off(MOTOR_PIN2);
}

void motors_off() {
  motor_1_off();
  motor_2_off();
}

const int freq = 60;
const int resolution = 8; 

std::unordered_map<int, Servo> escDictionary;

void init_motors() {
  //ledcSetup(0, freq, resolution);
  esc1.attach(MOTOR_PIN1);
  escDictionary[MOTOR_PIN1] = esc1;

  //ledcSetup(1, freq, resolution);
  esc2.attach(MOTOR_PIN2);
  escDictionary[MOTOR_PIN2] = esc2;


  //pinMode(MOTOR_PIN1, OUTPUT);
  //pinMode(MOTOR_PIN2, OUTPUT);
  motors_off();
}
