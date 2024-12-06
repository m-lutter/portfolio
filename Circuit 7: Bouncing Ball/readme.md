# Bouncing Ball Circuit
This circuit simulates a bouncing ball on an 8x8 pixel screen, beginning at one point on the screen and progressing, bouncing around the screen without user input. The focus of this circuit is the finite state machine governing the movement of the ball, although this circuit also posed some new challenges when displaying the output.
## The Simulation
This circuit is best enjoyed by downloading the simulation, so a link to download it is found above.
First click Simulation -> Ticks Enabled from the drop down menu at the top, and then clicking on the hand icon in the upper right corner, then pressing the button in the main circuit labeled RESET, the simulation will begin.

I would recommend starting at a low clock speed such as 1 to 4 Hz to begin so that you can see how the ball moves and bounces, and then using Simulation -> Tick Frequency to speed up the simulation to 16 to 32Hz for a more natural speed.

## Full Circuit
The simulation begins when the reset button is pressed. This button presets and clears some flip flops, starting the ball at a preset position. As the circuit progresses, in its current form the ball loops through a set cycle of positions, though my original plan was to make this game like pong, with a player paddle which could change the direction of the ball. This would require a finite state machine for the player and a slightly modified one for the horizontal movement. There is a finite state machine for the vertical and for the horizontal movement, and those are explained in more detail below. 

The finite state machines each output a 3 bit number which represents the player's position on the screen, either vertical or horizontal. Since there is not a 6 to 64 bit decoder which would be necessary to mirror the output implementation of the frogger circuit (Circuit 6), I instead used a 3 to 8 decoder to decode the horizontal position, and a demux with 3 control bits to select the vertical position of the output. This demux took in an 8 bit horizontal position from the decoder (since the decoder is 1-hot, the output is an 8 bit number with one 1, corresponding to the position of the 'ball'), and output that number to the corresponding vertical position, and 0000 0000 to the remaining positions. This meant that any position representable by a 6 bit number could be represented on the 8x8 screen, which has 64 pixels.
![Full Circuit](https://github.com/user-attachments/assets/ad65f8ca-3a35-42a8-bce2-36ef2d3fe912)

## Vertical and Horizontal Finite State Machines
The vertical and horizontal finite state machines are identical except for their reset functions, since resetting both identical machines to the same value yields a pixel which starts along the diagonal of the display and remains on that diagonal. Therefore, I will explain both here.
![Vertical Finite State Machine](https://github.com/user-attachments/assets/10392ac5-ab2d-462d-8921-0784af76774d)
![Horizontal Finite State Machine](https://github.com/user-attachments/assets/7e77c3e5-83b7-49a1-b1c9-1e60a0d4b483)
The behavior I sought was a finite state machine which counted up to 8 from any value and then down to 0. The circuit has no inputs, but the same vertical position has two valid next states since most positions can either travel down or up from their current position, and I sought to be able to change the direction of the ball other than hitting a wall. Therefore I used three bits for the position of the ball and one bit for the direction of the movement. 

For state assignments I used the binary representation of the number since I would be decoding the value anyways, so any savings made in logic would be paid again to make a sensible output. I used JK flip flops because D flip flops did not seem to yield simple equations. The transition table and K-maps can be seen below:
![image](https://github.com/user-attachments/assets/6cf2081e-4747-4cf9-bd9f-bcbfec26bc48)


