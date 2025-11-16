#include "piston_sm.h"

const char *piston_sm_states_strings[] =
    {
        "PISTON_IDLE", "PISTON_MOVING"
    };

piston_sm_states piston_sm_state = PISTON_IDLE;
uint32_t piston_sm_timer = 0;

volatile uint32_t new_time = 0;


void set_piston_sm_state(piston_sm_states st)
{
    piston_sm_state = st;
    Serial.printf("piston_sm_state: %s\n", piston_sm_states_strings[piston_sm_state]);
    piston_sm_timer = millis();
}

piston_sm_states get_piston_sm_state()
{
    return piston_sm_state;
}

void start_move_sm(piston_motor* motor, uint16_t time_in_ms, uint8_t direction)
{
    new_time = time_in_ms;
    set_piston_sm_state(PISTON_MOVING);
    motor->motorMove(direction);
}

void piston_sm_loop(piston_motor* motor)
{    
    switch (piston_sm_state)
    {
        case PISTON_IDLE:
            break;

        case PISTON_MOVING:
            if(millis() - piston_sm_timer > new_time)
            {
                set_piston_sm_state(PISTON_IDLE);
                motor->motorMove(0);
            }
        break;

    }

}

