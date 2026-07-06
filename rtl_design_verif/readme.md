# RTL Design & Verification Stage
---
## RTL Design
- Design of the Ascon Core, AXI Master & Slave - completed by Lakshmi
- Design of SPI completed 
- Verification of SPI - Librelane verification in progress (Tested & verified in Vivado)

## Verification of the Design.

### Verification of the ASCON Core

#### 1] Verilog based TB: (completed by yash, jun 9 2026)
- a standard verilog based testbench was developed to feed stimulus to the design and test different possible cases of the ASCON core's functionality.
- the design has been tested against a total of 7 cases: (1-4 from yash's TB, 5-7 later adopted from lakshmi's TB)

##### 7 test cases:
- Test 1: Empty AD, empty PT (key=0, nonce=0)
- Test 2: Empty AD, 5-byte PT "Hello" (key=000102...0f, nonce=same)
- Test 3: Encrypt-then-decrypt roundtrip of Test 2
- Test 4: 8-byte AD ("metadata"), 6-byte PT ("secret") (key=000102...0f, nonce=same)
- Test 5: Multi-block Encrypt -- 13B AD ("header-data!!"), 40B PT (nonce != key)
- Test 6: Multi-block Decrypt -- same vectors as Test 5, correct tag, auth_ok=1
- Test 7: Tampered-tag Decrypt -- 1 bit flipped in tag, auth_ok must be 0

the design passes all 7 cases. 
the same was verilog tb was used in Timing Aware simulation at the gate level (post-synthesis).

- working environment: https://www.edaplayground.com/x/Vjk5
- compiler log:
```
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
$finish called from file "testbench.sv", line 740.
$finish at simulation time             15060000
```
---

#### 2] Coco-TB based TB: (completed by yash, jun 9 2026)
- to add to the verification coverage and more constrainted randomization, a coco-tb based testbench was also developed and used to verify the design of the core.
- It uses a cycle-accurate Python golden reference model to automatically verify the hardware outputs.

- The test cases are:
- **Category A: Directed Known-Answer Tests (KATs)**: A group of tests driving fixed inputs to check if the core produces the exact expected ciphertext and tags.
- **Category B: Boundary Edge Cases**: Testing plaintext and AD lengths that fall exactly on, just before, and just after the 128-bit (16-byte) block boundaries (e.g., 1, 15, 16, and 17 bytes).
- **Category C: Authentication Fault Injection (Security Testing)**: Deliberately feeding the core tampered ciphertexts and corrupted authentication tags during decryption, to check if core can detect malicious forgery or data manipulation and correctly drives the `auth_ok` signal to 0, safeguarding data.
- **Category D: Randomized Encryption Sweep**: Generating 50 completely random combinations of Keys, Nonces, Associated Data, and Plaintexts (varying from 0 to 256 bytes in length). The hardware output is checked against the Python golden model.
- **Category E: Randomized Encrypt-then-Decrypt Roundtrip**: Running 20 random cycles where a random message is encrypted by the core, and the resulting ciphertext and tag are immediately fed back into the core for decryption. 

The core successfully passed all randomized and edge-case Cocotb tests, ensuring robust functional coverage. \

- compiler: icarus verilog 12.0
- working environment: https://www.edaplayground.com/x/K_Fn
- Complier log:

```

[2026-06-09 15:41:58 UTC] export SIM=icarus; python3 testbench.py 
     -.--ns INFO     gpi                                ..mbed/gpi_embed.cpp:78   in set_program_name_in_venv        Did not detect Python virtual environment. Using system-wide Python interpreter
     -.--ns INFO     gpi                                ../gpi/GpiCommon.cpp:101  in gpi_print_registered_impl       VPI registered
     0.00ns INFO     cocotb                             Running on Icarus Verilog version 12.0 (stable)
     0.00ns INFO     cocotb                             Running tests with cocotb v1.8.1 from /usr/local/lib64/python3.6/site-packages/cocotb
     0.00ns INFO     cocotb                             Seeding Python random module with 1781019720
     0.00ns INFO     cocotb.regression                  pytest not found, install it to enable better AssertionError messages
     0.00ns INFO     cocotb.regression                  Found test testbench.test_enc_empty_ad_empty_pt
     0.00ns INFO     cocotb.regression                  Found test testbench.test_enc_empty_ad_short_pt
     0.00ns INFO     cocotb.regression                  Found test testbench.test_enc_empty_ad_one_block
     0.00ns INFO     cocotb.regression                  Found test testbench.test_enc_empty_ad_multi_block
     0.00ns INFO     cocotb.regression                  Found test testbench.test_enc_short_ad_short_pt
     0.00ns INFO     cocotb.regression                  Found test testbench.test_enc_multi_ad_multi_pt
     0.00ns INFO     cocotb.regression                  Found test testbench.test_dec_valid_tag
     0.00ns INFO     cocotb.regression                  Found test testbench.test_dec_invalid_tag
     0.00ns INFO     cocotb.regression                  Found test testbench.test_dec_tampered_ct
     0.00ns INFO     cocotb.regression                  Found test testbench.test_enc_1byte_pt
     0.00ns INFO     cocotb.regression                  Found test testbench.test_enc_15byte_pt
     0.00ns INFO     cocotb.regression                  Found test testbench.test_enc_16byte_pt
     0.00ns INFO     cocotb.regression                  Found test testbench.test_enc_17byte_pt
     0.00ns INFO     cocotb.regression                  Found test testbench.test_enc_max_ad_bytes
     0.00ns INFO     cocotb.regression                  Found test testbench.test_random_encrypt
     0.00ns INFO     cocotb.regression                  Found test testbench.test_random_encrypt_decrypt_roundtrip
     0.00ns INFO     cocotb.regression                  running test_enc_empty_ad_empty_pt (1/16)
   380.00ns INFO     cocotb                             [PASS] enc_empty_ad_empty_pt
   380.00ns INFO     cocotb                               CT  = (empty)
   380.00ns INFO     cocotb                               Tag = 0x90f0fbf991dae8f1_ae1bd9ca7ce3f3ca
   380.00ns INFO     cocotb.regression                  test_enc_empty_ad_empty_pt passed
   380.00ns INFO     cocotb.regression                  running test_enc_empty_ad_short_pt (2/16)
   770.00ns INFO     cocotb                             [PASS] enc_empty_ad_short_pt
   770.00ns INFO     cocotb                               CT  = af18
   770.00ns INFO     cocotb                               Tag = 0x67fd66dd976682bd_7665eacd3491bb16
   770.00ns INFO     cocotb.regression                  test_enc_empty_ad_short_pt passed
   770.00ns INFO     cocotb.regression                  running test_enc_empty_ad_one_block (3/16)
  1160.00ns INFO     cocotb                             [PASS] enc_empty_ad_one_block
  1160.00ns INFO     cocotb                               CT  = ad53ec51d0e3e5f182df2dbc75ab5e0a
  1160.00ns INFO     cocotb                               Tag = 0xc70a185e2dafe413_218d8dc2bfb5ae39
  1160.00ns INFO     cocotb.regression                  test_enc_empty_ad_one_block passed
  1160.00ns INFO     cocotb.regression                  running test_enc_empty_ad_multi_block (4/16)
  1730.00ns INFO     cocotb                             [PASS] enc_empty_ad_multi_block
  1730.00ns INFO     cocotb                               CT  = 9da1452e86dbb69f888435fe33f74415ca72b28a14b350f6f48d5ccff59801dbf58ca5879d91f8a362ab71bb458c9d30
  1730.00ns INFO     cocotb                               Tag = 0xaf36d1ca122ec3fc_990c7bf23a8768e2
  1730.00ns INFO     cocotb.regression                  test_enc_empty_ad_multi_block passed
  1730.00ns INFO     cocotb.regression                  running test_enc_short_ad_short_pt (5/16)
  2200.00ns INFO     cocotb                             [PASS] enc_short_ad_short_pt
  2200.00ns INFO     cocotb                               CT  = 620d139f5417ce5677ca
  2200.00ns INFO     cocotb                               Tag = 0xf620d0af1da8bf2b_9afc6373069ea085
  2200.01ns INFO     cocotb.regression                  test_enc_short_ad_short_pt passed
  2200.01ns INFO     cocotb.regression                  running test_enc_multi_ad_multi_pt (6/16)
  3120.01ns INFO     cocotb                             [PASS] enc_multi_ad_multi_pt
  3120.01ns INFO     cocotb                               CT  = 42710a9da483962617430bdc5d9df32db62a00527859f77cb5b1f23d75fe34088a9f0e69105b61fc77aead7f6fcec8f4
  3120.01ns INFO     cocotb                               Tag = 0x6378831a61b13798_d743ddb3112105c0
  3120.01ns INFO     cocotb.regression                  test_enc_multi_ad_multi_pt passed
  3120.01ns INFO     cocotb.regression                  running test_dec_valid_tag (7/16)
  3590.01ns INFO     cocotb                             [PASS] dec_valid_tag (encrypt phase)
  3590.01ns INFO     cocotb                               CT  = 620d139f5417ce5677ca
  3590.01ns INFO     cocotb                               Tag = 0xf620d0af1da8bf2b_9afc6373069ea085
  4060.01ns INFO     cocotb                             [PASS] dec_valid_tag: auth_ok=1, PT recovered correctly
  4060.01ns INFO     cocotb.regression                  test_dec_valid_tag passed
  4060.01ns INFO     cocotb.regression                  running test_dec_invalid_tag (8/16)
  4530.01ns INFO     cocotb                             [PASS] dec_invalid_tag: auth_ok=0 (tampered tag correctly rejected)
  4530.01ns INFO     cocotb.regression                  test_dec_invalid_tag passed
  4530.01ns INFO     cocotb.regression                  running test_dec_tampered_ct (9/16)
  5000.01ns INFO     cocotb                             [PASS] dec_tampered_ct: auth_ok=0 (tampered CT correctly rejected)
  5000.01ns INFO     cocotb.regression                  test_dec_tampered_ct passed
  5000.01ns INFO     cocotb.regression                  running test_enc_1byte_pt (10/16)
  5390.01ns INFO     cocotb                             [PASS] enc_1byte_pt
  5390.01ns INFO     cocotb                               CT  = 3f
  5390.01ns INFO     cocotb                               Tag = 0x023ec50a938ce680_ffb94671700d9cea
  5390.01ns INFO     cocotb.regression                  test_enc_1byte_pt passed
  5390.01ns INFO     cocotb.regression                  running test_enc_15byte_pt (11/16)
  5780.01ns INFO     cocotb                             [PASS] enc_15byte_pt
  5780.01ns INFO     cocotb                               CT  = bea76cac83ae6f8f4e1baccd3317f6
  5780.01ns INFO     cocotb                               Tag = 0x3c81ba0700a72ffa_5b50ead41f18af45
  5780.01ns INFO     cocotb.regression                  test_enc_15byte_pt passed
  5780.01ns INFO     cocotb.regression                  running test_enc_16byte_pt (12/16)
  6170.01ns INFO     cocotb                             [PASS] enc_16byte_pt
  6170.01ns INFO     cocotb                               CT  = ad53ec51d0e3e5f182df2dbc75ab5e0a
  6170.01ns INFO     cocotb                               Tag = 0xc70a185e2dafe413_218d8dc2bfb5ae39
  6170.01ns INFO     cocotb.regression                  test_enc_16byte_pt passed
  6170.01ns INFO     cocotb.regression                  running test_enc_17byte_pt (13/16)
  6650.01ns INFO     cocotb                             [PASS] enc_17byte_pt
  6650.01ns INFO     cocotb                               CT  = 89011560cfe924ca32d9e6c97b33ca6d73
  6650.01ns INFO     cocotb                               Tag = 0xae605530fcaad981_32195df9ffce2a39
  6650.01ns INFO     cocotb.regression                  test_enc_17byte_pt passed
  6650.01ns INFO     cocotb.regression                  running test_enc_max_ad_bytes (14/16)
  7120.01ns INFO     cocotb                             [PASS] enc_ad_1bytes
  7120.01ns INFO     cocotb                               CT  = 35a8dff8
  7120.01ns INFO     cocotb                               Tag = 0xe74f1fcef032059a_8392c2c53ed8adff
  7590.01ns INFO     cocotb                             [PASS] enc_ad_2bytes
  7590.01ns INFO     cocotb                               CT  = f04fd423
  7590.01ns INFO     cocotb                               Tag = 0x7267b7250671264c_3377eec80eb5fd7b
  8060.01ns INFO     cocotb                             [PASS] enc_ad_3bytes
  8060.01ns INFO     cocotb                               CT  = 01a8809c
  8060.01ns INFO     cocotb                               Tag = 0x1e0a5451f33c535d_33e1d468fcd0c2e4
  8530.01ns INFO     cocotb                             [PASS] enc_ad_4bytes
  8530.01ns INFO     cocotb                               CT  = 10230701
  8530.01ns INFO     cocotb                               Tag = 0x7f89251077c79ac0_f52c9105bebca4c2
  9000.01ns INFO     cocotb                             [PASS] enc_ad_5bytes
  9000.01ns INFO     cocotb                               CT  = 5c5f12ea
  9000.01ns INFO     cocotb                               Tag = 0x8f168247fcc9fd1a_2f9990b4fb3628cc
  9470.01ns INFO     cocotb                             [PASS] enc_ad_6bytes
  9470.01ns INFO     cocotb                               CT  = 489637e8
  9470.01ns INFO     cocotb                               Tag = 0x181b94a9b63dd0a8_d1da0c5e991fe849
  9940.01ns INFO     cocotb                             [PASS] enc_ad_7bytes
  9940.01ns INFO     cocotb                               CT  = ce1ca08a
  9940.01ns INFO     cocotb                               Tag = 0x847fbd1b2acf0289_45da12aecc7ff811
 10410.01ns INFO     cocotb                             [PASS] enc_ad_8bytes
 10410.01ns INFO     cocotb                               CT  = 295ea70f
 10410.01ns INFO     cocotb                               Tag = 0x7339b1e7cfb8a44f_d26c3c51b789bc9c
 10880.01ns INFO     cocotb                             [PASS] enc_ad_9bytes
 10880.01ns INFO     cocotb                               CT  = a0f890c2
 10880.01ns INFO     cocotb                               Tag = 0x0ff6492199e5c33b_780c20531e01a54e
 11350.01ns INFO     cocotb                             [PASS] enc_ad_10bytes
 11350.01ns INFO     cocotb                               CT  = 8c7ba1ae
 11350.01ns INFO     cocotb                               Tag = 0xe41ee9686f7dfc11_d0a95974599bb851
 11820.01ns INFO     cocotb                             [PASS] enc_ad_11bytes
 11820.01ns INFO     cocotb                               CT  = 16d2a61d
 11820.01ns INFO     cocotb                               Tag = 0x81e704a16cec08ce_d718ab36d2e0038f
 12290.01ns INFO     cocotb                             [PASS] enc_ad_12bytes
 12290.01ns INFO     cocotb                               CT  = bd67a901
 12290.01ns INFO     cocotb                               Tag = 0x8eaaa393e4b7e94a_2fd09ae7f9358d95
 12760.01ns INFO     cocotb                             [PASS] enc_ad_13bytes
 12760.01ns INFO     cocotb                               CT  = 284ac76d
 12760.01ns INFO     cocotb                               Tag = 0x2fb35ac8c9f5b055_5254de9dc938c5da
 13230.01ns INFO     cocotb                             [PASS] enc_ad_14bytes
 13230.01ns INFO     cocotb                               CT  = c73424e1
 13230.01ns INFO     cocotb                               Tag = 0xf62fc042d5f9b078_e47c3442e0e33368
 13700.01ns INFO     cocotb                             [PASS] enc_ad_15bytes
 13700.01ns INFO     cocotb                               CT  = c213b473
 13700.01ns INFO     cocotb                               Tag = 0x179d574c6e2022f0_1f9ec8a75b61e238
 14260.01ns INFO     cocotb                             [PASS] enc_ad_16bytes
 14260.01ns INFO     cocotb                               CT  = c9ce9dc8
 14260.01ns INFO     cocotb                               Tag = 0x9c763387f60aef14_74ab8843c5c54e9d
 14260.01ns INFO     cocotb                             [PASS] enc_max_ad_bytes: All AD lengths 1-16 passed
 14260.01ns INFO     cocotb.regression                  test_enc_max_ad_bytes passed
 14260.01ns INFO     cocotb.regression                  running test_random_encrypt (15/16)
 16350.01ns INFO     cocotb                             [PASS] random_enc_0
 16350.01ns INFO     cocotb                               CT  = 417da1b47729e3c924e126dd79c43a7df66f3d83a5e7fc9bc18a5606ef3115f6c9e63bbc951a775f95075c24dde7ce95bdb2a5d99aa2c3cdb562b361b526d1e58d0254e8a8139c732338dc3404726921ff32b0e974e94b5a615ee481d3c3130ac442ee8b074bfe4f0228dc136c2ed0a6aeddc2547a4598a666535350
 16350.01ns INFO     cocotb                               Tag = 0x2a83d19b0c91db20_00988cdec8a63f0d
 17630.01ns INFO     cocotb                             [PASS] random_enc_1
 17630.01ns INFO     cocotb                               CT  = 5bfe52e968eb253a7cd6b0220ffea01242ebe79dd1df4fe8687387b37f19b13eaaf9b07e300b199996652acb3b502edf15ac8244a1cf65b1060a9ac0063126a322fb88312eebb1515ce26a4b2b85d06a7c83e8adc9d6f477867335366b42486ea70f5f39c5f35121a4c39f
 17630.01ns INFO     cocotb                               Tag = 0x55b716ddd63292d5_7295042c6151aa3e
 19990.01ns INFO     cocotb                             [PASS] random_enc_2
 19990.01ns INFO     cocotb                               CT  = 1ed222e21dc20a95b1f2172c820d085ef289e1be0c7aee47e354bfc96f5ff7a5b0300a089bce3cacd3406952308c4142ecf1b8d703be09f2fd8f41c20d555f70f96b08c35afeec4e408729ed7b3b6690528bebb7273ff1a6ad053f313edeeaa54fb708f77b1850da91be6fcaafb378a1a89f1e3b33a833de14f91e4d213d0889c86d22a790b3c31a592fda81a770c0
 19990.01ns INFO     cocotb                               Tag = 0x4e33830df0079f72_5ea7f0d9c6e9287f
 21990.01ns INFO     cocotb                             [PASS] random_enc_3
 21990.01ns INFO     cocotb                               CT  = e6c2c6fdb129dd9de58b8fc1dd796e4b342027a68dff1081f1c0168174f25eb45f4a
 21990.01ns INFO     cocotb                               Tag = 0xc7ed373ef65e1f2a_61f3fda696fe4ec6
 24080.01ns INFO     cocotb                             [PASS] random_enc_4
 24080.01ns INFO     cocotb                               CT  = 8938a43686ec6a309ad07b9be7c2f9164c575e87dcf36c261a2f35fbbe848b449270eefb9b03e60e9eb0ab12e59b0c565675b07dd095d3891b3e81689f84bfcc75a0e35caba1b6317b85f5a9184fbee17adcfafbb274a82289bb3dd55a1c2df546a66103f4569b6207feddd032b6c1348d436a29e05ebffcef617d126c19ed8ad8438bfe680fcd489b6f03c978fe02962562c0ffe2145b4cfef0e78feb7a6b23236c2451c58a62a31651767358d5745037f30905701144701fab5de839e291841023ff0f5172d3280397acd9ef6f2a24bbb689221477a799f168728c37c25151a639e30e
 24080.01ns INFO     cocotb                               Tag = 0x8aa74253ac0fa3b2_8a75ee2c16f39302
 25720.01ns INFO     cocotb                             [PASS] random_enc_5
 25720.01ns INFO     cocotb                               CT  = c3673081b36d7df8fc35a68866ff0871344d7e720b83d49586447c88515316cb4fce58efce9891dce0622ac86c7af045b36251214f1976950fcb42b66eb72cb875b6ac30ab66863e5672f3fb5b8c345f6b07cd3ecaf69f9ea7b22f5b1d13b9d8b495f6d9a9dc06760bd4130d78f27b9e43587d53ac25ee484da2764ec3b1869131e932c51e9fef15915044929e3c
 25720.01ns INFO     cocotb                               Tag = 0x2520d227fd8cc33f_be895a82ac4aab08
 27180.01ns INFO     cocotb                             [PASS] random_enc_6
 27180.01ns INFO     cocotb                               CT  = 42265a8084ee7b709d13ec80535ab17c44b37c035e8992af1909b675168419ba0d2eb37a074a60ab703206628ec95ada28762e
 27180.01ns INFO     cocotb                               Tag = 0xa4ce47a625dffad3_ebb6533d0f266d7a
 29900.01ns INFO     cocotb                             [PASS] random_enc_7
 29900.01ns INFO     cocotb                               CT  = e17e3011d2d1039f9a5828d6861dfa4d00f2930fefe9bfde1ac53c907f0e39b8f4ac16389ecdea56e6c61ea04f8a0971574123734261dd2f1eaa23f4bb8f3cde7b1b4bcb9450fac68edfaf2685ac7e4d966a2ac24072b0cc622dd153168a29a471c288b35cc52bc21a87dd9f9e418a673f9cf9bf89191bfbc104babd8c339ea51672eedcca8541960427cddfc966ffb675812510cc0c74af9a6c80f5fc4979b9a2808f56
 29900.01ns INFO     cocotb                               Tag = 0x5c4f76c7fd45fb41_6d19e3d4edbc3132
 31540.01ns INFO     cocotb                             [PASS] random_enc_8
 31540.01ns INFO     cocotb                               CT  = 4bd13e41c1285c0ff210dbd0e9d59c8480ca0800fd64df5e4ce50d0abe04a00e13d524dbf712f581e5a3b858cbc0be9dc5b888be7ed290504627bbf4d64184961616adf8ea94ff0a1dbba47ab14dbbe63b1eccf6d96d6c1c6f05762b28dee18fb2197e30e378049cea5ce17c090c2d972f06f43dd166fecacead6bf1914998bf0ea05376fa6a4db63e48681ad2789dc53fcc3c39048607c18166a4761b6ee1f1d4bcd635e11c5fc8810dbacae5eef4f2037414370b4ad5bc7b2e556d98828694ad
 31540.01ns INFO     cocotb                               Tag = 0x64b2b96ee30a5017_44f165141eb52b33
 33810.01ns INFO     cocotb                             [PASS] random_enc_9
 33810.01ns INFO     cocotb                               CT  = a4c7eee2c9adf7b9d27fd86a141b138a6bbe57d1ec37ea27687a8bfadbd00b0e95a0e757580412d7b0296e47ca0828af0878056912e76f91f37a5b95e65654209d19819f72f09637301f26c73ee752e8fd57f4382887fe3fe8d05c4ca2ea5e61f882173b3afee87ca6154f7fcc941629b9ed5dfb70f3a680fb7d71bf07c44485044d9c01b5cd4a1e97b4ed59f35389fde6422d5d09
 33810.01ns INFO     cocotb                               Tag = 0xdcc7dbcef12d5bfc_7dd0304ea0ba60e6
 35630.01ns INFO     cocotb                             [PASS] random_enc_10
 35630.01ns INFO     cocotb                               CT  = f79c623b64a1140633ab195e342283448d6308168b088ce9abdf18bd0ced5e76d094d13469f42aa6e1d869280f3463066dc8da9b3e6f598db2dbf380c453cc5a8ac6372a1441f8838d27481b29a3dd65774f85be1f375f431a4178245dff5c
 35630.01ns INFO     cocotb                               Tag = 0x077342369da73900_a0ef98e9e0c61341
 37630.01ns INFO     cocotb                             [PASS] random_enc_11
 37630.01ns INFO     cocotb                               CT  = fdde6cc369bf5f3097b3962d658ea9f2321adc84f9a22f4bbc401c04c62f5413097c478775f1cc51761be32a0b331971e77915cabbcb612864d9df05ada01905282b42a4ae2a7fc97af7bd0a7d94a48cefa0c0b55ab8e204250a920eaa138672f3e11a04
 37630.01ns INFO     cocotb                               Tag = 0xf1e33007d4f1ca75_921939f64c3e804f
 39450.01ns INFO     cocotb                             [PASS] random_enc_12
 39450.01ns INFO     cocotb                               CT  = 45a50817ade6636e69fc38964ff9e5e11f496af75c2618cdc751778eb2d4cdef1d2544ccdfbd6b16bde1fef4bbc721
 39450.01ns INFO     cocotb                               Tag = 0x465308ab2c66a3a7_a8850e14713b7eaf
 41270.01ns INFO     cocotb                             [PASS] random_enc_13
 41270.01ns INFO     cocotb                               CT  = de7bf30c248966e65501fad022d1ebc526c5345394d00511f6146e0b338724a8c24bfc0c276e5e763b37aec83f70fe52693c0e98e823813dc546837d6303fd07f4cf11e4537ce22c22a4a058c3b9839d775b0ec9fdf2ea345d5e93189f924e357db70e20203f2f7e012fc82cfb1a5ae76667b6fa
 41270.01ns INFO     cocotb                               Tag = 0x7736f3f86d251db4_22fcabe1f401ace7
 43450.01ns INFO     cocotb                             [PASS] random_enc_14
 43450.01ns INFO     cocotb                               CT  = 4a8b5e706c2cc13b87c947dd3861146cf04be41b9434720371ec2103a750a186cf787a7b24e48ea2096627fb68e497722a822c98cf1864b135949a56566d547a282c0e1e59a87048ae9af55a5d2fdc56ba467f10495e4fd348512f4af40684ba369180a3c09b74537b4ff134f67508687517dd62415dd7dc9a5df47a51dc132fe8d1adca2eeda76d4dc665791148012059db108ea333508725993f233270fc
 43450.01ns INFO     cocotb                               Tag = 0xf9fe433d4e364346_cd4102f18a2895f7
 44010.01ns INFO     cocotb                             [PASS] random_enc_15
 44010.01ns INFO     cocotb                               CT  = b604a5c4174b248480b9365ddf28f88095
 44010.01ns INFO     cocotb                               Tag = 0xeba51a2c6505d15b_732327ba7c447698
 46370.01ns INFO     cocotb                             [PASS] random_enc_16
 46370.01ns INFO     cocotb                               CT  = af3d80745c8505a120c7dd09364562347c5dd421ff9007e234c2b7bff43ef61218dda39e3a22fcf5e5bde63b4b4508926a3345ce9828ae52e7851ee90e8b13743ca3c7b2ba9b6549c8ca8561947469228a0e6417d06b48a6b4ab70ce47bc981eadd0ba3df8f12a9577fdbc7d72fc5d570f76e7fa91433c8b26403311a086ac0f15e306d6119981886e37fe45bb81bde3ce63248280f195c34c324efd8b76b3a064d94184875620a438bbcce8b26270077f9e7639dda547cc91b1919cd1fe805b
 46370.01ns INFO     cocotb                               Tag = 0x4e7641ba1c22d6ad_57ea14ea6fd92b12
 48640.01ns INFO     cocotb                             [PASS] random_enc_17
 48640.01ns INFO     cocotb                               CT  = 75d1b81e2d1863c08c2e9486a036600582db236bde152375e8874a46236a7d020f061f7c022ac00ca8fdf3ad1af690f91a876b2406e5613b0813f96a85e316d09488fbeaa71fe37fe8b1c19d81070807138d8e406d33489948b1d973538e343198427194fc6b09268a8f042f4060edad9dd94d7f722972c1ceae5f5dba15c825c9063837cda09d627eda5913d9a7107c5ada153d114580c5e004c83b4c1dcdf330cbf2be95ea0b6de532e08101a11092eb920519dca542a221365cee95645e4986bbdad9ee63a64843c80a4e4c57babfe703aacc2542a7b8ed65e22fcbb2f95471a7ee34762ca943c1b604866c994504a8a6
 48640.01ns INFO     cocotb                               Tag = 0x10a3b8304e3d9f73_4fb5d625d4c0793b
 51180.01ns INFO     cocotb                             [PASS] random_enc_18
 51180.01ns INFO     cocotb                               CT  = f60dfddfe4c3595a8f971e0efa51ca2a9aa07c4b0d98b7c62e83c11799fce94e0ceeba703dd6e07f50a15157c604d56d2311f8bccbb5cde4779a1f050438eb6393aea263e5d0e5e89ed89040b6aead2dd164ff614bee13b37afebcd781bf16e116177d005ce24e2de1fdb009659cc415f90c71e10145d4610353cc03fac8a49a67d820e45a476c603d9c673a36e1889b696f1402b53fd1157676f066ce60f31adb572a2ab6673341726cbfa0f6f9e72f5bddb515ebaef71b4d5875a21d9b11cae5471a26b0f8e715fafae71133fdcac380a9eec201e3f43bf8
 51180.01ns INFO     cocotb                               Tag = 0xaada9489ab0c04cc_b798961f20dd84e7
 53180.01ns INFO     cocotb                             [PASS] random_enc_19
 53180.01ns INFO     cocotb                               CT  = f35ad0c461abc37e8860db1c56b8040bb746e3a7ac4e251edacb592201e11f362bfe5c2592689fb219740a70717229cd140d60f893f1b0b77d0977073f97ee7949b18839314056f96ab5e05ee194bec4d7c8106b0f33a5c26a6e39051c24a980e957b629aa0219141b1f9557373be51dea7830e885d5819bdf049395cada364b3543a3eb3f33134f7731ed20774f2a2f95f22fb09456661ff987e5246af1
 53180.01ns INFO     cocotb                               Tag = 0x195b673d0df6ba3b_063b8c53b9a47a91
 55000.01ns INFO     cocotb                             [PASS] random_enc_20
 55000.01ns INFO     cocotb                               CT  = a1468ceeafbc225ab48cc8376299bad2e82b9ae9c2fa30d19d2e11743f01ae7f0620e5b5cb5239ccec5911ec69735001dc5b5cc8381032e98cc298a5e6fb373c388cf956d1b24a19db3cd6db94370583a5357294f43a27a6668e8d9d59b6081eddd2c085ddae5019156fe4f86aac2009c7f6d768f5efc6a8d14abc6b637189dba31a0fc1b1e6813425248bef8736a026f80e0a0cbc89e7f339a2394ab54395ff21a4749f456dcc2224b9de3f2c111dca03003e1c90cca993b8c3a90cfb6973efd65af092bc658b909a98fa2609fc3411fee61bd2c31793a263033ecdb366
 55000.01ns INFO     cocotb                               Tag = 0x8f230fe17773ad8a_d57981ac1a2062a3
 57000.01ns INFO     cocotb                             [PASS] random_enc_21
 57000.01ns INFO     cocotb                               CT  = 1200cbbcb217071ad18ae0a47d056296e7f2d4cbc484bb078fc723af0ef23ad9878f331cbd644910a3b46a5879c4b299b3a10648f8745de27d0821bc2ae5ee8c36e6066bfadea0dbd6b436f861ae2aef872b9dd83bf7b39d61a32715
 57000.01ns INFO     cocotb                               Tag = 0x9a8219c905793cac_e188f9005d9bffba
 58730.01ns INFO     cocotb                             [PASS] random_enc_22
 58730.01ns INFO     cocotb                               CT  = c7935c245a66f74d0aaf8d41bd326cd3eca6ea3673fcb79ea5b4d012b53d2667b733fc08f314a622379f2718906db73cdc253ae2f68fa60987e2c341870ae63b652d84dc709615d3942d53126e23174c50ff4480ee8d2826e20f05f9c1e8cca6cff2c7ad97b13f79640d80e5a07b1cc882827e22c4396ae32a1f7178a73d818b81608b8d0f424a6793c333ede55e69ee06a0fdd514d6fe2137ef717568014bb125101ea81f39b7ea03966405b91ba5239ee10237dba99995dd54c912fa87a90beac4ba273b3b0c4e726e7fcd272702537837e762e2498cd6
 58730.01ns INFO     cocotb                               Tag = 0xaf83f6e28219825e_29a4ecebf2a2172b
 60550.01ns INFO     cocotb                             [PASS] random_enc_23
 60550.01ns INFO     cocotb                               CT  = a7b489250a50ba74b375eca4acb4ba5ffb497fe16315d5e813f4184a8dbc
 60550.01ns INFO     cocotb                               Tag = 0x7e3d2b5906d4ed9b_b2bed74aa460e827
 62550.01ns INFO     cocotb                             [PASS] random_enc_24
 62550.01ns INFO     cocotb                               CT  = a2f0e1e193be9f6f58d0591a617a094410d8084d8fc07494dc92144e40b2ff47fba490f9ccad4b9cf03e81377fe2ff12a3993340ec6e1b5f9e89a6b42adf9870021e4a24fbaf6461f6fc6021ec443cecf48a7f1af7f69140cc549cc6d220b49079541ecea6b6d6d54bb04e9606fda8793648cdea6fb844ee4f2e43ac8174
 62550.01ns INFO     cocotb                               Tag = 0xf3ec79f84fb1c0c3_40d39681e7860fed
 65180.01ns INFO     cocotb                             [PASS] random_enc_25
 65180.01ns INFO     cocotb                               CT  = c5d7369bbca8561ebc232bfec5b972bd331133bc8b74dd6d48d8689dde6bd019553242f71f35c83eba654bb88919221f224c27ead64756f5c57a6cae58100371f48c5a5e28589d8e8676e6eca5805db1ee64aa5bfef0308fccb939f4977c81828e216e29e6ab83cb319d8c28ac5a37c159d5bc386e7f823b2d61506d0e1e60543ed3f13f3dcf08fe930bcc39207ff326be518075deec1fe0a214864b0ab4bf59fe158ecde2124c21d158345b834be149d6bb96d97a8ead342b6cf3067f097e672b118622c778e4a424ebbf69437c1bc9a53dc27ed0fb26972d87d463e9c206f8
 65180.01ns INFO     cocotb                               Tag = 0x25005f2af2af0fe9_f2954d7bd2ec60c6
 67720.01ns INFO     cocotb                             [PASS] random_enc_26
 67720.01ns INFO     cocotb                               CT  = 13de81efa4a98b96c4fa56e928ad2ad68663f0d7a7817f5fe00dc1739a03bc2fa809befa829903f3b62ad01267e0a9a8ec730d4090935c215602f2f0506effa1afc9dc45d1b99ecc0e71a8a4fdde990bc2449bac61a07b72398cde4ba06030ec2b2579aa3c437aefe88d0d5b19a42a9ea17f53889dced97ca60609bf476ad6c041066018e2887537a635757fb342d8203c73d3738d56109de9214af0dea7a49d16572c16246ead4238f6c58f2bb8833fdba7bfe1c4a2137ce609c18aeb9c7acf40bfd7e14d6ce5
 67720.01ns INFO     cocotb                               Tag = 0xc11ef8bc09a913b0_b1026728cf2f3d5b
 69000.01ns INFO     cocotb                             [PASS] random_enc_27
 69000.01ns INFO     cocotb                               CT  = e06aeede9c9906f0bc80ef7921949ebe87539573d56927663bcfd4e12a4a0263f439d37c97f2d518f06bdd55d08eeb1db8755cc914df5f
 69000.01ns INFO     cocotb                               Tag = 0x3015539682fdf019_d3737306c1eb6e9a
 71360.01ns INFO     cocotb                             [PASS] random_enc_28
 71360.01ns INFO     cocotb                               CT  = 7ada6e0f5f73530d1425e61624a3e48f3db7fc3133b1ada229f4c034c868069024112f29dbe99aa3b37864ae487ef8684ecfd9e7fe55c2d01062450f96b3022bb200f0c737fe5fd8bf9bef581ef9f2b5e2fa3a5450a11a48c01c318171c2a3431b1f03c34d8061884ab6476041f94650d6bf4fafafafbd42a15053982965bd5ff8150292d1405df9b30dff95ca0e72dd0fba1d9bed3eacf50f7cc83bcff83936e3d30092421a5839219c5b45bb4fe2872cae0a9a5fa137792fce67ed9b1cdd4c168453a8f465
 71360.01ns INFO     cocotb                               Tag = 0x50cc6dd72d29b3c7_7f13eb672c3f20eb
 72820.01ns INFO     cocotb                             [PASS] random_enc_29
 72820.01ns INFO     cocotb                               CT  = d98f987d615bc9d8d49b276198f163c1d05e67138061eb8e69e245cca3c27b4cd61f81339a489ac86ce02c2386c15ab1f79e722ea7a70dd8bf
 72820.01ns INFO     cocotb                               Tag = 0xd192db00486f8ddc_1b0c31f6965a3f6c
 75450.01ns INFO     cocotb                             [PASS] random_enc_30
 75450.01ns INFO     cocotb                               CT  = 721858461c1e1ab190df525a2cbe79592020ed4b1428512b4fe896935f2fed2a24ec6297ff162350790d77e3d1369ba69adab0c4e7225024aae996384a6d7dc592300e8db66647a4e675cd479d68547dd5bef15689de7826e96c54d17aace79ab7e69194b16e6f7493cc1d0176bc3085bc98326d864a76b2868beab36a9c2686abdd940b68cb02e6f6902418ece3fa7d76978a4f5823d7542c284284dbede851df93a8da84dfeefdf529e7d731
 75450.01ns INFO     cocotb                               Tag = 0x72d28de805c7e8e4_1c2a107461e05334
 76280.01ns INFO     cocotb                             [PASS] random_enc_31
 76280.01ns INFO     cocotb                               CT  = 1437f4cde8d83e9f9d2a88c6903158
 76280.01ns INFO     cocotb                               Tag = 0x198e09e7b8a18250_2bff05dcae452a9a
 78010.01ns INFO     cocotb                             [PASS] random_enc_32
 78010.01ns INFO     cocotb                               CT  = d6bbc550dc284a4403b19697be0ed1
 78010.01ns INFO     cocotb                               Tag = 0x17e50b351552eab2_7200e91d1e75f6e0
 80460.01ns INFO     cocotb                             [PASS] random_enc_33
 80460.01ns INFO     cocotb                               CT  = d02d035105219cd16acdc7262f0df7b98b8d7985fdab18761ffbd2121975de207e19aa4fda7c267402a39d097ff0e4eb77665858b03a234ef211d4bbe278c9985609bc05bba03c7ee517d0c2efe61bd11b6456ce10aa9f4127431fc823377f8fcbe03cf156128659ada59b839d9b342e0b590b3d3bbcedacccc6457187fbf8bae6e9e2eb794814674878cafcb8d0e3ae8ba310d5bfc7310458aaa38bc9d4b003bc7897daa4eda5aa6eea8272836dd769cbf1fcfa09433d6c15f7b5294a673f81c31022df34
 80460.01ns INFO     cocotb                               Tag = 0x7647725e869eecf9_019fda6732156910
 81920.01ns INFO     cocotb                             [PASS] random_enc_34
 81920.01ns INFO     cocotb                               CT  = 061486228a5294ab0dec6027b2ca6e72d6bba53a7026c44749cdf836d406b8bf7ef4de45535c5bd690a1c2287c74680b74c77ce1023146e8af68ae538fa32bda362421edb9cccd28262b17a85392d5b2b07aa3a49de04a8c38349850842f3418ff61a4d5012315622bddadcd114ad4cbd3378646905c59070b385ef0fc61a83af34a2e9b406b5a95adba9614ab3470512f509c88b2ca0bd77cee38513df5213cce6ffb1b2d1d9e2aa390
 81920.01ns INFO     cocotb                               Tag = 0x8581c42c5e6bb09f_2c5805f81b38c651
 84190.01ns INFO     cocotb                             [PASS] random_enc_35
 84190.01ns INFO     cocotb                               CT  = 1bdfc6067090e98fc2e4b91d84eedb40ac9d6771f3d76bfaf8242db002851d4c8fb0d9c1957e00ccf07085431e3a2a0b782288bb5505df204ce73d1682d61c7a2e52338125f28d63936da1c0667ca5e8803106601a201f494057f884728ea55fadedbcd55b48f88570054c1074286302a7ffcc5925959e9fe457701e84ae7bb8bda79665d809f891040fac0d05d7387d83b9b2c70f9e07a837412f3a3a505722e7ed916b83d3070d9de5afd0f0c55310726543a90dee83825facf59a0fe2b9191cfe7982b4ebffb15081cbf70ddb0b8e1cda11d2d518a5bdf05a45078898d79246c2f39b07eb09bc30e45d
 84190.01ns INFO     cocotb                               Tag = 0x6368100dc50a0e7e_b45ecad8f63141a5
 86820.01ns INFO     cocotb                             [PASS] random_enc_36
 86820.01ns INFO     cocotb                               CT  = dd3b2b072e0b0a960a903dbcf80cbce5883a9de0a451045db7142a17add33d09c0b684b1528cbf17ae1712c5992716c5a0d6ddc2259502290ef7c24c91de5a9e35e569896bbfac2c2174872e32dcca9c1a22897bc630106b3f703121136392e16e0e07f143d70bde3183b091b1e9e6239d216b77c4778fd5f7f9eb1174b80e929b2c0aef305a5abf09c6717ee0263600bdfa795b6e43f03437b0d0cfcb37172186405f88d5d7e28ec91521ee7c3e8c0a9a904815443496ac8b93c1ca2aed29b2a2716f39efee61fcedcf50dd28cc03323eca0998e583c7fa49d1750350d09754dad41ec078a5f014618bb92e2149729b9b7d3fc3c8ab5e213eee
 86820.01ns INFO     cocotb                               Tag = 0x739b700564d37372_34eadfa79d764eaa
 89090.01ns INFO     cocotb                             [PASS] random_enc_37
 89090.01ns INFO     cocotb                               CT  = 1ab57fd7b72f1cdeb6bb6014f2c3f1dae005fc0ab55259e9eb415f43583f7f6a4bb7f12b19ebd1e6824b5bbe3ed000a106b9150ec6600bfcfca0b1181f0ef76c8c1f7a1228b8aa6728e1293820a5c2d02e92f63939db27177da8c4
 89090.01ns INFO     cocotb                               Tag = 0xcc7933a051ae3f10_f36797c33d88097f
 90730.01ns INFO     cocotb                             [PASS] random_enc_38
 90730.01ns INFO     cocotb                               CT  = 2812ef1a78e4001512406521b908ea5502f022c6c5f99a762b706baab9127443a173feb5d042b7cd9aeecb4970fe418a638c130cb5a6a3e647c77e7f0df50ba0c648bac8aa92a38c263178e65509bc0aaec84a0906c33508aea96d4c5ed3c6093335c4efe4fe81b9ecddb0829322969479d06811231a84172b0496682fe116a140
 90730.01ns INFO     cocotb                               Tag = 0xdadcde264e52e8be_aa2f9d05972115df
 92100.01ns INFO     cocotb                             [PASS] random_enc_39
 92100.01ns INFO     cocotb                               CT  = 88d48290158ca9454be3ad51f11a9df750494204c5e47c46dc6482c115c04d2c0825bf6d94cf085d1bdf8d479758686c7902099adfb8e466a2dd0a6a1ac6bf64ca5eeb7dc92c14c0798f85af
 92100.01ns INFO     cocotb                               Tag = 0x1ecda032a6dedb46_0c8902be666b73fe
 93650.01ns INFO     cocotb                             [PASS] random_enc_40
 93650.01ns INFO     cocotb                               CT  = 1867dca7fe26b83ac859c95a5e8eeec8ec38ba275a7d361505bbb1bee1f5555808a76a4012f2
 93650.01ns INFO     cocotb                               Tag = 0xdbca7b7eba84d5f0_ac3840d5a5d27177
 96010.01ns INFO     cocotb                             [PASS] random_enc_41
 96010.01ns INFO     cocotb                               CT  = 6e8b605290eb762af29c022e97d02c46a7ce764ffd267bb32efd0c644dc7eaf90d167891364299ece45fe5b80a50937a88dc60aa6b8c89abbcddfc5211e1594d015d5e21b8c1c379a0b26ae26425f34f93d4c0f540036086c96b871ca785b68101dd2550ab0dbc0a60851e1a881be06268df77ee0fa27a182c90dc
 96010.01ns INFO     cocotb                               Tag = 0xcddbf2a57c041876_f8d531b1d1871afe
 96760.01ns INFO     cocotb                             [PASS] random_enc_42
 96760.01ns INFO     cocotb                               CT  = f3f7fa7a1181e0976f8eb70c976b578dca5af6d4cf24060178f1b58a5bcab65fbfa59e1f16533bf12d3de68d3db547bda37ab76cdec39f0a87460f66b2d092a961cd33c5ac1264
 96760.01ns INFO     cocotb                               Tag = 0x2eac474d6116dbf7_cd475801388e716f
 98760.01ns INFO     cocotb                             [PASS] random_enc_43
 98760.01ns INFO     cocotb                               CT  = 47a833af08a0486a7e8ef4cd724bda815c0a766b2e4ba115714773d4953f4b62bdf34c3b30046eebd996be294a466c99e1ea46
 98760.01ns INFO     cocotb                               Tag = 0xa2478ec40e9d84cd_1cb6a567ea7415ee
101030.01ns INFO     cocotb                             [PASS] random_enc_44
101030.01ns INFO     cocotb                               CT  = 3d22a5f63719a6a12af4b9d8272f839a7d6d3bd89439ce1b076f2b60a3dde0cd6078954c86a465a9f3373adffd42c11097f103e41f21ccafd5754252d8ee520798a814efefc0bbb6d84c1eed9034780f99e6c490094587fbc8c6479c466c468a6d35eb07ba5a4024d3080d6384adef08cae241b86e0f83eaf7976df891ec4cff95d0fb3ef14e92fe44e9229fc6e3491b1f962b2a2a216b8494ea0aa7b2122b615b867e02f9fe8df853675d4a4df2ebb49c9f14e3d873adb7099c2463db68291d23b5501196d45b
101030.01ns INFO     cocotb                               Tag = 0x15929305a7068c63_5c6357c8049b2c6f
102760.01ns INFO     cocotb                             [PASS] random_enc_45
102760.01ns INFO     cocotb                               CT  = f7bec5343dd72820213bc8f69ebe7df80ca918cc4a14343ef31fa39aec7cfaf5fdaa3633a84870e103d2cb7602a3228861cc0ea6d6d191aa6fa234e8075e23311b9c380dfd19a2aa70a761b2d4bf344b4e068ce7e97f50ada0cf7d8578401caea898d79b70b0e9a3f8ab0727483e9f6e2a36c876d81537dfb3a92a8399c2ccc13a4c927ed26d13d7
102760.01ns INFO     cocotb                               Tag = 0xe88d6021e94cd1bb_a98231bba26bd90c
103410.01ns INFO     cocotb                             [PASS] random_enc_46
103410.01ns INFO     cocotb                               CT  = 59b680c7a45c927dc94cab6b198df7ab8a9ce947422b5810c0b0d0133032e43296b0c7918508db
103410.01ns INFO     cocotb                               Tag = 0xbfb7cab2972d51a7_fb79ea261ca3fb9b
106310.01ns INFO     cocotb                             [PASS] random_enc_47
106310.01ns INFO     cocotb                               CT  = 9d6e5887d4de0606630db799a74353897d7b6e69e63bad59d1e5350f8e17073c8bd475c33778ac1d83a8e5b0fa8fe76ef309c1a9a2e98f9b0fff257e5ac97d4aad45d168860cf57281a00ecf43235edce8e963601052558bdf8041d797721075c595e4829a0cf244152dd8d09b9fa9cf20c11ba5b6c41267377300e0f38b09e19856a9d398ee19cd4562788b524bf9b272c7f0575a9284e02c22a0a446f20c5f09e13f6e6f52545405f3e71969f3e69aa97b4e2fc562a9c85d199d53b6246d0cdd4d8fe4aa1ced5f
106310.01ns INFO     cocotb                               Tag = 0xda54e55443ecb844_db84094715a4b2c4
107140.01ns INFO     cocotb                             [PASS] random_enc_48
107140.01ns INFO     cocotb                               CT  = 4b28afb5e503226236c1cbcb3c70b0900a23
107140.01ns INFO     cocotb                               Tag = 0xc6adf58235863c13_c899176abd63797a
108150.01ns INFO     cocotb                             [PASS] random_enc_49
108150.01ns INFO     cocotb                               CT  = b7a5b3811b0cbb702d5867c0213631fa0f065787cba280113fbf26a9de233ced2018
108150.01ns INFO     cocotb                               Tag = 0x0ff0d93b5983fcd0_6d8fefc4d5e27c69
108150.01ns INFO     cocotb                             [PASS] test_random_encrypt: All 50 random vectors passed
108150.01ns INFO     cocotb.regression                  test_random_encrypt passed
108150.01ns INFO     cocotb.regression                  running test_random_encrypt_decrypt_roundtrip (16/16)
                                                          D2: 20 random encrypt->decrypt cycles, verify plaintext recovery.
109160.01ns INFO     cocotb                             [PASS] roundtrip_0_enc
109160.01ns INFO     cocotb                               CT  = 1d3d94d342bd7bc4564c3aabff3e9c00fcb32c0707dd130e3b
109160.01ns INFO     cocotb                               Tag = 0xe77f1cb5cda4211d_b666df002c7260d0
110170.01ns INFO     cocotb                             [PASS] roundtrip_0: enc+dec OK (AD=81B, PT=25B)
111360.01ns INFO     cocotb                             [PASS] roundtrip_1_enc
111360.01ns INFO     cocotb                               CT  = 089b9275394e5e4a1e40e9ab734de124038ed883f6fbbfcd20b572367754e167160feb036f3b469e59f6f99a5fc24628a3a8276a09a9148ce2474c08e802dd60c77976676b2cc4cb0b8f5c74178d2c2cc6e58a63c96d2df9c2cb6b6c2dc9213a24bafd
111360.01ns INFO     cocotb                               Tag = 0x1238d4a7b26df6d0_c8b8270f9e9dfcb2
112550.01ns INFO     cocotb                             [PASS] roundtrip_1: enc+dec OK (AD=42B, PT=99B)
113200.01ns INFO     cocotb                             [PASS] roundtrip_2_enc
113200.01ns INFO     cocotb                               CT  = bc7cca3377
113200.01ns INFO     cocotb                               Tag = 0xadba5d656fd5dc07_b57ba37185b6679b
113850.01ns INFO     cocotb                             [PASS] roundtrip_2: enc+dec OK (AD=43B, PT=5B)
115400.01ns INFO     cocotb                             [PASS] roundtrip_3_enc
115400.01ns INFO     cocotb                               CT  = f00cbfcb48f6b98b1b8e985b5818b9762dc0b11fcd61bbd06e868a27f7f02400a9fa3698b5c23fad2fe0d9fba97546ee362a2a1afaa2371acf98db78869e32a233a342f6c5c26052f9515c2440e851549ed9e452b6b701
115400.01ns INFO     cocotb                               Tag = 0x2ea702d967697edd_81b34cf628f88d64
116950.01ns INFO     cocotb                             [PASS] roundtrip_3: enc+dec OK (AD=119B, PT=87B)
118590.01ns INFO     cocotb                             [PASS] roundtrip_4_enc
118590.01ns INFO     cocotb                               CT  = c2760b44552327b9ddc9cd6ee7cd33756347343e7917d7249b4291c3354bdff997f5108ac4ebb2fe5dc67c7c43468e8abfc043669feefc21282cd38ace879cf18c779a672012e3225822a24f13dbcf28ed7a3387eabf4c1ad75e552f0dcfa723a005914b0abf5ee026d82147
118590.01ns INFO     cocotb                               Tag = 0x34edfe02d1cfd84f_f3d1b20ee99d02d5
120230.01ns INFO     cocotb                             [PASS] roundtrip_4: enc+dec OK (AD=118B, PT=108B)
121150.01ns INFO     cocotb                             [PASS] roundtrip_5_enc
121150.01ns INFO     cocotb                               CT  = 7c0dee583e7c1aec4a1a93e99f8881695a0dbfa783f1e3dffb18de50f60ce8f65bc0c82b8b9e426d70b523613b8a673ac380af8db31c10af1cc7751d875603b0bf3e473e35bd69804f751eac20cc89e8978a6884
121150.01ns INFO     cocotb                               Tag = 0x324e5a910f1a97b0_667dafb476e061ca
122070.01ns INFO     cocotb                             [PASS] roundtrip_5: enc+dec OK (AD=14B, PT=84B)
122810.01ns INFO     cocotb                             [PASS] roundtrip_6_enc
122810.01ns INFO     cocotb                               CT  = bb12d634910a0c4599333d2293b61ce014afe91c44faed3d2098a5d08cd0f73643e16871547c6547588a5dad5d54c70475b22bcfe8dfb28d
122810.01ns INFO     cocotb                               Tag = 0x3ad6936a5d6ccffc_f474232a3c934d9c
123550.01ns INFO     cocotb                             [PASS] roundtrip_6: enc+dec OK (AD=9B, PT=56B)
124380.01ns INFO     cocotb                             [PASS] roundtrip_7_enc
124380.01ns INFO     cocotb                               CT  = 129a3bae824ecdbe070cfc7444d0465c501998c918fc95b8d6304d9d0b78445c4cb279524c220b651cc6797eaea81d69ffdd33148c94fb0cfd9dccaba6496a23d38bf9a3f5d9bdea0c868d
124380.01ns INFO     cocotb                               Tag = 0x1f6d9e1216f7e85a_9d2926e893262a17
125210.01ns INFO     cocotb                             [PASS] roundtrip_7: enc+dec OK (AD=11B, PT=75B)
126040.01ns INFO     cocotb                             [PASS] roundtrip_8_enc
126040.01ns INFO     cocotb                               CT  = 4a9627b0f603703f2536473aea2e8128469e04b66b9834c3f9
126040.01ns INFO     cocotb                               Tag = 0x15c9240e101582e9_e8315ce9ddc52f58
126870.01ns INFO     cocotb                             [PASS] roundtrip_8: enc+dec OK (AD=58B, PT=25B)
128150.01ns INFO     cocotb                             [PASS] roundtrip_9_enc
128150.01ns INFO     cocotb                               CT  = 1cf73e05c67578a3c29d338408e06c2f86114bdc293d9257ab2b15a8912146fdd67319441347705c60390855725fc2d93b639836ab186bb61a8f445b3c36f7b07a3cee4ac2ce45668fa36cb9d28e44ebf9b4edf7574506fe1d58fb3a
128150.01ns INFO     cocotb                               Tag = 0x6500229ed2c3d81f_fcc620073277bd33
129430.01ns INFO     cocotb                             [PASS] roundtrip_9: enc+dec OK (AD=77B, PT=92B)
130530.01ns INFO     cocotb                             [PASS] roundtrip_10_enc
130530.01ns INFO     cocotb                               CT  = 03253d4e2422511fcea26633e68967777cbc5d9f249d41aa798276aabe3c3eba630a3ead0695532fda4b3ee3
130530.01ns INFO     cocotb                               Tag = 0x4431d1fc45dae21b_9c30abf4acd2983f
131630.02ns INFO     cocotb                             [PASS] roundtrip_10: enc+dec OK (AD=85B, PT=44B)
133180.02ns INFO     cocotb                             [PASS] roundtrip_11_enc
133180.02ns INFO     cocotb                               CT  = e99f08a7a4c943707dc6798311c74f8b2117e915f20c01e5874bc03b029d8c674f315cca058d6a8abfb0b8aa99a1e1483dcd751856fe7a77c012a670cd8c6294608245a471cb37e451723507c82593785fe5b093d2d2
133180.02ns INFO     cocotb                               Tag = 0x611bca1231f674aa_5fcf5deb534b1b49
134730.02ns INFO     cocotb                             [PASS] roundtrip_11: enc+dec OK (AD=121B, PT=86B)
136280.02ns INFO     cocotb                             [PASS] roundtrip_12_enc
136280.02ns INFO     cocotb                               CT  = ff6928081984799cf74f8405da96910dcb05205200d43d66fca745999c53db9be9d2f394ea396e2bd72f90e7af012e665ca217e80c2ea53eb7ce951f1b8669c05e5c70c95decf20b9c33a5231431ff94b470122d0fa5ceb23de4429e05
136280.02ns INFO     cocotb                               Tag = 0xa391e33b3461e3bc_719245a7c04497db
137830.02ns INFO     cocotb                             [PASS] roundtrip_12: enc+dec OK (AD=113B, PT=93B)
139110.02ns INFO     cocotb                             [PASS] roundtrip_13_enc
139110.02ns INFO     cocotb                               CT  = 43a17f31a6886b932c0e03eb0d6be8cb2b6058b4833b78bc2430cd6db78af2f182cfbacee187f49de668677c366f3bc938b8bb65b5299b44fcf1a2d3bc6b08a1a8e7c8de8d9b22a3540d03da17f569d0f3f25b42b9471e3c86cd5c738a
139110.02ns INFO     cocotb                               Tag = 0x2f3fccc8ecd1373b_45741cd3ad67ff1d
140390.02ns INFO     cocotb                             [PASS] roundtrip_13: enc+dec OK (AD=76B, PT=93B)
141940.02ns INFO     cocotb                             [PASS] roundtrip_14_enc
141940.02ns INFO     cocotb                               CT  = a9f121ea930b8232c02f04cdfe13781ff94487922e85a8ad32a9c9afc16b70054b9e4eb139c9d8ed56bf3a018de55f0467656e14c6db584192ecdfc5d85fe49f50c1d810593660cd4f30a000985e31a788d06616365840aea3a25bd8248e98fbcc
141940.02ns INFO     cocotb                               Tag = 0x0aea54d48aa5bc68_174c5be384978e28
143490.02ns INFO     cocotb                             [PASS] roundtrip_14: enc+dec OK (AD=103B, PT=97B)
145040.02ns INFO     cocotb                             [PASS] roundtrip_15_enc
145040.02ns INFO     cocotb                               CT  = c2a9cd6f3543b66354725711c313104576c347f8979126b3af568d04d36f26edaae0a733c64a68cc1c4591acbdf4d6b93ddad06acbe8fd27975966bfce9cb29cf57160bd4b1b38459d65a795478e58287350739c3e9f95df7398bdbc618aa3cbeb0728620ca34b9c
145040.02ns INFO     cocotb                               Tag = 0xd0e7e8cbb9ab3718_b7c884785fda23de
146590.02ns INFO     cocotb                             [PASS] roundtrip_15: enc+dec OK (AD=107B, PT=104B)
147150.02ns INFO     cocotb                             [PASS] roundtrip_16_enc
147150.02ns INFO     cocotb                               CT  = 96ca62ced47431
147150.02ns INFO     cocotb                               Tag = 0xbb3ca175357add7c_4877b425b3e68efa
147710.02ns INFO     cocotb                             [PASS] roundtrip_16: enc+dec OK (AD=27B, PT=7B)
148270.02ns INFO     cocotb                             [PASS] roundtrip_17_enc
148270.02ns INFO     cocotb                               CT  = bcc5cc2dac0c1b1e9013f6b4d7d15b23a9
148270.02ns INFO     cocotb                               Tag = 0xa185b02ff9604053_578967755f17a010
148830.02ns INFO     cocotb                             [PASS] roundtrip_17: enc+dec OK (AD=15B, PT=17B)
149930.02ns INFO     cocotb                             [PASS] roundtrip_18_enc
149930.02ns INFO     cocotb                               CT  = 60bb6cdfc6dc67d41b399a053270ce4011c5848a2d755b26ef94c87bef5d81888d724acc646ab17f5fc4be859de32ea92fba044aed98d2529f8dfcfcdd04be13407eaeca5be7d5e4a56f5c469d38d3226f04607e25471aca75
149930.02ns INFO     cocotb                               Tag = 0x3f47dc27a361aeff_c083dc1be63b5c07
151030.02ns INFO     cocotb                             [PASS] roundtrip_18: enc+dec OK (AD=44B, PT=89B)
152130.02ns INFO     cocotb                             [PASS] roundtrip_19_enc
152130.02ns INFO     cocotb                               CT  = 6152339ce98d30c23b532fd9eabd9362db14a5a62f2895340187ac60194b6488cd2ec23bebb5f046a1f82eb3ff7d73150def8784df0483e58ed6f3100fdfb6cc17b5e7850a5182310596a454a56c674f2cfe33a0722bd7dc9488ac7f2b33f0f4223eb882f72b6858bf5af3f6bfc7b60fb24a7e04
152130.02ns INFO     cocotb                               Tag = 0xfd6888309508eba6_0908fbd6f73b4e49
153230.02ns INFO     cocotb                             [PASS] roundtrip_19: enc+dec OK (AD=3B, PT=116B)
153230.02ns INFO     cocotb                             [PASS] test_random_encrypt_decrypt_roundtrip: All 20 roundtrips passed
153230.02ns INFO     cocotb.regression                  test_random_encrypt_decrypt_roundtrip passed
153230.02ns INFO     cocotb.regression                  *********************************************************************************************************
                                                        ** TEST                                             STATUS  SIM TIME (ns)  REAL TIME (s)  RATIO (ns/s) **
                                                        *********************************************************************************************************
                                                        ** testbench.test_enc_empty_ad_empty_pt              PASS         380.00           0.04       9232.00  **
                                                        ** testbench.test_enc_empty_ad_short_pt              PASS         390.00           0.04      10305.70  **
                                                        ** testbench.test_enc_empty_ad_one_block             PASS         390.00           0.04      11016.86  **
                                                        ** testbench.test_enc_empty_ad_multi_block           PASS         570.00           0.06      10319.71  **
                                                        ** testbench.test_enc_short_ad_short_pt              PASS         470.00           0.04      10520.20  **
                                                        ** testbench.test_enc_multi_ad_multi_pt              PASS         920.00           0.09      10033.14  **
                                                        ** testbench.test_dec_valid_tag                      PASS         940.00           0.09      10720.16  **
                                                        ** testbench.test_dec_invalid_tag                    PASS         470.00           0.04      10734.62  **
                                                        ** testbench.test_dec_tampered_ct                    PASS         470.00           0.04      10733.57  **
                                                        ** testbench.test_enc_1byte_pt                       PASS         390.00           0.04      10958.92  **
                                                        ** testbench.test_enc_15byte_pt                      PASS         390.00           0.04      11052.74  **
                                                        ** testbench.test_enc_16byte_pt                      PASS         390.00           0.04      11043.71  **
                                                        ** testbench.test_enc_17byte_pt                      PASS         480.00           0.05      10451.33  **
                                                        ** testbench.test_enc_max_ad_bytes                   PASS        7610.00           0.68      11153.79  **
                                                        ** testbench.test_random_encrypt                     PASS       93890.00          10.62       8838.99  **
                                                        ** testbench.test_random_encrypt_decrypt_roundtrip   PASS       45080.00           5.03       8963.33  **
                                                        *********************************************************************************************************
                                                        ** TESTS=16 PASS=16 FAIL=0 SKIP=0                              153230.02          17.04       8991.55  **
                                                        *********************************************************************************************************
                                                        
testbench.py:656: UserWarning: Python runners and associated APIs are an experimental feature and subject to change.
  from cocotb.runner import get_runner

  
INFO: Running command iverilog -o /home/runner/sim_build/sim.vvp -D COCOTB_SIM=1 -g2012 -g2012 /home/runner/design.sv in directory /home/runner/sim_build
INFO: Running command vvp -M /usr/local/lib64/python3.6/site-packages/cocotb/libs -m libcocotbvpi_icarus /home/runner/sim_build/sim.vvp in directory /home/runner/sim_build
INFO: Results file: /home/runner/sim_build/results.xml

```

## NIST Based Vectors for verification

We recieved a great comment from reviewer `Luqman` in proposal reviewer round to use Official NIST Vectors for verification.
To add this into our verification workflow, we found NIST uses the NIST ACVP (Automated Cryptographic Validation Protocol) which is relevant to this. 
Upon further research, we found:  https://github.com/itzmeanjan/ascon/blob/master/kats/ascon_aead128.kat \
it has 1089 KATs, (known-answer-tests) based on the aforementioned ACVP, so we used this to just test code again and it passed all 1089 cases.

#### Log screenshot:
<img width="717" height="392" alt="image" src="https://github.com/user-attachments/assets/c9c0253d-2d6f-46eb-a351-256af4330145" />
---
