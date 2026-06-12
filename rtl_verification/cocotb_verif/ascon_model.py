"""
ascon_model.py — Golden reference model for ASCON-AEAD128
"""
 
MASK64 = 0xFFFFFFFFFFFFFFFF
IV_CONST = 0x00001000808c0001
DOMSEP = 0x8000000000000000


def rotr64(x, n):
    return ((x >> n) | (x << (64 - n))) & MASK64


def ascon_round_fn(s0, s1, s2, s3, s4, rc):
    s2 ^= rc

    s0 ^= s4;  s4 ^= s3;  s2 ^= s1
    t0 = (~s0 & MASK64) & s1
    t1 = (~s1 & MASK64) & s2
    t2 = (~s2 & MASK64) & s3
    t3 = (~s3 & MASK64) & s4
    t4 = (~s4 & MASK64) & s0
    s0 ^= t1;  s1 ^= t2;  s2 ^= t3;  s3 ^= t4;  s4 ^= t0
    s1 ^= s0;  s0 ^= s4;  s3 ^= s2;  s2 = (~s2) & MASK64

    s0 = s0 ^ rotr64(s0, 19) ^ rotr64(s0, 28)
    s1 = s1 ^ rotr64(s1, 61) ^ rotr64(s1, 39)
    s2 = s2 ^ rotr64(s2,  1) ^ rotr64(s2,  6)
    s3 = s3 ^ rotr64(s3, 10) ^ rotr64(s3, 17)
    s4 = s4 ^ rotr64(s4,  7) ^ rotr64(s4, 41)

    return s0, s1, s2, s3, s4


RCON_TABLE = {
    4: 0xf0, 5: 0xe1, 6: 0xd2, 7: 0xc3,
    8: 0xb4, 9: 0xa5, 10: 0x96, 11: 0x87,
    12: 0x78, 13: 0x69, 14: 0x5a, 15: 0x4b,
}


def ascon_p(s0, s1, s2, s3, s4, num_rounds):
    start_ci = 16 - num_rounds
    for ci in range(start_ci, 16):
        rc = RCON_TABLE[ci]
        s0, s1, s2, s3, s4 = ascon_round_fn(s0, s1, s2, s3, s4, rc)
    return s0, s1, s2, s3, s4


def bytes_to_u64(b8):
    return int.from_bytes(b8, 'little')


def u64_to_bytes(w):
    return (w & MASK64).to_bytes(8, 'little')


def bytes_to_key_nonce(key_bytes, nonce_bytes):
    assert len(key_bytes) == 16, f"Key must be 16 bytes, got {len(key_bytes)}"
    assert len(nonce_bytes) == 16, f"Nonce must be 16 bytes, got {len(nonce_bytes)}"
    k0 = bytes_to_u64(key_bytes[0:8])
    k1 = bytes_to_u64(key_bytes[8:16])
    n0 = bytes_to_u64(nonce_bytes[0:8])
    n1 = bytes_to_u64(nonce_bytes[8:16])
    return k0, k1, n0, n1


def pad_to_128(data, nbytes):
    block = bytearray(16)
    for i in range(nbytes):
        block[i] = data[i]
    if nbytes < 16:
        block[nbytes] = 0x01
    lo = int.from_bytes(block[0:8], 'little')
    hi = int.from_bytes(block[8:16], 'little')
    return lo, hi


def absorb_ad(S0, S1, S2, S3, S4, ad_bytes_data):
    ad_len = len(ad_bytes_data)
    if ad_len == 0:
        return S0, S1, S2, S3, S4

    RATE = 16
    full_blocks = ad_len // RATE
    remaining = ad_len % RATE

    for i in range(full_blocks):
        chunk = ad_bytes_data[i*RATE : (i+1)*RATE]
        a_lo = int.from_bytes(chunk[0:8], 'little')
        a_hi = int.from_bytes(chunk[8:16], 'little')
        S0 ^= a_lo
        S1 ^= a_hi
        S0, S1, S2, S3, S4 = ascon_p(S0, S1, S2, S3, S4, 8)

    tail = ad_bytes_data[full_blocks*RATE:]
    a_lo, a_hi = pad_to_128(tail, remaining)
    S0 ^= a_lo
    S1 ^= a_hi
    S0, S1, S2, S3, S4 = ascon_p(S0, S1, S2, S3, S4, 8)

    return S0, S1, S2, S3, S4


