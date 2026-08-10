# Synthesis - using YosysHQ 0.64 
---

## Synthesis results of the ASCON Core Design

- Total standard cell count: 6,298 total cells
- Total area: 178785.868800  µm² which is 14.78% of 1210000 µm² (1100 x 1100 die)
- Sequential area: 38.28% of total area = 68,441.95 µm²

This was done via the librelane flow, and restricting it only upto synthesis stage (stage 06/80) - which means only first six stages were run and rest were skipped.

## Netlist Visualization using `netlistsvg` by Neil Turley (GitHub):
this image represents a visualized circuit based on the netlist generate after the synthesis stage. it shows how  the circuit will look like. you can open image in a new tab and zoom in and see the individual cells like the flip-flops and gates. this visualization is ABC format which means it is Tech-Agnostic (not attached to a PDK) as pdk standard cells are not clearly visualized by this tool. (the pdk based netlist image is available in post_synthesis_GLS's readme, if you would like to see.)

<img width="3934" height="17014" alt="image" src="https://github.com/user-attachments/assets/85430363-ac2d-4f62-a380-96f8b36179f7" />


### Area report from yosys:
- critical path delay from this log at this stage (06/80) is 92711.50 ps (step 132.1.1) which is 92.7ns.
- *Note: This is an inflated pre-routing value; the actual logic depth is only 8 gates (cited as `lev = 8` in Step 132.1.1).*
```
139. Printing statistics.

=== ascon_core_adpt_encdec ===

        +----------Local Count, excluding submodules.
        |        +-Local Area, excluding submodules.
        |        | 
     6060        - wires
     6957        - wire bits
      681        - public wires
     1578        - public wire bits
       30        - ports
      927        - port bits
     6298 1.79E+05 cells
       61 1.07E+03   gf180mcu_fd_sc_mcu7t5v0__and2_1
       17  373.184   gf180mcu_fd_sc_mcu7t5v0__and3_1
        3   72.442   gf180mcu_fd_sc_mcu7t5v0__and4_1
       96 2.11E+03   gf180mcu_fd_sc_mcu7t5v0__aoi211_1
      535  9.4E+03   gf180mcu_fd_sc_mcu7t5v0__aoi21_1
       81 1.96E+03   gf180mcu_fd_sc_mcu7t5v0__aoi221_1
       72 2.21E+03   gf180mcu_fd_sc_mcu7t5v0__aoi222_1
      131 2.59E+03   gf180mcu_fd_sc_mcu7t5v0__aoi22_1
      295 2.59E+03   gf180mcu_fd_sc_mcu7t5v0__clkinv_1
      917 6.84E+04   gf180mcu_fd_sc_mcu7t5v0__dffrnq_1
      153 5.04E+03   gf180mcu_fd_sc_mcu7t5v0__mux2_2
      973 1.07E+04   gf180mcu_fd_sc_mcu7t5v0__nand2_1
       42  645.389   gf180mcu_fd_sc_mcu7t5v0__nand3_1
       13  256.838   gf180mcu_fd_sc_mcu7t5v0__nand4_1
      426 5.61E+03   gf180mcu_fd_sc_mcu7t5v0__nor2_1
       12  210.739   gf180mcu_fd_sc_mcu7t5v0__nor3_1
       34  746.368   gf180mcu_fd_sc_mcu7t5v0__nor4_1
      141  3.1E+03   gf180mcu_fd_sc_mcu7t5v0__oai211_1
      637 1.12E+04   gf180mcu_fd_sc_mcu7t5v0__oai21_1
       37  974.669   gf180mcu_fd_sc_mcu7t5v0__oai221_1
       78 1.71E+03   gf180mcu_fd_sc_mcu7t5v0__oai22_1
       90 2.17E+03   gf180mcu_fd_sc_mcu7t5v0__oai31_1
       26  684.902   gf180mcu_fd_sc_mcu7t5v0__oai32_1
       13  228.301   gf180mcu_fd_sc_mcu7t5v0__or2_1
        4   87.808   gf180mcu_fd_sc_mcu7t5v0__or3_1
        1   26.342   gf180mcu_fd_sc_mcu7t5v0__or4_1
       93 2.65E+03   gf180mcu_fd_sc_mcu7t5v0__xnor2_1
       68 3.58E+03   gf180mcu_fd_sc_mcu7t5v0__xnor3_1
     1022 2.69E+04   gf180mcu_fd_sc_mcu7t5v0__xor2_1
      227 1.15E+04   gf180mcu_fd_sc_mcu7t5v0__xor3_1

   Chip area for module '\ascon_core_adpt_encdec': 178785.868800
     of which used for sequential elements: 68441.945600 (38.28%)

```

### Graph visualization through graphviz-sfdp: ( pls open in new tab and zoom )

 <img width="1679" height="839" alt="image" src="https://github.com/user-attachments/assets/9734a3d8-ed9b-4564-b55b-5a69a7720049" />

---
terminal log:

```
 
────────────────────────────────────────────────────── Synthesis ───────────────────────────────────────────────────────
[15:13:31] VERBOSE  Running 'Yosys.Synthesis' at 'runs/RUN_2026-07-03_15-13-26/06-yosys-synthesis'…         step.py:1138
[15:13:31] VERBOSE  Logging subprocess to                                                                   step.py:1338
                    'runs/RUN_2026-07-03_15-13-26/06-yosys-synthesis/yosys-synthesis.log'…

 /----------------------------------------------------------------------------\
 |  yosys -- Yosys Open SYnthesis Suite                                       |
 |  Copyright (C) 2012 - 2026  Claire Xenia Wolf <claire@yosyshq.com>         |
 |  Distributed under an ISC-like license, type "license" to see terms        |
 \----------------------------------------------------------------------------/
 Yosys 0.64 (git sha1 6d2c445ae, g++ 13.3.0-6ubuntu2~24.04.1 -fPIC -O3)

1. Executing Liberty frontend:
/foss/pdks/gf180mcuD/libs.ref/gf180mcu_fd_sc_mcu7t5v0/lib/gf180mcu_fd_sc_mcu7t5v0__tt_025C_3v30.lib
Imported 229 cell types from liberty file.
[INFO] Using SDC file '/foss/designs/ascon_pipelined/runs/RUN_2026-07-03_15-13-26/06-yosys-synthesis/synthesis.abc.sdc'
for ABC…wtaf

2. Executing Verilog-2005 frontend: /foss/designs/ascon_pipelined/design.v
Parsing SystemVerilog input from `/foss/designs/ascon_pipelined/design.v' to AST representation.
Storing AST representation for module `$abstract\ascon_core_adpt_encdec'.
Storing AST representation for module `$abstract\ascon_round_s1'.
Storing AST representation for module `$abstract\ascon_round_s2'.
Successfully finished Verilog frontend.

3. Executing HIERARCHY pass (managing design hierarchy).

4. Executing AST frontend in derive mode using pre-parsed AST for module `\ascon_core_adpt_encdec'.
Generating RTLIL representation for module `\ascon_core_adpt_encdec'.

4.1. Analyzing design hierarchy..
Top module:  \ascon_core_adpt_encdec

4.2. Executing AST frontend in derive mode using pre-parsed AST for module `\ascon_round_s2'.
Generating RTLIL representation for module `\ascon_round_s2'.

4.3. Executing AST frontend in derive mode using pre-parsed AST for module `\ascon_round_s1'.
Generating RTLIL representation for module `\ascon_round_s1'.

4.4. Analyzing design hierarchy..
Top module:  \ascon_core_adpt_encdec
Used module:     \ascon_round_s2
Used module:     \ascon_round_s1

4.5. Analyzing design hierarchy..
Top module:  \ascon_core_adpt_encdec
Used module:     \ascon_round_s2
Used module:     \ascon_round_s1
Removing unused module `$abstract\ascon_round_s2'.
Removing unused module `$abstract\ascon_round_s1'.
Removing unused module `$abstract\ascon_core_adpt_encdec'.
Removed 3 unused modules.
Renaming module ascon_core_adpt_encdec to ascon_core_adpt_encdec.

5. Executing ATTRMAP pass (move or copy attributes).

6. Executing HIERARCHY pass (managing design hierarchy).

6.1. Analyzing design hierarchy..
Top module:  \ascon_core_adpt_encdec
Used module:     \ascon_round_s2
Used module:     \ascon_round_s1

6.2. Analyzing design hierarchy..
Top module:  \ascon_core_adpt_encdec
Used module:     \ascon_round_s2
Used module:     \ascon_round_s1
Removed 0 unused modules.

7. Executing PROC_CLEAN pass (remove empty switches from decision trees).
Cleaned up 0 empty switches.

8. Executing PROC_RMDEAD pass (remove dead branches from decision trees).
Removed 1 dead cases from process $proc$/foss/designs/ascon_pipelined/design.v:104$160 in module ascon_core_adpt_encdec.
Marked 6 switch rules as full_case in process $proc$/foss/designs/ascon_pipelined/design.v:104$160 in module
ascon_core_adpt_encdec.
Marked 48 switch rules as full_case in process $proc$/foss/designs/ascon_pipelined/design.v:79$47 in module
ascon_core_adpt_encdec.
Marked 32 switch rules as full_case in process $proc$/foss/designs/ascon_pipelined/design.v:58$6 in module
ascon_core_adpt_encdec.
Marked 1 switch rules as full_case in process $proc$/foss/designs/ascon_pipelined/design.v:46$5 in module
ascon_core_adpt_encdec.
Removed a total of 1 dead cases.

9. Executing PROC_PRUNE pass (remove redundant assignments in processes).
Removed 2 redundant assignments.
Promoted 51 assignments to connections.

10. Executing PROC_INIT pass (extract init attributes).

11. Executing PROC_ARST pass (detect async resets in processes).
Found async reset \rst_n in `\ascon_core_adpt_encdec.$proc$/foss/designs/ascon_pipelined/design.v:104$160'.

12. Executing PROC_ROM pass (convert switches to ROMs).
Converted 1 switch.
<suppressed ~88 debug messages>

13. Executing PROC_MUX pass (convert decision trees to multiplexers).
Creating decoders for process `\ascon_core_adpt_encdec.$proc$/foss/designs/ascon_pipelined/design.v:104$160'.
     1/23: $0\dout_valid[0:0]
     2/23: $0\done[0:0]
     3/23: $0\ph[0:0]
     4/23: $0\B0[63:0]
     5/23: $0\ci[3:0]
     6/23: $0\ret_st[2:0]
     7/23: $0\st[2:0]
     8/23: $0\t1_out[63:0]
     9/23: $0\t0_out[63:0]
    10/23: $0\auth_ok[0:0]
    11/23: $0\busy[0:0]
    12/23: $0\dout_bytes[4:0]
    13/23: $0\dout_data[127:0]
    14/23: $0\dout_last[0:0]
    15/23: $0\S0[63:0]
    16/23: $0\S4[63:0]
    17/23: $0\S3[63:0]
    18/23: $0\S2[63:0]
    19/23: $0\S1[63:0]
    20/23: $0\B4[63:0]
    21/23: $0\B3[63:0]
    22/23: $0\B2[63:0]
    23/23: $0\B1[63:0]
Creating decoders for process `\ascon_core_adpt_encdec.$proc$/foss/designs/ascon_pipelined/design.v:79$47'.
     1/48: $32\last_nrate[127:120]
     2/48: $31\last_nrate[127:120]
     3/48: $16\last_dout[127:120]
     4/48: $30\last_nrate[119:112]
     5/48: $29\last_nrate[119:112]
     6/48: $15\last_dout[119:112]
     7/48: $28\last_nrate[111:104]
     8/48: $27\last_nrate[111:104]
     9/48: $14\last_dout[111:104]
    10/48: $26\last_nrate[103:96]
    11/48: $25\last_nrate[103:96]
    12/48: $13\last_dout[103:96]
    13/48: $24\last_nrate[95:88]
    14/48: $23\last_nrate[95:88]
    15/48: $12\last_dout[95:88]
    16/48: $22\last_nrate[87:80]
    17/48: $21\last_nrate[87:80]
    18/48: $11\last_dout[87:80]
    19/48: $20\last_nrate[79:72]
    20/48: $19\last_nrate[79:72]
    21/48: $10\last_dout[79:72]
    22/48: $18\last_nrate[71:64]
    23/48: $17\last_nrate[71:64]
    24/48: $9\last_dout[71:64]
    25/48: $16\last_nrate[63:56]
    26/48: $15\last_nrate[63:56]
    27/48: $8\last_dout[63:56]
    28/48: $14\last_nrate[55:48]
    29/48: $13\last_nrate[55:48]
    30/48: $7\last_dout[55:48]
    31/48: $12\last_nrate[47:40]
    32/48: $11\last_nrate[47:40]
    33/48: $6\last_dout[47:40]
    34/48: $10\last_nrate[39:32]
    35/48: $9\last_nrate[39:32]
    36/48: $5\last_dout[39:32]
    37/48: $8\last_nrate[31:24]
    38/48: $7\last_nrate[31:24]
    39/48: $4\last_dout[31:24]
    40/48: $6\last_nrate[23:16]
    41/48: $5\last_nrate[23:16]
    42/48: $3\last_dout[23:16]
    43/48: $4\last_nrate[15:8]
    44/48: $3\last_nrate[15:8]
    45/48: $2\last_dout[15:8]
    46/48: $2\last_nrate[7:0]
    47/48: $1\last_nrate[7:0]
    48/48: $1\last_dout[7:0]
Creating decoders for process `\ascon_core_adpt_encdec.$proc$/foss/designs/ascon_pipelined/design.v:58$6'.
     1/32: $32\ad_pad[127:120]
     2/32: $31\ad_pad[127:120]
     3/32: $30\ad_pad[119:112]
     4/32: $29\ad_pad[119:112]
     5/32: $28\ad_pad[111:104]
     6/32: $27\ad_pad[111:104]
     7/32: $26\ad_pad[103:96]
     8/32: $25\ad_pad[103:96]
     9/32: $24\ad_pad[95:88]
    10/32: $23\ad_pad[95:88]
    11/32: $22\ad_pad[87:80]
    12/32: $21\ad_pad[87:80]
    13/32: $20\ad_pad[79:72]
    14/32: $19\ad_pad[79:72]
    15/32: $18\ad_pad[71:64]
    16/32: $17\ad_pad[71:64]
    17/32: $16\ad_pad[63:56]
    18/32: $15\ad_pad[63:56]
    19/32: $14\ad_pad[55:48]
    20/32: $13\ad_pad[55:48]
    21/32: $12\ad_pad[47:40]
    22/32: $11\ad_pad[47:40]
    23/32: $10\ad_pad[39:32]
    24/32: $9\ad_pad[39:32]
    25/32: $8\ad_pad[31:24]
    26/32: $7\ad_pad[31:24]
    27/32: $6\ad_pad[23:16]
    28/32: $5\ad_pad[23:16]
    29/32: $4\ad_pad[15:8]
    30/32: $3\ad_pad[15:8]
    31/32: $2\ad_pad[7:0]
    32/32: $1\ad_pad[7:0]
Creating decoders for process `\ascon_core_adpt_encdec.$proc$/foss/designs/ascon_pipelined/design.v:46$5'.
     1/1: $1\rcon[7:0]

14. Executing PROC_DLATCH pass (convert process syncs to latches).
No latch inferred for signal `\ascon_core_adpt_encdec.\last_dout' from process
`\ascon_core_adpt_encdec.$proc$/foss/designs/ascon_pipelined/design.v:79$47'.
No latch inferred for signal `\ascon_core_adpt_encdec.\last_nrate' from process
`\ascon_core_adpt_encdec.$proc$/foss/designs/ascon_pipelined/design.v:79$47'.
No latch inferred for signal `\ascon_core_adpt_encdec.\di' from process
`\ascon_core_adpt_encdec.$proc$/foss/designs/ascon_pipelined/design.v:79$47'.
No latch inferred for signal `\ascon_core_adpt_encdec.\ad_pad' from process
`\ascon_core_adpt_encdec.$proc$/foss/designs/ascon_pipelined/design.v:58$6'.
No latch inferred for signal `\ascon_core_adpt_encdec.\ai' from process
`\ascon_core_adpt_encdec.$proc$/foss/designs/ascon_pipelined/design.v:58$6'.
No latch inferred for signal `\ascon_core_adpt_encdec.\rcon' from process
`\ascon_core_adpt_encdec.$proc$/foss/designs/ascon_pipelined/design.v:46$5'.

15. Executing PROC_DFF pass (convert process syncs to FFs).
Creating register for signal `\ascon_core_adpt_encdec.\B1' using process
`\ascon_core_adpt_encdec.$proc$/foss/designs/ascon_pipelined/design.v:104$160'.
  created $adff cell `$procdff$857' with positive edge clock and positive level reset.
Creating register for signal `\ascon_core_adpt_encdec.\B2' using process
`\ascon_core_adpt_encdec.$proc$/foss/designs/ascon_pipelined/design.v:104$160'.
  created $adff cell `$procdff$862' with positive edge clock and positive level reset.
Creating register for signal `\ascon_core_adpt_encdec.\B3' using process
`\ascon_core_adpt_encdec.$proc$/foss/designs/ascon_pipelined/design.v:104$160'.
  created $adff cell `$procdff$867' with positive edge clock and positive level reset.
Creating register for signal `\ascon_core_adpt_encdec.\B4' using process
`\ascon_core_adpt_encdec.$proc$/foss/designs/ascon_pipelined/design.v:104$160'.
  created $adff cell `$procdff$872' with positive edge clock and positive level reset.
Creating register for signal `\ascon_core_adpt_encdec.\S1' using process
`\ascon_core_adpt_encdec.$proc$/foss/designs/ascon_pipelined/design.v:104$160'.
  created $adff cell `$procdff$877' with positive edge clock and positive level reset.
Creating register for signal `\ascon_core_adpt_encdec.\S2' using process
`\ascon_core_adpt_encdec.$proc$/foss/designs/ascon_pipelined/design.v:104$160'.
  created $adff cell `$procdff$882' with positive edge clock and positive level reset.
Creating register for signal `\ascon_core_adpt_encdec.\S3' using process
`\ascon_core_adpt_encdec.$proc$/foss/designs/ascon_pipelined/design.v:104$160'.
  created $adff cell `$procdff$887' with positive edge clock and positive level reset.
Creating register for signal `\ascon_core_adpt_encdec.\S4' using process
`\ascon_core_adpt_encdec.$proc$/foss/designs/ascon_pipelined/design.v:104$160'.
  created $adff cell `$procdff$892' with positive edge clock and positive level reset.
Creating register for signal `\ascon_core_adpt_encdec.\S0' using process
`\ascon_core_adpt_encdec.$proc$/foss/designs/ascon_pipelined/design.v:104$160'.
  created $adff cell `$procdff$897' with positive edge clock and positive level reset.
Creating register for signal `\ascon_core_adpt_encdec.\dout_valid' using process
`\ascon_core_adpt_encdec.$proc$/foss/designs/ascon_pipelined/design.v:104$160'.
  created $adff cell `$procdff$902' with positive edge clock and positive level reset.
Creating register for signal `\ascon_core_adpt_encdec.\dout_last' using process
`\ascon_core_adpt_encdec.$proc$/foss/designs/ascon_pipelined/design.v:104$160'.
  created $adff cell `$procdff$907' with positive edge clock and positive level reset.
Creating register for signal `\ascon_core_adpt_encdec.\dout_data' using process
`\ascon_core_adpt_encdec.$proc$/foss/designs/ascon_pipelined/design.v:104$160'.
  created $adff cell `$procdff$912' with positive edge clock and positive level reset.
Creating register for signal `\ascon_core_adpt_encdec.\dout_bytes' using process
`\ascon_core_adpt_encdec.$proc$/foss/designs/ascon_pipelined/design.v:104$160'.
  created $adff cell `$procdff$917' with positive edge clock and positive level reset.
Creating register for signal `\ascon_core_adpt_encdec.\busy' using process
`\ascon_core_adpt_encdec.$proc$/foss/designs/ascon_pipelined/design.v:104$160'.
  created $adff cell `$procdff$922' with positive edge clock and positive level reset.
Creating register for signal `\ascon_core_adpt_encdec.\done' using process
`\ascon_core_adpt_encdec.$proc$/foss/designs/ascon_pipelined/design.v:104$160'.
  created $adff cell `$procdff$927' with positive edge clock and positive level reset.
Creating register for signal `\ascon_core_adpt_encdec.\auth_ok' using process
`\ascon_core_adpt_encdec.$proc$/foss/designs/ascon_pipelined/design.v:104$160'.
  created $adff cell `$procdff$932' with positive edge clock and positive level reset.
Creating register for signal `\ascon_core_adpt_encdec.\t0_out' using process
`\ascon_core_adpt_encdec.$proc$/foss/designs/ascon_pipelined/design.v:104$160'.
  created $adff cell `$procdff$937' with positive edge clock and positive level reset.
Creating register for signal `\ascon_core_adpt_encdec.\t1_out' using process
`\ascon_core_adpt_encdec.$proc$/foss/designs/ascon_pipelined/design.v:104$160'.
  created $adff cell `$procdff$942' with positive edge clock and positive level reset.
Creating register for signal `\ascon_core_adpt_encdec.\st' using process
`\ascon_core_adpt_encdec.$proc$/foss/designs/ascon_pipelined/design.v:104$160'.
  created $adff cell `$procdff$947' with positive edge clock and positive level reset.
Creating register for signal `\ascon_core_adpt_encdec.\ret_st' using process
`\ascon_core_adpt_encdec.$proc$/foss/designs/ascon_pipelined/design.v:104$160'.
  created $adff cell `$procdff$952' with positive edge clock and positive level reset.
Creating register for signal `\ascon_core_adpt_encdec.\ci' using process
`\ascon_core_adpt_encdec.$proc$/foss/designs/ascon_pipelined/design.v:104$160'.
  created $adff cell `$procdff$957' with positive edge clock and positive level reset.
Creating register for signal `\ascon_core_adpt_encdec.\B0' using process
`\ascon_core_adpt_encdec.$proc$/foss/designs/ascon_pipelined/design.v:104$160'.
  created $adff cell `$procdff$962' with positive edge clock and positive level reset.
Creating register for signal `\ascon_core_adpt_encdec.\ph' using process
`\ascon_core_adpt_encdec.$proc$/foss/designs/ascon_pipelined/design.v:104$160'.
  created $adff cell `$procdff$967' with positive edge clock and positive level reset.

16. Executing PROC_MEMWR pass (convert process memory writes to cells).

17. Executing PROC_CLEAN pass (remove empty switches from decision trees).
Found and cleaned up 8 empty switches in `\ascon_core_adpt_encdec.$proc$/foss/designs/ascon_pipelined/design.v:104$160'.
Removing empty process `ascon_core_adpt_encdec.$proc$/foss/designs/ascon_pipelined/design.v:104$160'.
Found and cleaned up 48 empty switches in `\ascon_core_adpt_encdec.$proc$/foss/designs/ascon_pipelined/design.v:79$47'.
Removing empty process `ascon_core_adpt_encdec.$proc$/foss/designs/ascon_pipelined/design.v:79$47'.
Found and cleaned up 32 empty switches in `\ascon_core_adpt_encdec.$proc$/foss/designs/ascon_pipelined/design.v:58$6'.
Removing empty process `ascon_core_adpt_encdec.$proc$/foss/designs/ascon_pipelined/design.v:58$6'.
Found and cleaned up 1 empty switch in `\ascon_core_adpt_encdec.$proc$/foss/designs/ascon_pipelined/design.v:46$5'.
Removing empty process `ascon_core_adpt_encdec.$proc$/foss/designs/ascon_pipelined/design.v:46$5'.
Cleaned up 89 empty switches.

18. Executing CHECK pass (checking for obvious problems).
Checking module ascon_core_adpt_encdec...
Checking module ascon_round_s2...
Checking module ascon_round_s1...
Found and reported 0 problems.

19. Executing OPT_EXPR pass (perform const folding).
Optimizing module ascon_core_adpt_encdec.
<suppressed ~89 debug messages>
Optimizing module ascon_round_s2.
<suppressed ~20 debug messages>
Optimizing module ascon_round_s1.

20. Executing FLATTEN pass (flatten design).
Deleting now unused module ascon_round_s2.
Deleting now unused module ascon_round_s1.
<suppressed ~2 debug messages>

21. Executing OPT_EXPR pass (perform const folding).
Optimizing module ascon_core_adpt_encdec.

22. Executing OPT_CLEAN pass (remove unused cells and wires).
Finding unused cells or wires in module \ascon_core_adpt_encdec..
Removed 25 unused cells and 442 unused wires.
<suppressed ~26 debug messages>

23. Executing OPT_EXPR pass (perform const folding).
Optimizing module ascon_core_adpt_encdec.

24. Executing OPT_MERGE pass (detect identical cells).
Finding identical cells in module `\ascon_core_adpt_encdec'.
Computing hashes of 488 cells of `\ascon_core_adpt_encdec'.
Finding duplicate cells in `\ascon_core_adpt_encdec'.
Computing hashes of 400 cells of `\ascon_core_adpt_encdec'.
Finding duplicate cells in `\ascon_core_adpt_encdec'.
<suppressed ~264 debug messages>
Removed a total of 88 cells.

25. Executing OPT_MUXTREE pass (detect dead branches in mux trees).
Running muxtree optimizer on module \ascon_core_adpt_encdec..
  Creating internal representation of mux trees.
  Evaluating internal representation of mux trees.
  Analyzing evaluation results.
    dead port 1/2 on $mux $procmux$775.
    dead port 1/2 on $mux $procmux$766.
    dead port 1/2 on $mux $procmux$757.
    dead port 1/2 on $mux $procmux$748.
    dead port 1/2 on $mux $procmux$739.
    dead port 1/2 on $mux $procmux$730.
    dead port 1/2 on $mux $procmux$721.
    dead port 1/2 on $mux $procmux$712.
    dead port 1/2 on $mux $procmux$700.
    dead port 1/2 on $mux $procmux$688.
    dead port 1/2 on $mux $procmux$676.
    dead port 1/2 on $mux $procmux$664.
    dead port 1/2 on $mux $procmux$652.
    dead port 1/2 on $mux $procmux$640.
    dead port 1/2 on $mux $procmux$628.
    dead port 1/2 on $mux $procmux$616.
    dead port 1/2 on $mux $procmux$604.
    dead port 1/2 on $mux $procmux$592.
    dead port 1/2 on $mux $procmux$580.
    dead port 1/2 on $mux $procmux$568.
    dead port 1/2 on $mux $procmux$556.
    dead port 1/2 on $mux $procmux$544.
    dead port 1/2 on $mux $procmux$532.
    dead port 1/2 on $mux $procmux$520.
    dead port 1/2 on $mux $procmux$847.
    dead port 1/2 on $mux $procmux$838.
    dead port 1/2 on $mux $procmux$829.
    dead port 1/2 on $mux $procmux$820.
    dead port 1/2 on $mux $procmux$811.
    dead port 1/2 on $mux $procmux$802.
    dead port 1/2 on $mux $procmux$793.
    dead port 1/2 on $mux $procmux$784.
Removed 32 multiplexer ports.
<suppressed ~237 debug messages>

26. Executing OPT_REDUCE pass (consolidate $*mux and $reduce_* inputs).
  Optimizing cells in module \ascon_core_adpt_encdec.
Performed a total of 0 changes.

27. Executing OPT_MERGE pass (detect identical cells).
Finding identical cells in module `\ascon_core_adpt_encdec'.
Computing hashes of 368 cells of `\ascon_core_adpt_encdec'.
Finding duplicate cells in `\ascon_core_adpt_encdec'.
Removed a total of 0 cells.

28. Executing OPT_DFF pass (perform DFF optimizations).

29. Executing OPT_CLEAN pass (remove unused cells and wires).
Finding unused cells or wires in module \ascon_core_adpt_encdec..
Removed 0 unused cells and 120 unused wires.
<suppressed ~1 debug messages>

30. Executing OPT_EXPR pass (perform const folding).
Optimizing module ascon_core_adpt_encdec.

31. Rerunning OPT passes. (Maybe there is more to do…)

32. Executing OPT_MUXTREE pass (detect dead branches in mux trees).
Running muxtree optimizer on module \ascon_core_adpt_encdec..
  Creating internal representation of mux trees.
  Evaluating internal representation of mux trees.
  Analyzing evaluation results.
Removed 0 multiplexer ports.
<suppressed ~205 debug messages>

33. Executing OPT_REDUCE pass (consolidate $*mux and $reduce_* inputs).
  Optimizing cells in module \ascon_core_adpt_encdec.
Performed a total of 0 changes.

34. Executing OPT_MERGE pass (detect identical cells).
Finding identical cells in module `\ascon_core_adpt_encdec'.
Computing hashes of 368 cells of `\ascon_core_adpt_encdec'.
Finding duplicate cells in `\ascon_core_adpt_encdec'.
Removed a total of 0 cells.

35. Executing OPT_DFF pass (perform DFF optimizations).

36. Executing OPT_CLEAN pass (remove unused cells and wires).
Finding unused cells or wires in module \ascon_core_adpt_encdec..

37. Executing OPT_EXPR pass (perform const folding).
Optimizing module ascon_core_adpt_encdec.

38. Executing FSM pass (extract and optimize FSM).

38.1. Executing FSM_DETECT pass (finding FSMs in design).
Not marking ascon_core_adpt_encdec.ret_st as FSM state register:
    Users of register don't seem to benefit from recoding.

38.2. Executing FSM_EXTRACT pass (extracting FSM from design).

38.3. Executing FSM_OPT pass (simple optimizations of FSMs).

38.4. Executing OPT_CLEAN pass (remove unused cells and wires).
Finding unused cells or wires in module \ascon_core_adpt_encdec..

38.5. Executing FSM_OPT pass (simple optimizations of FSMs).

38.6. Executing FSM_RECODE pass (re-assigning FSM state encoding).

38.7. Executing FSM_INFO pass (dumping all available information on FSM cells).

38.8. Executing FSM_MAP pass (mapping FSMs to basic logic).

39. Executing OPT_EXPR pass (perform const folding).
Optimizing module ascon_core_adpt_encdec.

40. Executing OPT_MERGE pass (detect identical cells).
Finding identical cells in module `\ascon_core_adpt_encdec'.
Computing hashes of 368 cells of `\ascon_core_adpt_encdec'.
Finding duplicate cells in `\ascon_core_adpt_encdec'.
Removed a total of 0 cells.

41. Executing OPT_MUXTREE pass (detect dead branches in mux trees).
Running muxtree optimizer on module \ascon_core_adpt_encdec..
  Creating internal representation of mux trees.
  Evaluating internal representation of mux trees.
  Analyzing evaluation results.
Removed 0 multiplexer ports.
<suppressed ~205 debug messages>

42. Executing OPT_REDUCE pass (consolidate $*mux and $reduce_* inputs).
  Optimizing cells in module \ascon_core_adpt_encdec.
Performed a total of 0 changes.

43. Executing OPT_MERGE pass (detect identical cells).
Finding identical cells in module `\ascon_core_adpt_encdec'.
Computing hashes of 368 cells of `\ascon_core_adpt_encdec'.
Finding duplicate cells in `\ascon_core_adpt_encdec'.
Removed a total of 0 cells.

44. Executing OPT_DFF pass (perform DFF optimizations).
Adding EN signal on $procdff$967 ($adff) from module ascon_core_adpt_encdec (D = $0\ph[0:0], Q = \ph).
Adding EN signal on $procdff$962 ($adff) from module ascon_core_adpt_encdec (D = \b0, Q = \B0).
Adding EN signal on $procdff$957 ($adff) from module ascon_core_adpt_encdec (D = $0\ci[3:0], Q = \ci).
Adding EN signal on $procdff$952 ($adff) from module ascon_core_adpt_encdec (D = $0\ret_st[2:0], Q = \ret_st).
Adding EN signal on $procdff$947 ($adff) from module ascon_core_adpt_encdec (D = $0\st[2:0], Q = \st).
Adding EN signal on $procdff$942 ($adff) from module ascon_core_adpt_encdec (D =
$xor$/foss/designs/ascon_pipelined/design.v:130$166_Y, Q = \t1_out).
Adding EN signal on $procdff$937 ($adff) from module ascon_core_adpt_encdec (D =
$xor$/foss/designs/ascon_pipelined/design.v:130$165_Y, Q = \t0_out).
Adding EN signal on $procdff$932 ($adff) from module ascon_core_adpt_encdec (D =
$ternary$/foss/designs/ascon_pipelined/design.v:156$180_Y, Q = \auth_ok).
Adding EN signal on $procdff$922 ($adff) from module ascon_core_adpt_encdec (D = $0\busy[0:0], Q = \busy).
Adding EN signal on $procdff$917 ($adff) from module ascon_core_adpt_encdec (D = $procmux$373_Y, Q = \dout_bytes).
Adding EN signal on $procdff$912 ($adff) from module ascon_core_adpt_encdec (D = $procmux$382_Y, Q = \dout_data).
Adding EN signal on $procdff$907 ($adff) from module ascon_core_adpt_encdec (D = \din_last, Q = \dout_last).
Adding EN signal on $procdff$897 ($adff) from module ascon_core_adpt_encdec (D = $0\S0[63:0] [7:1], Q = \S0 [7:1]).
Adding EN signal on $procdff$897 ($adff) from module ascon_core_adpt_encdec (D = $0\S0[63:0] [0], Q = \S0 [0]).
Adding EN signal on $procdff$897 ($adff) from module ascon_core_adpt_encdec (D = $0\S0[63:0] [15:9], Q = \S0 [15:9]).
Adding EN signal on $procdff$897 ($adff) from module ascon_core_adpt_encdec (D = $0\S0[63:0] [8], Q = \S0 [8]).
Adding EN signal on $procdff$897 ($adff) from module ascon_core_adpt_encdec (D = $0\S0[63:0] [23:17], Q = \S0 [23:17]).
Adding EN signal on $procdff$897 ($adff) from module ascon_core_adpt_encdec (D = $0\S0[63:0] [16], Q = \S0 [16]).
Adding EN signal on $procdff$897 ($adff) from module ascon_core_adpt_encdec (D = $0\S0[63:0] [31:25], Q = \S0 [31:25]).
Adding EN signal on $procdff$897 ($adff) from module ascon_core_adpt_encdec (D = $0\S0[63:0] [24], Q = \S0 [24]).
Adding EN signal on $procdff$897 ($adff) from module ascon_core_adpt_encdec (D = $0\S0[63:0] [39:33], Q = \S0 [39:33]).
Adding EN signal on $procdff$897 ($adff) from module ascon_core_adpt_encdec (D = $0\S0[63:0] [32], Q = \S0 [32]).
Adding EN signal on $procdff$897 ($adff) from module ascon_core_adpt_encdec (D = $0\S0[63:0] [47:41], Q = \S0 [47:41]).
Adding EN signal on $procdff$897 ($adff) from module ascon_core_adpt_encdec (D = $0\S0[63:0] [40], Q = \S0 [40]).
Adding EN signal on $procdff$897 ($adff) from module ascon_core_adpt_encdec (D = $0\S0[63:0] [55:49], Q = \S0 [55:49]).
Adding EN signal on $procdff$897 ($adff) from module ascon_core_adpt_encdec (D = $0\S0[63:0] [48], Q = \S0 [48]).
Adding EN signal on $procdff$897 ($adff) from module ascon_core_adpt_encdec (D = $0\S0[63:0] [63:57], Q = \S0 [63:57]).
Adding EN signal on $procdff$897 ($adff) from module ascon_core_adpt_encdec (D = $0\S0[63:0] [56], Q = \S0 [56]).
Adding EN signal on $procdff$892 ($adff) from module ascon_core_adpt_encdec (D = $0\S4[63:0] [63], Q = \S4 [63]).
Adding EN signal on $procdff$892 ($adff) from module ascon_core_adpt_encdec (D = $0\S4[63:0] [62:0], Q = \S4 [62:0]).
Adding EN signal on $procdff$887 ($adff) from module ascon_core_adpt_encdec (D = $0\S3[63:0], Q = \S3).
Adding EN signal on $procdff$882 ($adff) from module ascon_core_adpt_encdec (D = $0\S2[63:0], Q = \S2).
Adding EN signal on $procdff$877 ($adff) from module ascon_core_adpt_encdec (D = $0\S1[63:0] [7:1], Q = \S1 [7:1]).
Adding EN signal on $procdff$877 ($adff) from module ascon_core_adpt_encdec (D = $0\S1[63:0] [0], Q = \S1 [0]).
Adding EN signal on $procdff$877 ($adff) from module ascon_core_adpt_encdec (D = $0\S1[63:0] [15:9], Q = \S1 [15:9]).
Adding EN signal on $procdff$877 ($adff) from module ascon_core_adpt_encdec (D = $0\S1[63:0] [8], Q = \S1 [8]).
Adding EN signal on $procdff$877 ($adff) from module ascon_core_adpt_encdec (D = $0\S1[63:0] [23:17], Q = \S1 [23:17]).
Adding EN signal on $procdff$877 ($adff) from module ascon_core_adpt_encdec (D = $0\S1[63:0] [16], Q = \S1 [16]).
Adding EN signal on $procdff$877 ($adff) from module ascon_core_adpt_encdec (D = $0\S1[63:0] [31:25], Q = \S1 [31:25]).
Adding EN signal on $procdff$877 ($adff) from module ascon_core_adpt_encdec (D = $0\S1[63:0] [24], Q = \S1 [24]).
Adding EN signal on $procdff$877 ($adff) from module ascon_core_adpt_encdec (D = $0\S1[63:0] [39:33], Q = \S1 [39:33]).
Adding EN signal on $procdff$877 ($adff) from module ascon_core_adpt_encdec (D = $0\S1[63:0] [32], Q = \S1 [32]).
Adding EN signal on $procdff$877 ($adff) from module ascon_core_adpt_encdec (D = $0\S1[63:0] [47:41], Q = \S1 [47:41]).
Adding EN signal on $procdff$877 ($adff) from module ascon_core_adpt_encdec (D = $0\S1[63:0] [40], Q = \S1 [40]).
Adding EN signal on $procdff$877 ($adff) from module ascon_core_adpt_encdec (D = $0\S1[63:0] [55:49], Q = \S1 [55:49]).
Adding EN signal on $procdff$877 ($adff) from module ascon_core_adpt_encdec (D = $0\S1[63:0] [48], Q = \S1 [48]).
Adding EN signal on $procdff$877 ($adff) from module ascon_core_adpt_encdec (D = $0\S1[63:0] [63:57], Q = \S1 [63:57]).
Adding EN signal on $procdff$877 ($adff) from module ascon_core_adpt_encdec (D = $0\S1[63:0] [56], Q = \S1 [56]).
Adding EN signal on $procdff$872 ($adff) from module ascon_core_adpt_encdec (D = \b4, Q = \B4).
Adding EN signal on $procdff$867 ($adff) from module ascon_core_adpt_encdec (D = \b3, Q = \B3).
Adding EN signal on $procdff$862 ($adff) from module ascon_core_adpt_encdec (D = \b2, Q = \B2).
Adding EN signal on $procdff$857 ($adff) from module ascon_core_adpt_encdec (D = \b1, Q = \B1).

45. Executing OPT_CLEAN pass (remove unused cells and wires).
Finding unused cells or wires in module \ascon_core_adpt_encdec..
Removed 19 unused cells and 19 unused wires.
<suppressed ~20 debug messages>

46. Executing OPT_EXPR pass (perform const folding).
Optimizing module ascon_core_adpt_encdec.
<suppressed ~42 debug messages>

47. Rerunning OPT passes. (Maybe there is more to do…)

48. Executing OPT_MUXTREE pass (detect dead branches in mux trees).
Running muxtree optimizer on module \ascon_core_adpt_encdec..
  Creating internal representation of mux trees.
  Evaluating internal representation of mux trees.
  Analyzing evaluation results.
Removed 0 multiplexer ports.
<suppressed ~178 debug messages>

49. Executing OPT_REDUCE pass (consolidate $*mux and $reduce_* inputs).
  Optimizing cells in module \ascon_core_adpt_encdec.
Performed a total of 0 changes.

50. Executing OPT_MERGE pass (detect identical cells).
Finding identical cells in module `\ascon_core_adpt_encdec'.
Computing hashes of 697 cells of `\ascon_core_adpt_encdec'.
Finding duplicate cells in `\ascon_core_adpt_encdec'.
Computing hashes of 478 cells of `\ascon_core_adpt_encdec'.
Finding duplicate cells in `\ascon_core_adpt_encdec'.
Computing hashes of 474 cells of `\ascon_core_adpt_encdec'.
Finding duplicate cells in `\ascon_core_adpt_encdec'.
<suppressed ~669 debug messages>
Removed a total of 223 cells.

51. Executing OPT_DFF pass (perform DFF optimizations).

52. Executing OPT_CLEAN pass (remove unused cells and wires).
Finding unused cells or wires in module \ascon_core_adpt_encdec..
Removed 0 unused cells and 223 unused wires.
<suppressed ~1 debug messages>

53. Executing OPT_EXPR pass (perform const folding).
Optimizing module ascon_core_adpt_encdec.

54. Rerunning OPT passes. (Maybe there is more to do…)

55. Executing OPT_MUXTREE pass (detect dead branches in mux trees).
Running muxtree optimizer on module \ascon_core_adpt_encdec..
  Creating internal representation of mux trees.
  Evaluating internal representation of mux trees.
  Analyzing evaluation results.
Removed 0 multiplexer ports.
<suppressed ~178 debug messages>

56. Executing OPT_REDUCE pass (consolidate $*mux and $reduce_* inputs).
  Optimizing cells in module \ascon_core_adpt_encdec.
Performed a total of 0 changes.

57. Executing OPT_MERGE pass (detect identical cells).
Finding identical cells in module `\ascon_core_adpt_encdec'.
Computing hashes of 474 cells of `\ascon_core_adpt_encdec'.
Finding duplicate cells in `\ascon_core_adpt_encdec'.
Removed a total of 0 cells.

58. Executing OPT_DFF pass (perform DFF optimizations).

59. Executing OPT_CLEAN pass (remove unused cells and wires).
Finding unused cells or wires in module \ascon_core_adpt_encdec..

60. Executing OPT_EXPR pass (perform const folding).
Optimizing module ascon_core_adpt_encdec.

61. Executing WREDUCE pass (reducing word size of cells).
Removed top 28 address bits (of 32) from memory init port ascon_core_adpt_encdec.$auto$mem.cc:351:emit$247
($auto$proc_rom.cc:155:do_switch$245).
Removed top 2 bits (of 4) from port B of cell ascon_core_adpt_encdec.$auto$opt_dff.cc:235:make_patterns_logic$1665
($ne).
Removed top 1 bits (of 3) from port B of cell ascon_core_adpt_encdec.$auto$opt_dff.cc:235:make_patterns_logic$1648
($ne).
Removed top 2 bits (of 4) from port B of cell ascon_core_adpt_encdec.$auto$opt_dff.cc:235:make_patterns_logic$1631
($ne).
Removed top 1 bits (of 3) from port B of cell ascon_core_adpt_encdec.$auto$opt_dff.cc:235:make_patterns_logic$1614
($ne).
Removed top 2 bits (of 4) from port B of cell ascon_core_adpt_encdec.$auto$opt_dff.cc:235:make_patterns_logic$1597
($ne).
Removed top 1 bits (of 3) from port B of cell ascon_core_adpt_encdec.$auto$opt_dff.cc:235:make_patterns_logic$1580
($ne).
Removed top 2 bits (of 4) from port B of cell ascon_core_adpt_encdec.$auto$opt_dff.cc:235:make_patterns_logic$1563
($ne).
Removed top 1 bits (of 3) from port B of cell ascon_core_adpt_encdec.$auto$opt_dff.cc:235:make_patterns_logic$1546
($ne).
Removed top 2 bits (of 4) from port B of cell ascon_core_adpt_encdec.$auto$opt_dff.cc:235:make_patterns_logic$1529
($ne).
Removed top 1 bits (of 3) from port B of cell ascon_core_adpt_encdec.$auto$opt_dff.cc:235:make_patterns_logic$1512
($ne).
Removed top 2 bits (of 4) from port B of cell ascon_core_adpt_encdec.$auto$opt_dff.cc:235:make_patterns_logic$1495
($ne).
Removed top 1 bits (of 3) from port B of cell ascon_core_adpt_encdec.$auto$opt_dff.cc:235:make_patterns_logic$1478
($ne).
Removed top 2 bits (of 4) from port B of cell ascon_core_adpt_encdec.$auto$opt_dff.cc:235:make_patterns_logic$1461
($ne).
Removed top 1 bits (of 3) from port B of cell ascon_core_adpt_encdec.$auto$opt_dff.cc:235:make_patterns_logic$1444
($ne).
Removed top 2 bits (of 4) from port B of cell ascon_core_adpt_encdec.$auto$opt_dff.cc:235:make_patterns_logic$1427
($ne).
Removed top 1 bits (of 3) from port B of cell ascon_core_adpt_encdec.$auto$opt_dff.cc:235:make_patterns_logic$1410
($ne).
Removed top 2 bits (of 4) from port B of cell ascon_core_adpt_encdec.$auto$opt_dff.cc:235:make_patterns_logic$1355
($ne).
Removed top 1 bits (of 3) from port B of cell ascon_core_adpt_encdec.$auto$opt_dff.cc:235:make_patterns_logic$1338
($ne).
Removed top 2 bits (of 4) from port B of cell ascon_core_adpt_encdec.$auto$opt_dff.cc:235:make_patterns_logic$1321
($ne).
Removed top 1 bits (of 3) from port B of cell ascon_core_adpt_encdec.$auto$opt_dff.cc:235:make_patterns_logic$1304
($ne).
Removed top 2 bits (of 4) from port B of cell ascon_core_adpt_encdec.$auto$opt_dff.cc:235:make_patterns_logic$1287
($ne).
Removed top 1 bits (of 3) from port B of cell ascon_core_adpt_encdec.$auto$opt_dff.cc:235:make_patterns_logic$1270
($ne).
Removed top 2 bits (of 4) from port B of cell ascon_core_adpt_encdec.$auto$opt_dff.cc:235:make_patterns_logic$1253
($ne).
Removed top 1 bits (of 3) from port B of cell ascon_core_adpt_encdec.$auto$opt_dff.cc:235:make_patterns_logic$1236
($ne).
Removed top 2 bits (of 4) from port B of cell ascon_core_adpt_encdec.$auto$opt_dff.cc:235:make_patterns_logic$1219
($ne).
Removed top 1 bits (of 3) from port B of cell ascon_core_adpt_encdec.$auto$opt_dff.cc:235:make_patterns_logic$1202
($ne).
Removed top 2 bits (of 4) from port B of cell ascon_core_adpt_encdec.$auto$opt_dff.cc:235:make_patterns_logic$1185
($ne).
Removed top 1 bits (of 3) from port B of cell ascon_core_adpt_encdec.$auto$opt_dff.cc:235:make_patterns_logic$1168
($ne).
Removed top 2 bits (of 4) from port B of cell ascon_core_adpt_encdec.$auto$opt_dff.cc:235:make_patterns_logic$1151
($ne).
Removed top 1 bits (of 3) from port B of cell ascon_core_adpt_encdec.$auto$opt_dff.cc:235:make_patterns_logic$1134
($ne).
Removed top 2 bits (of 4) from port B of cell ascon_core_adpt_encdec.$auto$opt_dff.cc:235:make_patterns_logic$1117
($ne).
Removed top 1 bits (of 3) from port B of cell ascon_core_adpt_encdec.$auto$opt_dff.cc:235:make_patterns_logic$1100
($ne).
Removed top 31 bits (of 32) from port A of cell ascon_core_adpt_encdec.$lt$/foss/designs/ascon_pipelined/design.v:60$7
($lt).
Removed top 31 bits (of 32) from port A of cell ascon_core_adpt_encdec.$lt$/foss/designs/ascon_pipelined/design.v:60$9
($lt).
Removed top 4 bits (of 5) from port A of cell ascon_core_adpt_encdec.$eq$/foss/designs/ascon_pipelined/design.v:61$10
($eq).
Removed top 30 bits (of 32) from port A of cell ascon_core_adpt_encdec.$lt$/foss/designs/ascon_pipelined/design.v:60$11
($lt).
Removed top 3 bits (of 5) from port A of cell ascon_core_adpt_encdec.$eq$/foss/designs/ascon_pipelined/design.v:61$12
($eq).
Removed top 30 bits (of 32) from port A of cell ascon_core_adpt_encdec.$lt$/foss/designs/ascon_pipelined/design.v:60$13
($lt).
Removed top 3 bits (of 5) from port A of cell ascon_core_adpt_encdec.$eq$/foss/designs/ascon_pipelined/design.v:61$14
($eq).
Removed top 29 bits (of 32) from port A of cell ascon_core_adpt_encdec.$lt$/foss/designs/ascon_pipelined/design.v:60$15
($lt).
Removed top 2 bits (of 5) from port A of cell ascon_core_adpt_encdec.$eq$/foss/designs/ascon_pipelined/design.v:61$16
($eq).
Removed top 29 bits (of 32) from port A of cell ascon_core_adpt_encdec.$lt$/foss/designs/ascon_pipelined/design.v:60$17
($lt).
Removed top 2 bits (of 5) from port A of cell ascon_core_adpt_encdec.$eq$/foss/designs/ascon_pipelined/design.v:61$18
($eq).
Removed top 29 bits (of 32) from port A of cell ascon_core_adpt_encdec.$lt$/foss/designs/ascon_pipelined/design.v:60$19
($lt).
Removed top 2 bits (of 5) from port A of cell ascon_core_adpt_encdec.$eq$/foss/designs/ascon_pipelined/design.v:61$20
($eq).
Removed top 29 bits (of 32) from port A of cell ascon_core_adpt_encdec.$lt$/foss/designs/ascon_pipelined/design.v:60$21
($lt).
Removed top 2 bits (of 5) from port A of cell ascon_core_adpt_encdec.$eq$/foss/designs/ascon_pipelined/design.v:61$22
($eq).
Removed top 28 bits (of 32) from port A of cell ascon_core_adpt_encdec.$lt$/foss/designs/ascon_pipelined/design.v:60$23
($lt).
Removed top 1 bits (of 5) from port A of cell ascon_core_adpt_encdec.$eq$/foss/designs/ascon_pipelined/design.v:61$24
($eq).
Removed top 28 bits (of 32) from port A of cell ascon_core_adpt_encdec.$lt$/foss/designs/ascon_pipelined/design.v:60$25
($lt).
Removed top 1 bits (of 5) from port A of cell ascon_core_adpt_encdec.$eq$/foss/designs/ascon_pipelined/design.v:61$26
($eq).
Removed top 28 bits (of 32) from port A of cell ascon_core_adpt_encdec.$lt$/foss/designs/ascon_pipelined/design.v:60$27
($lt).
Removed top 1 bits (of 5) from port A of cell ascon_core_adpt_encdec.$eq$/foss/designs/ascon_pipelined/design.v:61$28
($eq).
Removed top 28 bits (of 32) from port A of cell ascon_core_adpt_encdec.$lt$/foss/designs/ascon_pipelined/design.v:60$29
($lt).
Removed top 1 bits (of 5) from port A of cell ascon_core_adpt_encdec.$eq$/foss/designs/ascon_pipelined/design.v:61$30
($eq).
Removed top 28 bits (of 32) from port A of cell ascon_core_adpt_encdec.$lt$/foss/designs/ascon_pipelined/design.v:60$31
($lt).
Removed top 1 bits (of 5) from port A of cell ascon_core_adpt_encdec.$eq$/foss/designs/ascon_pipelined/design.v:61$32
($eq).
Removed top 28 bits (of 32) from port A of cell ascon_core_adpt_encdec.$lt$/foss/designs/ascon_pipelined/design.v:60$33
($lt).
Removed top 1 bits (of 5) from port A of cell ascon_core_adpt_encdec.$eq$/foss/designs/ascon_pipelined/design.v:61$34
($eq).
Removed top 28 bits (of 32) from port A of cell ascon_core_adpt_encdec.$lt$/foss/designs/ascon_pipelined/design.v:60$35
($lt).
Removed top 1 bits (of 5) from port A of cell ascon_core_adpt_encdec.$eq$/foss/designs/ascon_pipelined/design.v:61$36
($eq).
Removed top 28 bits (of 32) from port A of cell ascon_core_adpt_encdec.$lt$/foss/designs/ascon_pipelined/design.v:60$37
($lt).
Removed top 1 bits (of 5) from port A of cell ascon_core_adpt_encdec.$eq$/foss/designs/ascon_pipelined/design.v:61$38
($eq).
Removed top 31 bits (of 32) from port A of cell ascon_core_adpt_encdec.$lt$/foss/designs/ascon_pipelined/design.v:83$50
($lt).
Removed top 31 bits (of 32) from port A of cell ascon_core_adpt_encdec.$lt$/foss/designs/ascon_pipelined/design.v:83$57
($lt).
Removed top 4 bits (of 5) from port A of cell ascon_core_adpt_encdec.$eq$/foss/designs/ascon_pipelined/design.v:85$60
($eq).
Removed top 30 bits (of 32) from port A of cell ascon_core_adpt_encdec.$lt$/foss/designs/ascon_pipelined/design.v:83$64
($lt).
Removed top 3 bits (of 5) from port A of cell ascon_core_adpt_encdec.$eq$/foss/designs/ascon_pipelined/design.v:85$67
($eq).
Removed top 30 bits (of 32) from port A of cell ascon_core_adpt_encdec.$lt$/foss/designs/ascon_pipelined/design.v:83$71
($lt).
Removed top 3 bits (of 5) from port A of cell ascon_core_adpt_encdec.$eq$/foss/designs/ascon_pipelined/design.v:85$74
($eq).
Removed top 29 bits (of 32) from port A of cell ascon_core_adpt_encdec.$lt$/foss/designs/ascon_pipelined/design.v:83$78
($lt).
Removed top 2 bits (of 5) from port A of cell ascon_core_adpt_encdec.$eq$/foss/designs/ascon_pipelined/design.v:85$81
($eq).
Removed top 29 bits (of 32) from port A of cell ascon_core_adpt_encdec.$lt$/foss/designs/ascon_pipelined/design.v:83$85
($lt).
Removed top 2 bits (of 5) from port A of cell ascon_core_adpt_encdec.$eq$/foss/designs/ascon_pipelined/design.v:85$88
($eq).
Removed top 29 bits (of 32) from port A of cell ascon_core_adpt_encdec.$lt$/foss/designs/ascon_pipelined/design.v:83$92
($lt).
Removed top 2 bits (of 5) from port A of cell ascon_core_adpt_encdec.$eq$/foss/designs/ascon_pipelined/design.v:85$95
($eq).
Removed top 29 bits (of 32) from port A of cell ascon_core_adpt_encdec.$lt$/foss/designs/ascon_pipelined/design.v:83$99
($lt).
Removed top 2 bits (of 5) from port A of cell ascon_core_adpt_encdec.$eq$/foss/designs/ascon_pipelined/design.v:85$102
($eq).
Removed top 28 bits (of 32) from port A of cell ascon_core_adpt_encdec.$lt$/foss/designs/ascon_pipelined/design.v:83$106
($lt).
Removed top 1 bits (of 5) from port A of cell ascon_core_adpt_encdec.$eq$/foss/designs/ascon_pipelined/design.v:85$109
($eq).
Removed top 28 bits (of 32) from port A of cell ascon_core_adpt_encdec.$lt$/foss/designs/ascon_pipelined/design.v:83$113
($lt).
Removed top 1 bits (of 5) from port A of cell ascon_core_adpt_encdec.$eq$/foss/designs/ascon_pipelined/design.v:85$116
($eq).
Removed top 28 bits (of 32) from port A of cell ascon_core_adpt_encdec.$lt$/foss/designs/ascon_pipelined/design.v:83$120
($lt).
Removed top 1 bits (of 5) from port A of cell ascon_core_adpt_encdec.$eq$/foss/designs/ascon_pipelined/design.v:85$123
($eq).
Removed top 28 bits (of 32) from port A of cell ascon_core_adpt_encdec.$lt$/foss/designs/ascon_pipelined/design.v:83$127
($lt).
Removed top 1 bits (of 5) from port A of cell ascon_core_adpt_encdec.$eq$/foss/designs/ascon_pipelined/design.v:85$130
($eq).
Removed top 28 bits (of 32) from port A of cell ascon_core_adpt_encdec.$lt$/foss/designs/ascon_pipelined/design.v:83$134
($lt).
Removed top 1 bits (of 5) from port A of cell ascon_core_adpt_encdec.$eq$/foss/designs/ascon_pipelined/design.v:85$137
($eq).
Removed top 28 bits (of 32) from port A of cell ascon_core_adpt_encdec.$lt$/foss/designs/ascon_pipelined/design.v:83$141
($lt).
Removed top 1 bits (of 5) from port A of cell ascon_core_adpt_encdec.$eq$/foss/designs/ascon_pipelined/design.v:85$144
($eq).
Removed top 28 bits (of 32) from port A of cell ascon_core_adpt_encdec.$lt$/foss/designs/ascon_pipelined/design.v:83$148
($lt).
Removed top 1 bits (of 5) from port A of cell ascon_core_adpt_encdec.$eq$/foss/designs/ascon_pipelined/design.v:85$151
($eq).
Removed top 28 bits (of 32) from port A of cell ascon_core_adpt_encdec.$lt$/foss/designs/ascon_pipelined/design.v:83$155
($lt).
Removed top 1 bits (of 5) from port A of cell ascon_core_adpt_encdec.$eq$/foss/designs/ascon_pipelined/design.v:85$158
($eq).
Removed top 3 bits (of 4) from port B of cell ascon_core_adpt_encdec.$add$/foss/designs/ascon_pipelined/design.v:127$164
($add).
Removed top 1 bits (of 3) from port B of cell ascon_core_adpt_encdec.$procmux$432_CMP0 ($eq).
Removed top 1 bits (of 3) from port B of cell ascon_core_adpt_encdec.$procmux$464_CMP0 ($eq).
Removed top 2 bits (of 3) from port B of cell ascon_core_adpt_encdec.$procmux$515_CMP0 ($eq).
Removed top 7 bits (of 8) from mux cell ascon_core_adpt_encdec.$procmux$517 ($mux).
Removed top 7 bits (of 8) from mux cell ascon_core_adpt_encdec.$procmux$529 ($mux).
Removed top 7 bits (of 8) from mux cell ascon_core_adpt_encdec.$procmux$541 ($mux).
Removed top 7 bits (of 8) from mux cell ascon_core_adpt_encdec.$procmux$553 ($mux).
Removed top 7 bits (of 8) from mux cell ascon_core_adpt_encdec.$procmux$565 ($mux).
Removed top 7 bits (of 8) from mux cell ascon_core_adpt_encdec.$procmux$577 ($mux).
Removed top 7 bits (of 8) from mux cell ascon_core_adpt_encdec.$procmux$589 ($mux).
Removed top 7 bits (of 8) from mux cell ascon_core_adpt_encdec.$procmux$601 ($mux).
Removed top 7 bits (of 8) from mux cell ascon_core_adpt_encdec.$procmux$613 ($mux).
Removed top 7 bits (of 8) from mux cell ascon_core_adpt_encdec.$procmux$625 ($mux).
Removed top 7 bits (of 8) from mux cell ascon_core_adpt_encdec.$procmux$637 ($mux).
Removed top 7 bits (of 8) from mux cell ascon_core_adpt_encdec.$procmux$649 ($mux).
Removed top 7 bits (of 8) from mux cell ascon_core_adpt_encdec.$procmux$661 ($mux).
Removed top 7 bits (of 8) from mux cell ascon_core_adpt_encdec.$procmux$673 ($mux).
Removed top 7 bits (of 8) from mux cell ascon_core_adpt_encdec.$procmux$685 ($mux).
Removed top 7 bits (of 8) from mux cell ascon_core_adpt_encdec.$procmux$697 ($mux).
Removed top 7 bits (of 8) from mux cell ascon_core_adpt_encdec.$procmux$709 ($mux).
Removed top 7 bits (of 8) from mux cell ascon_core_adpt_encdec.$procmux$718 ($mux).
Removed top 7 bits (of 8) from mux cell ascon_core_adpt_encdec.$procmux$727 ($mux).
Removed top 7 bits (of 8) from mux cell ascon_core_adpt_encdec.$procmux$736 ($mux).
Removed top 7 bits (of 8) from mux cell ascon_core_adpt_encdec.$procmux$745 ($mux).
Removed top 7 bits (of 8) from mux cell ascon_core_adpt_encdec.$procmux$754 ($mux).
Removed top 7 bits (of 8) from mux cell ascon_core_adpt_encdec.$procmux$763 ($mux).
Removed top 7 bits (of 8) from mux cell ascon_core_adpt_encdec.$procmux$772 ($mux).
Removed top 7 bits (of 8) from mux cell ascon_core_adpt_encdec.$procmux$781 ($mux).
Removed top 7 bits (of 8) from mux cell ascon_core_adpt_encdec.$procmux$790 ($mux).
Removed top 7 bits (of 8) from mux cell ascon_core_adpt_encdec.$procmux$799 ($mux).
Removed top 7 bits (of 8) from mux cell ascon_core_adpt_encdec.$procmux$808 ($mux).
Removed top 7 bits (of 8) from mux cell ascon_core_adpt_encdec.$procmux$817 ($mux).
Removed top 7 bits (of 8) from mux cell ascon_core_adpt_encdec.$procmux$826 ($mux).
Removed top 7 bits (of 8) from mux cell ascon_core_adpt_encdec.$procmux$835 ($mux).
Removed top 7 bits (of 8) from mux cell ascon_core_adpt_encdec.$procmux$844 ($mux).
Removed top 1 bits (of 64) from port A of cell
ascon_core_adpt_encdec.$flatten\u_s2.$or$/foss/designs/ascon_pipelined/design.v:218$203 ($or).
Removed top 17 bits (of 64) from port A of cell
ascon_core_adpt_encdec.$flatten\u_s2.$or$/foss/designs/ascon_pipelined/design.v:219$215 ($or).
Removed top 39 bits (of 64) from port A of cell
ascon_core_adpt_encdec.$flatten\u_s2.$or$/foss/designs/ascon_pipelined/design.v:217$199 ($or).
Removed top 6 bits (of 64) from port A of cell
ascon_core_adpt_encdec.$flatten\u_s2.$or$/foss/designs/ascon_pipelined/design.v:218$207 ($or).
Removed top 61 bits (of 64) from port A of cell
ascon_core_adpt_encdec.$flatten\u_s2.$or$/foss/designs/ascon_pipelined/design.v:217$195 ($or).
Removed top 7 bits (of 64) from port A of cell
ascon_core_adpt_encdec.$flatten\u_s2.$or$/foss/designs/ascon_pipelined/design.v:220$219 ($or).
Removed top 28 bits (of 64) from port A of cell
ascon_core_adpt_encdec.$flatten\u_s2.$or$/foss/designs/ascon_pipelined/design.v:216$191 ($or).
Removed top 10 bits (of 64) from port A of cell
ascon_core_adpt_encdec.$flatten\u_s2.$or$/foss/designs/ascon_pipelined/design.v:219$211 ($or).
Removed top 19 bits (of 64) from port A of cell
ascon_core_adpt_encdec.$flatten\u_s2.$or$/foss/designs/ascon_pipelined/design.v:216$187 ($or).
Removed top 41 bits (of 64) from port A of cell
ascon_core_adpt_encdec.$flatten\u_s2.$or$/foss/designs/ascon_pipelined/design.v:220$223 ($or).
Removed top 7 bits (of 8) from wire ascon_core_adpt_encdec.$10\ad_pad[39:32].
Removed top 7 bits (of 8) from wire ascon_core_adpt_encdec.$10\last_nrate[39:32].
Removed top 7 bits (of 8) from wire ascon_core_adpt_encdec.$12\ad_pad[47:40].
Removed top 7 bits (of 8) from wire ascon_core_adpt_encdec.$12\last_nrate[47:40].
Removed top 7 bits (of 8) from wire ascon_core_adpt_encdec.$14\ad_pad[55:48].
Removed top 7 bits (of 8) from wire ascon_core_adpt_encdec.$14\last_nrate[55:48].
Removed top 7 bits (of 8) from wire ascon_core_adpt_encdec.$16\ad_pad[63:56].
Removed top 7 bits (of 8) from wire ascon_core_adpt_encdec.$16\last_nrate[63:56].
Removed top 7 bits (of 8) from wire ascon_core_adpt_encdec.$18\ad_pad[71:64].
Removed top 7 bits (of 8) from wire ascon_core_adpt_encdec.$18\last_nrate[71:64].
Removed top 7 bits (of 8) from wire ascon_core_adpt_encdec.$20\ad_pad[79:72].
Removed top 7 bits (of 8) from wire ascon_core_adpt_encdec.$20\last_nrate[79:72].
Removed top 7 bits (of 8) from wire ascon_core_adpt_encdec.$22\ad_pad[87:80].
Removed top 7 bits (of 8) from wire ascon_core_adpt_encdec.$22\last_nrate[87:80].
Removed top 7 bits (of 8) from wire ascon_core_adpt_encdec.$24\ad_pad[95:88].
Removed top 7 bits (of 8) from wire ascon_core_adpt_encdec.$24\last_nrate[95:88].
Removed top 7 bits (of 8) from wire ascon_core_adpt_encdec.$26\ad_pad[103:96].
Removed top 7 bits (of 8) from wire ascon_core_adpt_encdec.$26\last_nrate[103:96].
Removed top 7 bits (of 8) from wire ascon_core_adpt_encdec.$28\ad_pad[111:104].
Removed top 7 bits (of 8) from wire ascon_core_adpt_encdec.$28\last_nrate[111:104].
Removed top 7 bits (of 8) from wire ascon_core_adpt_encdec.$2\ad_pad[7:0].
Removed top 7 bits (of 8) from wire ascon_core_adpt_encdec.$2\last_nrate[7:0].
Removed top 7 bits (of 8) from wire ascon_core_adpt_encdec.$30\ad_pad[119:112].
Removed top 7 bits (of 8) from wire ascon_core_adpt_encdec.$30\last_nrate[119:112].
Removed top 7 bits (of 8) from wire ascon_core_adpt_encdec.$32\ad_pad[127:120].
Removed top 7 bits (of 8) from wire ascon_core_adpt_encdec.$32\last_nrate[127:120].
Removed top 7 bits (of 8) from wire ascon_core_adpt_encdec.$4\ad_pad[15:8].
Removed top 7 bits (of 8) from wire ascon_core_adpt_encdec.$4\last_nrate[15:8].
Removed top 7 bits (of 8) from wire ascon_core_adpt_encdec.$6\ad_pad[23:16].
Removed top 7 bits (of 8) from wire ascon_core_adpt_encdec.$6\last_nrate[23:16].
Removed top 7 bits (of 8) from wire ascon_core_adpt_encdec.$8\ad_pad[31:24].
Removed top 7 bits (of 8) from wire ascon_core_adpt_encdec.$8\last_nrate[31:24].

62. Executing PEEPOPT pass (run peephole optimizers).

63. Executing OPT_CLEAN pass (remove unused cells and wires).
Finding unused cells or wires in module \ascon_core_adpt_encdec..
Removed 0 unused cells and 32 unused wires.
<suppressed ~1 debug messages>

64. Executing ALUMACC pass (create $alu and $macc cells).
Extracting $alu and $macc cells in module ascon_core_adpt_encdec:
  creating $macc model for $add$/foss/designs/ascon_pipelined/design.v:127$164 ($add).
  creating $alu model for $macc $add$/foss/designs/ascon_pipelined/design.v:127$164.
  creating $alu model for $lt$/foss/designs/ascon_pipelined/design.v:60$11 ($lt): new $alu
  creating $alu model for $lt$/foss/designs/ascon_pipelined/design.v:60$13 ($lt): new $alu
  creating $alu model for $lt$/foss/designs/ascon_pipelined/design.v:60$15 ($lt): new $alu
  creating $alu model for $lt$/foss/designs/ascon_pipelined/design.v:60$17 ($lt): new $alu
  creating $alu model for $lt$/foss/designs/ascon_pipelined/design.v:60$19 ($lt): new $alu
  creating $alu model for $lt$/foss/designs/ascon_pipelined/design.v:60$21 ($lt): new $alu
  creating $alu model for $lt$/foss/designs/ascon_pipelined/design.v:60$23 ($lt): new $alu
  creating $alu model for $lt$/foss/designs/ascon_pipelined/design.v:60$25 ($lt): new $alu
  creating $alu model for $lt$/foss/designs/ascon_pipelined/design.v:60$27 ($lt): new $alu
  creating $alu model for $lt$/foss/designs/ascon_pipelined/design.v:60$29 ($lt): new $alu
  creating $alu model for $lt$/foss/designs/ascon_pipelined/design.v:60$31 ($lt): new $alu
  creating $alu model for $lt$/foss/designs/ascon_pipelined/design.v:60$33 ($lt): new $alu
  creating $alu model for $lt$/foss/designs/ascon_pipelined/design.v:60$35 ($lt): new $alu
  creating $alu model for $lt$/foss/designs/ascon_pipelined/design.v:60$37 ($lt): new $alu
  creating $alu model for $lt$/foss/designs/ascon_pipelined/design.v:60$7 ($lt): new $alu
  creating $alu model for $lt$/foss/designs/ascon_pipelined/design.v:60$9 ($lt): new $alu
  creating $alu model for $lt$/foss/designs/ascon_pipelined/design.v:83$106 ($lt): new $alu
  creating $alu model for $lt$/foss/designs/ascon_pipelined/design.v:83$113 ($lt): new $alu
  creating $alu model for $lt$/foss/designs/ascon_pipelined/design.v:83$120 ($lt): new $alu
  creating $alu model for $lt$/foss/designs/ascon_pipelined/design.v:83$127 ($lt): new $alu
  creating $alu model for $lt$/foss/designs/ascon_pipelined/design.v:83$134 ($lt): new $alu
  creating $alu model for $lt$/foss/designs/ascon_pipelined/design.v:83$141 ($lt): new $alu
  creating $alu model for $lt$/foss/designs/ascon_pipelined/design.v:83$148 ($lt): new $alu
  creating $alu model for $lt$/foss/designs/ascon_pipelined/design.v:83$155 ($lt): new $alu
  creating $alu model for $lt$/foss/designs/ascon_pipelined/design.v:83$50 ($lt): new $alu
  creating $alu model for $lt$/foss/designs/ascon_pipelined/design.v:83$57 ($lt): new $alu
  creating $alu model for $lt$/foss/designs/ascon_pipelined/design.v:83$64 ($lt): new $alu
  creating $alu model for $lt$/foss/designs/ascon_pipelined/design.v:83$71 ($lt): new $alu
  creating $alu model for $lt$/foss/designs/ascon_pipelined/design.v:83$78 ($lt): new $alu
  creating $alu model for $lt$/foss/designs/ascon_pipelined/design.v:83$85 ($lt): new $alu
  creating $alu model for $lt$/foss/designs/ascon_pipelined/design.v:83$92 ($lt): new $alu
  creating $alu model for $lt$/foss/designs/ascon_pipelined/design.v:83$99 ($lt): new $alu
  creating $alu model for $eq$/foss/designs/ascon_pipelined/design.v:61$10 ($eq): merged with
$lt$/foss/designs/ascon_pipelined/design.v:60$9.
  creating $alu model for $eq$/foss/designs/ascon_pipelined/design.v:61$12 ($eq): merged with
$lt$/foss/designs/ascon_pipelined/design.v:60$11.
  creating $alu model for $eq$/foss/designs/ascon_pipelined/design.v:61$14 ($eq): merged with
$lt$/foss/designs/ascon_pipelined/design.v:60$13.
  creating $alu model for $eq$/foss/designs/ascon_pipelined/design.v:61$16 ($eq): merged with
$lt$/foss/designs/ascon_pipelined/design.v:60$15.
  creating $alu model for $eq$/foss/designs/ascon_pipelined/design.v:61$18 ($eq): merged with
$lt$/foss/designs/ascon_pipelined/design.v:60$17.
  creating $alu model for $eq$/foss/designs/ascon_pipelined/design.v:61$20 ($eq): merged with
$lt$/foss/designs/ascon_pipelined/design.v:60$19.
  creating $alu model for $eq$/foss/designs/ascon_pipelined/design.v:61$22 ($eq): merged with
$lt$/foss/designs/ascon_pipelined/design.v:60$21.
  creating $alu model for $eq$/foss/designs/ascon_pipelined/design.v:61$24 ($eq): merged with
$lt$/foss/designs/ascon_pipelined/design.v:60$23.
  creating $alu model for $eq$/foss/designs/ascon_pipelined/design.v:61$26 ($eq): merged with
$lt$/foss/designs/ascon_pipelined/design.v:60$25.
  creating $alu model for $eq$/foss/designs/ascon_pipelined/design.v:61$28 ($eq): merged with
$lt$/foss/designs/ascon_pipelined/design.v:60$27.
  creating $alu model for $eq$/foss/designs/ascon_pipelined/design.v:61$30 ($eq): merged with
$lt$/foss/designs/ascon_pipelined/design.v:60$29.
  creating $alu model for $eq$/foss/designs/ascon_pipelined/design.v:61$32 ($eq): merged with
$lt$/foss/designs/ascon_pipelined/design.v:60$31.
  creating $alu model for $eq$/foss/designs/ascon_pipelined/design.v:61$34 ($eq): merged with
$lt$/foss/designs/ascon_pipelined/design.v:60$33.
  creating $alu model for $eq$/foss/designs/ascon_pipelined/design.v:61$36 ($eq): merged with
$lt$/foss/designs/ascon_pipelined/design.v:60$35.
  creating $alu model for $eq$/foss/designs/ascon_pipelined/design.v:61$38 ($eq): merged with
$lt$/foss/designs/ascon_pipelined/design.v:60$37.
  creating $alu model for $eq$/foss/designs/ascon_pipelined/design.v:85$102 ($eq): merged with
$lt$/foss/designs/ascon_pipelined/design.v:83$99.
  creating $alu model for $eq$/foss/designs/ascon_pipelined/design.v:85$109 ($eq): merged with
$lt$/foss/designs/ascon_pipelined/design.v:83$106.
  creating $alu model for $eq$/foss/designs/ascon_pipelined/design.v:85$116 ($eq): merged with
$lt$/foss/designs/ascon_pipelined/design.v:83$113.
  creating $alu model for $eq$/foss/designs/ascon_pipelined/design.v:85$123 ($eq): merged with
$lt$/foss/designs/ascon_pipelined/design.v:83$120.
  creating $alu model for $eq$/foss/designs/ascon_pipelined/design.v:85$130 ($eq): merged with
$lt$/foss/designs/ascon_pipelined/design.v:83$127.
  creating $alu model for $eq$/foss/designs/ascon_pipelined/design.v:85$137 ($eq): merged with
$lt$/foss/designs/ascon_pipelined/design.v:83$134.
  creating $alu model for $eq$/foss/designs/ascon_pipelined/design.v:85$144 ($eq): merged with
$lt$/foss/designs/ascon_pipelined/design.v:83$141.
  creating $alu model for $eq$/foss/designs/ascon_pipelined/design.v:85$151 ($eq): merged with
$lt$/foss/designs/ascon_pipelined/design.v:83$148.
  creating $alu model for $eq$/foss/designs/ascon_pipelined/design.v:85$158 ($eq): merged with
$lt$/foss/designs/ascon_pipelined/design.v:83$155.
  creating $alu model for $eq$/foss/designs/ascon_pipelined/design.v:85$60 ($eq): merged with
$lt$/foss/designs/ascon_pipelined/design.v:83$57.
  creating $alu model for $eq$/foss/designs/ascon_pipelined/design.v:85$67 ($eq): merged with
$lt$/foss/designs/ascon_pipelined/design.v:83$64.
  creating $alu model for $eq$/foss/designs/ascon_pipelined/design.v:85$74 ($eq): merged with
$lt$/foss/designs/ascon_pipelined/design.v:83$71.
  creating $alu model for $eq$/foss/designs/ascon_pipelined/design.v:85$81 ($eq): merged with
$lt$/foss/designs/ascon_pipelined/design.v:83$78.
  creating $alu model for $eq$/foss/designs/ascon_pipelined/design.v:85$88 ($eq): merged with
$lt$/foss/designs/ascon_pipelined/design.v:83$85.
  creating $alu model for $eq$/foss/designs/ascon_pipelined/design.v:85$95 ($eq): merged with
$lt$/foss/designs/ascon_pipelined/design.v:83$92.
  creating $alu cell for $lt$/foss/designs/ascon_pipelined/design.v:83$99,
$eq$/foss/designs/ascon_pipelined/design.v:85$102: $auto$alumacc.cc:512:replace_alu$1754
  creating $alu cell for $lt$/foss/designs/ascon_pipelined/design.v:83$92,
$eq$/foss/designs/ascon_pipelined/design.v:85$95: $auto$alumacc.cc:512:replace_alu$1761
  creating $alu cell for $lt$/foss/designs/ascon_pipelined/design.v:83$85,
$eq$/foss/designs/ascon_pipelined/design.v:85$88: $auto$alumacc.cc:512:replace_alu$1768
  creating $alu cell for $lt$/foss/designs/ascon_pipelined/design.v:83$78,
$eq$/foss/designs/ascon_pipelined/design.v:85$81: $auto$alumacc.cc:512:replace_alu$1775
  creating $alu cell for $lt$/foss/designs/ascon_pipelined/design.v:83$71,
$eq$/foss/designs/ascon_pipelined/design.v:85$74: $auto$alumacc.cc:512:replace_alu$1782
  creating $alu cell for $lt$/foss/designs/ascon_pipelined/design.v:83$64,
$eq$/foss/designs/ascon_pipelined/design.v:85$67: $auto$alumacc.cc:512:replace_alu$1789
  creating $alu cell for $lt$/foss/designs/ascon_pipelined/design.v:83$57,
$eq$/foss/designs/ascon_pipelined/design.v:85$60: $auto$alumacc.cc:512:replace_alu$1796
  creating $alu cell for $lt$/foss/designs/ascon_pipelined/design.v:83$50: $auto$alumacc.cc:512:replace_alu$1803
  creating $alu cell for $lt$/foss/designs/ascon_pipelined/design.v:83$155,
$eq$/foss/designs/ascon_pipelined/design.v:85$158: $auto$alumacc.cc:512:replace_alu$1808
  creating $alu cell for $lt$/foss/designs/ascon_pipelined/design.v:83$148,
$eq$/foss/designs/ascon_pipelined/design.v:85$151: $auto$alumacc.cc:512:replace_alu$1815
  creating $alu cell for $lt$/foss/designs/ascon_pipelined/design.v:83$141,
$eq$/foss/designs/ascon_pipelined/design.v:85$144: $auto$alumacc.cc:512:replace_alu$1822
  creating $alu cell for $lt$/foss/designs/ascon_pipelined/design.v:83$134,
$eq$/foss/designs/ascon_pipelined/design.v:85$137: $auto$alumacc.cc:512:replace_alu$1829
  creating $alu cell for $lt$/foss/designs/ascon_pipelined/design.v:83$127,
$eq$/foss/designs/ascon_pipelined/design.v:85$130: $auto$alumacc.cc:512:replace_alu$1836
  creating $alu cell for $lt$/foss/designs/ascon_pipelined/design.v:83$120,
$eq$/foss/designs/ascon_pipelined/design.v:85$123: $auto$alumacc.cc:512:replace_alu$1843
  creating $alu cell for $lt$/foss/designs/ascon_pipelined/design.v:83$113,
$eq$/foss/designs/ascon_pipelined/design.v:85$116: $auto$alumacc.cc:512:replace_alu$1850
  creating $alu cell for $lt$/foss/designs/ascon_pipelined/design.v:83$106,
$eq$/foss/designs/ascon_pipelined/design.v:85$109: $auto$alumacc.cc:512:replace_alu$1857
  creating $alu cell for $lt$/foss/designs/ascon_pipelined/design.v:60$9,
$eq$/foss/designs/ascon_pipelined/design.v:61$10: $auto$alumacc.cc:512:replace_alu$1864
  creating $alu cell for $lt$/foss/designs/ascon_pipelined/design.v:60$7: $auto$alumacc.cc:512:replace_alu$1871
  creating $alu cell for $lt$/foss/designs/ascon_pipelined/design.v:60$37,
$eq$/foss/designs/ascon_pipelined/design.v:61$38: $auto$alumacc.cc:512:replace_alu$1876
  creating $alu cell for $lt$/foss/designs/ascon_pipelined/design.v:60$35,
$eq$/foss/designs/ascon_pipelined/design.v:61$36: $auto$alumacc.cc:512:replace_alu$1883
  creating $alu cell for $lt$/foss/designs/ascon_pipelined/design.v:60$33,
$eq$/foss/designs/ascon_pipelined/design.v:61$34: $auto$alumacc.cc:512:replace_alu$1890
  creating $alu cell for $lt$/foss/designs/ascon_pipelined/design.v:60$31,
$eq$/foss/designs/ascon_pipelined/design.v:61$32: $auto$alumacc.cc:512:replace_alu$1897
  creating $alu cell for $lt$/foss/designs/ascon_pipelined/design.v:60$29,
$eq$/foss/designs/ascon_pipelined/design.v:61$30: $auto$alumacc.cc:512:replace_alu$1904
  creating $alu cell for $lt$/foss/designs/ascon_pipelined/design.v:60$27,
$eq$/foss/designs/ascon_pipelined/design.v:61$28: $auto$alumacc.cc:512:replace_alu$1911
  creating $alu cell for $lt$/foss/designs/ascon_pipelined/design.v:60$25,
$eq$/foss/designs/ascon_pipelined/design.v:61$26: $auto$alumacc.cc:512:replace_alu$1918
  creating $alu cell for $lt$/foss/designs/ascon_pipelined/design.v:60$23,
$eq$/foss/designs/ascon_pipelined/design.v:61$24: $auto$alumacc.cc:512:replace_alu$1925
  creating $alu cell for $lt$/foss/designs/ascon_pipelined/design.v:60$21,
$eq$/foss/designs/ascon_pipelined/design.v:61$22: $auto$alumacc.cc:512:replace_alu$1932
  creating $alu cell for $lt$/foss/designs/ascon_pipelined/design.v:60$19,
$eq$/foss/designs/ascon_pipelined/design.v:61$20: $auto$alumacc.cc:512:replace_alu$1939
  creating $alu cell for $lt$/foss/designs/ascon_pipelined/design.v:60$17,
$eq$/foss/designs/ascon_pipelined/design.v:61$18: $auto$alumacc.cc:512:replace_alu$1946
  creating $alu cell for $lt$/foss/designs/ascon_pipelined/design.v:60$15,
$eq$/foss/designs/ascon_pipelined/design.v:61$16: $auto$alumacc.cc:512:replace_alu$1953
  creating $alu cell for $lt$/foss/designs/ascon_pipelined/design.v:60$13,
$eq$/foss/designs/ascon_pipelined/design.v:61$14: $auto$alumacc.cc:512:replace_alu$1960
  creating $alu cell for $lt$/foss/designs/ascon_pipelined/design.v:60$11,
$eq$/foss/designs/ascon_pipelined/design.v:61$12: $auto$alumacc.cc:512:replace_alu$1967
  creating $alu cell for $add$/foss/designs/ascon_pipelined/design.v:127$164: $auto$alumacc.cc:512:replace_alu$1974
  created 33 $alu and 0 $macc cells.

65. Executing SHARE pass (SAT-based resource sharing).

66. Executing OPT_EXPR pass (perform const folding).
Optimizing module ascon_core_adpt_encdec.
<suppressed ~48 debug messages>

67. Executing OPT_MERGE pass (detect identical cells).
Finding identical cells in module `\ascon_core_adpt_encdec'.
Computing hashes of 506 cells of `\ascon_core_adpt_encdec'.
Finding duplicate cells in `\ascon_core_adpt_encdec'.
Removed a total of 0 cells.

68. Executing OPT_MUXTREE pass (detect dead branches in mux trees).
Running muxtree optimizer on module \ascon_core_adpt_encdec..
  Creating internal representation of mux trees.
  Evaluating internal representation of mux trees.
  Analyzing evaluation results.
Removed 0 multiplexer ports.
<suppressed ~178 debug messages>

69. Executing OPT_REDUCE pass (consolidate $*mux and $reduce_* inputs).
  Optimizing cells in module \ascon_core_adpt_encdec.
Performed a total of 0 changes.

70. Executing OPT_MERGE pass (detect identical cells).
Finding identical cells in module `\ascon_core_adpt_encdec'.
Computing hashes of 506 cells of `\ascon_core_adpt_encdec'.
Finding duplicate cells in `\ascon_core_adpt_encdec'.
Removed a total of 0 cells.

71. Executing OPT_DFF pass (perform DFF optimizations).

72. Executing OPT_CLEAN pass (remove unused cells and wires).
Finding unused cells or wires in module \ascon_core_adpt_encdec..
Removed 16 unused cells and 78 unused wires.
<suppressed ~17 debug messages>

73. Executing OPT_EXPR pass (perform const folding).
Optimizing module ascon_core_adpt_encdec.

74. Rerunning OPT passes. (Maybe there is more to do…)

75. Executing OPT_MUXTREE pass (detect dead branches in mux trees).
Running muxtree optimizer on module \ascon_core_adpt_encdec..
  Creating internal representation of mux trees.
  Evaluating internal representation of mux trees.
  Analyzing evaluation results.
Removed 0 multiplexer ports.
<suppressed ~178 debug messages>

76. Executing OPT_REDUCE pass (consolidate $*mux and $reduce_* inputs).
  Optimizing cells in module \ascon_core_adpt_encdec.
Performed a total of 0 changes.

77. Executing OPT_MERGE pass (detect identical cells).
Finding identical cells in module `\ascon_core_adpt_encdec'.
Computing hashes of 490 cells of `\ascon_core_adpt_encdec'.
Finding duplicate cells in `\ascon_core_adpt_encdec'.
Removed a total of 0 cells.

78. Executing OPT_DFF pass (perform DFF optimizations).

79. Executing OPT_CLEAN pass (remove unused cells and wires).
Finding unused cells or wires in module \ascon_core_adpt_encdec..

80. Executing OPT_EXPR pass (perform const folding).
Optimizing module ascon_core_adpt_encdec.

81. Executing MEMORY pass.

81.1. Executing OPT_MEM pass (optimize memories).
Performed a total of 0 transformations.

81.2. Executing OPT_MEM_PRIORITY pass (removing unnecessary memory write priority relations).
Performed a total of 0 transformations.

81.3. Executing OPT_MEM_FEEDBACK pass (finding memory read-to-write feedback paths).

81.4. Executing MEMORY_BMUX2ROM pass (converting muxes to ROMs).

81.5. Executing MEMORY_DFF pass (merging $dff cells to $memrd).
Checking read port `$auto$proc_rom.cc:155:do_switch$245'[0] in module `\ascon_core_adpt_encdec': no output FF found.
Checking read port address `$auto$proc_rom.cc:155:do_switch$245'[0] in module `\ascon_core_adpt_encdec': address FF has
async set and/or reset, not supported.

81.6. Executing OPT_CLEAN pass (remove unused cells and wires).
Finding unused cells or wires in module \ascon_core_adpt_encdec..

81.7. Executing MEMORY_SHARE pass (consolidating $memrd/$memwr cells).

81.8. Executing OPT_MEM_WIDEN pass (optimize memories where all ports are wide).
Performed a total of 0 transformations.

81.9. Executing OPT_CLEAN pass (remove unused cells and wires).
Finding unused cells or wires in module \ascon_core_adpt_encdec..

81.10. Executing MEMORY_COLLECT pass (generating $mem cells).

82. Executing OPT_CLEAN pass (remove unused cells and wires).
Finding unused cells or wires in module \ascon_core_adpt_encdec..

83. Executing OPT_EXPR pass (perform const folding).
Optimizing module ascon_core_adpt_encdec.
<suppressed ~101 debug messages>

84. Executing OPT_MERGE pass (detect identical cells).
Finding identical cells in module `\ascon_core_adpt_encdec'.
Computing hashes of 446 cells of `\ascon_core_adpt_encdec'.
Finding duplicate cells in `\ascon_core_adpt_encdec'.
Computing hashes of 423 cells of `\ascon_core_adpt_encdec'.
Finding duplicate cells in `\ascon_core_adpt_encdec'.
<suppressed ~69 debug messages>
Removed a total of 23 cells.

85. Executing OPT_DFF pass (perform DFF optimizations).

86. Executing OPT_CLEAN pass (remove unused cells and wires).
Finding unused cells or wires in module \ascon_core_adpt_encdec..
Removed 8 unused cells and 104 unused wires.
<suppressed ~9 debug messages>

87. Executing MEMORY_MAP pass (converting memories to logic and flip-flops).
Mapping memory $auto$proc_rom.cc:155:do_switch$245 in module \ascon_core_adpt_encdec:
  created 16 $dff cells and 0 static cells of width 8.
  read interface: 0 $dff and 15 $mux cells.
  write interface: 0 write mux blocks.

88. Executing OPT_EXPR pass (perform const folding).
Optimizing module ascon_core_adpt_encdec.
<suppressed ~3 debug messages>

89. Executing OPT_MERGE pass (detect identical cells).
Finding identical cells in module `\ascon_core_adpt_encdec'.
Computing hashes of 426 cells of `\ascon_core_adpt_encdec'.
Finding duplicate cells in `\ascon_core_adpt_encdec'.
Removed a total of 0 cells.

90. Executing OPT_MUXTREE pass (detect dead branches in mux trees).
Running muxtree optimizer on module \ascon_core_adpt_encdec..
  Creating internal representation of mux trees.
  Evaluating internal representation of mux trees.
  Analyzing evaluation results.
Removed 0 multiplexer ports.
<suppressed ~114 debug messages>

91. Executing OPT_REDUCE pass (consolidate $*mux and $reduce_* inputs).
  Optimizing cells in module \ascon_core_adpt_encdec.
    Consolidated identical input bits for $mux cell $memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][3][3]$2069:
      Old ports: A=8'11010010, B=8'11000011, Y=$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][1]$b$2053
      New ports: A=2'10, B=2'01, Y={ $memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][1]$b$2053 [4]
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][1]$b$2053 [0] }
      New connections: { $memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][1]$b$2053 [7:5]
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][1]$b$2053 [3:1] } = 6'110001
    Consolidated identical input bits for $mux cell $memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][3][2]$2066:
      Old ports: A=8'11110000, B=8'11100001, Y=$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][1]$a$2052
      New ports: A=2'10, B=2'01, Y={ $memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][1]$a$2052 [4]
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][1]$a$2052 [0] }
      New connections: { $memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][1]$a$2052 [7:5]
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][1]$a$2052 [3:1] } = 6'111000
    Consolidated identical input bits for $mux cell $memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][3][6]$2078:
      Old ports: A=8'01111000, B=8'01101001, Y=$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][3]$a$2058
      New ports: A=2'10, B=2'01, Y={ $memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][3]$a$2058 [4]
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][3]$a$2058 [0] }
      New connections: { $memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][3]$a$2058 [7:5]
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][3]$a$2058 [3:1] } = 6'011100
    Consolidated identical input bits for $mux cell $memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][3][5]$2075:
      Old ports: A=8'10010110, B=8'10000111, Y=$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][2]$b$2056
      New ports: A=2'10, B=2'01, Y={ $memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][2]$b$2056 [4]
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][2]$b$2056 [0] }
      New connections: { $memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][2]$b$2056 [7:5]
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][2]$b$2056 [3:1] } = 6'100011
    Consolidated identical input bits for $mux cell $memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][3][4]$2072:
      Old ports: A=8'10110100, B=8'10100101, Y=$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][2]$a$2055
      New ports: A=2'10, B=2'01, Y={ $memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][2]$a$2055 [4]
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][2]$a$2055 [0] }
      New connections: { $memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][2]$a$2055 [7:5]
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][2]$a$2055 [3:1] } = 6'101010
    Consolidated identical input bits for $mux cell $memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][3][7]$2081:
      Old ports: A=8'01011010, B=8'01001011, Y=$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][3]$b$2059
      New ports: A=2'10, B=2'01, Y={ $memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][3]$b$2059 [4]
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][3]$b$2059 [0] }
      New connections: { $memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][3]$b$2059 [7:5]
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][3]$b$2059 [3:1] } = 6'010101
    New ctrl vector for $pmux cell $procmux$257: $procmux$274_CMP
    New ctrl vector for $pmux cell $procmux$290: { $procmux$274_CMP $auto$opt_reduce.cc:137:opt_pmux$2085 }
    New ctrl vector for $pmux cell $procmux$332: { $procmux$274_CMP $procmux$348_CMP \ad_ready $procmux$341_CMP
\din_ready $0\done[0:0] }
    Consolidated identical input bits for $mux cell $procmux$336:
      Old ports: A=3'001, B=3'110, Y=$procmux$336_Y
      New ports: A=2'01, B=2'10, Y=$procmux$336_Y [1:0]
      New connections: $procmux$336_Y [2] = $procmux$336_Y [1]
    Consolidated identical input bits for $mux cell $procmux$345:
      Old ports: A=3'001, B=3'100, Y=$procmux$345_Y
      New ports: A=2'01, B=2'10, Y={ $procmux$345_Y [2] $procmux$345_Y [0] }
      New connections: $procmux$345_Y [1] = 1'0
    Consolidated identical input bits for $mux cell $ternary$/foss/designs/ascon_pipelined/design.v:135$169:
      Old ports: A=3'011, B=3'100, Y=$procmux$323_Y
      New ports: A=2'01, B=2'10, Y={ $procmux$323_Y [2] $procmux$323_Y [0] }
      New connections: $procmux$323_Y [1] = $procmux$323_Y [0]
  Optimizing cells in module \ascon_core_adpt_encdec.
    Consolidated identical input bits for $mux cell $memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][3]$2057:
      Old ports: A=$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][3]$a$2058,
