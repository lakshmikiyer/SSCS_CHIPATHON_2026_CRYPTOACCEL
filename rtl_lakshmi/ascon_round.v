
module ascon_round (
    input  wire [63:0] s0_i,
    input  wire [63:0] s1_i,
    input  wire [63:0] s2_i,
    input  wire [63:0] s3_i,
    input  wire [63:0] s4_i,
    input  wire [7:0]  rcon,   // round constant (only low byte of S2 is touched)
    output wire [63:0] s0_o,
    output wire [63:0] s1_o,
    output wire [63:0] s2_o,
    output wire [63:0] s3_o,
    output wire [63:0] s4_o
);
    // ---- pC: constant addition (only S2's low byte changes) -----------------
    wire [63:0] c0 = s0_i;
    wire [63:0] c1 = s1_i;
    wire [63:0] c2 = {s2_i[63:8], s2_i[7:0] ^ rcon};
    wire [63:0] c3 = s3_i;
    wire [63:0] c4 = s4_i;
 
    // ---- pS: bit-sliced 5-bit S-box, applied to all 64 columns (Eq. 7) ------
    wire [63:0] x0 = c0, x1 = c1, x2 = c2, x3 = c3, x4 = c4;
    wire [63:0] y0 = (x4 & x1) ^ x3 ^ (x2 & x1) ^ x2 ^ (x1 & x0) ^ x1 ^ x0;
    wire [63:0] y1 = x4 ^ (x3 & x2) ^ (x3 & x1) ^ x3 ^ (x2 & x1) ^ x2 ^ x1 ^ x0;
    wire [63:0] y2 = (x4 & x3) ^ x4 ^ x2 ^ x1 ^ 64'hFFFFFFFFFFFFFFFF; // "^1" per bit
    wire [63:0] y3 = (x4 & x0) ^ x4 ^ (x3 & x0) ^ x3 ^ x2 ^ x1 ^ x0;
    wire [63:0] y4 = (x4 & x1) ^ x4 ^ x3 ^ (x1 & x0) ^ x1;
 
    // ---- pL: linear diffusion layer (Eq. 8-12) ------------------------------
    function [63:0] rotr;
        input [63:0] v;
        input integer n;
        rotr = (v >> n) | (v << (64 - n));
    endfunction
 
    assign s0_o = y0 ^ rotr(y0, 19) ^ rotr(y0, 28);
    assign s1_o = y1 ^ rotr(y1, 61) ^ rotr(y1, 39);
    assign s2_o = y2 ^ rotr(y2,  1) ^ rotr(y2,  6);
    assign s3_o = y3 ^ rotr(y3, 10) ^ rotr(y3, 17);
    assign s4_o = y4 ^ rotr(y4,  7) ^ rotr(y4, 41);
    
endmodule