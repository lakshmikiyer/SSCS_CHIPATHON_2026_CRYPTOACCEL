"""
test_ascon.py - cocotb testbench for ascon_core_adpt_encdec 
  verification of ASCON-AEAD128 encrypt + decrypt.

Categories:
  A) Directed Known-Answer Tests (encrypt)
  B) Decrypt + Authentication Tests
  C) Edge Cases (boundary byte counts)
  D) Randomized Tests
 
"""
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, ClockCycles, Timer, ReadOnly, FallingEdge

import random
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from ascon_model import (
    ascon_encrypt, ascon_decrypt,
    key_nonce_to_words, tag_to_words,
    bytes_to_u64, u64_to_bytes,
)

RANDOM_SEED = 0xA5C0_2026
random.seed(RANDOM_SEED)

CLK_PERIOD_NS = 10


async def reset_dut(dut):
    dut.rst_n.value = 0
    dut.start.value = 0
    dut.dec_mode.value = 0
    dut.k0_in.value = 0
    dut.k1_in.value = 0
    dut.n0_in.value = 0
    dut.n1_in.value = 0
    dut.tag0_in.value = 0
    dut.tag1_in.value = 0
    dut.ad_empty.value = 0
    dut.ad_valid.value = 0
    dut.ad_last.value = 0
    dut.ad_data.value = 0
    dut.ad_bytes.value = 0
    dut.din_valid.value = 0
    dut.din_last.value = 0
    dut.din_data.value = 0
    dut.din_bytes.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 2)


def split_ad_to_dut_blocks(data):
    RATE = 16
    blocks = []
    total = len(data)
    if total == 0:
        return blocks

    full = total // RATE
    remaining = total % RATE

    for i in range(full):
        chunk = data[i*RATE : (i+1)*RATE]
        val = int.from_bytes(chunk, 'little')
        blocks.append({
            'data_128': val,
            'nbytes': 16,
            'is_last': False,
        })

    if remaining > 0:
        chunk = data[full*RATE:]
        padded = chunk + b'\x00' * (RATE - len(chunk))
        val = int.from_bytes(padded, 'little')
        blocks.append({
            'data_128': val,
            'nbytes': remaining,
            'is_last': True,
        })
    else:
        blocks.append({
            'data_128': 0,
            'nbytes': 0,
            'is_last': True,
        })

    return blocks


def split_din_to_dut_blocks(data):
    RATE = 16
    blocks = []
    total = len(data)
    full = total // RATE
    remaining = total % RATE

    for i in range(full):
        chunk = data[i*RATE : (i+1)*RATE]
        val = int.from_bytes(chunk, 'little')
        is_last = (remaining == 0) and (i == full - 1)
        blocks.append({
            'data_128': val,
            'nbytes': 16,
            'is_last': is_last,
        })

    if remaining > 0:
        chunk = data[full*RATE:]
        padded = chunk + b'\x00' * (RATE - len(chunk))
        val = int.from_bytes(padded, 'little')
        blocks.append({
            'data_128': val,
            'nbytes': remaining,
            'is_last': True,
        })

    if total == 0:
        blocks.append({
            'data_128': 0,
            'nbytes': 0,
            'is_last': True,
        })

    return blocks


async def wait_for_signal(dut, signal, timeout_cycles=5000):
    for _ in range(timeout_cycles):
        await RisingEdge(dut.clk)
        await ReadOnly()
        if signal.value == 1:
            return True
    raise TimeoutError(f"Signal {signal._name} did not assert within {timeout_cycles} cycles")


