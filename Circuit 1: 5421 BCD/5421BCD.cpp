// Maxwell Lutter
// Simple truth table generator
#include <iostream>

int main()
{
  bool a, b , c, d, f;
  for (int i = 0; i < 16; i++) {
      // generating the input values
      if (i < 8) {
            a = 0;
        } else {
            a = 1;
        }
        if (i < 4 || (i < 12 && i > 7)) {
            b = 0;
        } else {
            b = 1;
        }
        c = i % 4 / 2;
        d = i % 2;
        // put test expression below
        f = (a && !b && d) || (!a && !d && c) || (!a && b && !c && d) || (a && !c && !d) || (!b && c && d) || (!a && !b && !d);
        std::cout << f << std::endl;
  }
}
