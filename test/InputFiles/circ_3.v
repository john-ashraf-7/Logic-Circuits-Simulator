module circ_3(a, b, c, o);
input a;
input b;
input c;     // declaring inputs

output o;    // declaring output

wire w1;
wire w2;
wire w3;
wire w4;     // declaring internal wires

  not g0(w1, c); // c'
  nand g1(w2, a, b); // (ab)'
  and g2(w3, w1, b); // c'b
  and g3(w4, w2, c); // c(ab)'
  or g4(o, w3, w4); // o = c'b + c(ab)'
