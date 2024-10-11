# Circuit Overview
This circuit takes in two 4 bit binary numbers and outputs the sum using a 7-segment display. 
The circuit first uses a 4 bit adder chip, feeds that output to a BCD 7-segment decoder, and finally outputs the result via a common anode 7-segment display.

# Design Process
The design for this circuit was not exceptionally complicated; the main hurdle I faced was understanding all of the components of the circuit individually.
Therefore, I took time to build each component of the circuit separately to understand exactly how to achieve the output I was looking for.
I initially planned on incorporating an overflow functionality, but time and space constraints precluded me from finishing that part of the circuit.

I found the hardest part of this circuit was troubleshooting, especially with the physical parts. The display I had is broken, and I didn't realize for quite some time,
and I had many issues that came from physically wiring incorrectly or having components fall out or short together. This is why I eventually took the time to
build each section separately, since I was having different problems with each section; my DIP switch would not stay in the breadboard, I didn't fully understand the pinout of 
my BCD decoder or my 7 segment display for a while, and my adder was giving false results from off-by-one wiring errors.

Once I built each section separately, it was simple to consolidate them into one cohesive circuit and I was able to get it working.

# Contents
This branch includes photos of the circuit, a schematic for the circuit, and a block diagram for the circuit.

# Topic
The topic this circuit best fits is decoders.
