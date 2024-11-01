module circ_4(a, b, c, o);
input a;
input b;
input c;     // declaring inputs

output o;    // declaring output

wire w1;
wire w2;     // declaring internal wires

  nand (w1, a, b); // (ab)'
  or (w2, w1, b); // (ab)' + b
  nor (o, c, w2); // o = (c + (ab)' + b)'
  
