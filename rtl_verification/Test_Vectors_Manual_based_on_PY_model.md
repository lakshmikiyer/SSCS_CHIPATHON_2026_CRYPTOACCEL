# Ascon-AEAD128 Test Vectors — NIST SP 800-232
> **CryptoAccel — Chipathon 2026**
> Cross-verified against reference Python implementation -- https://github.com/meichlseder/pyascon/blob/master/ascon.py

---

## Algorithm Parameters

| Parameter      | Value                          |
|----------------|--------------------------------|
| **Algorithm**  | Ascon-AEAD128                  |
| **Standard**   | NIST SP 800-232 (August 2025)  |
| **IV**         | `0x00001000808c0001`           |
| **Key size**   | 128 bits (16 bytes)            |
| **Nonce size** | 128 bits (16 bytes)            |
| **Tag size**   | 128 bits (16 bytes)            |
| **Rate**       | 128 bits (16 bytes)            |
| **Capacity**   | 192 bits                       |
| **State**      | 320 bits (5 × 64-bit words)    |
| **Byte order** | Little-endian                  |
| **Init perm**  | Ascon-p[12] — 12 rounds        |
| **Block perm** | Ascon-p[8] — 8 rounds          |
| **Final perm** | Ascon-p[12] — 12 rounds        |

> All hex values below are in **little-endian byte order** as per NIST SP 800-232.

---

---

# PART 1 — ENCRYPTION

```
expected input and output:
Encrypt(Key, Nonce, AD, Plaintext) → (Ciphertext, Tag)
```

---
Naming convention: Test Vector - Encryption 01 (TV-E01)
## TV-E01 — Empty AD, Empty Plaintext

Tests initialization + finalization only (no AD/PT looping).

**INPUT:**

| Field      | Value (hex)                          | Length   |
|------------|--------------------------------------|----------|
| **Key**    | `00000000000000000000000000000000`    | 16 bytes |
| **Nonce**  | `00000000000000000000000000000000`    | 16 bytes |
| **AD**     | —                                     | 0 bytes  |
| **PT**     | —                                     | 0 bytes  |

**EXPECTED OUTPUT:**

| Field      | Value (hex)                          | Length   |
|------------|--------------------------------------|----------|
| **CT**     | —                                    | 0 bytes  |
| **Tag**    | `f1e8da91f9fbf090caf3e37ccad91bae`    | 16 bytes |

---

## TV-E02 — Short Plaintext (5 bytes), No AD

Tests partial-block padding. Plaintext = ASCII `"Hello"`.

**INPUT:**

| Field      | Value (hex)                          | Length   |
|------------|--------------------------------------|----------|
| **Key**    | `000102030405060708090a0b0c0d0e0f`    | 16 bytes |
| **Nonce**  | `000102030405060708090a0b0c0d0e0f`    | 16 bytes |
| **AD**     | —                                    | 0 bytes  |
| **PT**     | `48656c6c6f`                          | 5 bytes  |

**EXPECTED OUTPUT:**

| Field      | Value (hex)                          | Length   |
|------------|--------------------------------------|----------|
| **CT**     | `af14bce6b9`                          | 5 bytes  |
| **Tag**    | `b6588c3aa63f9ddc5a0cf5f565f358b0`    | 16 bytes |

---

## TV-E03 — Exactly 16-byte Plaintext, No AD

Tests full-block boundary (1 full 128-bit block).

**INPUT:**

| Field      | Value (hex)                          | Length   |
|------------|--------------------------------------|----------|
| **Key**    | `0123456789abcdef0123456789abcdef`    | 16 bytes |
| **Nonce**  | `fedcba9876543210fedcba9876543210`    | 16 bytes |
| **AD**     | —                                    | 0 bytes  |
| **PT**     | `000102030405060708090a0b0c0d0e0f`    | 16 bytes |

**EXPECTED OUTPUT:**

| Field      | Value (hex)                          | Length   |
|------------|--------------------------------------|----------|
| **CT**     | `ad53ec51d0e3e5f182df2dbc75ab5e0a`    | 16 bytes |
| **Tag**    | `815b7c4cfe6162564c21d08585f99b56`    | 16 bytes |

---

## TV-E04 — Short AD (8 bytes) + Short Plaintext (10 bytes)

