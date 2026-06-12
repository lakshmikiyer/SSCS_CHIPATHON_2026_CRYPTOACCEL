// =====================================================================
// RTL/Lakshmi: ascon_round.v
// =====================================================================

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

// =====================================================================
// RTL/Lakshmi: ascon_core_adpt_encdec.v
// =====================================================================

`timescale 1ns/1ps
module ascon_core_adpt_encdec (
    input  wire        clk, rst_n, start,
    input  wire        dec_mode,
    input  wire [63:0] k0_in, k1_in, n0_in, n1_in,
    input  wire [63:0] tag0_in, tag1_in,      // expected tag (decrypt only)
    // associated-data input stream
    input  wire        ad_empty, ad_valid, ad_last,
    input  wire [127:0]ad_data,
    input  wire [4:0]  ad_bytes,
    output wire        ad_ready,
    // data input stream  (plaintext if enc, ciphertext if dec)
    input  wire        din_valid, din_last,
    input  wire [127:0]din_data,
    input  wire [4:0]  din_bytes,
    output wire        din_ready,
    // data output stream (ciphertext if enc, plaintext if dec)
    output reg         dout_valid, dout_last,
    output reg [127:0] dout_data,
    output reg [4:0]   dout_bytes,
    // status + results
    output reg         busy, done,
    output reg         auth_ok,               // decrypt: 1 = tag verified
    output reg [63:0]  t0_out, t1_out         // encrypt: the tag (T'); dec: T'
);
    localparam [63:0] init_val = 64'h00001000808c0001;
    localparam [63:0] DOMSEP   = 64'h8000000000000000;

    localparam [2:0] S_IDLE=3'd0, S_RUN=3'd1, S_INITKEY=3'd2, S_AD_WAIT=3'd3,
                     S_DOMSEP=3'd4, S_DAT_WAIT=3'd5, S_FINKEY=3'd6, S_TAGS=3'd7;

    reg [2:0]  st, ret_st;
    reg [3:0]  ci;
    reg [63:0] S0, S1, S2, S3, S4;

    assign ad_ready  = (st == S_AD_WAIT);
    assign din_ready = (st == S_DAT_WAIT);

    // ---- round-constant ROM -------------------------------------------------
    reg [7:0] rcon;
    always @(*) begin
        case (ci)
            4'd4: rcon=8'hf0; 4'd5: rcon=8'he1; 4'd6: rcon=8'hd2; 4'd7: rcon=8'hc3;
            4'd8: rcon=8'hb4; 4'd9: rcon=8'ha5; 4'd10:rcon=8'h96; 4'd11:rcon=8'h87;
            4'd12:rcon=8'h78; 4'd13:rcon=8'h69; 4'd14:rcon=8'h5a; 4'd15:rcon=8'h4b;
            default: rcon=8'h00;
        endcase
    end

    // ---- AD padding for the last AD block ----------------------------------
    reg [127:0] ad_pad;
    integer ai;
    always @(*) begin
        for (ai=0; ai<16; ai=ai+1) begin
            if      (ai <  ad_bytes) ad_pad[ai*8 +: 8] = ad_data[ai*8 +: 8];
            else if (ai == ad_bytes) ad_pad[ai*8 +: 8] = 8'h01;
            else                     ad_pad[ai*8 +: 8] = 8'h00;
        end
    end
    wire [63:0] ad_lo = ad_last ? ad_pad[63:0]   : ad_data[63:0];
    wire [63:0] ad_hi = ad_last ? ad_pad[127:64] : ad_data[127:64];

    // ---- data-block logic (unified enc/dec) --------------------------------
    wire [127:0] rate128 = {S1, S0};
    wire [63:0]  din_lo = din_data[63:0];
    wire [63:0]  din_hi = din_data[127:64];
    // full block:
    wire [127:0] full_dout = {S1 ^ din_hi, S0 ^ din_lo};        // dout = rate ^ din
    wire [63:0]  full_nS0  = dec_mode ? din_lo : (S0 ^ din_lo); // rate <- din(dec)/dout(enc)
    wire [63:0]  full_nS1  = dec_mode ? din_hi : (S1 ^ din_hi);
    // last (partial) block, byte-granular:
    reg [127:0] last_dout, last_nrate;
    integer di;
    always @(*) begin
        for (di=0; di<16; di=di+1) begin
            if (di < din_bytes) last_dout[di*8 +: 8] = rate128[di*8 +: 8] ^ din_data[di*8 +: 8];
            else                last_dout[di*8 +: 8] = 8'h00;
            if      (di <  din_bytes) last_nrate[di*8 +: 8] = dec_mode ? din_data[di*8 +: 8]
                                                                       : (rate128[di*8 +: 8] ^ din_data[di*8 +: 8]);
            else if (di == din_bytes) last_nrate[di*8 +: 8] = rate128[di*8 +: 8] ^ 8'h01; // pad bit
            else                      last_nrate[di*8 +: 8] = rate128[di*8 +: 8];          // unchanged
        end
    end

    // ---- one combinational round -------------------------------------------
    wire [63:0] r0, r1, r2, r3, r4;
    ascon_round u_round (
        .s0_i(S0), .s1_i(S1), .s2_i(S2), .s3_i(S3), .s4_i(S4), .rcon(rcon),
        .s0_o(r0), .s1_o(r1), .s2_o(r2), .s3_o(r3), .s4_o(r4)
    );

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            st<=S_IDLE; ret_st<=S_IDLE; ci<=4'd0; busy<=1'b0; done<=1'b0; auth_ok<=1'b0;
            S0<=0; S1<=0; S2<=0; S3<=0; S4<=0; t0_out<=0; t1_out<=0;
            dout_valid<=1'b0; dout_data<=0; dout_bytes<=0; dout_last<=1'b0;
        end else begin
            done <= 1'b0; dout_valid <= 1'b0;
            case (st)
                S_IDLE: begin
                    busy <= 1'b0;
                    if (start) begin
                        S0<=init_val; S1<=k0_in; S2<=k1_in; S3<=n0_in; S4<=n1_in;
                        ci<=4'd4; ret_st<=S_INITKEY; st<=S_RUN; busy<=1'b1;
                    end
                end
                S_RUN: begin
                    S0<=r0; S1<=r1; S2<=r2; S3<=r3; S4<=r4;
                    if (ci==4'd15) st<=ret_st; else ci<=ci+4'd1;
                end
                S_INITKEY: begin S3<=S3^k0_in; S4<=S4^k1_in; st<=S_AD_WAIT; end
                S_AD_WAIT: begin
                    if (ad_empty) st<=S_DOMSEP;
                    else if (ad_valid) begin
                        S0<=S0^ad_lo; S1<=S1^ad_hi;
                        ci<=4'd8; ret_st <= ad_last ? S_DOMSEP : S_AD_WAIT; st<=S_RUN;
                    end
                end
                S_DOMSEP: begin S4<=S4^DOMSEP; st<=S_DAT_WAIT; end
                S_DAT_WAIT: begin
                    if (din_valid) begin
                        dout_valid<=1'b1; dout_last<=din_last;
                        if (din_last) begin
                            S0<=last_nrate[63:0]; S1<=last_nrate[127:64];
                            dout_data<=last_dout; dout_bytes<=din_bytes;
                            st<=S_FINKEY;                      // no permutation
                        end else begin
                            S0<=full_nS0; S1<=full_nS1;
                            dout_data<=full_dout; dout_bytes<=5'd16;
                            ci<=4'd8; ret_st<=S_DAT_WAIT; st<=S_RUN;
                        end
                    end
                end
                S_FINKEY: begin S2<=S2^k0_in; S3<=S3^k1_in; ci<=4'd4; ret_st<=S_TAGS; st<=S_RUN; end
                S_TAGS: begin
                    t0_out <= S3^k0_in; t1_out <= S4^k1_in;
                    auth_ok<= dec_mode ? (((S3^k0_in)==tag0_in) && ((S4^k1_in)==tag1_in)) : 1'b1;
                    done<=1'b1; busy<=1'b0; st<=S_IDLE;
                end
                default: st<=S_IDLE;
            endcase
        end
    end
endmodule