B=$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][3]$b$2059,
Y=$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][1][1]$b$2047
      New ports: A={ 1'1 $memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][3]$a$2058 [4] 1'0
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][3]$a$2058 [0] }, B={ 1'0
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][3]$b$2059 [4] 1'1
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][3]$b$2059 [0] }, Y={
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][1][1]$b$2047 [5:4]
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][1][1]$b$2047 [1:0] }
      New connections: { $memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][1][1]$b$2047 [7:6]
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][1][1]$b$2047 [3:2] } = 4'0110
    Consolidated identical input bits for $mux cell $memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][2]$2054:
      Old ports: A=$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][2]$a$2055,
B=$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][2]$b$2056,
Y=$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][1][1]$a$2046
      New ports: A={ 1'1 $memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][2]$a$2055 [4] 1'0
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][2]$a$2055 [0] }, B={ 1'0
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][2]$b$2056 [4] 1'1
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][2]$b$2056 [0] }, Y={
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][1][1]$a$2046 [5:4]
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][1][1]$a$2046 [1:0] }
      New connections: { $memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][1][1]$a$2046 [7:6]
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][1][1]$a$2046 [3:2] } = 4'1001
    Consolidated identical input bits for $mux cell $memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][1]$2051:
      Old ports: A=$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][1]$a$2052,