Tests AD absorption, domain separation, and partial PT. AD = `"metadata"`, PT = `"secret msg"`.

**INPUT:**

| Field      | Value (hex)                          | Length   |
|------------|--------------------------------------|----------|
| **Key**    | `deadbeefcafebabe1122334455667788`    | 16 bytes |
| **Nonce**  | `aabbccddeeff00110011223344556677`    | 16 bytes |
| **AD**     | `6d65746164617461`                    | 8 bytes  |
| **PT**     | `736563726574206d7367`                | 10 bytes |

**EXPECTED OUTPUT:**

| Field      | Value (hex)                          | Length   |
|------------|--------------------------------------|----------|
| **CT**     | `620d139f5417ce5677ca`                | 10 bytes |
| **Tag**    | `2bbfa81dafd020f685a09e067363fc9a`    | 16 bytes |

---

## TV-E05 — AD Only, Empty Plaintext (Authenticate-Only)

Tests authenticate-only mode — AD is protected but no data is encrypted.

**INPUT:**

| Field      | Value (hex)                                | Length   |
|------------|--------------------------------------------|----------|
| **Key**    | `aaaabbbbccccddddeeee11112222ffff`          | 16 bytes |
| **Nonce**  | `11111111222222223333333344444444`          | 16 bytes |
| **AD**     | `48656164657220446174613a2056312e30`        | 17 bytes |
| **PT**     | —                                          | 0 bytes  |

**EXPECTED OUTPUT:**

| Field      | Value (hex)                          | Length   |
|------------|--------------------------------------|----------|
| **CT**     | —                                    | 0 bytes  |
| **Tag**    | `498f3c78f360a5bc6fafe31362f5f04c`    | 16 bytes |

---

## TV-E06 — Multi-block AD (32 bytes) + 16-byte Plaintext

Tests AD looping with 2 full AD blocks + 1 padded.

**INPUT:**

| Field      | Value (hex)                                                              | Length   |
|------------|--------------------------------------------------------------------------|----------|
| **Key**    | `a0a1a2a3a4a5a6a7a8a9aaabacadaeaf`                                      | 16 bytes |
| **Nonce**  | `b0b1b2b3b4b5b6b7b8b9babbbcbdbebf`                                      | 16 bytes |
| **AD**     | `000102030405060708090a0b0c0d0e0f` `101112131415161718191a1b1c1d1e1f`     | 32 bytes |
| **PT**     | `f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff`                                      | 16 bytes |

**EXPECTED OUTPUT:**

| Field      | Value (hex)                          | Length   |
|------------|--------------------------------------|----------|
| **CT**     | `e7ced7dca12ba41238b5d35a56652903`    | 16 bytes |
| **Tag**    | `d25e5dbe1f15ec4faa06ed144eafb2e9`    | 16 bytes |

---

## TV-E07 — Multi-block Plaintext (48 bytes), No AD

Tests PT looping with 3 full blocks + 1 empty padded.

**INPUT:**

| Field      | Value (hex)                                                                                              | Length   |
|------------|----------------------------------------------------------------------------------------------------------|----------|
| **Key**    | `c0c1c2c3c4c5c6c7c8c9cacbcccdcecf`                                                                      | 16 bytes |
| **Nonce**  | `d0d1d2d3d4d5d6d7d8d9dadbdcdddedf`                                                                      | 16 bytes |
| **AD**     | —                                                                                                        | 0 bytes  |
| **PT**     | `000102030405060708090a0b0c0d0e0f` `101112131415161718191a1b1c1d1e1f` `202122232425262728292a2b2c2d2e2f`  | 48 bytes |

**EXPECTED OUTPUT:**

| Field      | Value (hex)                                                                                              | Length   |
|------------|----------------------------------------------------------------------------------------------------------|----------|
| **CT**     | `9da1452e86dbb69f888435fe33f74415` `ca72b28a14b350f6f48d5ccff59801db` `f58ca5879d91f8a362ab71bb458c9d30`  | 48 bytes |
| **Tag**    | `08c16ac8ad18cd1c6b414882324ee1a7`                                                                      | 16 bytes |

---

## TV-E08 — Multi-block AD (33 bytes) + Multi-block Plaintext (35 bytes)

Full loop test — both AD and PT require multiple iterations.

**INPUT:**