def ascon_encrypt(key_bytes, nonce_bytes, ad_bytes_data, pt_bytes):
    k0, k1, n0, n1 = bytes_to_key_nonce(key_bytes, nonce_bytes)

    S0, S1, S2, S3, S4 = IV_CONST, k0, k1, n0, n1
    S0, S1, S2, S3, S4 = ascon_p(S0, S1, S2, S3, S4, 12)

    S3 ^= k0
    S4 ^= k1

    S0, S1, S2, S3, S4 = absorb_ad(S0, S1, S2, S3, S4, ad_bytes_data)

    S4 ^= DOMSEP

    ct = bytearray()
    pt_len = len(pt_bytes)
    RATE = 16

    if pt_len > 0:
        full_pt = pt_len // RATE

        for i in range(full_pt):
            chunk = pt_bytes[i*RATE : (i+1)*RATE]
            p_lo = int.from_bytes(chunk[0:8], 'little')
            p_hi = int.from_bytes(chunk[8:16], 'little')
            is_last = (i == full_pt - 1) and (pt_len % RATE == 0)

            if is_last:
                c_lo = S0 ^ p_lo
                c_hi = S1 ^ p_hi
                ct.extend(u64_to_bytes(c_lo))
                ct.extend(u64_to_bytes(c_hi))
                S0 = S0 ^ p_lo
                S1 = S1 ^ p_hi
            else:
                c_lo = S0 ^ p_lo
                c_hi = S1 ^ p_hi
                ct.extend(u64_to_bytes(c_lo))
                ct.extend(u64_to_bytes(c_hi))
                S0 = S0 ^ p_lo
                S1 = S1 ^ p_hi
                S0, S1, S2, S3, S4 = ascon_p(S0, S1, S2, S3, S4, 8)

        remaining = pt_len - full_pt * RATE
        if remaining > 0:
            chunk = pt_bytes[full_pt*RATE:]
            rate_bytes = u64_to_bytes(S0) + u64_to_bytes(S1)

            ct_block = bytearray(16)
            new_rate = bytearray(16)
            for di in range(16):
                if di < remaining:
                    ct_block[di] = rate_bytes[di] ^ chunk[di]
                    new_rate[di] = rate_bytes[di] ^ chunk[di]
                elif di == remaining:
                    ct_block[di] = 0x00
                    new_rate[di] = rate_bytes[di] ^ 0x01
                else:
                    ct_block[di] = 0x00
                    new_rate[di] = rate_bytes[di]

            ct.extend(ct_block[:remaining])
            S0 = int.from_bytes(new_rate[0:8], 'little')
            S1 = int.from_bytes(new_rate[8:16], 'little')
    else:
        rate_bytes = u64_to_bytes(S0) + u64_to_bytes(S1)
        new_rate = bytearray(rate_bytes)
        new_rate[0] ^= 0x01
        S0 = int.from_bytes(new_rate[0:8], 'little')
        S1 = int.from_bytes(new_rate[8:16], 'little')

    S2 ^= k0
    S3 ^= k1

    S0, S1, S2, S3, S4 = ascon_p(S0, S1, S2, S3, S4, 12)

    t0 = S3 ^ k0
    t1 = S4 ^ k1
    tag = u64_to_bytes(t0) + u64_to_bytes(t1)

    return bytes(ct), bytes(tag)


