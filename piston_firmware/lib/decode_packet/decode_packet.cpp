#include <decode_packet.h>
#include "piston_sm.h"

void split_packet(String packet, String *arg1, String *arg2);

//! This module decodes packets in this format: "[char][arg1],[arg2]\n"
/**
 * @brief Function to decode incoming data from any sender (uart / server / whatever)
 * @param packet the packet that needs to be decoded
 * @param sender sender of the packet
 * @return void
 */
void decode_packet(String packet, int sender)
{
    Serial.printf("packet from: %d, received: ", sender);
    Serial.println(packet);

    if(packet.length() == 0)
    {
        Serial.println("Error: Empty packet received");
        return;
    }

    if(packet.length() < 1)
    {
        Serial.println("Error: Packet too short");
        return;
    }

    String arg1 = "", arg2 = "";

    if(packet.length() > 1)
    {
        split_packet(packet.substring(1), &arg1, &arg2);
    }

    String response = "";
    switch(packet[0])
    {
        case 'S':
            start_move_sm(&piston_motor_obj, arg1.toInt(), arg2.toInt());
        break;

        case 'K':
        case 'k':
            piston_motor_obj.motorMove(0);
        break;


        default:
            Serial.println("unknown command");
            break;
    }

}

void split_packet(String packet, String *arg1, String *arg2)
{
    *arg1 = "";
    *arg2 = "";
    
    if(packet.length() == 0)
    {
        return;
    }
    
    int index = 0, prev_index = 0;

    index = packet.indexOf(',', prev_index);
    if(index >= 0)
    {
        *arg1 = packet.substring(prev_index, index);
        prev_index = index + 1;

        index = packet.indexOf('\n', prev_index);
        if(index >= 0)
        {
            *arg2 = packet.substring(prev_index, index);
        }
        else
        {
            // No newline found, take rest of string as arg2
            *arg2 = packet.substring(prev_index);
        }
    }
    else  //no "," now check if theres \n and it means arg2 is empty
    {
        index = packet.indexOf('\n', prev_index);
        if(index >= 0)
        {
            *arg1 = packet.substring(prev_index, index);
        }
        else
        {
            // No newline found, take entire string as arg1
            *arg1 = packet.substring(prev_index);
        }
    }

    // Serial.println("arg1 = " + *arg1);
    // Serial.println("arg2 = " + *arg2);
}