| Field      | Value (hex)                                                                                    | Length   |
|------------|------------------------------------------------------------------------------------------------|----------|
| **Key**    | `1234567890abcdef1234567890abcdef`                                                              | 16 bytes |
| **Nonce**  | `abcdef0123456789abcdef0123456789`                                                              | 16 bytes |
| **AD**     | `416c6c20796f757220626173652061726520626c6f6e6720746f207573210100`                              | 32 bytes |
| **PT**     | `5468652071756963206272206f776e20` `666f78206a756d7073206f7665722074` `686520`                    | 35 bytes |

**EXPECTED OUTPUT:**

| Field      | Value (hex)                                                                                    | Length   |
|------------|------------------------------------------------------------------------------------------------|----------|
| **CT**     | `a9ab3243d7a7c7e64aa7756303d9f7af` `2348e2c0e51700bceeb1d16584c75ce4` `3723d8`                    | 35 bytes |
| **Tag**    | `275a71dba8a43d20aa66168635535e4f`                                                              | 16 bytes |

---

## TV-E09 — 1-byte AD + 1-byte Plaintext

Minimum non-empty case — maximum padding applied.

**INPUT:**

| Field      | Value (hex)                          | Length   |
|------------|--------------------------------------|----------|
| **Key**    | `ffffffffffffffffffffffffffffffff`    | 16 bytes |
| **Nonce**  | `eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee`    | 16 bytes |
| **AD**     | `aa`                                  | 1 byte   |
| **PT**     | `bb`                                  | 1 byte   |

**EXPECTED OUTPUT:**

| Field      | Value (hex)                          | Length   |
|------------|--------------------------------------|----------|
| **CT**     | `14`                                  | 1 byte   |
| **Tag**    | `176714566f601e224ec71bb58b11ffff`    | 16 bytes |

---

## TV-E10 — 15-byte AD + 15-byte Plaintext

Boundary condition — one byte short of a full 16-byte block.

**INPUT:**

| Field      | Value (hex)                          | Length   |
|------------|--------------------------------------|----------|
| **Key**    | `0f1e2d3c4b5a69780f1e2d3c4b5a6978`    | 16 bytes |
| **Nonce**  | `78695a4b3c2d1e0f78695a4b3c2d1e0f`    | 16 bytes |
| **AD**     | `0102030405060708090a0b0c0d0e0f`      | 15 bytes |
| **PT**     | `f0e0d0c0b0a0908070605040302010`      | 15 bytes |

**EXPECTED OUTPUT:**

| Field      | Value (hex)                          | Length   |
|------------|--------------------------------------|----------|
| **CT**     | `c48a1824adb295c7cdd5393d5d630b`      | 15 bytes |
| **Tag**    | `9c580dd9c366ced05192bab419fb5487`    | 16 bytes |

---

---

# PART 2 — DECRYPTION

```
Decrypt(Key, Nonce, AD, Ciphertext, Tag) → Plaintext  or  FAIL
```

---

## TV-D01 — Decrypt TV-E01 (Empty)

**INPUT:**

| Field      | Value (hex)                          | Length   |
|------------|--------------------------------------|----------|
| **Key**    | `00000000000000000000000000000000`    | 16 bytes |
| **Nonce**  | `00000000000000000000000000000000`    | 16 bytes |
| **AD**     | —                                    | 0 bytes  |
| **CT**     | —                                    | 0 bytes  |
| **Tag**    | `f1e8da91f9fbf090caf3e37ccad91bae`    | 16 bytes |

**EXPECTED OUTPUT:**

| Field            | Value                                |
|------------------|--------------------------------------|
| **Tag Valid?**   |     YES                               |
| **PT**           | —  (0 bytes)                         |

---

## TV-D02 — Decrypt TV-E02 (Short PT)

**INPUT:**

| Field      | Value (hex)                          | Length   |
|------------|--------------------------------------|----------|
| **Key**    | `000102030405060708090a0b0c0d0e0f`    | 16 bytes |
| **Nonce**  | `000102030405060708090a0b0c0d0e0f`    | 16 bytes |
| **AD**     | —                                    | 0 bytes  |
| **CT**     | `af14bce6b9`                          | 5 bytes  |
| **Tag**    | `b6588c3aa63f9ddc5a0cf5f565f358b0`    | 16 bytes |