B=$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][1]$b$2053,
Y=$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][1][0]$b$2044
      New ports: A={ 1'1 $memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][1]$a$2052 [4] 1'0
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][1]$a$2052 [0] }, B={ 1'0
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][1]$b$2053 [4] 1'1
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][1]$b$2053 [0] }, Y={
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][1][0]$b$2044 [5:4]
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][1][0]$b$2044 [1:0] }
      New connections: { $memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][1][0]$b$2044 [7:6]
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][1][0]$b$2044 [3:2] } = 4'1100
  Optimizing cells in module \ascon_core_adpt_encdec.
    Consolidated identical input bits for $mux cell $memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][1][1]$2045:
      Old ports: A=$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][1][1]$a$2046,
B=$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][1][1]$b$2047,
Y=$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][0][0]$b$2041
      New ports: A={ $memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][1][1]$a$2046 [5:4] 2'01
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][1][1]$a$2046 [1:0] }, B={
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][1][1]$b$2047 [5:4] 2'10
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][1][1]$b$2047 [1:0] },
Y=$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][0][0]$b$2041 [5:0]
      New connections: $memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][0][0]$b$2041 [7:6] = {
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][0][0]$b$2041 [2]
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][0][0]$b$2041 [3] }
    Consolidated identical input bits for $mux cell $memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][1][0]$2042:
      Old ports: A=8'00000000, B=$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][1][0]$b$2044,
