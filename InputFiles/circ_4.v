module circ_4(a, b, c, o);
input a;
input b;
input c;     // declaring inputs

output o;    // declaring output

wire w1;
wire w2;     // declaring internal wires

  nand g0 (w1, a, b); // (ab)'
  or g1 (w2, w1, b); // (ab)' + b
  nor g2 (o, c, w2); // o = (c + (ab)' + b)'
  
endmodule