def ascon_decrypt(key_bytes, nonce_bytes, ad_bytes_data, ct_bytes, tag_bytes):
    k0, k1, n0, n1 = bytes_to_key_nonce(key_bytes, nonce_bytes)

    S0, S1, S2, S3, S4 = IV_CONST, k0, k1, n0, n1
    S0, S1, S2, S3, S4 = ascon_p(S0, S1, S2, S3, S4, 12)
    S3 ^= k0
    S4 ^= k1

    S0, S1, S2, S3, S4 = absorb_ad(S0, S1, S2, S3, S4, ad_bytes_data)

    S4 ^= DOMSEP

    pt = bytearray()
    ct_len = len(ct_bytes)
    RATE = 16

    if ct_len > 0:
        full_ct = ct_len // RATE

        for i in range(full_ct):
            chunk = ct_bytes[i*RATE : (i+1)*RATE]
            c_lo = int.from_bytes(chunk[0:8], 'little')
            c_hi = int.from_bytes(chunk[8:16], 'little')
            is_last = (i == full_ct - 1) and (ct_len % RATE == 0)

            if is_last:
                p_lo = S0 ^ c_lo
                p_hi = S1 ^ c_hi
                pt.extend(u64_to_bytes(p_lo))
                pt.extend(u64_to_bytes(p_hi))
                S0 = c_lo
                S1 = c_hi
            else:
                p_lo = S0 ^ c_lo
                p_hi = S1 ^ c_hi
                pt.extend(u64_to_bytes(p_lo))
                pt.extend(u64_to_bytes(p_hi))
                S0 = c_lo
                S1 = c_hi
                S0, S1, S2, S3, S4 = ascon_p(S0, S1, S2, S3, S4, 8)

        remaining = ct_len - full_ct * RATE
        if remaining > 0:
            chunk = ct_bytes[full_ct*RATE:]
            rate_bytes = u64_to_bytes(S0) + u64_to_bytes(S1)

            pt_block = bytearray(16)
            new_rate = bytearray(16)
            for di in range(16):
                if di < remaining:
                    pt_block[di] = rate_bytes[di] ^ chunk[di]
                    new_rate[di] = chunk[di]
                elif di == remaining:
                    pt_block[di] = 0x00
                    new_rate[di] = rate_bytes[di] ^ 0x01
                else:
                    pt_block[di] = 0x00
                    new_rate[di] = rate_bytes[di]

            pt.extend(pt_block[:remaining])
            S0 = int.from_bytes(new_rate[0:8], 'little')
            S1 = int.from_bytes(new_rate[8:16], 'little')
    else:
        rate_bytes = u64_to_bytes(S0) + u64_to_bytes(S1)
        new_rate = bytearray(rate_bytes)
        new_rate[0] ^= 0x01
        S0 = int.from_bytes(new_rate[0:8], 'little')
        S1 = int.from_bytes(new_rate[8:16], 'little')

    S2 ^= k0
    S3 ^= k1
    S0, S1, S2, S3, S4 = ascon_p(S0, S1, S2, S3, S4, 12)

    t0 = S3 ^ k0
    t1 = S4 ^ k1
    computed_tag = u64_to_bytes(t0) + u64_to_bytes(t1)

    auth_ok = (computed_tag == tag_bytes)

    return bytes(pt), auth_ok


def key_nonce_to_words(key_bytes, nonce_bytes):
    return bytes_to_key_nonce(key_bytes, nonce_bytes)


def tag_to_words(tag_bytes):
    assert len(tag_bytes) == 16
    t0 = int.from_bytes(tag_bytes[0:8], 'little')
    t1 = int.from_bytes(tag_bytes[8:16], 'little')
    return t0, t1