Y=$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][0][0]$a$2040
      New ports: A=5'00000, B={ 1'1 $memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][1][0]$b$2044 [5:4]
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][1][0]$b$2044 [1:0] }, Y={
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][0][0]$a$2040 [6:4]
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][0][0]$a$2040 [1:0] }
      New connections: { $memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][0][0]$a$2040 [7]
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][0][0]$a$2040 [3:2] } = {
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][0][0]$a$2040 [6] 2'00 }
  Optimizing cells in module \ascon_core_adpt_encdec.
Performed a total of 17 changes.

92. Executing OPT_MERGE pass (detect identical cells).
Finding identical cells in module `\ascon_core_adpt_encdec'.
Computing hashes of 427 cells of `\ascon_core_adpt_encdec'.
Finding duplicate cells in `\ascon_core_adpt_encdec'.
Computing hashes of 422 cells of `\ascon_core_adpt_encdec'.
Finding duplicate cells in `\ascon_core_adpt_encdec'.
Computing hashes of 420 cells of `\ascon_core_adpt_encdec'.
Finding duplicate cells in `\ascon_core_adpt_encdec'.
<suppressed ~21 debug messages>
Removed a total of 7 cells.

93. Executing OPT_SHARE pass.

94. Executing OPT_DFF pass (perform DFF optimizations).

95. Executing OPT_CLEAN pass (remove unused cells and wires).
Finding unused cells or wires in module \ascon_core_adpt_encdec..
Removed 0 unused cells and 26 unused wires.
<suppressed ~1 debug messages>

96. Executing OPT_EXPR pass (perform const folding).
Optimizing module ascon_core_adpt_encdec.
<suppressed ~1 debug messages>

97. Rerunning OPT passes. (Maybe there is more to do…)

98. Executing OPT_MUXTREE pass (detect dead branches in mux trees).
Running muxtree optimizer on module \ascon_core_adpt_encdec..
  Creating internal representation of mux trees.
  Evaluating internal representation of mux trees.
  Analyzing evaluation results.
Removed 0 multiplexer ports.
<suppressed ~116 debug messages>

99. Executing OPT_REDUCE pass (consolidate $*mux and $reduce_* inputs).
  Optimizing cells in module \ascon_core_adpt_encdec.
    Consolidated identical input bits for $mux cell $memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][3]$2057:
      Old ports: A={ 1'1 $memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][1]$a$2052 [4] 1'0
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][1]$a$2052 [0] }, B={ 1'0
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][1]$a$2052 [4] 1'1
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][1]$a$2052 [0] }, Y={
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][1][0]$b$2044 [5:4]
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][1][0]$b$2044 [1:0] }
      New ports: A=2'10, B=2'01, Y={ $memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][1][0]$b$2044 [5]
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][1][0]$b$2044 [1] }
      New connections: { $memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][1][0]$b$2044 [4]
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][1][0]$b$2044 [0] } = {
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][1]$a$2052 [4]
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][2][1]$a$2052 [0] }
    Consolidated identical input bits for $mux cell $memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][1][1]$2045:
      Old ports: A={ $memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][1][0]$b$2044 [5:4] 2'01
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][1][0]$b$2044 [1:0] }, B={
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][1][0]$b$2044 [5:4] 2'10
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][1][0]$b$2044 [1:0] },
Y=$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][0][0]$b$2041 [5:0]
      New ports: A=2'01, B=2'10, Y=$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][0][0]$b$2041 [3:2]
      New connections: { $memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][0][0]$b$2041 [5:4]
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][0][0]$b$2041 [1:0] } = {
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][1][0]$b$2044 [5:4]
$memory$auto$proc_rom.cc:155:do_switch$245$rdmux[0][1][0]$b$2044 [1:0] }
  Optimizing cells in module \ascon_core_adpt_encdec.
Performed a total of 2 changes.

100. Executing OPT_MERGE pass (detect identical cells).
Finding identical cells in module `\ascon_core_adpt_encdec'.
Computing hashes of 420 cells of `\ascon_core_adpt_encdec'.
Finding duplicate cells in `\ascon_core_adpt_encdec'.
Removed a total of 0 cells.

101. Executing OPT_SHARE pass.

102. Executing OPT_DFF pass (perform DFF optimizations).

103. Executing OPT_CLEAN pass (remove unused cells and wires).
Finding unused cells or wires in module \ascon_core_adpt_encdec..
Removed 0 unused cells and 2 unused wires.
<suppressed ~1 debug messages>

104. Executing OPT_EXPR pass (perform const folding).
Optimizing module ascon_core_adpt_encdec.

105. Rerunning OPT passes. (Maybe there is more to do…)

106. Executing OPT_MUXTREE pass (detect dead branches in mux trees).
Running muxtree optimizer on module \ascon_core_adpt_encdec..
  Creating internal representation of mux trees.
  Evaluating internal representation of mux trees.
  Analyzing evaluation results.
Removed 0 multiplexer ports.
<suppressed ~111 debug messages>

107. Executing OPT_REDUCE pass (consolidate $*mux and $reduce_* inputs).
  Optimizing cells in module \ascon_core_adpt_encdec.
Performed a total of 0 changes.

