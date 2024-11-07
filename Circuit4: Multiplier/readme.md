## 4-bit Multiplier

# Input/Output
This circuit takes two 4 bit unsigned inputs and uses binary addition and multiplexers to perform multiplication, with the output displayed on 8 LEDs.
The inputs are 4 bits and the output is 8 bits. This allows the circuit to have valid outputs for any input combination since overflow is not possible.
Although there is an attached simulation, the circuit is designed to be physically easy to make with the parts listed and the schematic provided, both at the bottom of the page.
![image](https://github.com/user-attachments/assets/3f3177a9-a50b-436f-9ecc-64c9e2d7a465)

# How it works
Two 4-bit inputs are entered, one on Top and one on Bottom. This circuit uses the top value as a base and uses the bottom input to guide "shift" operations which are then fed to adders.

The algorithm for this circuit breaks up the Bottom input into individual digits, and their position in the input dictates the amount of shifting that is done on the top input before it is added to the running total. This is essentially the same way that binary multiplication is done by hand, except in this case the overflow bits are omitted and the shifting that is done must be computed manually. 

A simple way to shift a number left by one is by adding the number to itself. The caveat is that overflow is likely, so the carry out must be accounted for. The first time a shift operation is done, the carry out is extended to a bitwidth of 4, simply placing 3 zeros in front of the value of the carry out. In a real circuit this would be done by simply grounding any pins on inputs this value is connected to that represent more significant bits. This can be observed on MUX #3 and Adder #3 on the schematic below.

In the first stage, the unmodified Top input's individual bits are connected to a Quad 2 to 1 MUX, with each bit connected to both input pins for a given output. The enable and control input are then connected together to the LSB of the Bottom input inverted . The result is an output equal to the full Top input string of bits when the LSB of the Bottom input is 1 and an output of 0000 if the LSB of the Bottom input is 0.

For example, if the Top input is 1010 and the bottom input is 0101, the output of the MUX would be 1010; conversely, for the same top input 1010 with a Bottom input of 0100, the output would be 0000. Basically, the LSB for the Bottom input works as an enable for the Top input to be added.



---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

The circuit uses 11 4-bit adders and 7 Quad 2 to 1 multiplexers.
The top input is used as a base and the bottom input is split into its individual bits.
Each bit of the bottom input is a stage of the addition process.
If the bit is 1, then the top input is fed to the adder; otherwise 0 is added. 
This is achieved using a multiplexer where the enable pin is connected to the bottom input's bit (inverted).

For the next bit, two 4-bit adders are used to multiply the top input by two (by adding it with itself) and split into its 4 most significant and 4 least significant bits,
and then a multiplexer determines if the value is added based on the same logic as before using the second bit in the bottom input.

This value is then added or 0000 is added to the adder from the first bit. The output of this adder goes to the next adder and the carry goes to one below to form an eight bit adder with two 4-bit components.
The benefit in using this approach is that these 4-bit strings can be kept mostly separate aside from carry out / carry in situations and then put back together at the end, rather than combining the two and dealing with the full 8-bit string.

For the next stage, the same process is repeated, except that the previously shifted value is used instead of the original input, and the third digit of the input is connected to the MUX enable pins. The final stage follows similarly.

# Simulation and Schematic
The circuit was designed using Logisim, and the file can be downloaded from 4bitMultiplier.circ

![image](https://github.com/user-attachments/assets/fbe8b0b6-0d28-431f-9eea-7813689253b6)

# Components
- 74LS283 4-bit full adder x 11
- 74LS157 Quad, 2 to 1 MUX x 7
- 74LS404 Hex Inverter x 1
- Resistor 220 Ohms x 16
- LED x 8
- DIP-8 x 1
