# Circuit 1
  This circuit takes in a 4-bit 5-4-2-1 Binary Coded Decimal (BCD) input from a DIP switch and decodes it using AND, OR and XOR logic gates, representing the output via a 7 segment common cathode display.

  My motivation for making this circuit was to find simple expressions for all outputs on the display from the given BCD and use boolean algebra to simplify the circuit to reduce the number of gates necessary.

# My design process
  First, I made a truth table with all of the possible inputs from the DIP switch and all of the outputs of the 7 segment display. Since there are some inputs with the same output (0101 = 1000 = 5 in this BCD representation), I marked the second instance of any outputs as Don't Cares.

  Next, I created Karnaugh Maps for each output and found the Sum of Products or Product of Sums expressions that were most obvious. Using these expressions, I then found the other version of each expression (SOP or POS).

  Once I had both SOP and POS representations of both circuits, I counted the number of AND and OR gates I would need to build the circuit. To further optimize the circuit, I tried to group terms together wherever possible using boolean algebra rules and I identified some cases where an XOR or XNOR gate would be efficient to use instead of AND/OR gates. In just one case, I was able to find a common term between two outputs that would save a gate, and that connection appears in the final circuit.

  As I settled on these expressions, I developed a simple C++ program to quickly verify that a boolean expression that I derived was still equal to the original expression. This helped me catch some mistakes that would have entirely foiled the end product.

  Finally, I created a schematic by building circuits according to the boolean expression that I created for each output and connecting the outputs to a common cathode LED display. I then used this schematic to guide me in building the circuit in TinkerCAD by building the circuit for each output mostly independently while reusing some outputs and inputs wherever I was able to identify the possiblility.

  The schematic for this circuit is available both as a file and as a pdf, and the circuit simulation on TinkerCad is also available.

  I believe the circuit may still be further simplified, and I think a natural improvement would come from finding the  optimal circuit to achieve the same output. I would achieve this by applying the Quine-McCluskey algorithm to the outputs simultaneously to efficiently find the common terms.

# Contents
This branch contains a download for the schematic, pictures of the schematic and circuit simulation, and 