108. Executing OPT_MERGE pass (detect identical cells).
Finding identical cells in module `\ascon_core_adpt_encdec'.
Computing hashes of 420 cells of `\ascon_core_adpt_encdec'.
Finding duplicate cells in `\ascon_core_adpt_encdec'.
Removed a total of 0 cells.

109. Executing OPT_SHARE pass.

110. Executing OPT_DFF pass (perform DFF optimizations).

111. Executing OPT_CLEAN pass (remove unused cells and wires).
Finding unused cells or wires in module \ascon_core_adpt_encdec..

112. Executing OPT_EXPR pass (perform const folding).
Optimizing module ascon_core_adpt_encdec.

113. Executing TECHMAP pass (map to technology primitives).

113.1. Executing Verilog-2005 frontend: /foss/tools/yosys/bin/../share/yosys/techmap.v
Parsing Verilog input from `/foss/tools/yosys/bin/../share/yosys/techmap.v' to AST representation.
Generating RTLIL representation for module `\_90_simplemap_bool_ops'.
Generating RTLIL representation for module `\_90_simplemap_reduce_ops'.
Generating RTLIL representation for module `\_90_simplemap_logic_ops'.
Generating RTLIL representation for module `\_90_simplemap_compare_ops'.
Generating RTLIL representation for module `\_90_simplemap_various'.
Generating RTLIL representation for module `\_90_simplemap_registers'.
Generating RTLIL representation for module `\_90_shift_ops_shr_shl_sshl_sshr'.
Generating RTLIL representation for module `\_90_shift_shiftx'.
Generating RTLIL representation for module `\_90_fa'.
Generating RTLIL representation for module `\_90_lcu_brent_kung'.
Generating RTLIL representation for module `\_90_alu'.
Generating RTLIL representation for module `\_90_macc'.
Generating RTLIL representation for module `\_90_alumacc'.
Generating RTLIL representation for module `$__div_mod_u'.
Generating RTLIL representation for module `$__div_mod_trunc'.
Generating RTLIL representation for module `\_90_div'.
Generating RTLIL representation for module `\_90_mod'.
Generating RTLIL representation for module `$__div_mod_floor'.
Generating RTLIL representation for module `\_90_divfloor'.
Generating RTLIL representation for module `\_90_modfloor'.
Generating RTLIL representation for module `\_90_pow'.
Generating RTLIL representation for module `\_90_pmux'.
Generating RTLIL representation for module `\_90_demux'.
Generating RTLIL representation for module `\_90_lut'.
Generating RTLIL representation for module `$connect'.
Generating RTLIL representation for module `$input_port'.
Successfully finished Verilog frontend.

113.2. Continuing TECHMAP pass.
Using extmapper simplemap for cells of type $reduce_or.
Using template $paramod$32a7b7b86c07519b7537abc18e96f0331f97914d\_90_alu for cells of type $alu.
Using extmapper simplemap for cells of type $reduce_and.
Using template $paramod$3ac6e4268d0279df14823f25676acf685165517e\_90_alu for cells of type $alu.
Using template $paramod$7af24cf7f572852703f08ef7a936c59efa2c57af\_90_alu for cells of type $alu.
Using template $paramod$03eba0cdd46566f6651a3011e0b5671fa6b5e494\_90_alu for cells of type $alu.
Using template $paramod$f85408ed1aa3d09e465edae8a7bf590332ae9f7b\_90_alu for cells of type $alu.
Using template $paramod$d1615bf4e5e328245ffd1550e5fe105901cda77b\_90_alu for cells of type $alu.
Using template $paramod$83dd457849c736323edf2edb15923eb27f99c683\_90_alu for cells of type $alu.
Using template $paramod$1a3a0c35c4a4896fbfd612699525c057298e72d2\_90_alu for cells of type $alu.
Using template $paramod$79fc7abbb3333dbd5736999d565fd903198fb1eb\_90_alu for cells of type $alu.
Using template $paramod$adbaf76fa5a3091a329503792521395f8ff4d1a4\_90_alu for cells of type $alu.
Using template $paramod$672a140277c71df8314410f22acc08d55222c3c7\_90_alu for cells of type $alu.
Using template $paramod$6b90a16b6f3b57b9c9d958838204f952a01dc262\_90_alu for cells of type $alu.
Using extmapper simplemap for cells of type $not.
Using extmapper simplemap for cells of type $adffe.
Using extmapper simplemap for cells of type $ne.
Using extmapper simplemap for cells of type $reduce_bool.
Using extmapper simplemap for cells of type $logic_not.
Using extmapper simplemap for cells of type $mux.
Using extmapper simplemap for cells of type $xor.
Using extmapper simplemap for cells of type $eq.
Using extmapper simplemap for cells of type $logic_and.
Using extmapper simplemap for cells of type $and.
Using template $paramod$bf2533632d512eac76dd186c0da49367e29b8e98\_90_pmux for cells of type $pmux.
Using template $paramod$85df5dc01c7df96a7d8e5f1fdf76ce9ac452af63\_90_pmux for cells of type $pmux.
Using template $paramod$57f63e8a3282e053be0430389b09fa050ac7dca0\_90_pmux for cells of type $pmux.
Using template $paramod$b76f0c7d813c9b9e201e1c450cfd00106058a636\_90_pmux for cells of type $pmux.
Using template $paramod$54a4503cc57b9df40b70c1899504d6aac2650719\_90_pmux for cells of type $pmux.
Using extmapper simplemap for cells of type $adff.
Using extmapper simplemap for cells of type $or.
Using extmapper simplemap for cells of type $pos.
Using template $paramod\_90_fa\WIDTH=32'00000000000000000000000000000010 for cells of type $fa.
Using template $paramod\_90_lcu_brent_kung\WIDTH=32'00000000000000000000000000000010 for cells of type $lcu.
Using template $paramod\_90_fa\WIDTH=32'00000000000000000000000000000101 for cells of type $fa.
Using template $paramod\_90_lcu_brent_kung\WIDTH=32'00000000000000000000000000000101 for cells of type $lcu.
Using template $paramod\_90_fa\WIDTH=32'00000000000000000000000000000100 for cells of type $fa.
Using template $paramod\_90_lcu_brent_kung\WIDTH=32'00000000000000000000000000000100 for cells of type $lcu.
Using template $paramod\_90_fa\WIDTH=32'00000000000000000000000000000011 for cells of type $fa.
Using template $paramod\_90_lcu_brent_kung\WIDTH=32'00000000000000000000000000000011 for cells of type $lcu.
Using template $paramod\_90_fa\WIDTH=32'00000000000000000000000000000001 for cells of type $fa.
Using template $paramod\_90_lcu_brent_kung\WIDTH=32'00000000000000000000000000000001 for cells of type $lcu.
No more expansions possible.
<suppressed ~2503 debug messages>

114. Executing OPT_EXPR pass (perform const folding).
Optimizing module ascon_core_adpt_encdec.
<suppressed ~2124 debug messages>

115. Executing OPT_MERGE pass (detect identical cells).
Finding identical cells in module `\ascon_core_adpt_encdec'.
Computing hashes of 7650 cells of `\ascon_core_adpt_encdec'.
Finding duplicate cells in `\ascon_core_adpt_encdec'.
Computing hashes of 7204 cells of `\ascon_core_adpt_encdec'.
Finding duplicate cells in `\ascon_core_adpt_encdec'.
Computing hashes of 6933 cells of `\ascon_core_adpt_encdec'.
Finding duplicate cells in `\ascon_core_adpt_encdec'.
Computing hashes of 6913 cells of `\ascon_core_adpt_encdec'.
Finding duplicate cells in `\ascon_core_adpt_encdec'.
Computing hashes of 6903 cells of `\ascon_core_adpt_encdec'.
Finding duplicate cells in `\ascon_core_adpt_encdec'.
Computing hashes of 6901 cells of `\ascon_core_adpt_encdec'.
Finding duplicate cells in `\ascon_core_adpt_encdec'.
<suppressed ~2247 debug messages>
Removed a total of 749 cells.

116. Executing OPT_DFF pass (perform DFF optimizations).

117. Executing OPT_CLEAN pass (remove unused cells and wires).
Finding unused cells or wires in module \ascon_core_adpt_encdec..
Removed 100 unused cells and 3110 unused wires.
<suppressed ~101 debug messages>

118. Executing OPT_EXPR pass (perform const folding).
Optimizing module ascon_core_adpt_encdec.

119. Executing OPT_MERGE pass (detect identical cells).
Finding identical cells in module `\ascon_core_adpt_encdec'.
Computing hashes of 6801 cells of `\ascon_core_adpt_encdec'.
Finding duplicate cells in `\ascon_core_adpt_encdec'.
Removed a total of 0 cells.

120. Executing OPT_DFF pass (perform DFF optimizations).

121. Executing OPT_CLEAN pass (remove unused cells and wires).
Finding unused cells or wires in module \ascon_core_adpt_encdec..

122. Executing ABC pass (technology mapping using ABC).

122.1. Extracting gate netlist of module `\ascon_core_adpt_encdec' to `<abc-temp-dir>/input.blif'..
Replacing 112 occurrences of constant undef bits with constant zero bits

122.1.1. Executed ABC.
Extracted 5882 gates and 7193 wires to a netlist network with 1308 inputs and 959 outputs.
Running ABC script: <abc-temp-dir>/abc.script
ABC: UC Berkeley, ABC 1.01 (compiled Apr 16 2026 21:01:18)
ABC: abc 01> empty
ABC: abc 01> source <abc-temp-dir>/abc.script
ABC: + read_blif <abc-temp-dir>/input.blif
ABC: + read_library <abc-temp-dir>/stdcells.genlib
ABC: + strash
ABC: + dretime
ABC: + map
ABC: + write_blif <abc-temp-dir>/output.blif
ABC:
ABC: YOSYS_ABC_DONE

122.1.2. Re-integrating ABC results.
ABC RESULTS:               AND cells:       97
ABC RESULTS:            ANDNOT cells:     1419
ABC RESULTS:               MUX cells:      938
ABC RESULTS:              NAND cells:       12
ABC RESULTS:               NOR cells:       25
ABC RESULTS:               NOT cells:      527
ABC RESULTS:                OR cells:      777
ABC RESULTS:             ORNOT cells:      154
ABC RESULTS:              XNOR cells:      957
ABC RESULTS:               XOR cells:      911
ABC RESULTS:        internal signals:     4926
ABC RESULTS:           input signals:     1308
ABC RESULTS:          output signals:      959
Removing temp directory.
Removing global temp directory.

123. Executing OPT pass (performing simple optimizations).

123.1. Executing OPT_EXPR pass (perform const folding).
Optimizing module ascon_core_adpt_encdec.
<suppressed ~388 debug messages>

123.2. Executing OPT_MERGE pass (detect identical cells).
Finding identical cells in module `\ascon_core_adpt_encdec'.
Computing hashes of 6736 cells of `\ascon_core_adpt_encdec'.
Finding duplicate cells in `\ascon_core_adpt_encdec'.
Computing hashes of 6733 cells of `\ascon_core_adpt_encdec'.
Finding duplicate cells in `\ascon_core_adpt_encdec'.
<suppressed ~9 debug messages>
Removed a total of 3 cells.

123.3. Executing OPT_DFF pass (perform DFF optimizations).

123.4. Executing OPT_CLEAN pass (remove unused cells and wires).
Finding unused cells or wires in module \ascon_core_adpt_encdec..
Removed 0 unused cells and 2760 unused wires.
<suppressed ~31 debug messages>

123.5. Finished fast OPT passes.

124. Executing HIERARCHY pass (managing design hierarchy).

124.1. Analyzing design hierarchy..
Top module:  \ascon_core_adpt_encdec

124.2. Analyzing design hierarchy..
Top module:  \ascon_core_adpt_encdec
Removed 0 unused modules.

125. Executing CHECK pass (checking for obvious problems).
Checking module ascon_core_adpt_encdec...
Found and reported 0 problems.

126. Printing statistics.

=== ascon_core_adpt_encdec ===

        +----------Local Count, excluding submodules.
        |
     5119 wires
     9203 wire bits
       75 public wires
     3450 public wire bits
       30 ports
      927 port bits
     6733 cells
     1419   $_ANDNOT_
       96   $_AND_
      915   $_DFFE_PN0P_
        2   $_DFF_PN0_
      937   $_MUX_
       11   $_NAND_
       25   $_NOR_
      527   $_NOT_
      154   $_ORNOT_
      777   $_OR_
      957   $_XNOR_
      911   $_XOR_
        2   $scopeinfo

127. Executing OPT pass (performing simple optimizations).

127.1. Executing OPT_EXPR pass (perform const folding).
Optimizing module ascon_core_adpt_encdec.

127.2. Executing OPT_MERGE pass (detect identical cells).
Finding identical cells in module `\ascon_core_adpt_encdec'.
Computing hashes of 6733 cells of `\ascon_core_adpt_encdec'.
Finding duplicate cells in `\ascon_core_adpt_encdec'.
Removed a total of 0 cells.

127.3. Executing OPT_MUXTREE pass (detect dead branches in mux trees).
Running muxtree optimizer on module \ascon_core_adpt_encdec..
  Creating internal representation of mux trees.
  No muxes found in this module.
Removed 0 multiplexer ports.

127.4. Executing OPT_REDUCE pass (consolidate $*mux and $reduce_* inputs).
  Optimizing cells in module \ascon_core_adpt_encdec.
Performed a total of 0 changes.

127.5. Executing OPT_MERGE pass (detect identical cells).
Finding identical cells in module `\ascon_core_adpt_encdec'.
Computing hashes of 6733 cells of `\ascon_core_adpt_encdec'.
Finding duplicate cells in `\ascon_core_adpt_encdec'.
Removed a total of 0 cells.

127.6. Executing OPT_DFF pass (perform DFF optimizations).

127.7. Executing OPT_CLEAN pass (remove unused cells and wires).
Finding unused cells or wires in module \ascon_core_adpt_encdec..

127.8. Executing OPT_EXPR pass (perform const folding).
Optimizing module ascon_core_adpt_encdec.

127.9. Finished fast OPT passes. (There is nothing left to do.)

128. Executing OPT_CLEAN pass (remove unused cells and wires).
Finding unused cells or wires in module \ascon_core_adpt_encdec..
Removed 2 unused cells and 26 unused wires.
<suppressed ~28 debug messages>
{
   "creator": "Yosys 0.64 (git sha1 6d2c445ae, g++ 13.3.0-6ubuntu2~24.04.1 -fPIC -O3)",
   "invocation": "stat -json -liberty
/foss/designs/ascon_pipelined/runs/RUN_2026-07-03_15-13-26/tmp/21487d43445f4c8fb643afeb0d99f888.lib ",
   "modules": {
      "\\ascon_core_adpt_encdec": {
         "num_wires":         5093,
         "num_wire_bits":     7651,
         "num_pub_wires":     49,
         "num_pub_wire_bits": 1898,
         "num_ports":         30,
         "num_port_bits":     927,
         "num_memories":      0,
         "num_memory_bits":   0,
         "num_processes":     0,
         "num_cells":         6731,
         "num_submodules":       0,
         "num_cells_by_type": {
            "$_ANDNOT_": 1419,
            "$_AND_": 96,
            "$_DFFE_PN0P_": 915,
            "$_DFF_PN0_": 2,
            "$_MUX_": 937,
            "$_NAND_": 11,
            "$_NOR_": 25,
            "$_NOT_": 527,
            "$_ORNOT_": 154,
            "$_OR_": 777,
            "$_XNOR_": 957,
            "$_XOR_": 911
         }
      }
   },
      "design": {
         "num_wires":         5093,
         "num_wire_bits":     7651,
         "num_pub_wires":     49,
         "num_pub_wire_bits": 1898,
         "num_ports":         30,
         "num_port_bits":     927,
         "num_memories":      0,
         "num_memory_bits":   0,
         "num_processes":     0,
         "num_cells":         6731,
         "num_submodules":       0,
         "num_cells_by_type": {
            "$_ANDNOT_": 1419,
            "$_AND_": 96,
            "$_DFFE_PN0P_": 915,
            "$_DFF_PN0_": 2,
            "$_MUX_": 937,
            "$_NAND_": 11,
            "$_NOR_": 25,
            "$_NOT_": 527,
            "$_ORNOT_": 154,
            "$_OR_": 777,
            "$_XNOR_": 957,
            "$_XOR_": 911
         }
      }
}

129. Printing statistics.

=== ascon_core_adpt_encdec ===

        +----------Local Count, excluding submodules.
        |
     5093 wires
     7651 wire bits
       49 public wires
     1898 public wire bits
       30 ports
      927 port bits
     6731 cells
     1419   $_ANDNOT_
       96   $_AND_
      915   $_DFFE_PN0P_
        2   $_DFF_PN0_
      937   $_MUX_
       11   $_NAND_
       25   $_NOR_
      527   $_NOT_
      154   $_ORNOT_
      777   $_OR_
      957   $_XNOR_
      911   $_XOR_

   Area for cell type $_ANDNOT_ is unknown!
   Area for cell type $_AND_ is unknown!
   Area for cell type $_DFFE_PN0P_ is unknown!
   Area for cell type $_DFF_PN0_ is unknown!
   Area for cell type $_MUX_ is unknown!
   Area for cell type $_NAND_ is unknown!
   Area for cell type $_NOR_ is unknown!
   Area for cell type $_NOT_ is unknown!
   Area for cell type $_ORNOT_ is unknown!
   Area for cell type $_OR_ is unknown!
   Area for cell type $_XNOR_ is unknown!
   Area for cell type $_XOR_ is unknown!

130. Executing DFFLIBMAP pass (mapping DFF cells to sequential cells from liberty file).
  cell gf180mcu_fd_sc_mcu7t5v0__dffnq_1 (noninv, pins=3, area=65.86) is a direct match for cell type $_DFF_N_.
  cell gf180mcu_fd_sc_mcu7t5v0__dffq_1 (noninv, pins=3, area=63.66) is a direct match for cell type $_DFF_P_.
  cell gf180mcu_fd_sc_mcu7t5v0__dffnrnq_1 (noninv, pins=4, area=74.64) is a direct match for cell type $_DFF_NN0_.
  cell gf180mcu_fd_sc_mcu7t5v0__dffnsnq_1 (noninv, pins=4, area=79.03) is a direct match for cell type $_DFF_NN1_.
  cell gf180mcu_fd_sc_mcu7t5v0__dffrnq_1 (noninv, pins=4, area=74.64) is a direct match for cell type $_DFF_PN0_.
  cell gf180mcu_fd_sc_mcu7t5v0__dffsnq_1 (noninv, pins=4, area=79.03) is a direct match for cell type $_DFF_PN1_.
  cell gf180mcu_fd_sc_mcu7t5v0__dffnrsnq_1 (noninv, pins=5, area=94.39) is a direct match for cell type $_DFFSR_NNN_.
  cell gf180mcu_fd_sc_mcu7t5v0__dffrsnq_1 (noninv, pins=5, area=85.61) is a direct match for cell type $_DFFSR_PNN_.
  final dff cell mappings:
    \gf180mcu_fd_sc_mcu7t5v0__dffnq_1 _DFF_N_ (.CLKN( C), .D( D), .Q( Q));
    \gf180mcu_fd_sc_mcu7t5v0__dffq_1 _DFF_P_ (.CLK( C), .D( D), .Q( Q));
    \gf180mcu_fd_sc_mcu7t5v0__dffnrnq_1 _DFF_NN0_ (.CLKN( C), .D( D), .Q( Q), .RN( R));
    \gf180mcu_fd_sc_mcu7t5v0__dffnsnq_1 _DFF_NN1_ (.CLKN( C), .D( D), .Q( Q), .SETN( R));
    unmapped dff cell: $_DFF_NP0_
    unmapped dff cell: $_DFF_NP1_
    \gf180mcu_fd_sc_mcu7t5v0__dffrnq_1 _DFF_PN0_ (.CLK( C), .D( D), .Q( Q), .RN( R));
    \gf180mcu_fd_sc_mcu7t5v0__dffsnq_1 _DFF_PN1_ (.CLK( C), .D( D), .Q( Q), .SETN( R));
    unmapped dff cell: $_DFF_PP0_
    unmapped dff cell: $_DFF_PP1_
    unmapped dff cell: $_DFFE_NN_
    unmapped dff cell: $_DFFE_NP_
    unmapped dff cell: $_DFFE_PN_
    unmapped dff cell: $_DFFE_PP_
    \gf180mcu_fd_sc_mcu7t5v0__dffnrsnq_1 _DFFSR_NNN_ (.CLKN( C), .D( D), .Q( Q), .RN( R), .SETN( S));
    unmapped dff cell: $_DFFSR_NNP_
    unmapped dff cell: $_DFFSR_NPN_
    unmapped dff cell: $_DFFSR_NPP_
    \gf180mcu_fd_sc_mcu7t5v0__dffrsnq_1 _DFFSR_PNN_ (.CLK( C), .D( D), .Q( Q), .RN( R), .SETN( S));
    unmapped dff cell: $_DFFSR_PNP_
    unmapped dff cell: $_DFFSR_PPN_
    unmapped dff cell: $_DFFSR_PPP_

130.1. Executing DFFLEGALIZE pass (convert FFs to types supported by the target).
Mapping DFF cells in module `\ascon_core_adpt_encdec':
  mapped 917 $_DFF_PN0_ cells to \gf180mcu_fd_sc_mcu7t5v0__dffrnq_1 cells.
{
   "creator": "Yosys 0.64 (git sha1 6d2c445ae, g++ 13.3.0-6ubuntu2~24.04.1 -fPIC -O3)",
   "invocation": "stat -json -liberty
/foss/designs/ascon_pipelined/runs/RUN_2026-07-03_15-13-26/tmp/21487d43445f4c8fb643afeb0d99f888.lib ",
   "modules": {
      "\\ascon_core_adpt_encdec": {
         "num_wires":         6008,
         "num_wire_bits":     8566,
         "num_pub_wires":     49,
         "num_pub_wire_bits": 1898,
         "num_ports":         30,
         "num_port_bits":     927,
         "num_memories":      0,
         "num_memory_bits":   0,
         "num_processes":     0,
         "num_cells":         7646,
         "num_submodules":       0,
         "area":              68441.945600,
         "sequential_area":    68441.945600,
         "num_cells_by_type": {
            "$_ANDNOT_": 1419,
            "$_AND_": 96,
            "$_MUX_": 1852,
            "$_NAND_": 11,
            "$_NOR_": 25,
            "$_NOT_": 527,
            "$_ORNOT_": 154,
            "$_OR_": 777,
            "$_XNOR_": 957,
            "$_XOR_": 911,
            "gf180mcu_fd_sc_mcu7t5v0__dffrnq_1": 917
         }
      }
   },
      "design": {
         "num_wires":         6008,
         "num_wire_bits":     8566,
         "num_pub_wires":     49,
         "num_pub_wire_bits": 1898,
         "num_ports":         30,
         "num_port_bits":     927,
         "num_memories":      0,
         "num_memory_bits":   0,
         "num_processes":     0,
         "num_cells":         7646,
         "num_submodules":       0,
         "area":              68441.945600,
         "sequential_area":    68441.945600,
         "num_cells_by_type": {
            "$_ANDNOT_": 1419,
            "$_AND_": 96,
            "$_MUX_": 1852,
            "$_NAND_": 11,
            "$_NOR_": 25,
            "$_NOT_": 527,
            "$_ORNOT_": 154,
            "$_OR_": 777,
            "$_XNOR_": 957,
            "$_XOR_": 911,
            "gf180mcu_fd_sc_mcu7t5v0__dffrnq_1": 917
         }
      }
}

131. Printing statistics.

=== ascon_core_adpt_encdec ===

        +----------Local Count, excluding submodules.
        |        +-Local Area, excluding submodules.
        |        |
     6008        - wires
     8566        - wire bits
       49        - public wires
     1898        - public wire bits
       30        - ports
      927        - port bits
     7646 6.84E+04 cells
     1419        -   $_ANDNOT_
       96        -   $_AND_
     1852        -   $_MUX_
       11        -   $_NAND_
       25        -   $_NOR_
      527        -   $_NOT_
      154        -   $_ORNOT_
      777        -   $_OR_
      957        -   $_XNOR_
      911        -   $_XOR_
      917 6.84E+04   gf180mcu_fd_sc_mcu7t5v0__dffrnq_1

   Area for cell type $_ANDNOT_ is unknown!
   Area for cell type $_AND_ is unknown!
   Area for cell type $_MUX_ is unknown!
   Area for cell type $_NAND_ is unknown!
   Area for cell type $_NOR_ is unknown!
   Area for cell type $_NOT_ is unknown!
   Area for cell type $_ORNOT_ is unknown!
   Area for cell type $_OR_ is unknown!
   Area for cell type $_XNOR_ is unknown!
   Area for cell type $_XOR_ is unknown!

   Chip area for module '\ascon_core_adpt_encdec': 68441.945600
     of which used for sequential elements: 68441.945600 (100.00%)

[INFO] Using generated ABC script
'/foss/designs/ascon_pipelined/runs/RUN_2026-07-03_15-13-26/06-yosys-synthesis/AREA_0.abc'…

132. Executing ABC pass (technology mapping using ABC).

132.1. Extracting gate netlist of module `\ascon_core_adpt_encdec' to `/tmp/yosys-abc-Esw2lA/input.blif'..