**EXPECTED OUTPUT:**

| Field            | Value (hex)                          | Length   |
|------------------|--------------------------------------|----------|
| **Tag Valid?**   |    YES                               |          |
| **PT**           | `48656c6c6f`                          | 5 bytes  |

---

## TV-D03 — Decrypt TV-E03 (Full Block)

**INPUT:**

| Field      | Value (hex)                          | Length   |
|------------|--------------------------------------|----------|
| **Key**    | `0123456789abcdef0123456789abcdef`    | 16 bytes |
| **Nonce**  | `fedcba9876543210fedcba9876543210`    | 16 bytes |
| **AD**     | —                                    | 0 bytes  |
| **CT**     | `ad53ec51d0e3e5f182df2dbc75ab5e0a`    | 16 bytes |
| **Tag**    | `815b7c4cfe6162564c21d08585f99b56`    | 16 bytes |

**EXPECTED OUTPUT:**

| Field            | Value (hex)                          | Length   |
|------------------|--------------------------------------|----------|
| **Tag Valid?**   |     YES                               |          |
| **PT**           | `000102030405060708090a0b0c0d0e0f`    | 16 bytes |

---

## TV-D04 — Decrypt TV-E04 (AD + PT)

**INPUT:**

| Field      | Value (hex)                          | Length   |
|------------|--------------------------------------|----------|
| **Key**    | `deadbeefcafebabe1122334455667788`    | 16 bytes |
| **Nonce**  | `aabbccddeeff00110011223344556677`    | 16 bytes |
| **AD**     | `6d65746164617461`                    | 8 bytes  |
| **CT**     | `620d139f5417ce5677ca`                | 10 bytes |
| **Tag**    | `2bbfa81dafd020f685a09e067363fc9a`    | 16 bytes |

**EXPECTED OUTPUT:**

| Field            | Value (hex)                          | Length   |
|------------------|--------------------------------------|----------|
| **Tag Valid?**   |     YES                               |          |
| **PT**           | `736563726574206d7367`                | 10 bytes |

---

## TV-D05 — Decrypt TV-E05 (Authenticate-Only)

**INPUT:**

| Field      | Value (hex)                                | Length   |
|------------|--------------------------------------------|----------|
| **Key**    | `aaaabbbbccccddddeeee11112222ffff`          | 16 bytes |
| **Nonce**  | `11111111222222223333333344444444`          | 16 bytes |
| **AD**     | `48656164657220446174613a2056312e30`        | 17 bytes |
| **CT**     | —                                          | 0 bytes  |
| **Tag**    | `498f3c78f360a5bc6fafe31362f5f04c`          | 16 bytes |

**EXPECTED OUTPUT:**

| Field            | Value                                |
|------------------|--------------------------------------|
| **Tag Valid?**   |     YES                               |
| **PT**           | —  (0 bytes)                         |

---

## TV-D06 — Decrypt TV-E06 (Multi-block AD)

**INPUT:**

| Field      | Value (hex)                                                              | Length   |
|------------|--------------------------------------------------------------------------|----------|
| **Key**    | `a0a1a2a3a4a5a6a7a8a9aaabacadaeaf`                                      | 16 bytes |
| **Nonce**  | `b0b1b2b3b4b5b6b7b8b9babbbcbdbebf`                                      | 16 bytes |
| **AD**     | `000102030405060708090a0b0c0d0e0f` `101112131415161718191a1b1c1d1e1f`     | 32 bytes |
| **CT**     | `e7ced7dca12ba41238b5d35a56652903`                                      | 16 bytes |
| **Tag**    | `d25e5dbe1f15ec4faa06ed144eafb2e9`                                      | 16 bytes |

**EXPECTED OUTPUT:**

| Field            | Value (hex)                          | Length   |
|------------------|--------------------------------------|----------|
| **Tag Valid?**   |     YES                               |          |
| **PT**           | `f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff`    | 16 bytes |

---

## TV-D07 — Decrypt TV-E07 (Multi-block PT)

**INPUT:**