async def run_encrypt(dut, key_bytes, nonce_bytes, ad_data, pt_data, timeout_cycles=5000):
    k0, k1, n0, n1 = key_nonce_to_words(key_bytes, nonce_bytes)

    ad_blocks = split_ad_to_dut_blocks(ad_data)
    pt_blocks = split_din_to_dut_blocks(pt_data)
    ad_is_empty = (len(ad_data) == 0)

    dut.dec_mode.value = 0
    dut.k0_in.value = k0
    dut.k1_in.value = k1
    dut.n0_in.value = n0
    dut.n1_in.value = n1
    dut.tag0_in.value = 0
    dut.tag1_in.value = 0
    dut.ad_empty.value = 1 if ad_is_empty else 0

    dut.start.value = 1
    await RisingEdge(dut.clk)
    dut.start.value = 0

    for _ in range(timeout_cycles):
        await RisingEdge(dut.clk)
        await ReadOnly()
        if dut.busy.value == 1:
            break

    if not ad_is_empty:
        for blk in ad_blocks:
            for _ in range(timeout_cycles):
                await FallingEdge(dut.clk)
                if dut.ad_ready.value == 1:
                    break

            dut.ad_valid.value = 1
            dut.ad_last.value = 1 if blk['is_last'] else 0
            dut.ad_data.value = blk['data_128']
            dut.ad_bytes.value = blk['nbytes']
            await RisingEdge(dut.clk)
            dut.ad_valid.value = 0
            dut.ad_last.value = 0

    ct_bytes = bytearray()

    for blk in pt_blocks:
        for _ in range(timeout_cycles):
            await FallingEdge(dut.clk)
            if dut.din_ready.value == 1:
                break

        dut.din_valid.value = 1
        dut.din_last.value = 1 if blk['is_last'] else 0
        dut.din_data.value = blk['data_128']
        dut.din_bytes.value = blk['nbytes']
        await RisingEdge(dut.clk)
        dut.din_valid.value = 0
        dut.din_last.value = 0

        await ReadOnly()
        assert dut.dout_valid.value == 1, \
            f"dout_valid not asserted after din_valid (blk nbytes={blk['nbytes']})"

        out_data = int(dut.dout_data.value)
        out_bytes_val = int(dut.dout_bytes.value)

        raw = out_data.to_bytes(16, 'little')
        ct_bytes.extend(raw[:out_bytes_val])

    for _ in range(timeout_cycles):
        await RisingEdge(dut.clk)
        await ReadOnly()
        if dut.done.value == 1:
            break

    tag0 = int(dut.t0_out.value)
    tag1 = int(dut.t1_out.value)
    auth_ok = int(dut.auth_ok.value)

    await RisingEdge(dut.clk)

    return bytes(ct_bytes), tag0, tag1, auth_ok


async def run_decrypt(dut, key_bytes, nonce_bytes, ad_data, ct_data,
                      tag0, tag1, timeout_cycles=5000):
    k0, k1, n0, n1 = key_nonce_to_words(key_bytes, nonce_bytes)

    ad_blocks = split_ad_to_dut_blocks(ad_data)
    ct_blocks = split_din_to_dut_blocks(ct_data)
    ad_is_empty = (len(ad_data) == 0)

    dut.dec_mode.value = 1
    dut.k0_in.value = k0
    dut.k1_in.value = k1
    dut.n0_in.value = n0
    dut.n1_in.value = n1
    dut.tag0_in.value = tag0
    dut.tag1_in.value = tag1
    dut.ad_empty.value = 1 if ad_is_empty else 0

    dut.start.value = 1
    await RisingEdge(dut.clk)
    dut.start.value = 0

    for _ in range(timeout_cycles):
        await RisingEdge(dut.clk)
        await ReadOnly()
        if dut.busy.value == 1:
            break

    if not ad_is_empty:
        for blk in ad_blocks:
            for _ in range(timeout_cycles):
                await FallingEdge(dut.clk)
                if dut.ad_ready.value == 1:
                    break

            dut.ad_valid.value = 1
            dut.ad_last.value = 1 if blk['is_last'] else 0
            dut.ad_data.value = blk['data_128']
            dut.ad_bytes.value = blk['nbytes']
            await RisingEdge(dut.clk)
            dut.ad_valid.value = 0
            dut.ad_last.value = 0

    pt_bytes = bytearray()

    for blk in ct_blocks:
        for _ in range(timeout_cycles):
            await FallingEdge(dut.clk)
            if dut.din_ready.value == 1:
                break

        dut.din_valid.value = 1
        dut.din_last.value = 1 if blk['is_last'] else 0
        dut.din_data.value = blk['data_128']
        dut.din_bytes.value = blk['nbytes']
        await RisingEdge(dut.clk)
        dut.din_valid.value = 0
        dut.din_last.value = 0

        await ReadOnly()
        assert dut.dout_valid.value == 1, \
            f"dout_valid not asserted after din_valid (blk nbytes={blk['nbytes']})"

        out_data = int(dut.dout_data.value)
        out_bytes_val = int(dut.dout_bytes.value)

        raw = out_data.to_bytes(16, 'little')
        pt_bytes.extend(raw[:out_bytes_val])

    for _ in range(timeout_cycles):
        await RisingEdge(dut.clk)
        await ReadOnly()
        if dut.done.value == 1:
            break

    auth_ok = int(dut.auth_ok.value)
    await RisingEdge(dut.clk)

    return bytes(pt_bytes), auth_ok