132.1.1. Executed ABC.
Extracted 6729 gates and 8301 wires to a netlist network with 1572 inputs and 919 outputs.
Running ABC script: /tmp/yosys-abc-Esw2lA/abc.script
ABC: UC Berkeley, ABC 1.01 (compiled Apr 16 2026 21:01:18)
ABC: abc 01> empty
ABC: abc 01> source /tmp/yosys-abc-Esw2lA/abc.script
ABC: + read_blif /tmp/yosys-abc-Esw2lA/input.blif
ABC: + read_lib -w /foss/designs/ascon_pipelined/runs/RUN_2026-07-03_15-13-26/tmp/21487d43445f4c8fb643afeb0d99f888.lib
ABC: Parsing finished successfully.  Parsing time =     0.21 sec
ABC: Scl_LibertyReadGenlib() skipped cell "gf180mcu_fd_sc_mcu7t5v0__antenna" without logic function.
ABC: Scl_LibertyReadGenlib() skipped three-state cell "gf180mcu_fd_sc_mcu7t5v0__bufz_1".
ABC: Scl_LibertyReadGenlib() skipped three-state cell "gf180mcu_fd_sc_mcu7t5v0__bufz_2".
ABC: Scl_LibertyReadGenlib() skipped three-state cell "gf180mcu_fd_sc_mcu7t5v0__bufz_3".
ABC: Scl_LibertyReadGenlib() skipped three-state cell "gf180mcu_fd_sc_mcu7t5v0__bufz_4".
ABC: Scl_LibertyReadGenlib() skipped three-state cell "gf180mcu_fd_sc_mcu7t5v0__bufz_8".
ABC: Scl_LibertyReadGenlib() skipped three-state cell "gf180mcu_fd_sc_mcu7t5v0__bufz_12".
ABC: Scl_LibertyReadGenlib() skipped three-state cell "gf180mcu_fd_sc_mcu7t5v0__bufz_16".
ABC: Scl_LibertyReadGenlib() skipped sequential cell "gf180mcu_fd_sc_mcu7t5v0__dffnq_1".
ABC: Scl_LibertyReadGenlib() skipped sequential cell "gf180mcu_fd_sc_mcu7t5v0__dffnq_2".
ABC: Scl_LibertyReadGenlib() skipped sequential cell "gf180mcu_fd_sc_mcu7t5v0__dffnq_4".
ABC: Scl_LibertyReadGenlib() skipped sequential cell "gf180mcu_fd_sc_mcu7t5v0__dffnrnq_1".
ABC: Scl_LibertyReadGenlib() skipped sequential cell "gf180mcu_fd_sc_mcu7t5v0__dffnrnq_2".
ABC: Scl_LibertyReadGenlib() skipped sequential cell "gf180mcu_fd_sc_mcu7t5v0__dffnrnq_4".
ABC: Scl_LibertyReadGenlib() skipped sequential cell "gf180mcu_fd_sc_mcu7t5v0__dffnrsnq_1".
ABC: Scl_LibertyReadGenlib() skipped sequential cell "gf180mcu_fd_sc_mcu7t5v0__dffnrsnq_2".
ABC: Scl_LibertyReadGenlib() skipped sequential cell "gf180mcu_fd_sc_mcu7t5v0__dffnrsnq_4".
ABC: Scl_LibertyReadGenlib() skipped sequential cell "gf180mcu_fd_sc_mcu7t5v0__dffnsnq_1".
ABC: Scl_LibertyReadGenlib() skipped sequential cell "gf180mcu_fd_sc_mcu7t5v0__dffnsnq_2".
ABC: Scl_LibertyReadGenlib() skipped sequential cell "gf180mcu_fd_sc_mcu7t5v0__dffnsnq_4".
ABC: Scl_LibertyReadGenlib() skipped sequential cell "gf180mcu_fd_sc_mcu7t5v0__dffq_1".
ABC: Scl_LibertyReadGenlib() skipped sequential cell "gf180mcu_fd_sc_mcu7t5v0__dffq_2".
ABC: Scl_LibertyReadGenlib() skipped sequential cell "gf180mcu_fd_sc_mcu7t5v0__dffq_4".
ABC: Scl_LibertyReadGenlib() skipped sequential cell "gf180mcu_fd_sc_mcu7t5v0__dffrnq_1".
ABC: Scl_LibertyReadGenlib() skipped sequential cell "gf180mcu_fd_sc_mcu7t5v0__dffrnq_2".
ABC: Scl_LibertyReadGenlib() skipped sequential cell "gf180mcu_fd_sc_mcu7t5v0__dffrnq_4".
ABC: Scl_LibertyReadGenlib() skipped sequential cell "gf180mcu_fd_sc_mcu7t5v0__dffrsnq_1".
ABC: Scl_LibertyReadGenlib() skipped sequential cell "gf180mcu_fd_sc_mcu7t5v0__dffrsnq_2".
ABC: Scl_LibertyReadGenlib() skipped sequential cell "gf180mcu_fd_sc_mcu7t5v0__dffrsnq_4".
ABC: Scl_LibertyReadGenlib() skipped sequential cell "gf180mcu_fd_sc_mcu7t5v0__dffsnq_1".
ABC: Scl_LibertyReadGenlib() skipped sequential cell "gf180mcu_fd_sc_mcu7t5v0__dffsnq_2".
ABC: Scl_LibertyReadGenlib() skipped sequential cell "gf180mcu_fd_sc_mcu7t5v0__dffsnq_4".
ABC: Scl_LibertyReadGenlib() skipped cell "gf180mcu_fd_sc_mcu7t5v0__endcap" without logic function.
ABC: Scl_LibertyReadGenlib() skipped cell "gf180mcu_fd_sc_mcu7t5v0__fill_1" without logic function.
ABC: Scl_LibertyReadGenlib() skipped cell "gf180mcu_fd_sc_mcu7t5v0__fill_2" without logic function.
ABC: Scl_LibertyReadGenlib() skipped cell "gf180mcu_fd_sc_mcu7t5v0__fill_4" without logic function.
ABC: Scl_LibertyReadGenlib() skipped cell "gf180mcu_fd_sc_mcu7t5v0__fill_8" without logic function.
ABC: Scl_LibertyReadGenlib() skipped cell "gf180mcu_fd_sc_mcu7t5v0__fill_16" without logic function.
ABC: Scl_LibertyReadGenlib() skipped cell "gf180mcu_fd_sc_mcu7t5v0__fill_32" without logic function.
ABC: Scl_LibertyReadGenlib() skipped cell "gf180mcu_fd_sc_mcu7t5v0__fill_64" without logic function.
ABC: Scl_LibertyReadGenlib() skipped cell "gf180mcu_fd_sc_mcu7t5v0__fillcap_4" without logic function.
ABC: Scl_LibertyReadGenlib() skipped cell "gf180mcu_fd_sc_mcu7t5v0__fillcap_8" without logic function.
ABC: Scl_LibertyReadGenlib() skipped cell "gf180mcu_fd_sc_mcu7t5v0__fillcap_16" without logic function.
ABC: Scl_LibertyReadGenlib() skipped cell "gf180mcu_fd_sc_mcu7t5v0__fillcap_32" without logic function.
ABC: Scl_LibertyReadGenlib() skipped cell "gf180mcu_fd_sc_mcu7t5v0__fillcap_64" without logic function.
ABC: Scl_LibertyReadGenlib() skipped cell "gf180mcu_fd_sc_mcu7t5v0__filltie" without logic function.
ABC: Scl_LibertyReadGenlib() skipped three-state cell "gf180mcu_fd_sc_mcu7t5v0__hold".
ABC: Scl_LibertyReadGenlib() skipped cell "gf180mcu_fd_sc_mcu7t5v0__icgtn_1" without logic function.
ABC: Scl_LibertyReadGenlib() skipped cell "gf180mcu_fd_sc_mcu7t5v0__icgtn_2" without logic function.
ABC: Scl_LibertyReadGenlib() skipped cell "gf180mcu_fd_sc_mcu7t5v0__icgtn_4" without logic function.
ABC: Scl_LibertyReadGenlib() skipped cell "gf180mcu_fd_sc_mcu7t5v0__icgtp_1" without logic function.
ABC: Scl_LibertyReadGenlib() skipped cell "gf180mcu_fd_sc_mcu7t5v0__icgtp_2" without logic function.
ABC: Scl_LibertyReadGenlib() skipped cell "gf180mcu_fd_sc_mcu7t5v0__icgtp_4" without logic function.
ABC: Scl_LibertyReadGenlib() skipped three-state cell "gf180mcu_fd_sc_mcu7t5v0__invz_1".
ABC: Scl_LibertyReadGenlib() skipped three-state cell "gf180mcu_fd_sc_mcu7t5v0__invz_2".
ABC: Scl_LibertyReadGenlib() skipped three-state cell "gf180mcu_fd_sc_mcu7t5v0__invz_3".
ABC: Scl_LibertyReadGenlib() skipped three-state cell "gf180mcu_fd_sc_mcu7t5v0__invz_4".
ABC: Scl_LibertyReadGenlib() skipped three-state cell "gf180mcu_fd_sc_mcu7t5v0__invz_8".
ABC: Scl_LibertyReadGenlib() skipped three-state cell "gf180mcu_fd_sc_mcu7t5v0__invz_12".
ABC: Scl_LibertyReadGenlib() skipped three-state cell "gf180mcu_fd_sc_mcu7t5v0__invz_16".
ABC: Scl_LibertyReadGenlib() skipped sequential cell "gf180mcu_fd_sc_mcu7t5v0__latq_1".
ABC: Scl_LibertyReadGenlib() skipped sequential cell "gf180mcu_fd_sc_mcu7t5v0__latq_2".
ABC: Scl_LibertyReadGenlib() skipped sequential cell "gf180mcu_fd_sc_mcu7t5v0__latq_4".
ABC: Scl_LibertyReadGenlib() skipped sequential cell "gf180mcu_fd_sc_mcu7t5v0__latrnq_1".
ABC: Scl_LibertyReadGenlib() skipped sequential cell "gf180mcu_fd_sc_mcu7t5v0__latrnq_2".
ABC: Scl_LibertyReadGenlib() skipped sequential cell "gf180mcu_fd_sc_mcu7t5v0__latrnq_4".
ABC: Scl_LibertyReadGenlib() skipped sequential cell "gf180mcu_fd_sc_mcu7t5v0__latrsnq_1".
ABC: Scl_LibertyReadGenlib() skipped sequential cell "gf180mcu_fd_sc_mcu7t5v0__latrsnq_2".
ABC: Scl_LibertyReadGenlib() skipped sequential cell "gf180mcu_fd_sc_mcu7t5v0__latrsnq_4".
ABC: Scl_LibertyReadGenlib() skipped sequential cell "gf180mcu_fd_sc_mcu7t5v0__latsnq_1".
ABC: Scl_LibertyReadGenlib() skipped sequential cell "gf180mcu_fd_sc_mcu7t5v0__latsnq_2".
ABC: Scl_LibertyReadGenlib() skipped sequential cell "gf180mcu_fd_sc_mcu7t5v0__latsnq_4".
ABC: Library "gf180mcu_fd_sc_mcu7t5v0__tt_025C_3v30" from
"/foss/designs/ascon_pipelined/runs/RUN_2026-07-03_15-13-26/tmp/21487d43445f4c8fb643afeb0d99f888.lib" has 143 cells (72
skipped: 36 seq; 15 tri-state; 21 no func; 0 dont_use; 0 with 2 outputs; 0 with 3+ outputs).  Time =     0.29 sec
ABC: Memory =   23.81 MB. Time =     0.29 sec
ABC: Warning: Detected 6 multi-output cells (for example, "gf180mcu_fd_sc_mcu7t5v0__addf_1").
ABC: + read_constr -v /foss/designs/ascon_pipelined/runs/RUN_2026-07-03_15-13-26/06-yosys-synthesis/synthesis.abc.sdc
ABC: Setting driving cell to be "gf180mcu_fd_sc_mcu7t5v0__inv_1/ZN".
ABC: Setting output load to be 72.910004.
ABC: + source /foss/designs/ascon_pipelined/runs/RUN_2026-07-03_15-13-26/06-yosys-synthesis/AREA_0.abc
ABC: Error: The network is combinational.
ABC: Cannot find the default PI driving cell (gf180mcu_fd_sc_mcu7t5v0__inv_1/ZN) in the library.
ABC: WireLoad = "none"  Gates =   5381 (  5.5 %)   Cap = 19.9 ff ( 17.9 %)   Area =   110343.92 ( 71.0 %)   Delay =
92711.50 ps  (  1.3 %)
ABC: Path  0 --     460 : 0    8 pi                              A =   0.00  Df =   0.0   -0.0 ps  S =   0.0 ps  Cin =
0.0 ff  Cout =  30.2 ff  Cmax =   0.0 ff  G =    0
ABC: Path  1 --    2754 : 2    6 gf180mcu_fd_sc_mcu7t5v0__or2_1  A =  17.56  Df = 803.1 -225.8 ps  S = 679.7 ps  Cin =
2.8 ff  Cout =  25.3 ff  Cmax = 359.9 ff  G =  901
ABC: Path  2 --    2758 : 3  382 gf180mcu_fd_sc_mcu7t5v0__nor3_1 A =  17.56  Df =68885.4-45938.3 ps  S =119835.5 ps  Cin
=  4.0 ff  Cout =1796.4 ff  Cmax = 122.2 ff  G =44898
ABC: Path  3 --    6045 : 3    1 gf180mcu_fd_sc_mcu7t5v0__mux2_2 A =  32.93  Df =92711.5-63279.6 ps  S =3187.5 ps  Cin =
6.4 ff  Cout =  72.9 ff  Cmax = 720.9 ff  G = 1143
ABC: Start-point = pi459 (\st [1]).  End-point = po610 ($auto$rtlil.cc:3501:MuxGate$20495).
ABC: netlist                       : i/o = 1572/  919  lat =    0  nd =  5381  edge =  14056  area =110342.90  delay =
8.00  lev = 8
ABC: + write_blif /tmp/yosys-abc-Esw2lA/output.blif
ABC:
ABC: YOSYS_ABC_DONE

132.1.2. Re-integrating ABC results.
ABC RESULTS:   gf180mcu_fd_sc_mcu7t5v0__and2_1 cells:       61
ABC RESULTS:   gf180mcu_fd_sc_mcu7t5v0__and3_1 cells:       17
ABC RESULTS:   gf180mcu_fd_sc_mcu7t5v0__and4_1 cells:        3
ABC RESULTS:   gf180mcu_fd_sc_mcu7t5v0__aoi211_1 cells:       96
ABC RESULTS:   gf180mcu_fd_sc_mcu7t5v0__aoi21_1 cells:      535
ABC RESULTS:   gf180mcu_fd_sc_mcu7t5v0__aoi221_1 cells:       81
ABC RESULTS:   gf180mcu_fd_sc_mcu7t5v0__aoi222_1 cells:       72
ABC RESULTS:   gf180mcu_fd_sc_mcu7t5v0__aoi22_1 cells:      131
ABC RESULTS:   gf180mcu_fd_sc_mcu7t5v0__clkinv_1 cells:      295
ABC RESULTS:   gf180mcu_fd_sc_mcu7t5v0__mux2_2 cells:      153
ABC RESULTS:   gf180mcu_fd_sc_mcu7t5v0__nand2_1 cells:      973
ABC RESULTS:   gf180mcu_fd_sc_mcu7t5v0__nand3_1 cells:       42
ABC RESULTS:   gf180mcu_fd_sc_mcu7t5v0__nand4_1 cells:       13
ABC RESULTS:   gf180mcu_fd_sc_mcu7t5v0__nor2_1 cells:      426
ABC RESULTS:   gf180mcu_fd_sc_mcu7t5v0__nor3_1 cells:       12
ABC RESULTS:   gf180mcu_fd_sc_mcu7t5v0__nor4_1 cells:       34
ABC RESULTS:   gf180mcu_fd_sc_mcu7t5v0__oai211_1 cells:      141
ABC RESULTS:   gf180mcu_fd_sc_mcu7t5v0__oai21_1 cells:      637
ABC RESULTS:   gf180mcu_fd_sc_mcu7t5v0__oai221_1 cells:       37
ABC RESULTS:   gf180mcu_fd_sc_mcu7t5v0__oai22_1 cells:       78
ABC RESULTS:   gf180mcu_fd_sc_mcu7t5v0__oai31_1 cells:       90
ABC RESULTS:   gf180mcu_fd_sc_mcu7t5v0__oai32_1 cells:       26
ABC RESULTS:   gf180mcu_fd_sc_mcu7t5v0__or2_1 cells:       13
ABC RESULTS:   gf180mcu_fd_sc_mcu7t5v0__or3_1 cells:        4
ABC RESULTS:   gf180mcu_fd_sc_mcu7t5v0__or4_1 cells:        1
ABC RESULTS:   gf180mcu_fd_sc_mcu7t5v0__xnor2_1 cells:       93
ABC RESULTS:   gf180mcu_fd_sc_mcu7t5v0__xnor3_1 cells:       68
ABC RESULTS:   gf180mcu_fd_sc_mcu7t5v0__xor2_1 cells:     1022
ABC RESULTS:   gf180mcu_fd_sc_mcu7t5v0__xor3_1 cells:      227
ABC RESULTS:        internal signals:     5810
ABC RESULTS:           input signals:     1572
ABC RESULTS:          output signals:      919
Removing temp directory.
Removing global temp directory.

133. Executing SETUNDEF pass (replace undef values with defined constants).

134. Executing HILOMAP pass (mapping to constant drivers).

135. Executing SPLITNETS pass (splitting up multi-bit signals).

136. Executing OPT_CLEAN pass (remove unused cells and wires).
Finding unused cells or wires in module \ascon_core_adpt_encdec..
Removed 63 unused cells and 8625 unused wires.
<suppressed ~384 debug messages>

137. Executing INSBUF pass (insert buffer cells for connected wires).

138. Executing CHECK pass (checking for obvious problems).
Checking module ascon_core_adpt_encdec...
Found and reported 0 problems.
{
   "creator": "Yosys 0.64 (git sha1 6d2c445ae, g++ 13.3.0-6ubuntu2~24.04.1 -fPIC -O3)",
   "invocation": "stat -json -liberty
/foss/designs/ascon_pipelined/runs/RUN_2026-07-03_15-13-26/tmp/21487d43445f4c8fb643afeb0d99f888.lib ",
   "modules": {
      "\\ascon_core_adpt_encdec": {
         "num_wires":         6060,
         "num_wire_bits":     6957,
         "num_pub_wires":     681,
         "num_pub_wire_bits": 1578,
         "num_ports":         30,
         "num_port_bits":     927,
         "num_memories":      0,
         "num_memory_bits":   0,
         "num_processes":     0,
         "num_cells":         6298,
         "num_submodules":       0,
         "area":              178785.868800,
         "sequential_area":    68441.945600,
         "num_cells_by_type": {
            "gf180mcu_fd_sc_mcu7t5v0__and2_1": 61,
            "gf180mcu_fd_sc_mcu7t5v0__and3_1": 17,
            "gf180mcu_fd_sc_mcu7t5v0__and4_1": 3,
            "gf180mcu_fd_sc_mcu7t5v0__aoi211_1": 96,
            "gf180mcu_fd_sc_mcu7t5v0__aoi21_1": 535,
            "gf180mcu_fd_sc_mcu7t5v0__aoi221_1": 81,
            "gf180mcu_fd_sc_mcu7t5v0__aoi222_1": 72,
            "gf180mcu_fd_sc_mcu7t5v0__aoi22_1": 131,
            "gf180mcu_fd_sc_mcu7t5v0__clkinv_1": 295,
            "gf180mcu_fd_sc_mcu7t5v0__dffrnq_1": 917,
            "gf180mcu_fd_sc_mcu7t5v0__mux2_2": 153,
            "gf180mcu_fd_sc_mcu7t5v0__nand2_1": 973,
            "gf180mcu_fd_sc_mcu7t5v0__nand3_1": 42,
            "gf180mcu_fd_sc_mcu7t5v0__nand4_1": 13,
            "gf180mcu_fd_sc_mcu7t5v0__nor2_1": 426,
            "gf180mcu_fd_sc_mcu7t5v0__nor3_1": 12,
            "gf180mcu_fd_sc_mcu7t5v0__nor4_1": 34,
            "gf180mcu_fd_sc_mcu7t5v0__oai211_1": 141,
            "gf180mcu_fd_sc_mcu7t5v0__oai21_1": 637,
            "gf180mcu_fd_sc_mcu7t5v0__oai221_1": 37,
            "gf180mcu_fd_sc_mcu7t5v0__oai22_1": 78,
            "gf180mcu_fd_sc_mcu7t5v0__oai31_1": 90,
            "gf180mcu_fd_sc_mcu7t5v0__oai32_1": 26,
            "gf180mcu_fd_sc_mcu7t5v0__or2_1": 13,
            "gf180mcu_fd_sc_mcu7t5v0__or3_1": 4,
            "gf180mcu_fd_sc_mcu7t5v0__or4_1": 1,
            "gf180mcu_fd_sc_mcu7t5v0__xnor2_1": 93,
            "gf180mcu_fd_sc_mcu7t5v0__xnor3_1": 68,
            "gf180mcu_fd_sc_mcu7t5v0__xor2_1": 1022,
            "gf180mcu_fd_sc_mcu7t5v0__xor3_1": 227
         }
      }
   },
      "design": {
         "num_wires":         6060,
         "num_wire_bits":     6957,
         "num_pub_wires":     681,
         "num_pub_wire_bits": 1578,
         "num_ports":         30,
         "num_port_bits":     927,
         "num_memories":      0,
         "num_memory_bits":   0,
         "num_processes":     0,
         "num_cells":         6298,
         "num_submodules":       0,
         "area":              178785.868800,
         "sequential_area":    68441.945600,
         "num_cells_by_type": {
            "gf180mcu_fd_sc_mcu7t5v0__and2_1": 61,
            "gf180mcu_fd_sc_mcu7t5v0__and3_1": 17,
            "gf180mcu_fd_sc_mcu7t5v0__and4_1": 3,
            "gf180mcu_fd_sc_mcu7t5v0__aoi211_1": 96,
            "gf180mcu_fd_sc_mcu7t5v0__aoi21_1": 535,
            "gf180mcu_fd_sc_mcu7t5v0__aoi221_1": 81,
            "gf180mcu_fd_sc_mcu7t5v0__aoi222_1": 72,
            "gf180mcu_fd_sc_mcu7t5v0__aoi22_1": 131,
            "gf180mcu_fd_sc_mcu7t5v0__clkinv_1": 295,
            "gf180mcu_fd_sc_mcu7t5v0__dffrnq_1": 917,
            "gf180mcu_fd_sc_mcu7t5v0__mux2_2": 153,
            "gf180mcu_fd_sc_mcu7t5v0__nand2_1": 973,
            "gf180mcu_fd_sc_mcu7t5v0__nand3_1": 42,
            "gf180mcu_fd_sc_mcu7t5v0__nand4_1": 13,
            "gf180mcu_fd_sc_mcu7t5v0__nor2_1": 426,
            "gf180mcu_fd_sc_mcu7t5v0__nor3_1": 12,
            "gf180mcu_fd_sc_mcu7t5v0__nor4_1": 34,
            "gf180mcu_fd_sc_mcu7t5v0__oai211_1": 141,
            "gf180mcu_fd_sc_mcu7t5v0__oai21_1": 637,
            "gf180mcu_fd_sc_mcu7t5v0__oai221_1": 37,
            "gf180mcu_fd_sc_mcu7t5v0__oai22_1": 78,
            "gf180mcu_fd_sc_mcu7t5v0__oai31_1": 90,
            "gf180mcu_fd_sc_mcu7t5v0__oai32_1": 26,
            "gf180mcu_fd_sc_mcu7t5v0__or2_1": 13,
            "gf180mcu_fd_sc_mcu7t5v0__or3_1": 4,
            "gf180mcu_fd_sc_mcu7t5v0__or4_1": 1,
            "gf180mcu_fd_sc_mcu7t5v0__xnor2_1": 93,
            "gf180mcu_fd_sc_mcu7t5v0__xnor3_1": 68,
            "gf180mcu_fd_sc_mcu7t5v0__xor2_1": 1022,
            "gf180mcu_fd_sc_mcu7t5v0__xor3_1": 227
         }
      }
}

139. Printing statistics.

=== ascon_core_adpt_encdec ===

        +----------Local Count, excluding submodules.
        |        +-Local Area, excluding submodules.
        |        |
     6060        - wires
     6957        - wire bits
      681        - public wires
     1578        - public wire bits
       30        - ports
      927        - port bits
     6298 1.79E+05 cells
       61 1.07E+03   gf180mcu_fd_sc_mcu7t5v0__and2_1
       17  373.184   gf180mcu_fd_sc_mcu7t5v0__and3_1
        3   72.442   gf180mcu_fd_sc_mcu7t5v0__and4_1
       96 2.11E+03   gf180mcu_fd_sc_mcu7t5v0__aoi211_1
      535  9.4E+03   gf180mcu_fd_sc_mcu7t5v0__aoi21_1
       81 1.96E+03   gf180mcu_fd_sc_mcu7t5v0__aoi221_1
       72 2.21E+03   gf180mcu_fd_sc_mcu7t5v0__aoi222_1
      131 2.59E+03   gf180mcu_fd_sc_mcu7t5v0__aoi22_1
      295 2.59E+03   gf180mcu_fd_sc_mcu7t5v0__clkinv_1
      917 6.84E+04   gf180mcu_fd_sc_mcu7t5v0__dffrnq_1
      153 5.04E+03   gf180mcu_fd_sc_mcu7t5v0__mux2_2
      973 1.07E+04   gf180mcu_fd_sc_mcu7t5v0__nand2_1
       42  645.389   gf180mcu_fd_sc_mcu7t5v0__nand3_1
       13  256.838   gf180mcu_fd_sc_mcu7t5v0__nand4_1
      426 5.61E+03   gf180mcu_fd_sc_mcu7t5v0__nor2_1
       12  210.739   gf180mcu_fd_sc_mcu7t5v0__nor3_1
       34  746.368   gf180mcu_fd_sc_mcu7t5v0__nor4_1
      141  3.1E+03   gf180mcu_fd_sc_mcu7t5v0__oai211_1
      637 1.12E+04   gf180mcu_fd_sc_mcu7t5v0__oai21_1
       37  974.669   gf180mcu_fd_sc_mcu7t5v0__oai221_1
       78 1.71E+03   gf180mcu_fd_sc_mcu7t5v0__oai22_1
       90 2.17E+03   gf180mcu_fd_sc_mcu7t5v0__oai31_1
       26  684.902   gf180mcu_fd_sc_mcu7t5v0__oai32_1
       13  228.301   gf180mcu_fd_sc_mcu7t5v0__or2_1
        4   87.808   gf180mcu_fd_sc_mcu7t5v0__or3_1
        1   26.342   gf180mcu_fd_sc_mcu7t5v0__or4_1
       93 2.65E+03   gf180mcu_fd_sc_mcu7t5v0__xnor2_1
       68 3.58E+03   gf180mcu_fd_sc_mcu7t5v0__xnor3_1
     1022 2.69E+04   gf180mcu_fd_sc_mcu7t5v0__xor2_1
      227 1.15E+04   gf180mcu_fd_sc_mcu7t5v0__xor3_1

   Chip area for module '\ascon_core_adpt_encdec': 178785.868800
     of which used for sequential elements: 68441.945600 (38.28%)

