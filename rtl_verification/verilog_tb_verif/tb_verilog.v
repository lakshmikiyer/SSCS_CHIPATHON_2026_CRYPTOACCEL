// ============================================================================
// tb_ascon_verilog.v  
// 4 test cases:
//   Test 1: Empty AD, empty PT (key=0, nonce=0)
//   Test 2: Empty AD, 5-byte PT "Hello" (key=000102...0f, nonce=same)
//   Test 3: Encrypt-then-decrypt roundtrip of Test 2
//   Test 4: 8-byte AD ("metadata"), 6-byte PT ("secret") (key=000102...0f, nonce=same)
// ============================================================================

`timescale 1ns / 1ps

module tb_ascon_verilog;

    // ========================================================================
    // Clock & reset
    // ========================================================================
    reg clk;
    reg rst_n;

    initial clk = 0;
    always #5 clk = ~clk;  // 10 ns period → 100 MHz

    // ========================================================================
    // DUT port signals
    // ========================================================================
    reg         start;
    reg         dec_mode;
    reg  [63:0] k0_in, k1_in, n0_in, n1_in;
    reg  [63:0] tag0_in, tag1_in;

    reg         ad_empty, ad_valid, ad_last;
    reg  [127:0] ad_data;
    reg  [4:0]  ad_bytes;
    wire        ad_ready;

    reg         din_valid, din_last;
    reg  [127:0] din_data;
    reg  [4:0]  din_bytes;
    wire        din_ready;

    wire        dout_valid, dout_last;
    wire [127:0] dout_data;
    wire [4:0]  dout_bytes;

    wire        busy, done;
    wire        auth_ok;
    wire [63:0] t0_out, t1_out;

    // ========================================================================
    // DUT instantiation
    // ========================================================================
    ascon_core_adpt_encdec u_dut (
        .clk       (clk),
        .rst_n     (rst_n),
        .start     (start),
        .dec_mode  (dec_mode),
        .k0_in     (k0_in),
        .k1_in     (k1_in),
        .n0_in     (n0_in),
        .n1_in     (n1_in),
        .tag0_in   (tag0_in),
        .tag1_in   (tag1_in),
        .ad_empty  (ad_empty),
        .ad_valid  (ad_valid),
        .ad_last   (ad_last),
        .ad_data   (ad_data),
        .ad_bytes  (ad_bytes),
        .ad_ready  (ad_ready),
        .din_valid (din_valid),
        .din_last  (din_last),
        .din_data  (din_data),
        .din_bytes (din_bytes),
        .din_ready (din_ready),
        .dout_valid(dout_valid),
        .dout_last (dout_last),
        .dout_data (dout_data),
        .dout_bytes(dout_bytes),
        .busy      (busy),
        .done      (done),
        .auth_ok   (auth_ok),
        .t0_out    (t0_out),
        .t1_out    (t1_out)
    );

    // ========================================================================
    // Test outcome counters
    // ========================================================================
    integer pass_count;
    integer fail_count;

    // Captured output for data blocks
    reg [127:0] captured_dout;
    reg [4:0]   captured_dout_bytes;

    // ========================================================================
    // Task: hw_reset — assert active-low reset for 5 cycles, then release
    // ========================================================================
    task hw_reset;
        begin
            rst_n     <= 1'b0;
            start     <= 1'b0;
            dec_mode  <= 1'b0;
            k0_in     <= 64'd0;
            k1_in     <= 64'd0;
            n0_in     <= 64'd0;
            n1_in     <= 64'd0;
            tag0_in   <= 64'd0;
            tag1_in   <= 64'd0;
            ad_empty  <= 1'b0;
            ad_valid  <= 1'b0;
            ad_last   <= 1'b0;
            ad_data   <= 128'd0;
            ad_bytes  <= 5'd0;
            din_valid <= 1'b0;
            din_last  <= 1'b0;
            din_data  <= 128'd0;
            din_bytes <= 5'd0;
            repeat (5) @(posedge clk);
            rst_n <= 1'b1;
            repeat (2) @(posedge clk);
        end
    endtask

    // ========================================================================
    // Task: pulse_start — set config then pulse start for one cycle
    // ========================================================================
    task pulse_start(
        input         i_dec_mode,
        input  [63:0] i_k0, i_k1, i_n0, i_n1,
        input  [63:0] i_tag0, i_tag1,
        input         i_ad_empty
    );
        begin
            dec_mode <= i_dec_mode;
            k0_in    <= i_k0;
            k1_in    <= i_k1;
            n0_in    <= i_n0;
            n1_in    <= i_n1;
            tag0_in  <= i_tag0;
            tag1_in  <= i_tag1;
            ad_empty <= i_ad_empty;
            start    <= 1'b1;
            @(posedge clk);
            start    <= 1'b0;
        end
    endtask

    // ========================================================================
    // Task: wait_busy — wait until busy=1 (timeout after 100 cycles)
    // ========================================================================
    task wait_busy;
        integer cnt;
        begin
            cnt = 0;
            while (busy !== 1'b1 && cnt < 100) begin
                @(posedge clk);
                cnt = cnt + 1;
            end
            if (cnt >= 100) begin
                $display("ERROR: Timeout waiting for busy=1");
            end
        end
    endtask

    // ========================================================================
    // Task: send_ad_block — wait for ad_ready, send one AD block
    // ========================================================================
    task send_ad_block(
        input [127:0] data,
        input [4:0]   nbytes,
        input         is_last
    );
        integer cnt;
        begin
            cnt = 0;
            while (ad_ready !== 1'b1 && cnt < 5000) begin
                @(posedge clk);
                cnt = cnt + 1;
            end
            if (cnt >= 5000) begin
                $display("ERROR: Timeout waiting for ad_ready");
            end

            ad_valid <= 1'b1;
            ad_last  <= is_last;
            ad_data  <= data;
            ad_bytes <= nbytes;
            @(posedge clk);
            ad_valid <= 1'b0;
            ad_last  <= 1'b0;
        end
    endtask

    // ========================================================================
    // Task: send_din_block — wait for din_ready, send one data block, capture output
    // ========================================================================
    task send_din_block(
        input [127:0] data,
        input [4:0]   nbytes,
        input         is_last
    );
        integer cnt;
        begin
            // Wait for din_ready
            cnt = 0;
            while (din_ready !== 1'b1 && cnt < 5000) begin
                @(posedge clk);
                cnt = cnt + 1;
            end
            if (cnt >= 5000) begin
                $display("ERROR: Timeout waiting for din_ready");
            end

            // Drive din signals — DUT samples on next rising edge
            din_valid <= 1'b1;
            din_last  <= is_last;
            din_data  <= data;
            din_bytes <= nbytes;
            @(posedge clk);
            din_valid <= 1'b0;
            din_last  <= 1'b0;

            // dout_valid is set by NBA on this same edge — need a small delay
            // so the NBA assignments settle before we read them.
            #1;
            captured_dout       = dout_data;
            captured_dout_bytes = dout_bytes;
        end
    endtask

    // ========================================================================
    // Task: wait_done — wait until done=1 (timeout after 5000 cycles)
    // ========================================================================
    task wait_done;
        integer cnt;
        begin
            cnt = 0;
            while (done !== 1'b1 && cnt < 5000) begin
                @(posedge clk);
                cnt = cnt + 1;
            end
            if (cnt >= 5000) begin
                $display("ERROR: Timeout waiting for done=1");
            end
        end
    endtask

    // ========================================================================
    // Main test sequence
    // ========================================================================
    initial begin
        // Optional: dump waveforms for viewing in EPWave or GTKWave
        $dumpfile("tb_ascon_verilog.vcd");
        $dumpvars(0, tb_ascon_verilog);

        pass_count = 0;
        fail_count = 0;

        // ====================================================================
        // TEST 1: Empty AD, Empty PT, key=0, nonce=0
        // Golden: ct=empty, tag0=0x90f0fbf991dae8f1, tag1=0xae1bd9ca7ce3f3ca
        // ====================================================================
        $display("------------------------------------------------------------");
        $display("TEST 1: Empty AD, Empty PT (key=0, nonce=0)");
        $display("------------------------------------------------------------");

        hw_reset;

        // Pulse start: encrypt mode, all-zero key/nonce, ad_empty=1
        pulse_start(
            1'b0,                 // i_dec_mode
            64'h0000000000000000, // i_k0
            64'h0000000000000000, // i_k1
            64'h0000000000000000, // i_n0
            64'h0000000000000000, // i_n1
            64'd0,                // i_tag0
            64'd0,                // i_tag1
            1'b1                  // i_ad_empty
        );

        wait_busy;

        // Send one din block: empty PT → din_bytes=0, din_last=1, din_data=0
        send_din_block(
            128'd0, // data
            5'd0,   // nbytes
            1'b1    // is_last
        );

        wait_done;

        // Check tag
        if (t0_out === 64'h90f0fbf991dae8f1 && t1_out === 64'hae1bd9ca7ce3f3ca) begin
            $display("[PASS] Test 1: Tag matches golden reference");
            $display("  t0_out = 0x%016h (expected 0x90f0fbf991dae8f1)", t0_out);
            $display("  t1_out = 0x%016h (expected 0xae1bd9ca7ce3f3ca)", t1_out);
            pass_count = pass_count + 1;
        end else begin
            $display("[FAIL] Test 1: Tag MISMATCH");
            $display("  t0_out = 0x%016h (expected 0x90f0fbf991dae8f1)", t0_out);
            $display("  t1_out = 0x%016h (expected 0xae1bd9ca7ce3f3ca)", t1_out);
            fail_count = fail_count + 1;
        end

        // ====================================================================
        // TEST 2: Empty AD, 5-byte PT "Hello", key=000102...0f, nonce=same
        // Golden: ct bytes = af 14 bc e6 b9 (5 bytes)
        //         tag0 = 0xdc9d3fa63a8c58b6, tag1 = 0xb058f365f5f50c5a
        // ====================================================================
        $display("");
        $display("------------------------------------------------------------");
        $display("TEST 2: Empty AD, 5-byte PT 'Hello'");
        $display("------------------------------------------------------------");

        hw_reset;

        // key = 00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f
        //   k0 = bytes_to_u64(key[0:8]) = 0x0706050403020100 (little-endian)
        //   k1 = bytes_to_u64(key[8:16])= 0x0f0e0d0c0b0a0908
        // nonce = same as key
        pulse_start(
            1'b0,                 // i_dec_mode
            64'h0706050403020100, // i_k0
            64'h0f0e0d0c0b0a0908, // i_k1
            64'h0706050403020100, // i_n0
            64'h0f0e0d0c0b0a0908, // i_n1
            64'd0,                // i_tag0
            64'd0,                // i_tag1
            1'b1                  // i_ad_empty
        );

        wait_busy;

        // "Hello" = 0x48 0x65 0x6c 0x6c 0x6f
        // Little-endian 128-bit: bytes go into din_data[39:0] = 0x6f_6c_6c_65_48
        send_din_block(
            128'h6f6c6c6548,                       // data
            5'd5,                                  // nbytes
            1'b1                                   // is_last
        );

        wait_done;

        // Check ciphertext (low 5 bytes of captured_dout)
        // Expected CT: af 14 bc e6 b9  →  LE 128-bit low 40 bits = 0xb9_e6_bc_14_af
        begin : test2_check
            reg [39:0] ct_got;
            reg [39:0] ct_exp;
            reg        ct_ok, t0_ok, t1_ok;

            ct_got = captured_dout[39:0];
            ct_exp = 40'hb9e6bc14af;
            ct_ok  = (ct_got === ct_exp);
            t0_ok  = (t0_out === 64'hdc9d3fa63a8c58b6);
            t1_ok  = (t1_out === 64'hb058f365f5f50c5a);

            if (ct_ok && t0_ok && t1_ok) begin
                $display("[PASS] Test 2: CT and Tag match golden reference");
                $display("  CT (5 bytes) = 0x%010h (expected 0xb9e6bc14af)", ct_got);
                $display("  t0_out = 0x%016h (expected 0xdc9d3fa63a8c58b6)", t0_out);
                $display("  t1_out = 0x%016h (expected 0xb058f365f5f50c5a)", t1_out);
                pass_count = pass_count + 1;
            end else begin
                $display("[FAIL] Test 2: MISMATCH");
                if (!ct_ok)
                    $display("  CT (5 bytes) = 0x%010h (expected 0xb9e6bc14af)", ct_got);
                if (!t0_ok)
                    $display("  t0_out = 0x%016h (expected 0xdc9d3fa63a8c58b6)", t0_out);
                if (!t1_ok)
                    $display("  t1_out = 0x%016h (expected 0xb058f365f5f50c5a)", t1_out);
                fail_count = fail_count + 1;
            end
        end

        // ====================================================================
        // TEST 3: Encrypt-then-Decrypt roundtrip of Test 2
        //   Step A: Encrypt "Hello" (same as Test 2) → get CT + tag
        //   Step B: Decrypt with the CT + tag → recover PT, check auth_ok=1
        // ====================================================================
        $display("");
        $display("------------------------------------------------------------");
        $display("TEST 3: Encrypt-then-Decrypt roundtrip of Test 2");
        $display("------------------------------------------------------------");

        // ------- Step A: Encrypt (reuse Test 2 results) -------
        // We already have ct and tag from Test 2.  Capture them into regs.
        begin : test3_block
            reg [127:0] enc_ct_data;
            reg [4:0]   enc_ct_bytes;
            reg [63:0]  enc_t0, enc_t1;
            reg [39:0]  dec_pt_got;
            reg         pt_ok, auth_pass;

            // Save encryption results from Test 2
            enc_ct_data  = captured_dout;
            enc_ct_bytes = captured_dout_bytes;
            enc_t0       = t0_out;
            enc_t1       = t1_out;

            $display("  Step A: Using encrypted CT = 0x%010h, tag0=0x%016h, tag1=0x%016h",
                     enc_ct_data[39:0], enc_t0, enc_t1);

            // ------- Step B: Decrypt -------
            hw_reset;

            // Same key/nonce, dec_mode=1, provide tag for authentication
            pulse_start(
                1'b1,                 // i_dec_mode
                64'h0706050403020100, // i_k0
                64'h0f0e0d0c0b0a0908, // i_k1
                64'h0706050403020100, // i_n0
                64'h0f0e0d0c0b0a0908, // i_n1
                enc_t0,               // i_tag0
                enc_t1,               // i_tag1
                1'b1                  // i_ad_empty
            );

            wait_busy;

            // Feed the ciphertext as din (same block structure)
            send_din_block(
                enc_ct_data,  // data
                enc_ct_bytes, // nbytes
                1'b1          // is_last
            );

            wait_done;

            // Check recovered plaintext
            // Expected: "Hello" = 0x48 0x65 0x6c 0x6c 0x6f → LE 40 bits = 0x6f6c6c6548
            dec_pt_got = captured_dout[39:0];
            pt_ok      = (dec_pt_got === 40'h6f6c6c6548);
            auth_pass  = (auth_ok === 1'b1);

            if (pt_ok && auth_pass) begin
                $display("[PASS] Test 3: Decrypt roundtrip successful");
                $display("  Recovered PT (5 bytes) = 0x%010h (expected 0x6f6c6c6548 = 'Hello')",
                         dec_pt_got);
                $display("  auth_ok = %0d (expected 1)", auth_ok);
                pass_count = pass_count + 1;
            end else begin
                $display("[FAIL] Test 3: Decrypt roundtrip MISMATCH");
                if (!pt_ok)
                    $display("  Recovered PT = 0x%010h (expected 0x6f6c6c6548)", dec_pt_got);
                if (!auth_pass)
                    $display("  auth_ok = %0d (expected 1)", auth_ok);
                fail_count = fail_count + 1;
            end
        end

        // ====================================================================
        // TEST 4: 8-byte AD ("metadata"), 6-byte PT ("secret")
        // Golden: ct = 0e188fde957f
        //         tag0 = 0x9acf10c942363add, tag1 = 0x987a35ce66cff532
        // ====================================================================
        $display("");
        $display("------------------------------------------------------------");
        $display("TEST 4: 8-byte AD ('metadata'), 6-byte PT ('secret')");
        $display("------------------------------------------------------------");

        hw_reset;

        pulse_start(
            1'b0,                 // i_dec_mode
            64'h0706050403020100, // i_k0
            64'h0f0e0d0c0b0a0908, // i_k1
            64'h0706050403020100, // i_n0
            64'h0f0e0d0c0b0a0908, // i_n1
            64'd0,                // i_tag0
            64'd0,                // i_tag1
            1'b0                  // i_ad_empty
        );

        wait_busy;

        // "metadata" = 0x6d 0x65 0x74 0x61 0x64 0x61 0x74 0x61
        // Little-endian 64-bit: 0x617461646174656d
        send_ad_block(
            128'h617461646174656d, // data
            5'd8,                  // nbytes
            1'b1                   // is_last
        );

        // "secret" = 0x73 0x65 0x63 0x72 0x65 0x74
        // Little-endian 48-bit: 0x746572636573
        send_din_block(
            128'h746572636573,     // data
            5'd6,                  // nbytes
            1'b1                   // is_last
        );

        wait_done;

        // Check ciphertext (low 6 bytes of captured_dout)
        // Expected CT: 0e 18 8f de 95 7f  ->  LE 128-bit low 48 bits = 0x7f95de8f180e
        begin : test4_check
            reg [47:0] ct_got;
            reg [47:0] ct_exp;
            reg        ct_ok, t0_ok, t1_ok;

            ct_got = captured_dout[47:0];
            ct_exp = 48'h7f95de8f180e;
            ct_ok  = (ct_got === ct_exp);
            t0_ok  = (t0_out === 64'h9acf10c942363add);
            t1_ok  = (t1_out === 64'h987a35ce66cff532);

            if (ct_ok && t0_ok && t1_ok) begin
                $display("[PASS] Test 4: CT and Tag match golden reference");
                $display("  CT (6 bytes) = 0x%012h (expected 0x7f95de8f180e)", ct_got);
                $display("  t0_out = 0x%016h (expected 0x9acf10c942363add)", t0_out);
                $display("  t1_out = 0x%016h (expected 0x987a35ce66cff532)", t1_out);
                pass_count = pass_count + 1;
            end else begin
                $display("[FAIL] Test 4: MISMATCH");
                if (!ct_ok)
                    $display("  CT (6 bytes) = 0x%012h (expected 0x7f95de8f180e)", ct_got);
                if (!t0_ok)
                    $display("  t0_out = 0x%016h (expected 0x9acf10c942363add)", t0_out);
                if (!t1_ok)
                    $display("  t1_out = 0x%016h (expected 0x987a35ce66cff532)", t1_out);
                fail_count = fail_count + 1;
            end
        end

 
        // Summary
        // ====================================================================
        $display("");
        $display("============================================================");
        $display("TEST SUMMARY: %0d PASSED, %0d FAILED out of 4 tests",
                 pass_count, fail_count);
        $display("============================================================");

        if (fail_count == 0)
            $display(">>> ALL TESTS PASSED <<<");
        else
            $display(">>> SOME TESTS FAILED <<<");

        $finish;
    end

endmodule
