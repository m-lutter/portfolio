## 4-bit Multiplier

# Input/Output
This circuit takes two 4 bit unsigned inputs and uses binary addition and multiplexers to perform multiplication, with the output displayed on 8 LEDs.
The inputs are 4 bits and the output is 8 bits. This allows the circuit to have valid outputs for any input combination since overflow is not possible.
![image](https://github.com/user-attachments/assets/3f3177a9-a50b-436f-9ecc-64c9e2d7a465)

# How it works
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

# Components
- 74LS283 4-bit full adder x 11
- 74LS157 Quad, 2 to 1 MUX x 7
- 74LS404 Hex Inverter x 1
- Resistor 220 Ohms x 16
- LED x 8
- DIP-8 x 1
