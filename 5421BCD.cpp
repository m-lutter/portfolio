// Maxwell Lutter
// very simple testing program for 5421 BCD
// prints out the truth table and one test expression

#include <iostream>

int main() {
    std::cout << "\tABCD   a b c d e f g test" << std::endl;
    std::cout << "\t-------------------------" << std::endl;
    
    bool a, b, c, d, fa, fb, fc, fd, ff, fe, fg, test;
    
    for (int i = 0; i <= 15; i++) {
        // first generating the input values
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
        
        // ignoring the don't care terms
        if (i > 7 && i != 11 && i != 12) {
            std::cout << '\t' << a << b << c << d << " | x x x x x x x x" << std::endl;
            continue;
        }
        
        // finding the value of each expression
        fa = a || c || (b == d);
        fb = !b || (c == d);
        fc = (b || !c || d);
        fd = (!b != (!c && d)) || (c && !d);
        fe = (!d || (a && c)) && (!b || c);
        ff = a || (b && (!c || !d)) || (!c && !d);
        fg = (b || c) && (!b || !c || !d);
        test = (b && !c) || (b && !d) || (c && !d) || (!b && c); // example g
        
        // print the result of each sequence of inputs
        std::cout << '\t' << a << b << c << d << " | " << fa << " " << fb  << " " << fc << " " << fd << " " << fe << " " << ff << " " << fg  << " " << test << std::endl;
        return 0;
    }
}