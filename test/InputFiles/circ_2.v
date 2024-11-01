module circ_2(a, b, c, o);
input a;
input b;
input c;     // declaring inputs

output o;    // declaring output

wire w1;
wire w2;     // declaring internal wires

  not g0 (w1, c);  // c'
  or g1 (w2, w1, b);  // b+c'
  nand g2 (o, a, w2)  // o = (a(b+c'))'
