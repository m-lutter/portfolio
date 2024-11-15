## Circuit 5: Counter-Decoder Circuit
This circuit uses a decoder to process a sequence of inputs from a counter which is then displayed on an led screen. The counter is used to generate the control bits for the decoder which then cycles through a preset but easily adjustable sequence of strings which control a 4x4 RGB LED matrix.

![image](https://github.com/user-attachments/assets/92db61f0-c519-4216-92e0-8736a30787ad)

# How it works
The circuit uses a 4-bit counter using JK flip flops. Here is the transition table and K-maps I used to make the counter circuit:
![image](https://github.com/user-attachments/assets/e80fef11-89a8-426a-b838-010fffd85f3d)
The counter counts from 0 to 15 and cycles back to 0 once it reaches 15. 

This 4-bit string is input as the control bits to a decoder. The decoder takes in 16 different 8-bit strings and outputs the string corresponding to the control bits. These inputs are somewhat arbitrary, so I chose strings to create interesting patterns and sequences, including one which imitates the movement of obstacles in the 'Frogger' type game I am working on for my design project.

# The Output
The LED display works somewhat unintuitively when compared to some other RGB matrix displays, causing some benefits and some drawbacks. The first difference is that the RGB LED matrix in this simulation uses one bit for each row and each column, and the intersection of asserted rows and columns dictates which LEDs light up. This means that only 8 bits are needed to control the screen compared to a more conventional 4x4 matrix which would have one input per LED (16 in this case). Consequently, not all patterns are possible to display, such as a hollow ring pattern. 

Another main difference is how the color is selected. Rather than having R, G, B pins for each LED, the input seen at the top of the display controls the color of the display from a 24 bit string. Since I am not interested in changing the color for this circuit, the only color I have connected is white, represented in this circuit by a 24 bitwidth VCC source. 

A final key difference is that the screen does not update in response to a change in the column and row inputs, so the screen must first clear and then draw a new output. The way this is done is by first drawing a pattern with white leds, and then 'drawing' the same pattern with black/OFF LED's. I used two tri-state buffers to switch the color between black and white in sync with the pattern changing by connecting the clock signal from the counter to one tri-state buffer's enable (with a 24 bitwidth GND connection) and the clock signal inverted to the other tri-state buffer (white/VCC).

This setup means that for every cycle of the clock, the decoder's output is both drawn (LOW clock signal) and then cleared (HIGH clock signal), while the counter increments only on the rising edge of the clock signal. An implementation of this circuit on a breadboard with a more conventional RGB grid would not require this clear step; this step would be problematic if I were to use something like this for my design project since there are gaps in the position of the LED output.

# Components
- 1 Clock signal 
- 4 JK flip flops
- 2 AND gates
- 1 Decoder
- 2 Tri-state buffers
- 1 Inverter
- 1 4x4 RGB LED matrix
