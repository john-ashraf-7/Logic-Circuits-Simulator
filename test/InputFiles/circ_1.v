module circ_1(a, b, c, o);
input a;
input b;
input c;     // declaring inputs

output o;    // declaring output

wire w1;
wire w2;     // declaring internal wires

  not g0 (w1, a);  // a'
  and g1 (w2, b, c);  // bc
  or g2 (o, w1, w2);  // o = a'+bc

endmodule