140. Executing Verilog backend.
Dumping module `\ascon_core_adpt_encdec'.

141. Executing JSON backend.
[15:13:47] VERBOSE  Parsing synthesis checks…                                                               pyosys.py:59
[15:13:47] INFO     Skipping step 'Unmapped Cells Checker'…                                            sequential.py:370
[15:13:47] INFO     Skipping step 'Yosys Synth Checks'…                                                sequential.py:370
[15:13:47] INFO     Skipping step 'Netlist Assign Statement Checker'…                                  sequential.py:370
[15:13:47] INFO     Skipping step 'Check SDC Files'…                                                   sequential.py:370
[15:13:47] INFO     Skipping step 'Check Macro Instances'…                                             sequential.py:370
[15:13:47] INFO     Skipping step 'STA (Pre-PnR)'…                                                     sequential.py:370
[15:13:47] INFO     Skipping step 'Floorplan Init'…                                                    sequential.py:370
[15:13:47] INFO     Skipping step 'Dump RC Values'…                                                    sequential.py:370
[15:13:47] INFO     Skipping step 'Check Antenna Properties of Macros Pins in Their LEF Views'…        sequential.py:370
[15:13:47] INFO     Skipping step 'Set Power Connections'…                                             sequential.py:370
[15:13:47] INFO     Skipping step 'Manual Macro Placement'…                                            sequential.py:370
[15:13:47] INFO     Skipping step 'Cut Rows'…                                                          sequential.py:370
[15:13:47] INFO     Skipping step 'Tap/Decap Insertion'…                                               sequential.py:370
[15:13:47] INFO     Skipping step 'Add PDN obstructions'…                                              sequential.py:370
[15:13:47] INFO     Skipping step 'Generate PDN'…                                                      sequential.py:370
[15:13:47] INFO     Skipping step 'Remove PDN obstructions'…                                           sequential.py:370
[15:13:47] INFO     Skipping step 'Add Obstructions'…                                                  sequential.py:370
[15:13:47] INFO     Skipping step 'Global Placement Skip IO'…                                          sequential.py:370
[15:13:47] INFO     Skipping step 'I/O Placement'…                                                     sequential.py:370
[15:13:47] INFO     Skipping step 'Custom I/O Placement'…                                              sequential.py:370
[15:13:47] INFO     Skipping step 'Apply DEF Template'…                                                sequential.py:370
[15:13:47] INFO     Skipping step 'Global Placement'…                                                  sequential.py:370
[15:13:47] INFO     Skipping step 'Write Verilog Header'…                                              sequential.py:370
[15:13:47] INFO     Skipping step 'Power Grid Violation Checker'…                                      sequential.py:370
[15:13:47] INFO     Skipping step 'STA (Mid-PnR)'…                                                     sequential.py:370
[15:13:47] INFO     Skipping step 'Repair Design (Post-Global Placement)'…                             sequential.py:370
[15:13:47] INFO     Skipping step 'Manual Global Placement'…                                           sequential.py:370
[15:13:47] INFO     Skipping step 'Detailed Placement'…                                                sequential.py:370
[15:13:47] INFO     Skipping step 'Clock Tree Synthesis'…                                              sequential.py:370
[15:13:47] INFO     Skipping step 'STA (Mid-PnR)'…                                                     sequential.py:370
[15:13:47] INFO     Skipping step 'Resizer Timing Optimizations (Post-Clock Tree Synthesis)'…          sequential.py:370
[15:13:47] INFO     Skipping step 'STA (Mid-PnR)'…                                                     sequential.py:370
[15:13:47] INFO     Skipping step 'Global Routing'…                                                    sequential.py:370
[15:13:47] INFO     Skipping step 'Check Antennas'…                                                    sequential.py:370
[15:13:47] INFO     Gating variable for step 'OpenROAD.RepairDesignPostGRT' set to 'False'- the step   sequential.py:362
                    will be skipped.
[15:13:47] INFO     Skipping step 'Repair Design (Post-Global Routing)'…                               sequential.py:370
[15:13:47] INFO     Skipping step 'Diodes on Ports'…                                                   sequential.py:370
[15:13:47] INFO     Skipping step 'Heuristic Diode Insertion'…                                         sequential.py:370
[15:13:47] INFO     Gating variable for step 'OpenROAD.RepairAntennas' set to 'False'- the step will   sequential.py:362
                    be skipped.
[15:13:47] INFO     Skipping step 'Antenna Repair'…                                                    sequential.py:370
[15:13:47] INFO     Gating variable for step 'OpenROAD.ResizerTimingPostGRT' set to 'False'- the step  sequential.py:362
                    will be skipped.
[15:13:47] INFO     Skipping step 'Resizer Timing Optimizations (Post-Global Routing)'…                sequential.py:370
[15:13:47] INFO     Skipping step 'STA (Mid-PnR)'…                                                     sequential.py:370
[15:13:47] INFO     Skipping step 'Detailed Routing'…                                                  sequential.py:370
[15:13:47] INFO     Skipping step 'Remove Obstructions'…                                               sequential.py:370
[15:13:47] INFO     Skipping step 'Check Antennas'…                                                    sequential.py:370
[15:13:47] INFO     Skipping step 'Routing DRC Checker'…                                               sequential.py:370
[15:13:47] INFO     Skipping step 'Report Disconnected Pins'…                                          sequential.py:370
[15:13:47] INFO     Skipping step 'Disconnected Pins Checker'…                                         sequential.py:370
[15:13:47] INFO     Skipping step 'Report Wire Length'…                                                sequential.py:370
[15:13:47] INFO     Skipping step 'Wire Length Threshold Checker'…                                     sequential.py:370
[15:13:47] INFO     Skipping step 'Fill Insertion'…                                                    sequential.py:370
[15:13:47] INFO     Skipping step 'Generate Cell Frequency Tables'…                                    sequential.py:370
[15:13:47] INFO     Skipping step 'Parasitics (RC) Extraction'…                                        sequential.py:370
[15:13:47] INFO     Skipping step 'STA (Post-PnR)'…                                                    sequential.py:370
[15:13:47] INFO     Skipping step 'IR Drop Report'…                                                    sequential.py:370
[15:13:47] INFO     Skipping step 'GDSII Stream Out (Magic)'…                                          sequential.py:370
[15:13:47] INFO     Skipping step 'GDSII Stream Out (KLayout)'…                                        sequential.py:370
[15:13:47] INFO     Skipping step 'Render Image (w/ KLayout)'…                                         sequential.py:370
[15:13:47] INFO     Skipping step 'Write LEF (Magic)'…                                                 sequential.py:370
[15:13:47] INFO     Skipping step 'Check Antenna Properties of Pins in The Generated Design LEF view'… sequential.py:370
[15:13:47] INFO     Skipping step 'KLayout vs. Magic XOR'…                                             sequential.py:370
[15:13:48] INFO     Skipping step 'XOR Difference Checker'…                                            sequential.py:370
[15:13:48] INFO     Skipping step 'DRC'…                                                               sequential.py:370
[15:13:48] INFO     Skipping step 'Design Rule Check (KLayout)'…                                       sequential.py:370
[15:13:48] INFO     Skipping step 'Magic DRC Checker'…                                                 sequential.py:370
[15:13:48] INFO     Skipping step 'KLayout DRC Checker'…                                               sequential.py:370
[15:13:48] INFO     Skipping step 'SPICE Extraction'…                                                  sequential.py:370
[15:13:48] INFO     Skipping step 'Illegal Overlap Checker'…                                           sequential.py:370
[15:13:48] INFO     Skipping step 'Netgen LVS'…                                                        sequential.py:370
[15:13:48] INFO     Skipping step 'LVS Error Checker'…                                                 sequential.py:370
[15:13:48] INFO     Gating variable for step 'Yosys.EQY' set to 'False'- the step will be skipped.     sequential.py:362
[15:13:48] INFO     Skipping step 'Equivalence Check'…                                                 sequential.py:370
[15:13:48] INFO     Skipping step 'Setup Timing Violations Checker'…                                   sequential.py:370
[15:13:48] INFO     Skipping step 'Hold Timing Violations Checker'…                                    sequential.py:370
[15:13:48] INFO     Skipping step 'Max Slew Violations Checker'…                                       sequential.py:370
[15:13:48] INFO     Skipping step 'Max Cap Violations Checker'…                                        sequential.py:370
[15:13:48] INFO     Skipping step 'Report Manufacturability'…                                          sequential.py:370
[15:13:48] INFO     Saving views to '/foss/designs/ascon_pipelined/runs/RUN_2026-07-03_15-13-26/final'…     state.py:209
[15:13:48] INFO     Flow complete.                                                                     sequential.py:413
Classic - Stage 80 - Report Manufacturability ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 80/80 0:00:20
[15:13:48] WARNING  The following warnings were generated by the flow:                                       flow.py:699
[15:13:48] WARNING  [Checker.LintWarnings] 301 Lint warnings found.                                          flow.py:701

/foss/designs/ascon_pipelined > cd runs/RUN_2026-07-03_15-13-26/*-yosys-synthesis
ls
AREA_0.abc                        COMMANDS     reports        state_out.json       yosys-synthesis.process_stats.json
ascon_core_adpt_encdec.nl.v       config.json  runtime.txt    synthesis.abc.sdc

```


---


 
## TIMING AWARE GATE LEVEL SIMULATION / VERIFICATION (POST-SYNTHESIS)

Tool: EDAPlayground with shell script (run.bash)
Working Environment: https://edaplayground.com/x/f5Wm


This work is trying to perform post synthesis verification on a synthesized verilog design, which generates a gate level netlist, and the same design as a netlist, is then simulated using the same functional verification testbench developed during RTL verification, to make sure that after synthesis stage is completed, the netlist before proceeding further in the physical implementation flow, is functionally correct.
Timing is modeled by back-annotating the generated SDF file into the gate-level netlist during simulation. , using the .sdf (from librelane stage 12 - STA Pre PNR) (standard textual format for representing delay and timing information such as cell delays, interconnect delays, and timing constraints) files, it helps us answer the question: After considering the real delays of gates and wires, does the circuit still work at the desired clock speed?


for this, i referred to caravel docs about post synthesis verification, to understand how gate level simulations (GLS) is performed in Open source toolchain projects.
- the underlying tool used was iverilog (Icarus Verilog)
- i tried running the old testbench which was using random 100Mhz and the code failed, as the rtl2gds runs we performed were aimed at 50Mhz (50 Mhz = 20ns clock period)
- from our previous librelane runs, we knew that @50Mhz, this pipelined design was giving -9.1 ns of WNS at the SS corner, which is a setup violation.
- to make it avoid this violation, providing sufficient timing margin, i gave it 25 Mhz instead , i.e. 40ns clock speed.
- icarus verilog failed to account for the sdf annotation inside the testbench as it couldn't map the complex conditional specify paths used in the GF180 standard cell library., and so was also not possible for verilator.  ( these are 2 majorly used open source compilers). Icarus was able to do Gate-level simulation with just netlist and tb, without accounting for delays, and all 4 cases passed.
- i shifted to eda playground to use commericial compilers like synopsys vcs, that are more suited for Gate-level simulation with SDF (timing-aware gate-level simulation). the netlist generated has almost 72,000+ lines of code, which exceeeds the limit of the EDAPlayground tool, so uploaded these files to github publicly, used a shell script to ask the edaplayground tool to download these files locally and then run synopsys vcs compiler using the testbench i gave, which was able to account for the sdf annotation as well.
- if you observe the log i have pasted in the block below, towards the end, you can see TEST SUMMARY: 4 PASSED, 0 FAILED out of 4 tests and >>> ALL TESTS PASSED <<<, meaning it worked at this speed and correctly did the right functionality expected from the design as per this testbench and under these annotated delays, thereby successfully completing the post-synthesis gate-level simulation for the implemented test cases.
- can re-run the same environment to verify the result personally from the working environment eda playground code given above.

---

# SYNTHESIS VISUALIZATION

### POST SYNTHESIS NETLIST BASED CIRCUIT VISUAL (using netlistssvg by Neil Turley)

<img width="10710" height="10127" alt="netlist" src="https://github.com/user-attachments/assets/6ecc76ba-c2cd-4e1f-b41f-72444926004c" />



---

# LOG ( updated on 03/07/2026 -- 13:10 IST):
updated on jul 3 -- added 3 more cases to tb from lakshmi's tb to this tb
updated on jul 2 -- from jun 29's version 
added "+neg_tchk" to the run.bash script - fixes errors.