def check_ct_tag(test_name, ct_dut, tag0_dut, tag1_dut, ct_ref, tag_ref):
    t0_ref, t1_ref = tag_to_words(tag_ref)

    ct_pass = (ct_dut == ct_ref)
    t0_pass = (tag0_dut == t0_ref)
    t1_pass = (tag1_dut == t1_ref)

    if ct_pass and t0_pass and t1_pass:
        cocotb.log.info(f"[PASS] {test_name}")
        cocotb.log.info(f"  CT  = {ct_dut.hex() if ct_dut else '(empty)'}")
        cocotb.log.info(f"  Tag = 0x{tag0_dut:016x}_{tag1_dut:016x}")
    else:
        msg = f"[FAIL] {test_name}\n"
        if not ct_pass:
            msg += f"  CT DUT = {ct_dut.hex() if ct_dut else '(empty)'}\n"
            msg += f"  CT REF = {ct_ref.hex() if ct_ref else '(empty)'}\n"
        if not t0_pass:
            msg += f"  T0 DUT = 0x{tag0_dut:016x}  REF = 0x{t0_ref:016x}\n"
        if not t1_pass:
            msg += f"  T1 DUT = 0x{tag1_dut:016x}  REF = 0x{t1_ref:016x}\n"
        cocotb.log.error(msg)
        assert False, msg


@cocotb.test()
async def test_enc_empty_ad_empty_pt(dut):
    clock = Clock(dut.clk, CLK_PERIOD_NS, units="ns")
    cocotb.start_soon(clock.start())
    await reset_dut(dut)

    key   = bytes(16)
    nonce = bytes(16)
    ad    = b""
    pt    = b""

    ct_ref, tag_ref = ascon_encrypt(key, nonce, ad, pt)
    ct_dut, t0, t1, _ = await run_encrypt(dut, key, nonce, ad, pt)
    check_ct_tag("enc_empty_ad_empty_pt", ct_dut, t0, t1, ct_ref, tag_ref)


@cocotb.test()
async def test_enc_empty_ad_short_pt(dut):
    clock = Clock(dut.clk, CLK_PERIOD_NS, units="ns")
    cocotb.start_soon(clock.start())
    await reset_dut(dut)

    key   = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
    nonce = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
    ad    = b""
    pt    = b"Hi"

    ct_ref, tag_ref = ascon_encrypt(key, nonce, ad, pt)
    ct_dut, t0, t1, _ = await run_encrypt(dut, key, nonce, ad, pt)
    check_ct_tag("enc_empty_ad_short_pt", ct_dut, t0, t1, ct_ref, tag_ref)


@cocotb.test()
async def test_enc_empty_ad_one_block(dut):
    clock = Clock(dut.clk, CLK_PERIOD_NS, units="ns")
    cocotb.start_soon(clock.start())
    await reset_dut(dut)

    key   = bytes.fromhex("0123456789abcdef0123456789abcdef")
    nonce = bytes.fromhex("fedcba9876543210fedcba9876543210")
    ad    = b""
    pt    = bytes.fromhex("000102030405060708090a0b0c0d0e0f")

    ct_ref, tag_ref = ascon_encrypt(key, nonce, ad, pt)
    ct_dut, t0, t1, _ = await run_encrypt(dut, key, nonce, ad, pt)
    check_ct_tag("enc_empty_ad_one_block", ct_dut, t0, t1, ct_ref, tag_ref)


@cocotb.test()
async def test_enc_empty_ad_multi_block(dut):
    clock = Clock(dut.clk, CLK_PERIOD_NS, units="ns")
    cocotb.start_soon(clock.start())
    await reset_dut(dut)

    key   = bytes.fromhex("c0c1c2c3c4c5c6c7c8c9cacbcccdcecf")
    nonce = bytes.fromhex("d0d1d2d3d4d5d6d7d8d9dadbdcdddedf")
    ad    = b""
    pt    = bytes.fromhex(
        "000102030405060708090a0b0c0d0e0f"
        "101112131415161718191a1b1c1d1e1f"
        "202122232425262728292a2b2c2d2e2f"
    )

    ct_ref, tag_ref = ascon_encrypt(key, nonce, ad, pt)
    ct_dut, t0, t1, _ = await run_encrypt(dut, key, nonce, ad, pt)
    check_ct_tag("enc_empty_ad_multi_block", ct_dut, t0, t1, ct_ref, tag_ref)


