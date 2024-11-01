module circ_5(a, b, c, o);
input a;
input b;
input c;     // declaring inputs

output o;    // declaring output

wire w1;
wire w2;
wire w3;     // declaring internal wires

  not g0 (w1, b);  // b'
  or g1 (w2, w1, c); // c+b'
  and g2 (w3, a, w1); // a(b')
  and g3 (o, w2, w3); // o = {(c+b')(b'a)}
