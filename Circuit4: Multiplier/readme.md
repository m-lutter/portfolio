# 4-bit Multiplier

## Input/Output
This circuit takes two 4 bit unsigned inputs and uses binary addition and multiplexers to perform multiplication, with the output displayed on 8 LEDs.
The inputs are 4 bits and the output is 8 bits. This allows the circuit to have valid outputs for any input combination since overflow is not possible.
Although there is an attached simulation, the circuit is designed to be physically easy to make with the parts listed and the schematic provided, both at the bottom of the page.

![image](https://github.com/user-attachments/assets/3f3177a9-a50b-436f-9ecc-64c9e2d7a465)

## How it works
Two 4-bit inputs are entered, one on Top and one on Bottom. This circuit uses the top value as a base and uses the bottom input to guide "shift" operations which are then fed to adders.

The algorithm for this circuit breaks up the Bottom input into individual digits, and their position in the input dictates the amount of shifting that is done on the top input before it is added to the running total. This is essentially the same way that binary multiplication is done by hand, except in this case the overflow bits are omitted and the shifting is done using addition. 

A simple way to shift a number left by one is by adding the number to itself. The caveat is that overflow is possible, so the carry out must be accounted for. The first time a shift operation is done, the carry out is extended to a bitwidth of 4. In the simulation a bit extender extends the carry out by simply placing 3 zeros in front of the value for bitwidth compatibility, but this step is unnecessary in a real circuit and is thus omitted on the schematic. In a real circuit this would be done by simply grounding any pins on inputs this value is connected to that represent more significant bits. This can be observed on MUX #3 and Adder #3 on the schematic below.

In the first stage, the unmodified Top input's individual bits are connected to a Quad 2 to 1 MUX, with each bit connected to both input pins for a given output. The enable and control inputs are then connected together to the LSB of the Bottom input (on the schematic this value is inverted first since the enable is active LOW, and the value of the control bit does not change the output). The result is an output equal to the full Top input string of bits when the LSB of the Bottom input is 1 and an output of 0000 if the LSB of the Bottom input is 0 (an AND gate would not work because the output must have a bitwidth of 4).

For example, if the Top input is 1010 and the bottom input is 0101, the output of the first MUX would be 1010; conversely, for the same top input 1010 with a Bottom input of 0100, the output would be 0000. Basically, the LSB for the Bottom input works to switch the value added; either the Top input is added, or 0000 is added.

Next, this MUX output is the input for the first adder in the top chain of adders keeping track of the running total. The other input of this adder is connected to the second MUX which outputs either the 4 least significant bits of the Top input shifted once if the second bit of the Bottom input is 1, or 0000 if the second bit of the bottom input is 0. 

This adder is the first in the chain of adders whose output is considered the 4 least significant bits of the running total. The carry out is then input to the carry in of the adder below it. This adder adds this bit to the third multiplexer's output, which is either the 4 most significant bits of the Top input shifted once, or 0000 if the second bit of the Bottom input is 0. This adder is the first in the chain of adders whose output is considered the 4 most significant bits of the output, and the carry out is ignored since it can never be 1 (the only possible values at this point are 0000, 0001 and 0010).

The logic of separating the 4 least significant bits of the value is consistent both in the top chain of adders summing the total and also in the bottom set of adders used to shift the top input successively. By keeping the shifted values separate, we can use two 4-bit adders with a carry from the adder with the 4 least significant bits into the adder with the 4 most significant bits, yielding two connected chains of adders each containing 4 bits of the running total.

Except for the first bit, each bit from the lower input controls two multiplexers containing the top input string shifted left once, twice, and thrice for the second, third and fourth input bits respectively. This shifted string is added to the running total if the bit is 1 and otherwise 00000000 is added to the running total. This is equivalent to multiplying by each bit individually (either shifting by the number of zeros following it or zeroing the string out) and then summing the result.

## Simulation and Schematic
The circuit was designed using Logisim, and the file can be downloaded from 4bitMultiplier.circ

![image](https://github.com/user-attachments/assets/fbe8b0b6-0d28-431f-9eea-7813689253b6)

## Components
- 74LS283 4-bit full adder x 11
- 74LS157 Quad, 2 to 1 MUX x 7
- 74LS404 Hex Inverter x 1
- Resistor 220 Ohms x 16
- LED x 8
- DIP-8 x 1