```
[2026-07-03 07:35:55 UTC] chmod +x run.bash; sed -i -e 's/\r//g' run.bash; ./run.bash  
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
  5 2978k    5  175k    0     0  2172k      0  0:00:01 --:--:--  0:00:01 2172k
100 2978k  100 2978k    0     0  28.5M      0 --:--:-- --:--:-- --:--:-- 28.2M
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
100 6207k  100 6207k    0     0  26.5M      0 --:--:-- --:--:-- --:--:-- 26.5M
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
100  952k  100  952k    0     0  12.9M      0 --:--:-- --:--:-- --:--:-- 12.9M
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
100  5541  100  5541    0     0  92350      0 --:--:-- --:--:-- --:--:-- 92350
                         Chronologic VCS (TM)
       Version X-2025.06-SP1_Full64 -- Fri Jul  3 03:35:56 2026

                    Copyright (c) 1991 - 2025 Synopsys, Inc.
   This software and the associated documentation are proprietary to Synopsys,
 Inc. This software may only be used in accordance with the terms and conditions
 of a written license agreement with Synopsys, Inc. All other use, reproduction,
   or distribution of this software is strictly prohibited.  Licensed Products
     communicate with Synopsys servers for the purpose of providing software
    updates, detecting software piracy and verifying that customers are using
    Licensed Products in conformity with the applicable License Key for such
  Licensed Products. Synopsys will use information gathered in connection with
    this process to deliver software updates and pursue software pirates and
                                   infringers.

 Inclusivity & Diversity - Visit SolvNetPlus to read the "Synopsys Statement on
            Inclusivity and Diversity" (Refer to article 000036315 at
                        https://solvnetplus.synopsys.com)

Parsing design file 'testbench.sv'
Parsing design file 'ascon_core_adpt_encdec.nl.v'
Parsing design file 'gf180mcu_fd_sc_mcu7t5v0.v'
Parsing design file 'primitives.v'
Top Level Modules:
       tb_ascon_verilog
       gf180mcu_fd_sc_mcu7t5v0__addf_1
       gf180mcu_fd_sc_mcu7t5v0__addf_2
       gf180mcu_fd_sc_mcu7t5v0__addf_4
       gf180mcu_fd_sc_mcu7t5v0__addh_1
       gf180mcu_fd_sc_mcu7t5v0__addh_2
       gf180mcu_fd_sc_mcu7t5v0__addh_4
       gf180mcu_fd_sc_mcu7t5v0__and3_2
       gf180mcu_fd_sc_mcu7t5v0__and3_4
       gf180mcu_fd_sc_mcu7t5v0__and4_2
       gf180mcu_fd_sc_mcu7t5v0__and4_4
       gf180mcu_fd_sc_mcu7t5v0__aoi22_4
       gf180mcu_fd_sc_mcu7t5v0__aoi221_2
       gf180mcu_fd_sc_mcu7t5v0__aoi221_4
       gf180mcu_fd_sc_mcu7t5v0__aoi222_2
       gf180mcu_fd_sc_mcu7t5v0__aoi222_4
       gf180mcu_fd_sc_mcu7t5v0__buf_1
       gf180mcu_fd_sc_mcu7t5v0__bufz_1
       gf180mcu_fd_sc_mcu7t5v0__bufz_2
       gf180mcu_fd_sc_mcu7t5v0__bufz_3
       gf180mcu_fd_sc_mcu7t5v0__bufz_4
       gf180mcu_fd_sc_mcu7t5v0__bufz_8
       gf180mcu_fd_sc_mcu7t5v0__bufz_12
       gf180mcu_fd_sc_mcu7t5v0__bufz_16
       gf180mcu_fd_sc_mcu7t5v0__clkbuf_1
       gf180mcu_fd_sc_mcu7t5v0__clkbuf_3
       gf180mcu_fd_sc_mcu7t5v0__clkbuf_4
       gf180mcu_fd_sc_mcu7t5v0__clkbuf_12
       gf180mcu_fd_sc_mcu7t5v0__clkbuf_20
       gf180mcu_fd_sc_mcu7t5v0__clkinv_3
       gf180mcu_fd_sc_mcu7t5v0__clkinv_4
       gf180mcu_fd_sc_mcu7t5v0__clkinv_16
       gf180mcu_fd_sc_mcu7t5v0__dffnq_1
       gf180mcu_fd_sc_mcu7t5v0__dffnq_2
       gf180mcu_fd_sc_mcu7t5v0__dffnq_4
       gf180mcu_fd_sc_mcu7t5v0__dffnrnq_1
       gf180mcu_fd_sc_mcu7t5v0__dffnrnq_2
       gf180mcu_fd_sc_mcu7t5v0__dffnrnq_4
       gf180mcu_fd_sc_mcu7t5v0__dffnrsnq_1
       gf180mcu_fd_sc_mcu7t5v0__dffnrsnq_2
       gf180mcu_fd_sc_mcu7t5v0__dffnrsnq_4
       gf180mcu_fd_sc_mcu7t5v0__dffnsnq_1
       gf180mcu_fd_sc_mcu7t5v0__dffnsnq_2
       gf180mcu_fd_sc_mcu7t5v0__dffnsnq_4
       gf180mcu_fd_sc_mcu7t5v0__dffq_1
       gf180mcu_fd_sc_mcu7t5v0__dffq_2
       gf180mcu_fd_sc_mcu7t5v0__dffq_4
       gf180mcu_fd_sc_mcu7t5v0__dffrsnq_1
       gf180mcu_fd_sc_mcu7t5v0__dffrsnq_2
       gf180mcu_fd_sc_mcu7t5v0__dffrsnq_4
       gf180mcu_fd_sc_mcu7t5v0__dffsnq_1
       gf180mcu_fd_sc_mcu7t5v0__dffsnq_2
       gf180mcu_fd_sc_mcu7t5v0__dffsnq_4
       gf180mcu_fd_sc_mcu7t5v0__dlya_1
       gf180mcu_fd_sc_mcu7t5v0__dlya_2
       gf180mcu_fd_sc_mcu7t5v0__dlya_4
       gf180mcu_fd_sc_mcu7t5v0__dlyb_1
       gf180mcu_fd_sc_mcu7t5v0__dlyb_2
       gf180mcu_fd_sc_mcu7t5v0__dlyb_4
       gf180mcu_fd_sc_mcu7t5v0__dlyc_1
       gf180mcu_fd_sc_mcu7t5v0__dlyc_2
       gf180mcu_fd_sc_mcu7t5v0__dlyc_4
       gf180mcu_fd_sc_mcu7t5v0__dlyd_2
       gf180mcu_fd_sc_mcu7t5v0__dlyd_4
       gf180mcu_fd_sc_mcu7t5v0__fill_4
       gf180mcu_fd_sc_mcu7t5v0__fill_8
       gf180mcu_fd_sc_mcu7t5v0__fill_16
       gf180mcu_fd_sc_mcu7t5v0__fill_32
       gf180mcu_fd_sc_mcu7t5v0__fill_64
       gf180mcu_fd_sc_mcu7t5v0__hold
       gf180mcu_fd_sc_mcu7t5v0__icgtn_1
       gf180mcu_fd_sc_mcu7t5v0__icgtn_2
       gf180mcu_fd_sc_mcu7t5v0__icgtn_4
       gf180mcu_fd_sc_mcu7t5v0__icgtp_1
       gf180mcu_fd_sc_mcu7t5v0__icgtp_2
       gf180mcu_fd_sc_mcu7t5v0__icgtp_4
       gf180mcu_fd_sc_mcu7t5v0__inv_1
       gf180mcu_fd_sc_mcu7t5v0__inv_16
       gf180mcu_fd_sc_mcu7t5v0__inv_20
       gf180mcu_fd_sc_mcu7t5v0__invz_1
       gf180mcu_fd_sc_mcu7t5v0__invz_2
       gf180mcu_fd_sc_mcu7t5v0__invz_3
       gf180mcu_fd_sc_mcu7t5v0__invz_4
       gf180mcu_fd_sc_mcu7t5v0__invz_8
       gf180mcu_fd_sc_mcu7t5v0__invz_12
       gf180mcu_fd_sc_mcu7t5v0__invz_16
       gf180mcu_fd_sc_mcu7t5v0__latq_1
       gf180mcu_fd_sc_mcu7t5v0__latq_2
       gf180mcu_fd_sc_mcu7t5v0__latq_4
       gf180mcu_fd_sc_mcu7t5v0__latrnq_1
       gf180mcu_fd_sc_mcu7t5v0__latrnq_2
       gf180mcu_fd_sc_mcu7t5v0__latrnq_4
       gf180mcu_fd_sc_mcu7t5v0__latrsnq_1
       gf180mcu_fd_sc_mcu7t5v0__latrsnq_2
       gf180mcu_fd_sc_mcu7t5v0__latrsnq_4
       gf180mcu_fd_sc_mcu7t5v0__latsnq_1
       gf180mcu_fd_sc_mcu7t5v0__latsnq_2
       gf180mcu_fd_sc_mcu7t5v0__latsnq_4
       gf180mcu_fd_sc_mcu7t5v0__mux2_1
       gf180mcu_fd_sc_mcu7t5v0__mux2_4
       gf180mcu_fd_sc_mcu7t5v0__mux4_1
       gf180mcu_fd_sc_mcu7t5v0__mux4_2
       gf180mcu_fd_sc_mcu7t5v0__mux4_4
       gf180mcu_fd_sc_mcu7t5v0__nor3_2
       gf180mcu_fd_sc_mcu7t5v0__oai22_4
       gf180mcu_fd_sc_mcu7t5v0__oai32_4
       gf180mcu_fd_sc_mcu7t5v0__oai33_1
       gf180mcu_fd_sc_mcu7t5v0__oai33_2
       gf180mcu_fd_sc_mcu7t5v0__oai33_4
       gf180mcu_fd_sc_mcu7t5v0__oai221_2
       gf180mcu_fd_sc_mcu7t5v0__oai221_4
       gf180mcu_fd_sc_mcu7t5v0__oai222_1
       gf180mcu_fd_sc_mcu7t5v0__oai222_2
       gf180mcu_fd_sc_mcu7t5v0__oai222_4
       gf180mcu_fd_sc_mcu7t5v0__or3_4
       gf180mcu_fd_sc_mcu7t5v0__or4_2
       gf180mcu_fd_sc_mcu7t5v0__or4_4
       gf180mcu_fd_sc_mcu7t5v0__sdffq_1
       gf180mcu_fd_sc_mcu7t5v0__sdffq_2
       gf180mcu_fd_sc_mcu7t5v0__sdffq_4
       gf180mcu_fd_sc_mcu7t5v0__sdffrnq_1
       gf180mcu_fd_sc_mcu7t5v0__sdffrnq_2
       gf180mcu_fd_sc_mcu7t5v0__sdffrnq_4
       gf180mcu_fd_sc_mcu7t5v0__sdffrsnq_1
       gf180mcu_fd_sc_mcu7t5v0__sdffrsnq_2
       gf180mcu_fd_sc_mcu7t5v0__sdffrsnq_4
       gf180mcu_fd_sc_mcu7t5v0__sdffsnq_1
       gf180mcu_fd_sc_mcu7t5v0__sdffsnq_2
       gf180mcu_fd_sc_mcu7t5v0__sdffsnq_4
       gf180mcu_fd_sc_mcu7t5v0__tieh
       gf180mcu_fd_sc_mcu7t5v0__tiel
       gf180mcu_fd_sc_mcu7t5v0__xnor2_4
       gf180mcu_fd_sc_mcu7t5v0__xnor3_2
       gf180mcu_fd_sc_mcu7t5v0__xnor3_4
       gf180mcu_fd_sc_mcu7t5v0__xor2_4
       gf180mcu_fd_sc_mcu7t5v0__xor3_2
       gf180mcu_fd_sc_mcu7t5v0__xor3_4
TimeScale is 1 ns / 1 ps

Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69112
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__clkbuf_8 clkload0( .I (clknet_4_3__leaf_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69113
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__clkbuf_8 clkload1( .I (clknet_4_7__leaf_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69114
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__inv_4 clkload10( .I (clknet_leaf_1_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69115
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__inv_4 clkload11( .I (clknet_leaf_74_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69116
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__clkbuf_2 clkload12( .I (clknet_leaf_67_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69117
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__inv_2 clkload13( .I (clknet_leaf_70_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69118
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__inv_4 clkload14( .I (clknet_leaf_72_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69119
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__clkbuf_2 clkload15( .I (clknet_leaf_64_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69120
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__clkbuf_2 clkload16( .I (clknet_leaf_66_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69121
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__clkbuf_2 clkload17( .I (clknet_leaf_8_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69122
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__clkbuf_2 clkload18( .I (clknet_leaf_10_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69123
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__clkinv_2 clkload19( .I (clknet_leaf_11_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69124
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__clkbuf_8 clkload2( .I (clknet_4_11__leaf_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69125
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__inv_2 clkload20( .I (clknet_leaf_14_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69126
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__clkbuf_2 clkload21( .I (clknet_leaf_15_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69127
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__clkinv_2 clkload22( .I (clknet_leaf_16_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69128
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__inv_4 clkload23( .I (clknet_leaf_17_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69129
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__clkbuf_2 clkload24( .I (clknet_leaf_22_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69130
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__clkbuf_2 clkload25( .I (clknet_leaf_24_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69131
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__inv_2 clkload26( .I (clknet_leaf_26_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69132
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__clkbuf_2 clkload27( .I (clknet_leaf_20_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69133
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__inv_4 clkload28( .I (clknet_leaf_55_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69134
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__clkbuf_2 clkload29( .I (clknet_leaf_56_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69135
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__clkbuf_8 clkload3( .I (clknet_4_13__leaf_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69136
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__clkbuf_2 clkload30( .I (clknet_leaf_59_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69137
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__clkbuf_2 clkload31( .I (clknet_leaf_60_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69138
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__clkbuf_2 clkload32( .I (clknet_leaf_45_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69139
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__inv_2 clkload33( .I (clknet_leaf_61_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69140
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__clkinv_2 clkload34( .I (clknet_leaf_62_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69141
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__clkinv_2 clkload35( .I (clknet_leaf_63_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69142
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__inv_2 clkload36( .I (clknet_leaf_49_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69143
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__inv_3 clkload37( .I (clknet_leaf_50_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69144
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__clkinv_8 clkload38( .I (clknet_leaf_53_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69145
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__clkinv_12 clkload39( .I (clknet_leaf_54_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69146
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__clkbuf_8 clkload4( .I (clknet_4_15__leaf_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69147
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__clkbuf_2 clkload40( .I (clknet_leaf_48_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69148
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__clkbuf_2 clkload41( .I (clknet_leaf_51_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69149
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__inv_4 clkload42( .I (clknet_leaf_52_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69150
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__inv_2 clkload43( .I (clknet_leaf_28_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69151
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__clkbuf_2 clkload44( .I (clknet_leaf_29_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69152
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__clkinv_2 clkload45( .I (clknet_leaf_30_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69153
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__clkinv_2 clkload46( .I (clknet_leaf_31_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69154
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__clkbuf_2 clkload47( .I (clknet_leaf_33_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69155
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__inv_4 clkload48( .I (clknet_leaf_34_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69156
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__inv_4 clkload49( .I (clknet_leaf_35_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69157
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__clkbuf_2 clkload5( .I (clknet_leaf_2_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69158
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__clkinv_2 clkload50( .I (clknet_leaf_37_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69159
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__inv_4 clkload51( .I (clknet_leaf_38_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69160
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__inv_2 clkload52( .I (clknet_leaf_41_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69161
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__clkinv_2 clkload53( .I (clknet_leaf_39_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69162
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__inv_2 clkload54( .I (clknet_leaf_40_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69163
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__inv_4 clkload55( .I (clknet_leaf_43_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69164
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__clkbuf_2 clkload6( .I (clknet_leaf_3_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69165
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__clkbuf_2 clkload7( .I (clknet_leaf_68_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69166
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__inv_8 clkload8( .I (clknet_leaf_73_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


Warning-[TFIPC] Too few instance port connections
ascon_core_adpt_encdec.nl.v, 69167
ascon_core_adpt_encdec, "gf180mcu_fd_sc_mcu7t5v0__clkinv_2 clkload9( .I (clknet_leaf_0_clk));"
  The above instance has fewer port connections than the module definition.
  Please use '+lint=TFIPC-L' to print out detailed information of unconnected 
  ports.


   ***   $sdf_annotate() version 1.2R
   ***    SDF file: "ascon_core_adpt_encdec.sdf"
   ***    Annotation scope: tb_ascon_verilog.u_dut
   ***    SDF Annotator log file: "MAXIMUM"
   ***    No MTM selection argument specified
   ***    No SCALE FACTORS argument specified
   ***    No SCALE TYPE argument specified
   ***    MTM selection defaulted to "TOOL_CONTROL":
               (+typdelays compiled, TYPICAL delays selected)
   ***    SCALE FACTORS defaulted to "1.0:1.0:1.0":
   ***    SCALE TYPE defaulted to: "FROM_MTM"
   ***    Turnoff delay: "FROM_FILE"
   ***    Approximation (mipd) policy: "MAXIMUM"

   ***    SDF annotation begin: Fri Jul  3 03:35:59 2026


SDF Info: +pulse_r/100, +pulse_e/100 in effect

Warning-[SDFCOM_UHICD] Up-hierarchy Interconnect Delay ignored
ascon_core_adpt_encdec.sdf, 18391
module: gf180mcu_fd_sc_mcu7t5v0__buf_2, "instance: tb_ascon_verilog.u_dut.output659"
  SDF Warning: INTERCONNECT Delay to up-hierarchy destination accOutput is 
  ignored, DEVICE Delay on port 'Z' applied.
  Up-hierarchy interconnect delay arises when the load is hierarchically above
  the source.


Warning-[SDFCOM_UHICD] Up-hierarchy Interconnect Delay ignored
ascon_core_adpt_encdec.sdf, 18392
module: gf180mcu_fd_sc_mcu7t5v0__dlyd_1, "instance: tb_ascon_verilog.u_dut.output660"
  SDF Warning: INTERCONNECT Delay to up-hierarchy destination accOutput is 
  ignored, DEVICE Delay on port 'Z' applied.
  Up-hierarchy interconnect delay arises when the load is hierarchically above
  the source.


Warning-[SDFCOM_UHICD] Up-hierarchy Interconnect Delay ignored
ascon_core_adpt_encdec.sdf, 18393
module: gf180mcu_fd_sc_mcu7t5v0__dlyd_1, "instance: tb_ascon_verilog.u_dut.output661"
  SDF Warning: INTERCONNECT Delay to up-hierarchy destination accOutput is 
  ignored, DEVICE Delay on port 'Z' applied.
  Up-hierarchy interconnect delay arises when the load is hierarchically above
  the source.


Warning-[SDFCOM_UHICD] Up-hierarchy Interconnect Delay ignored
ascon_core_adpt_encdec.sdf, 18394
module: gf180mcu_fd_sc_mcu7t5v0__buf_2, "instance: tb_ascon_verilog.u_dut.output662"
  SDF Warning: INTERCONNECT Delay to up-hierarchy destination accOutput is 
  ignored, DEVICE Delay on port 'Z' applied.
  Up-hierarchy interconnect delay arises when the load is hierarchically above
  the source.


Warning-[SDFCOM_UHICD] Up-hierarchy Interconnect Delay ignored
ascon_core_adpt_encdec.sdf, 18395
module: gf180mcu_fd_sc_mcu7t5v0__dlyd_1, "instance: tb_ascon_verilog.u_dut.output663"
  SDF Warning: INTERCONNECT Delay to up-hierarchy destination accOutput is 
  ignored, DEVICE Delay on port 'Z' applied.
  Up-hierarchy interconnect delay arises when the load is hierarchically above
  the source.


Warning-[SDFCOM_UHICD] Up-hierarchy Interconnect Delay ignored
ascon_core_adpt_encdec.sdf, 18396
module: gf180mcu_fd_sc_mcu7t5v0__dlyd_1, "instance: tb_ascon_verilog.u_dut.output664"
  SDF Warning: INTERCONNECT Delay to up-hierarchy destination accOutput is 
  ignored, DEVICE Delay on port 'Z' applied.
  Up-hierarchy interconnect delay arises when the load is hierarchically above
  the source.


Warning-[SDFCOM_UHICD] Up-hierarchy Interconnect Delay ignored
ascon_core_adpt_encdec.sdf, 18397
module: gf180mcu_fd_sc_mcu7t5v0__dlyd_1, "instance: tb_ascon_verilog.u_dut.output665"
  SDF Warning: INTERCONNECT Delay to up-hierarchy destination accOutput is 
  ignored, DEVICE Delay on port 'Z' applied.
  Up-hierarchy interconnect delay arises when the load is hierarchically above
  the source.


Warning-[SDFCOM_UHICD] Up-hierarchy Interconnect Delay ignored
ascon_core_adpt_encdec.sdf, 18398
module: gf180mcu_fd_sc_mcu7t5v0__dlyd_1, "instance: tb_ascon_verilog.u_dut.output666"
  SDF Warning: INTERCONNECT Delay to up-hierarchy destination accOutput is 
  ignored, DEVICE Delay on port 'Z' applied.
  Up-hierarchy interconnect delay arises when the load is hierarchically above
  the source.


Warning-[SDFCOM_UHICD] Up-hierarchy Interconnect Delay ignored
ascon_core_adpt_encdec.sdf, 18399
module: gf180mcu_fd_sc_mcu7t5v0__dlyd_1, "instance: tb_ascon_verilog.u_dut.output667"
  SDF Warning: INTERCONNECT Delay to up-hierarchy destination accOutput is 
  ignored, DEVICE Delay on port 'Z' applied.
  Up-hierarchy interconnect delay arises when the load is hierarchically above
  the source.

All future warnings not reported; use +sdfverbose to report them.
See also the log file: MAXIMUM

Warning-[SDFCOM_UHICD] Up-hierarchy Interconnect Delay ignored
ascon_core_adpt_encdec.sdf, 18400
module: gf180mcu_fd_sc_mcu7t5v0__dlyd_1, "instance: tb_ascon_verilog.u_dut.output668"
  SDF Warning: INTERCONNECT Delay to up-hierarchy destination accOutput is 
  ignored, DEVICE Delay on port 'Z' applied.
  Up-hierarchy interconnect delay arises when the load is hierarchically above
  the source.


          Total errors: 0
          Total warnings: 274
   ***    SDF annotation completed: Fri Jul  3 03:36:00 2026


Starting vcs inline pass...
257 modules and 4 UDPs read.
recompiling module tb_ascon_verilog
recompiling module ascon_core_adpt_encdec
recompiling module gf180mcu_fd_sc_mcu7t5v0__addf_1
recompiling module gf180mcu_fd_sc_mcu7t5v0__addf_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__addf_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__addf_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__addh_1
recompiling module gf180mcu_fd_sc_mcu7t5v0__addh_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__addh_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__addh_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__and2_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__and2_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__and2_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__and3_1
recompiling module gf180mcu_fd_sc_mcu7t5v0__and3_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__and3_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__and3_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__and4_1
recompiling module gf180mcu_fd_sc_mcu7t5v0__and4_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__and4_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__and4_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__antenna
recompiling module gf180mcu_fd_sc_mcu7t5v0__antenna_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__aoi21_1
recompiling module gf180mcu_fd_sc_mcu7t5v0__aoi21_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__aoi21_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__aoi21_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__aoi22_1
recompiling module gf180mcu_fd_sc_mcu7t5v0__aoi22_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__aoi22_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__aoi22_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__aoi211_1
recompiling module gf180mcu_fd_sc_mcu7t5v0__aoi211_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__aoi211_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__aoi211_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__aoi221_1
recompiling module gf180mcu_fd_sc_mcu7t5v0__aoi221_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__aoi221_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__aoi221_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__aoi222_1
recompiling module gf180mcu_fd_sc_mcu7t5v0__aoi222_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__aoi222_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__aoi222_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__buf_1
recompiling module gf180mcu_fd_sc_mcu7t5v0__buf_8
recompiling module gf180mcu_fd_sc_mcu7t5v0__bufz_1
recompiling module gf180mcu_fd_sc_mcu7t5v0__bufz_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__bufz_3
recompiling module gf180mcu_fd_sc_mcu7t5v0__bufz_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__bufz_8
50 of 257 modules done
recompiling module gf180mcu_fd_sc_mcu7t5v0__bufz_12
recompiling module gf180mcu_fd_sc_mcu7t5v0__bufz_16
recompiling module gf180mcu_fd_sc_mcu7t5v0__bufz_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__clkbuf_1
recompiling module gf180mcu_fd_sc_mcu7t5v0__clkbuf_3
recompiling module gf180mcu_fd_sc_mcu7t5v0__clkbuf_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__clkbuf_8
recompiling module gf180mcu_fd_sc_mcu7t5v0__clkbuf_12
recompiling module gf180mcu_fd_sc_mcu7t5v0__clkbuf_20
recompiling module gf180mcu_fd_sc_mcu7t5v0__clkinv_3
recompiling module gf180mcu_fd_sc_mcu7t5v0__clkinv_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__clkinv_8
recompiling module gf180mcu_fd_sc_mcu7t5v0__clkinv_16
recompiling module gf180mcu_fd_sc_mcu7t5v0__dffnq_1
recompiling module gf180mcu_fd_sc_mcu7t5v0__dffnq_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__dffnq_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__dffnq_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__dffnrnq_1
recompiling module gf180mcu_fd_sc_mcu7t5v0__dffnrnq_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__dffnrnq_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__dffnrnq_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__dffnrsnq_1
recompiling module gf180mcu_fd_sc_mcu7t5v0__dffnrsnq_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__dffnrsnq_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__dffnrsnq_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__dffnsnq_1
recompiling module gf180mcu_fd_sc_mcu7t5v0__dffnsnq_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__dffnsnq_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__dffnsnq_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__dffq_1
recompiling module gf180mcu_fd_sc_mcu7t5v0__dffq_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__dffq_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__dffq_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__dffrnq_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__dffrnq_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__dffrsnq_1
recompiling module gf180mcu_fd_sc_mcu7t5v0__dffrsnq_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__dffrsnq_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__dffrsnq_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__dffsnq_1
recompiling module gf180mcu_fd_sc_mcu7t5v0__dffsnq_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__dffsnq_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__dffsnq_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__dlya_1
recompiling module gf180mcu_fd_sc_mcu7t5v0__dlya_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__dlya_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__dlyb_1
recompiling module gf180mcu_fd_sc_mcu7t5v0__dlyb_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__dlyb_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__dlyc_1
100 of 257 modules done
recompiling module gf180mcu_fd_sc_mcu7t5v0__dlyc_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__dlyc_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__dlyd_1
recompiling module gf180mcu_fd_sc_mcu7t5v0__dlyd_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__dlyd_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__dlyd_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__endcap
recompiling module gf180mcu_fd_sc_mcu7t5v0__fill_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__fill_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__fill_8
recompiling module gf180mcu_fd_sc_mcu7t5v0__fill_16
recompiling module gf180mcu_fd_sc_mcu7t5v0__fill_32
recompiling module gf180mcu_fd_sc_mcu7t5v0__fill_64
recompiling module gf180mcu_fd_sc_mcu7t5v0__fillcap_8
recompiling module gf180mcu_fd_sc_mcu7t5v0__filltie
recompiling module gf180mcu_fd_sc_mcu7t5v0__filltie_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__hold
recompiling module gf180mcu_fd_sc_mcu7t5v0__hold_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__icgtn_1
recompiling module gf180mcu_fd_sc_mcu7t5v0__icgtn_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__icgtn_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__icgtn_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__icgtp_1
recompiling module gf180mcu_fd_sc_mcu7t5v0__icgtp_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__icgtp_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__icgtp_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__inv_1
recompiling module gf180mcu_fd_sc_mcu7t5v0__inv_8
recompiling module gf180mcu_fd_sc_mcu7t5v0__inv_16
recompiling module gf180mcu_fd_sc_mcu7t5v0__inv_20
recompiling module gf180mcu_fd_sc_mcu7t5v0__inv_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__invz_1
recompiling module gf180mcu_fd_sc_mcu7t5v0__invz_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__invz_3
recompiling module gf180mcu_fd_sc_mcu7t5v0__invz_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__invz_8
recompiling module gf180mcu_fd_sc_mcu7t5v0__invz_12
recompiling module gf180mcu_fd_sc_mcu7t5v0__invz_16
recompiling module gf180mcu_fd_sc_mcu7t5v0__invz_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__latq_1
recompiling module gf180mcu_fd_sc_mcu7t5v0__latq_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__latq_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__latq_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__latrnq_1
recompiling module gf180mcu_fd_sc_mcu7t5v0__latrnq_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__latrnq_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__latrnq_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__latrsnq_1
recompiling module gf180mcu_fd_sc_mcu7t5v0__latrsnq_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__latrsnq_4
150 of 257 modules done
recompiling module gf180mcu_fd_sc_mcu7t5v0__latrsnq_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__latsnq_1
recompiling module gf180mcu_fd_sc_mcu7t5v0__latsnq_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__latsnq_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__latsnq_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__mux2_1
recompiling module gf180mcu_fd_sc_mcu7t5v0__mux2_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__mux2_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__mux2_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__mux4_1
recompiling module gf180mcu_fd_sc_mcu7t5v0__mux4_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__mux4_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__mux4_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__nand2_1
recompiling module gf180mcu_fd_sc_mcu7t5v0__nand2_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__nand2_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__nand3_1
recompiling module gf180mcu_fd_sc_mcu7t5v0__nand3_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__nand3_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__nand3_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__nand4_1
recompiling module gf180mcu_fd_sc_mcu7t5v0__nand4_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__nand4_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__nand4_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__nor2_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__nor2_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__nor2_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__nor3_1
recompiling module gf180mcu_fd_sc_mcu7t5v0__nor3_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__nor3_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__nor3_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__nor4_1
recompiling module gf180mcu_fd_sc_mcu7t5v0__nor4_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__nor4_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__oai21_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__oai21_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__oai21_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__oai22_1
recompiling module gf180mcu_fd_sc_mcu7t5v0__oai22_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__oai22_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__oai22_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__oai31_1
recompiling module gf180mcu_fd_sc_mcu7t5v0__oai31_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__oai31_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__oai31_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__oai32_1
recompiling module gf180mcu_fd_sc_mcu7t5v0__oai32_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__oai32_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__oai32_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__oai33_1
200 of 257 modules done
recompiling module gf180mcu_fd_sc_mcu7t5v0__oai33_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__oai33_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__oai33_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__oai211_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__oai211_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__oai221_1
recompiling module gf180mcu_fd_sc_mcu7t5v0__oai221_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__oai221_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__oai221_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__oai222_1
recompiling module gf180mcu_fd_sc_mcu7t5v0__oai222_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__oai222_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__oai222_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__or2_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__or2_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__or2_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__or3_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__or3_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__or3_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__or4_1
recompiling module gf180mcu_fd_sc_mcu7t5v0__or4_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__or4_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__or4_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__sdffq_1
recompiling module gf180mcu_fd_sc_mcu7t5v0__sdffq_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__sdffq_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__sdffq_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__sdffrnq_1
recompiling module gf180mcu_fd_sc_mcu7t5v0__sdffrnq_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__sdffrnq_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__sdffrnq_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__sdffrsnq_1
recompiling module gf180mcu_fd_sc_mcu7t5v0__sdffrsnq_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__sdffrsnq_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__sdffrsnq_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__sdffsnq_1
recompiling module gf180mcu_fd_sc_mcu7t5v0__sdffsnq_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__sdffsnq_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__sdffsnq_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__tieh
recompiling module gf180mcu_fd_sc_mcu7t5v0__tieh_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__tiel
recompiling module gf180mcu_fd_sc_mcu7t5v0__tiel_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__xnor2_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__xnor2_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__xnor2_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__xnor3_1
recompiling module gf180mcu_fd_sc_mcu7t5v0__xnor3_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__xnor3_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__xnor3_func
250 of 257 modules done
recompiling module gf180mcu_fd_sc_mcu7t5v0__xor2_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__xor2_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__xor2_func
recompiling module gf180mcu_fd_sc_mcu7t5v0__xor3_1
recompiling module gf180mcu_fd_sc_mcu7t5v0__xor3_2
recompiling module gf180mcu_fd_sc_mcu7t5v0__xor3_4
recompiling module gf180mcu_fd_sc_mcu7t5v0__xor3_func
All of 257 modules done
rm -f _cuarc*.so _csrc*.so pre_vcsobj_*.so share_vcsobj_*.so
if [ -x ../simv ]; then chmod a-x ../simv; fi
g++  -o ../simv      -rdynamic  -Wl,-rpath='$ORIGIN'/simv.daidir -Wl,-rpath=./simv.daidir -Wl,-rpath=/apps/vcsmx/vcs/X-2025.06-SP1/linux64/lib -L/apps/vcsmx/vcs/X-2025.06-SP1/linux64/lib  -Wl,-rpath-link=./   objs/amcQw_d.o  _254_archive_1.so objs/udps/qzQ2U.o objs/udps/J6yjv.o objs/udps/Iq9kf.o objs/udps/s6J8P.o  SIM_l.o       rmapats_mop.o rmapats.o rmar.o rmar_nd.o  rmar_llvm_0_1.o rmar_llvm_0_0.o            -lvirsim -lerrorinf -lsnpsmalloc -lvfs      -lvcsnew -ldistsimclient -lsimprofile -luclinative /apps/vcsmx/vcs/X-2025.06-SP1/linux64/lib/vcs_tls.o   -Wl,-whole-archive  -lvcsucli    -Wl,-no-whole-archive          /apps/vcsmx/vcs/X-2025.06-SP1/linux64/lib/vcs_save_restore_new.o -ldl  -lc -lm -lpthread -ldl 
../simv up to date
CPU time: 9.480 seconds to compile + 2.371 seconds to elab + 4.056 seconds to link
Chronologic VCS simulator copyright 1991-2025
Contains Synopsys proprietary information.
Compiler version X-2025.06-SP1_Full64; Runtime version X-2025.06-SP1_Full64;  Jul  3 03:36 2026
Doing SDF annotation ...... Done
------------------------------------------------------------
TEST 1: Empty AD, Empty PT (key=0, nonce=0)
------------------------------------------------------------
[PASS] Test 1: Tag matches golden reference
  t0_out = 0x90f0fbf991dae8f1 (expected 0x90f0fbf991dae8f1)
  t1_out = 0xae1bd9ca7ce3f3ca (expected 0xae1bd9ca7ce3f3ca)

------------------------------------------------------------
TEST 2: Empty AD, 5-byte PT 'Hello'
------------------------------------------------------------
[PASS] Test 2: CT and Tag match golden reference
  CT (5 bytes) = 0xb9e6bc14af (expected 0xb9e6bc14af)
  t0_out = 0xdc9d3fa63a8c58b6 (expected 0xdc9d3fa63a8c58b6)
  t1_out = 0xb058f365f5f50c5a (expected 0xb058f365f5f50c5a)

------------------------------------------------------------
TEST 3: Encrypt-then-Decrypt roundtrip of Test 2
------------------------------------------------------------
  Step A: Using encrypted CT = 0xb9e6bc14af, tag0=0xdc9d3fa63a8c58b6, tag1=0xb058f365f5f50c5a
[PASS] Test 3: Decrypt roundtrip successful
  Recovered PT (5 bytes) = 0x6f6c6c6548 (expected 0x6f6c6c6548 = 'Hello')
  auth_ok = 1 (expected 1)

------------------------------------------------------------
TEST 4: 8-byte AD ('metadata'), 6-byte PT ('secret')
------------------------------------------------------------
[PASS] Test 4: CT and Tag match golden reference
  CT (6 bytes) = 0x7f95de8f180e (expected 0x7f95de8f180e)
  t0_out = 0x9acf10c942363add (expected 0x9acf10c942363add)
  t1_out = 0x987a35ce66cff532 (expected 0x987a35ce66cff532)

------------------------------------------------------------
TEST 5: Multi-block Encrypt - 13B AD, 40B PT (nonce != key)
------------------------------------------------------------
[PASS] Test 5: All CT blocks and Tag match
  t0_out = 0x82fecae37f5d2aa2 (expected 0x82fecae37f5d2aa2)
  t1_out = 0x0730f873e48e057a (expected 0x0730f873e48e057a)

------------------------------------------------------------
TEST 6: Multi-block Decrypt (correct tag, auth_ok=1)
------------------------------------------------------------
[PASS] Test 6: All PT blocks recovered, auth_ok=1

------------------------------------------------------------
TEST 7: Tampered-tag Decrypt (auth_ok must be 0)
------------------------------------------------------------
[PASS] Test 7: Tampered tag correctly rejected (auth_ok=0)

============================================================
TEST SUMMARY: 7 PASSED, 0 FAILED out of 7 tests
============================================================
>>> ALL TESTS PASSED <<<
$finish called from file "testbench.sv", line 739.
$finish at simulation time             24980000
           V C S   S i m u l a t i o n   R e p o r t 
Time: 24980000 ps
CPU Time:      5.140 seconds;       Data structure size:   3.6Mb
Fri Jul  3 03:36:18 2026
Done
```

---


## ICarus Verilog based GLS (No SDF)

<img width="667" height="893" alt="image" src="https://github.com/user-attachments/assets/c4e763b7-b308-4464-984f-1abf53a6d139" />

---

## Coco tb based timing aware gate level simulation attempt

We attempted to run Timing-Aware Gate-Level Simulation (GLS) with a Python-based cocotb testbench to increase verification functional coverage. so, created a script to dynamically load the netlist, SDF timing files, and Python tests from this GitHub Repo into EDA Playground using the Synopsys VCS simulator.

However, this failed because EDA Playground's security sandbox completely blocks the background connections (VPI shared libraries) needed for Python and VCS to communicate. Therefore, running cocotb-based timing simulations is not feasible when sticking strictly to freesource/opensource, cloud-based tools like EDA Playground.
