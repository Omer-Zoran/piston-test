#include "piston_motor.h"   

piston_motor piston_motor_obj(PISTON_PWM, PISTON_DIR);

void piston_motor::init()
{
    pinMode(this->_pwm_pin, OUTPUT);
    pinMode(this->_dir_pin, OUTPUT);

}


void piston_motor :: motorMove(int8_t speed)
{
    if(speed > 0)
    {
        digitalWrite(this->_dir_pin, LOW);
        // analogWrite(this->_pwm_pin, speed);
        digitalWrite(this->_pwm_pin, HIGH);
    }
    else if(speed < 0)
    {
        digitalWrite(this->_dir_pin, HIGH);
        // analogWrite(this->_pwm_pin, -speed);
        digitalWrite(this->_pwm_pin, HIGH);
    }
    else
    {
        // analogWrite(this->_pwm_pin, 0);
        digitalWrite(this->_pwm_pin, LOW);
    }
}