| Field      | Value (hex)                                                                                              | Length   |
|------------|----------------------------------------------------------------------------------------------------------|----------|
| **Key**    | `c0c1c2c3c4c5c6c7c8c9cacbcccdcecf`                                                                      | 16 bytes |
| **Nonce**  | `d0d1d2d3d4d5d6d7d8d9dadbdcdddedf`                                                                      | 16 bytes |
| **AD**     | —                                                                                                        | 0 bytes  |
| **CT**     | `9da1452e86dbb69f888435fe33f74415` `ca72b28a14b350f6f48d5ccff59801db` `f58ca5879d91f8a362ab71bb458c9d30`  | 48 bytes |
| **Tag**    | `08c16ac8ad18cd1c6b414882324ee1a7`                                                                      | 16 bytes |

**EXPECTED OUTPUT:**

| Field            | Value (hex)                                                                                              | Length   |
|------------------|----------------------------------------------------------------------------------------------------------|----------|
| **Tag Valid?**   |     YES                                                                                                    |          |
| **PT**           | `000102030405060708090a0b0c0d0e0f` `101112131415161718191a1b1c1d1e1f` `202122232425262728292a2b2c2d2e2f`  | 48 bytes |

---

## TV-D08 — Decrypt TV-E08 (Multi-block AD + PT)

**INPUT:**

| Field      | Value (hex)                                                                                    | Length   |
|------------|------------------------------------------------------------------------------------------------|----------|
| **Key**    | `1234567890abcdef1234567890abcdef`                                                              | 16 bytes |
| **Nonce**  | `abcdef0123456789abcdef0123456789`                                                              | 16 bytes |
| **AD**     | `416c6c20796f757220626173652061726520626c6f6e6720746f207573210100`                              | 32 bytes |
| **CT**     | `a9ab3243d7a7c7e64aa7756303d9f7af` `2348e2c0e51700bceeb1d16584c75ce4` `3723d8`                    | 35 bytes |
| **Tag**    | `275a71dba8a43d20aa66168635535e4f`                                                              | 16 bytes |

**EXPECTED OUTPUT:**

| Field            | Value (hex)                                                                                    | Length   |
|------------------|------------------------------------------------------------------------------------------------|----------|
| **Tag Valid?**   |   YES                                                                                          |          |
| **PT**           | `5468652071756963206272206f776e20` `666f78206a756d7073206f7665722074` `686520`                    | 35 bytes |

---

## TV-D09 — Tampered Ciphertext (1 bit flipped)

CT byte 0 changed from `62` → `63` (bit 0 flipped). Decryption must reject.

**INPUT:**

| Field      | Value (hex)                          | Length   |
|------------|--------------------------------------|----------|
| **Key**    | `deadbeefcafebabe1122334455667788`    | 16 bytes |
| **Nonce**  | `aabbccddeeff00110011223344556677`    | 16 bytes |
| **AD**     | `6d65746164617461`                    | 8 bytes  |
| **CT**     | `630d139f5417ce5677ca`                | 10 bytes |
| **Tag**    | `2bbfa81dafd020f685a09e067363fc9a`    | 16 bytes |

**EXPECTED OUTPUT:**

| Field            | Value                                         |
|------------------|-----------------------------------------------|
| **Tag Valid?**   |   **NO** — computed tag does not match input  |
| **PT**           | **FAIL** — do not release any plaintext        |

---

## TV-D10 — Tampered Tag (last byte inverted)

Tag byte 15 changed from `a7` → `58` (all bits inverted). Decryption must reject.

**INPUT:**

| Field      | Value (hex)                                                                                              | Length   |
|------------|----------------------------------------------------------------------------------------------------------|----------|
| **Key**    | `c0c1c2c3c4c5c6c7c8c9cacbcccdcecf`                                                                      | 16 bytes |
| **Nonce**  | `d0d1d2d3d4d5d6d7d8d9dadbdcdddedf`                                                                      | 16 bytes |
| **AD**     | —                                                                                                        | 0 bytes  |
| **CT**     | `9da1452e86dbb69f888435fe33f74415` `ca72b28a14b350f6f48d5ccff59801db` `f58ca5879d91f8a362ab71bb458c9d30`  | 48 bytes |
| **Tag**    | `08c16ac8ad18cd1c6b414882324ee158`                                                                      | 16 bytes |

**EXPECTED OUTPUT:**

| Field            | Value                                         |
|------------------|-----------------------------------------------|
| **Tag Valid?**   |   **NO** — computed tag does not match input  |
| **PT**           |**FAIL** — do not release any plaintext        |

---

 
