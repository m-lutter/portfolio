## 4-bit Multiplier

# Input/Output
This circuit takes two 4 bit unsigned inputs and uses binary addition and shift operations to perform multiplication.
The input is 4 bits and the output is 8 bits. This allows the circuit to have valid outputs for any input combination since overflow is not possible.
![image](https://github.com/user-attachments/assets/3f3177a9-a50b-436f-9ecc-64c9e2d7a465)

# How it works
The circuit uses 3 8-bit adders.
In the first stage, a MUX uses the first bit as an enable bit and the top input as its input. 
This means that if the first digit of the bottom input is 1, the top input is added, and otherwise 00000000 is added.
In the next stage, the top input is shifted left once with a SL SER value of 0, and the same MUX logic is performed with the second digit of the bottom input. 

In the third stage, the same process is repeated, except that the previously shifted value is used instead of the original input, and the third digit of the input is connected to the MUX inputs. The final stage follows similarly.

