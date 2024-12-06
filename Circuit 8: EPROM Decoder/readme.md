# EPROM Decoder Circuit
This circuit takes in a 7 bit DIP input and outputs the number to a common anode 2-digit 7 segment display. 
An AM27C1024 EPROM is used to accept a 7 bit input and output 14 bits of output to the seven segment display.

![IMG_5183](https://github.com/user-attachments/assets/2030bd44-f971-40a2-8ec7-672575392d2f)

## Schematic
![image](https://github.com/user-attachments/assets/dee7567a-e77d-4661-99bc-7ac90fa3dc31)

The DIP input is connected to the 7 LSB of the EPROM input. The EPROM chip has 16 input pins, so the other pins are grounded.
There are 16 output pins, so the last 2 outputs are left floating.

## Truth Table
Here is a google sheets version of the truth table programmed on the EPROM chip.
![image](https://github.com/user-attachments/assets/e524ad68-d014-4a1c-b603-0beb05452ab0)

## Components
- 220 Ohm Resistor x 21
- DIP-8 input x 1
- MAN6410 Common Anode display x 1
- AM27C1024 EPROM chip x 1

![IMG_5181](https://github.com/user-attachments/assets/57ef7053-18fa-4826-96d0-02fd8a0d31bb)
