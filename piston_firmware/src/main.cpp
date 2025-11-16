#include <Arduino.h>
#include "decode_packet.h"
#include "piston_sm.h"

int8_t direction = 1;
uint32_t loop_timer = 0;
void uart_listener();

void setup() {
  Serial.begin(115200);
  piston_motor_obj.init();

}

void loop() {
  // if(millis() - loop_timer > 13000)
  // {
  //   direction *= -1;
  //   piston_motor_obj.motorMove(direction);
  //   loop_timer = millis();
  // }
  piston_sm_loop(&piston_motor_obj);
  uart_listener();
}

void uart_listener()
{
  if(Serial.available())
  {
    String packet = Serial.readStringUntil('\n');
    decode_packet(packet, 1);
  }
}