@cocotb.test()
async def test_enc_short_ad_short_pt(dut):
    clock = Clock(dut.clk, CLK_PERIOD_NS, units="ns")
    cocotb.start_soon(clock.start())
    await reset_dut(dut)

    key   = bytes.fromhex("deadbeefcafebabe1122334455667788")
    nonce = bytes.fromhex("aabbccddeeff00110011223344556677")
    ad    = b"metadata"
    pt    = b"secret msg"

    ct_ref, tag_ref = ascon_encrypt(key, nonce, ad, pt)
    ct_dut, t0, t1, _ = await run_encrypt(dut, key, nonce, ad, pt)
    check_ct_tag("enc_short_ad_short_pt", ct_dut, t0, t1, ct_ref, tag_ref)


@cocotb.test()
async def test_enc_multi_ad_multi_pt(dut):
    clock = Clock(dut.clk, CLK_PERIOD_NS, units="ns")
    cocotb.start_soon(clock.start())
    await reset_dut(dut)

    key   = bytes.fromhex("a0a1a2a3b0b1b2b3c0c1c2c3d0d1d2d3")
    nonce = bytes.fromhex("e0e1e2e3f0f1f2f3a0a1a2a3b0b1b2b3")
    ad    = bytes(range(48))
    pt    = bytes(range(48))

    ct_ref, tag_ref = ascon_encrypt(key, nonce, ad, pt)
    ct_dut, t0, t1, _ = await run_encrypt(dut, key, nonce, ad, pt)
    check_ct_tag("enc_multi_ad_multi_pt", ct_dut, t0, t1, ct_ref, tag_ref)


@cocotb.test()
async def test_dec_valid_tag(dut):
    clock = Clock(dut.clk, CLK_PERIOD_NS, units="ns")
    cocotb.start_soon(clock.start())

    key   = bytes.fromhex("deadbeefcafebabe1122334455667788")
    nonce = bytes.fromhex("aabbccddeeff00110011223344556677")
    ad    = b"metadata"
    pt    = b"secret msg"

    ct_ref, tag_ref = ascon_encrypt(key, nonce, ad, pt)
    t0_ref, t1_ref = tag_to_words(tag_ref)

    await reset_dut(dut)
    ct_dut, t0_enc, t1_enc, _ = await run_encrypt(dut, key, nonce, ad, pt)
    check_ct_tag("dec_valid_tag (encrypt phase)", ct_dut, t0_enc, t1_enc, ct_ref, tag_ref)

    await reset_dut(dut)
    pt_dut, auth_ok = await run_decrypt(dut, key, nonce, ad, ct_ref, t0_ref, t1_ref)

    assert auth_ok == 1, f"[FAIL] dec_valid_tag: auth_ok={auth_ok}, expected 1"
    assert pt_dut == pt, f"[FAIL] dec_valid_tag: PT mismatch: {pt_dut.hex()} vs {pt.hex()}"
    cocotb.log.info("[PASS] dec_valid_tag: auth_ok=1, PT recovered correctly")


@cocotb.test()
async def test_dec_invalid_tag(dut):
    clock = Clock(dut.clk, CLK_PERIOD_NS, units="ns")
    cocotb.start_soon(clock.start())
    await reset_dut(dut)

    key   = bytes.fromhex("deadbeefcafebabe1122334455667788")
    nonce = bytes.fromhex("aabbccddeeff00110011223344556677")
    ad    = b"metadata"
    pt    = b"secret msg"

    ct_ref, tag_ref = ascon_encrypt(key, nonce, ad, pt)
    t0_ref, t1_ref = tag_to_words(tag_ref)

    t0_bad = t0_ref ^ 0x1

    _, auth_ok = await run_decrypt(dut, key, nonce, ad, ct_ref, t0_bad, t1_ref)
    assert auth_ok == 0, f"[FAIL] dec_invalid_tag: auth_ok={auth_ok}, expected 0"
    cocotb.log.info("[PASS] dec_invalid_tag: auth_ok=0 (tampered tag correctly rejected)")


