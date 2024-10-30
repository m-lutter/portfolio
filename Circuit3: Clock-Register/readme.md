## Circuit 3: Clock Register Circuit
This Circuit uses a 555 timer, connected in an astable configuration, combined with a simple edge detection circuit as a clock signal for a 4-bit register. (rising edge)
This register then takes in two push button inputs connected to the S0 and S1 inputs and the SR SER and SL SER inputs to allow the user to control the output, which is then displayed on four LEDs.
This circuit also works as a simple game to create fun patterns or control the lights, and the user can even get better at the game as they play and learn the controls.

#How it works
By default, the LEDs are all off. The bottom button controls the SR SER and SL SER inputs, so holding this button until the display updates (from the clock signal) will light up the top LED.
This is because the default direction is set to right, so the uppermost LED corresponding to the MSB of the output from the shift register will light up once a shift occurs. 
A shift will occur every clock cycle, so the state of the push buttons will affect the output once every second or so.

Holding down the lower button will fill the display top to bottom if the top button is not pressed, and bottom to top if the top button is also pressed.
Releasing the lower button will clear the display from the same direction the display filled if the top button's state does not change.

With one LED lit up, the 

#Design Decisions
- Default State: By starting with LED's all off, the user can create any pattern they want, or control a single output signal simply. The SR SER and SL SER are also off by default so the game "waits" for some user input to change.
- User input: The user can control the 'flow' or direction the shift register operates with one button and the behavior of the outermost LEDs with the other button, allowing the user to make any possible output combination and to control the display in an intuitive way. The main omission would be a 'hold' function, which would require a third button. Although this would be trivial to incorporate, it may make the circuit feel less responsive or just be an added button for a marginal change depending on the implementation.
- Clock Speed: I chose a slow clock speed so the output would be easier to control and view, rather than a fast one which would 
