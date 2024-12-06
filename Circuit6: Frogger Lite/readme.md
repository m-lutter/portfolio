# Frogger Lite - Player Movement FSM
This circuit simulates the full game of frogger from my design project, though the focus of this circuit for my portfolio is the finite state machine allowing for player movement. This circuit displays the player and the obstacles separately, to mirror the functionality of using an RGB display which would have multiple output colors for the same screen, though collision and win logic are fully functional.

The player begins at the bottom of their screen, and can move in any direction. Their goal is to advance to the top row of LEDs. In their path, red obstacle pixels cross a screen of the same size. If the player character is ever in the same location on their screen as one of the obstacles on its screen, the game will freeze, indicating a loss, until the reset button is pressed.
## The Full Circuit
The full circuit can be seen below. The output for the player movement is shown on the lower LED screen and the output for the obstacles can be seen on the upper screen. The circuit takes advantage of subcircuits which can be seen on the left side of the screen, labeled accordingly.

At the top are two ring counters which generate obstacles. Their output is fed directly to the LED display, since their outputs are one-hot and 4 bits, so they do not need to be decoded to be displayed. Any unused inputs are grounded in this simulation. Each counter is given a unique clock signal speed to allow for more variable gameplay, and the counters are meaningfully different as described below.

The user provides inputs to the circuit using the push buttons on the left. the arrow buttons move the player, and the reset button resets the circuit by presetting and clearing all of the flip flops asynchronously.

Below it, two identical finite state machines take in input from the arrow buttons on the left. These buttons move the player by one pixel on the rising edge of the clock signal. The player cannot move off of the screen. Each FSM takes in two inputs, representing up and down, or right and left, and outputs a two bit number representing the vertical or horizontal position. 

The vertical position FSM's output is connected to the two LSB of the input to a decoder, and the horizontal FSM's output is connected to the two MSB of the the input to a decoder. This decoder is output as four 4-bit numbers, one for each row of the 4x4 LED display, with the single HIGH output of the decoder corresponding to the player's position on the screen.

Finally, the 8 outputs of the obstacle circuit are ANDed with the corresponding outputs of the player movement circuit where obstacles are possible, and these ANDs are NORed together. The outputs for the top row of LEDs on the player movement circuit are then ORed together, and this output is then inverted and ANDed with the obstacle collision circuit, and connected to tri state buffers which interrupt the clock signals, freezing the circuit in place.

These circuits are also fed to some LEDs to display a win or a loss.

![image](https://github.com/user-attachments/assets/031760e1-44f2-439b-9b41-cc7287707d42)

![image](https://github.com/user-attachments/assets/6190fcee-512d-44dc-839e-f61731b32f62)

![image](https://github.com/user-attachments/assets/ca01f357-5545-425b-b803-bb318192b547)

![image](https://github.com/user-attachments/assets/d2f5e0ec-ffa8-4ce5-9b06-391d65cc861d)