@cocotb.test()
async def test_dec_tampered_ct(dut):
    clock = Clock(dut.clk, CLK_PERIOD_NS, units="ns")
    cocotb.start_soon(clock.start())
    await reset_dut(dut)

    key   = bytes.fromhex("deadbeefcafebabe1122334455667788")
    nonce = bytes.fromhex("aabbccddeeff00110011223344556677")
    ad    = b"metadata"
    pt    = b"secret msg"

    ct_ref, tag_ref = ascon_encrypt(key, nonce, ad, pt)
    t0_ref, t1_ref = tag_to_words(tag_ref)

    ct_bad = bytearray(ct_ref)
    ct_bad[0] ^= 0xFF
    ct_bad = bytes(ct_bad)

    _, auth_ok = await run_decrypt(dut, key, nonce, ad, ct_bad, t0_ref, t1_ref)
    assert auth_ok == 0, f"[FAIL] dec_tampered_ct: auth_ok={auth_ok}, expected 0"
    cocotb.log.info("[PASS] dec_tampered_ct: auth_ok=0 (tampered CT correctly rejected)")


@cocotb.test()
async def test_enc_1byte_pt(dut):
    clock = Clock(dut.clk, CLK_PERIOD_NS, units="ns")
    cocotb.start_soon(clock.start())
    await reset_dut(dut)

    key   = bytes.fromhex("ffffffffffffffffffffffffffffffff")
    nonce = bytes.fromhex("eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
    ad    = b""
    pt    = b"\xAA"

    ct_ref, tag_ref = ascon_encrypt(key, nonce, ad, pt)
    ct_dut, t0, t1, _ = await run_encrypt(dut, key, nonce, ad, pt)
    check_ct_tag("enc_1byte_pt", ct_dut, t0, t1, ct_ref, tag_ref)


@cocotb.test()
async def test_enc_15byte_pt(dut):
    clock = Clock(dut.clk, CLK_PERIOD_NS, units="ns")
    cocotb.start_soon(clock.start())
    await reset_dut(dut)

    key   = bytes.fromhex("0f1e2d3c4b5a69780f1e2d3c4b5a6978")
    nonce = bytes.fromhex("78695a4b3c2d1e0f78695a4b3c2d1e0f")
    ad    = b""
    pt    = bytes.fromhex("f0e0d0c0b0a0908070605040302010")

    ct_ref, tag_ref = ascon_encrypt(key, nonce, ad, pt)
    ct_dut, t0, t1, _ = await run_encrypt(dut, key, nonce, ad, pt)
    check_ct_tag("enc_15byte_pt", ct_dut, t0, t1, ct_ref, tag_ref)


@cocotb.test()
async def test_enc_16byte_pt(dut):
    clock = Clock(dut.clk, CLK_PERIOD_NS, units="ns")
    cocotb.start_soon(clock.start())
    await reset_dut(dut)

    key   = bytes.fromhex("0123456789abcdef0123456789abcdef")
    nonce = bytes.fromhex("fedcba9876543210fedcba9876543210")
    ad    = b""
    pt    = bytes(range(16))

    ct_ref, tag_ref = ascon_encrypt(key, nonce, ad, pt)
    ct_dut, t0, t1, _ = await run_encrypt(dut, key, nonce, ad, pt)
    check_ct_tag("enc_16byte_pt", ct_dut, t0, t1, ct_ref, tag_ref)


@cocotb.test()
async def test_enc_17byte_pt(dut):
    clock = Clock(dut.clk, CLK_PERIOD_NS, units="ns")
    cocotb.start_soon(clock.start())
    await reset_dut(dut)

    key   = bytes.fromhex("abcdef0123456789abcdef0123456789")
    nonce = bytes.fromhex("1234567890abcdef1234567890abcdef")
    ad    = b""
    pt    = bytes(range(17))

    ct_ref, tag_ref = ascon_encrypt(key, nonce, ad, pt)
    ct_dut, t0, t1, _ = await run_encrypt(dut, key, nonce, ad, pt)
    check_ct_tag("enc_17byte_pt", ct_dut, t0, t1, ct_ref, tag_ref)


@cocotb.test()
async def test_enc_max_ad_bytes(dut):
    clock = Clock(dut.clk, CLK_PERIOD_NS, units="ns")
    cocotb.start_soon(clock.start())

    key   = bytes.fromhex("aabbccdd11223344aabbccdd11223344")
    nonce = bytes.fromhex("55667788eeff0011556677889900aabb")
    pt    = b"test"

    for ad_len in range(1, 17):
        await reset_dut(dut)
        ad = bytes(range(ad_len))

        ct_ref, tag_ref = ascon_encrypt(key, nonce, ad, pt)
        ct_dut, t0, t1, _ = await run_encrypt(dut, key, nonce, ad, pt)
        check_ct_tag(f"enc_ad_{ad_len}bytes", ct_dut, t0, t1, ct_ref, tag_ref)

    cocotb.log.info("[PASS] enc_max_ad_bytes: All AD lengths 1-16 passed")


@cocotb.test()
async def test_random_encrypt(dut):
    clock = Clock(dut.clk, CLK_PERIOD_NS, units="ns")
    cocotb.start_soon(clock.start())

    random.seed(RANDOM_SEED)

    for i in range(50):
        await reset_dut(dut)

        key   = bytes([random.randint(0, 255) for _ in range(16)])
        nonce = bytes([random.randint(0, 255) for _ in range(16)])
        ad_len = random.randint(0, 256)
        pt_len = random.randint(0, 256)
        ad = bytes([random.randint(0, 255) for _ in range(ad_len)])
        pt = bytes([random.randint(0, 255) for _ in range(pt_len)])

        ct_ref, tag_ref = ascon_encrypt(key, nonce, ad, pt)
        ct_dut, t0, t1, _ = await run_encrypt(dut, key, nonce, ad, pt)

        try:
            check_ct_tag(f"random_enc_{i}", ct_dut, t0, t1, ct_ref, tag_ref)
        except AssertionError:
            cocotb.log.error(f"  Key   = {key.hex()}")
            cocotb.log.error(f"  Nonce = {nonce.hex()}")
            cocotb.log.error(f"  AD    = {ad.hex()} ({ad_len} bytes)")
            cocotb.log.error(f"  PT    = {pt.hex()} ({pt_len} bytes)")
            raise

    cocotb.log.info("[PASS] test_random_encrypt: All 50 random vectors passed")

@cocotb.test()
async def test_random_encrypt_decrypt_roundtrip(dut):
    """D2: 20 random encrypt->decrypt cycles, verify plaintext recovery."""
    clock = Clock(dut.clk, CLK_PERIOD_NS, units="ns")
    cocotb.start_soon(clock.start())

    random.seed(RANDOM_SEED + 1)  # Different seed from D1

    for i in range(20):
        # FIX: Replaced randbytes with list comprehensions for Python 3.6 compatibility
        key   = bytes([random.randint(0, 255) for _ in range(16)])
        nonce = bytes([random.randint(0, 255) for _ in range(16)])
        ad_len = random.randint(0, 128)
        pt_len = random.randint(0, 128)
        ad = bytes([random.randint(0, 255) for _ in range(ad_len)])
        pt = bytes([random.randint(0, 255) for _ in range(pt_len)])

        # Compute reference
        ct_ref, tag_ref = ascon_encrypt(key, nonce, ad, pt)
        t0_ref, t1_ref = tag_to_words(tag_ref)

        # Encrypt on DUT
        await reset_dut(dut)
        ct_dut, t0_enc, t1_enc, _ = await run_encrypt(dut, key, nonce, ad, pt)
        check_ct_tag(f"roundtrip_{i}_enc", ct_dut, t0_enc, t1_enc, ct_ref, tag_ref)

        # Decrypt on DUT using DUT's own ciphertext and tag
        await reset_dut(dut)
        pt_dut, auth_ok = await run_decrypt(dut, key, nonce, ad, ct_dut, t0_enc, t1_enc)

        assert auth_ok == 1, (
            f"[FAIL] roundtrip_{i}_dec: auth_ok={auth_ok}, expected 1\n"
            f"  Key={key.hex()} Nonce={nonce.hex()} AD_len={ad_len} PT_len={pt_len}"
        )
        assert pt_dut == pt, (
            f"[FAIL] roundtrip_{i}_dec: PT mismatch\n"
            f"  DUT = {pt_dut.hex()}\n  REF = {pt.hex()}"
        )

        cocotb.log.info(f"[PASS] roundtrip_{i}: enc+dec OK (AD={ad_len}B, PT={pt_len}B)")

    cocotb.log.info("[PASS] test_random_encrypt_decrypt_roundtrip: All 20 roundtrips passed")


if __name__ == "__main__":
    from cocotb.runner import get_runner
    import os

    sim = os.getenv("SIM", "icarus")
    runner = get_runner(sim)

    runner.build(
        verilog_sources=["design.sv"],
        hdl_toplevel="ascon_core_adpt_encdec",
        always=True,
        build_args=["-g2012"] if sim == "icarus" else []
    )

    runner.test(
        hdl_toplevel="ascon_core_adpt_encdec",
        test_module="testbench"
    )
