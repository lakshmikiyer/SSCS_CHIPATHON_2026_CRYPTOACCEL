### output log as of jun 9, 2026. compiler: synopsys vcs 2025.06
### link to demo: https://www.edaplayground.com/x/Vjk5
```
[2026-06-09 15:48:59 UTC] vcs -full64 -licqueue '-timescale=1ns/1ns' '+vcs+flush+all' '+warn=all' '-sverilog' design.sv testbench.sv  && ./simv +vcs+lic+wait  
                         Chronologic VCS (TM)
       Version X-2025.06-SP1_Full64 -- Tue Jun  9 11:49:01 2026

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

Parsing design file 'design.sv'
Parsing design file 'testbench.sv'
Top Level Modules:
       tb_ascon_verilog
TimeScale is 1 ns / 1 ps
Starting vcs inline pass...
1 module and 0 UDP read.
recompiling module tb_ascon_verilog
rm -f _cuarc*.so _csrc*.so pre_vcsobj_*.so share_vcsobj_*.so
if [ -x ../simv ]; then chmod a-x ../simv; fi
g++  -o ../simv      -rdynamic  -Wl,-rpath='$ORIGIN'/simv.daidir -Wl,-rpath=./simv.daidir -Wl,-rpath=/apps/vcsmx/vcs/X-2025.06-SP1/linux64/lib -L/apps/vcsmx/vcs/X-2025.06-SP1/linux64/lib  -Wl,-rpath-link=./   objs/amcQw_d.o  _287_archive_1.so  SIM_l.o       rmapats_mop.o rmapats.o rmar.o rmar_nd.o  rmar_llvm_0_1.o rmar_llvm_0_0.o            -lvirsim -lerrorinf -lsnpsmalloc -lvfs      -lvcsnew -ldistsimclient -lsimprofile -luclinative /apps/vcsmx/vcs/X-2025.06-SP1/linux64/lib/vcs_tls.o   -Wl,-whole-archive  -lvcsucli    -Wl,-no-whole-archive          /apps/vcsmx/vcs/X-2025.06-SP1/linux64/lib/vcs_save_restore_new.o -ldl  -lc -lm -lpthread -ldl 
../simv up to date
CPU time: .946 seconds to compile + .630 seconds to elab + .812 seconds to link
Chronologic VCS simulator copyright 1991-2025
Contains Synopsys proprietary information.
Compiler version X-2025.06-SP1_Full64; Runtime version X-2025.06-SP1_Full64;  Jun  9 11:49 2026
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

============================================================
TEST SUMMARY: 4 PASSED, 0 FAILED out of 4 tests
============================================================
>>> ALL TESTS PASSED <<<
$finish called from file "testbench.sv", line 544.
$finish at simulation time              1685000
           V C S   S i m u l a t i o n   R e p o r t 
Time: 1685000 ps
CPU Time:      0.580 seconds;       Data structure size:   0.0Mb
Tue Jun  9 11:49:04 2026
Finding VCD file...
./tb_ascon_verilog.vcd
[2026-06-09 15:49:05 UTC] Opening EPWave...
```
