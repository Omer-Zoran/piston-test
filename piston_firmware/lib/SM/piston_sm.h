#ifndef PISTON_SM_H
#define PISTON_SM_H
#include "Arduino.h"
#include <piston_motor.h>

typedef enum piston_sm_states {PISTON_IDLE, PISTON_MOVING} piston_sm_states;

void set_piston_sm_state(piston_sm_states st);
piston_sm_states get_piston_sm_state();
void start_move_sm(piston_motor* motor, uint8_t precent, uint8_t direction);
void piston_sm_loop(piston_motor* motor);

#endif // PISTON_SM_H