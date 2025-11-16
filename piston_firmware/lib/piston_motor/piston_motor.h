#ifndef PISTON__H
#define PISTON__H

#include <Arduino.h>

class piston_motor
{
    public:
        piston_motor(uint8_t pwn_pin, uint8_t dir_pin):
            _pwm_pin(pwn_pin),
            _dir_pin(dir_pin){}
        void init();
        void motorMove(int8_t speed);

    private:
        char _motor_name[20];
        uint8_t _pwm_pin;
        uint8_t _dir_pin;
        uint16_t _raw_current;

};

#define PISTON_PWM 22
#define PISTON_DIR 23

extern piston_motor piston_motor_obj;

#endif // PISTON__H