if __name__ == "__main__":
    print("=" * 60)
    print("ASCON-AEAD128 Golden Model Self-Test")
    print("=" * 60)

    ct, tag = ascon_encrypt(bytes(16), bytes(16), b"", b"")
    assert tag.hex() == "f1e8da91f9fbf090caf3e37ccad91bae", f"TV-E01 tag FAIL: {tag.hex()}"
    assert ct == b"", f"TV-E01 ct FAIL"
    print("TV-E01 PASS (empty AD, empty PT)")

    ct, tag = ascon_encrypt(
        bytes.fromhex("000102030405060708090a0b0c0d0e0f"),
        bytes.fromhex("000102030405060708090a0b0c0d0e0f"),
        b"", b"Hello"
    )
    assert ct.hex() == "af14bce6b9", f"TV-E02 ct FAIL: {ct.hex()}"
    assert tag.hex() == "b6588c3aa63f9ddc5a0cf5f565f358b0", f"TV-E02 tag FAIL: {tag.hex()}"
    print("TV-E02 PASS (5-byte PT)")

    ct, tag = ascon_encrypt(
        bytes.fromhex("0123456789abcdef0123456789abcdef"),
        bytes.fromhex("fedcba9876543210fedcba9876543210"),
        b"",
        bytes.fromhex("000102030405060708090a0b0c0d0e0f")
    )
    assert ct.hex() == "ad53ec51d0e3e5f182df2dbc75ab5e0a", f"TV-E03 ct FAIL: {ct.hex()}"
    assert tag.hex() == "13e4af2d5e180ac739aeb5bfc28d8d21", f"TV-E03 tag FAIL: {tag.hex()}"
    print("TV-E03 PASS (16-byte PT)")

    ct, tag = ascon_encrypt(
        bytes.fromhex("deadbeefcafebabe1122334455667788"),
        bytes.fromhex("aabbccddeeff00110011223344556677"),
        b"metadata", b"secret msg"
    )
    assert ct.hex() == "620d139f5417ce5677ca", f"TV-E04 ct FAIL: {ct.hex()}"
    assert tag.hex() == "2bbfa81dafd020f685a09e067363fc9a", f"TV-E04 tag FAIL: {tag.hex()}"
    print("TV-E04 PASS (8-byte AD, 10-byte PT)")

    ct, tag = ascon_encrypt(
        bytes.fromhex("a0a1a2a3a4a5a6a7a8a9aaabacadaeaf"),
        bytes.fromhex("b0b1b2b3b4b5b6b7b8b9babbbcbdbebf"),
        bytes.fromhex("000102030405060708090a0b0c0d0e0f"
                       "101112131415161718191a1b1c1d1e1f"),
        bytes.fromhex("f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff")
    )
    assert ct.hex() == "e7ced7dca12ba41238b5d35a56652903", f"TV-E06 ct FAIL: {ct.hex()}"
    assert tag.hex() == "3daeefbdf6ec6ecd2f2466fe97328f87", f"TV-E06 tag FAIL: {tag.hex()}"
    print("TV-E06 PASS (32-byte AD + 16-byte PT)")

    ct, tag = ascon_encrypt(
        bytes.fromhex("c0c1c2c3c4c5c6c7c8c9cacbcccdcecf"),
        bytes.fromhex("d0d1d2d3d4d5d6d7d8d9dadbdcdddedf"),
        b"",
        bytes.fromhex("000102030405060708090a0b0c0d0e0f"
                       "101112131415161718191a1b1c1d1e1f"
                       "202122232425262728292a2b2c2d2e2f")
    )
    assert ct.hex() == ("9da1452e86dbb69f888435fe33f74415"
                        "ca72b28a14b350f6f48d5ccff59801db"
                        "f58ca5879d91f8a362ab71bb458c9d30"), f"TV-E07 ct FAIL: {ct.hex()}"
    assert tag.hex() == "fcc32e12cad136afe268873af27b0c99", f"TV-E07 tag FAIL: {tag.hex()}"
    print("TV-E07 PASS (48-byte PT, 3 blocks)")

    ct, tag = ascon_encrypt(
        bytes.fromhex("ffffffffffffffffffffffffffffffff"),
        bytes.fromhex("eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"),
        b"\xaa", b"\xbb"
    )
    assert ct.hex() == "14", f"TV-E09 ct FAIL: {ct.hex()}"
    assert tag.hex() == "176714566f601e224ec71bb58b11ffff", f"TV-E09 tag FAIL: {tag.hex()}"
    print("TV-E09 PASS (1-byte AD + 1-byte PT)")

    key = bytes.fromhex("deadbeefcafebabe1122334455667788")
    nonce = bytes.fromhex("aabbccddeeff00110011223344556677")
    ad = b"metadata"
    pt_orig = b"secret msg"
    ct, tag = ascon_encrypt(key, nonce, ad, pt_orig)
    pt_dec, auth = ascon_decrypt(key, nonce, ad, ct, tag)
    assert auth, "Decrypt auth FAIL"
    assert pt_dec == pt_orig, f"Decrypt PT mismatch: {pt_dec.hex()} vs {pt_orig.hex()}"
    print("Decrypt roundtrip PASS")

    bad_tag = bytearray(tag)
    bad_tag[0] ^= 0xFF
    _, auth_bad = ascon_decrypt(key, nonce, ad, ct, bytes(bad_tag))
    assert not auth_bad, "Tampered tag should FAIL auth"
    print("Tampered tag correctly rejected")

    key2 = bytes.fromhex("a0a1a2a3a4a5a6a7a8a9aaabacadaeaf")
    nonce2 = bytes.fromhex("b0b1b2b3b4b5b6b7b8b9babbbcbdbebf")
    ad2 = bytes.fromhex("000102030405060708090a0b0c0d0e0f"
                         "101112131415161718191a1b1c1d1e1f")
    pt2 = bytes.fromhex("f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff")
    ct2, tag2 = ascon_encrypt(key2, nonce2, ad2, pt2)
    pt2_dec, auth2 = ascon_decrypt(key2, nonce2, ad2, ct2, tag2)
    assert auth2, "32B AD decrypt auth FAIL"
    assert pt2_dec == pt2, f"32B AD decrypt PT mismatch"
    print("32-byte AD roundtrip PASS")

    print("\n" + "=" * 60)
    print("ALL SELF-TESTS PASSED")
    print("=" * 60)

