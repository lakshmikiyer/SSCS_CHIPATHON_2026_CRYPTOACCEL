# ASCON Verification Log

## round_constant.v

Status:
PASS

Verification:
GTKWave + Simulation

Expected Output:

0  -> F0
1  -> E1
2  -> D2
3  -> C3
4  -> B4
5  -> A5
6  -> 96
7  -> 87
8  -> 78
9  -> 69
10 -> 5A
11 -> 4B

Result:
PASS

## diffusion.v

Status:
PASS

Verification:
Simulation + GTKWave

Test Inputs:
0123456789ABCDEF
FEDCBA9876543210
89ABCDEF01234567
A5A5A5A5A5A5A5A5
5A5A5A5A5A5A5A5A

Result:
PASS

## sbox5.v

Status:
PASS

Verification:
Compared all 32 entries against official ASCON S-box table.

Result:
PASS

## substitution_layer.v

Status:
PASS

Description:
64-way parallel ASCON substitution layer implemented using
64 instances of the verified 5-bit ASCON S-box.

Test Inputs:
S0 = 0123456789ABCDEF
S1 = FEDCBA9876543210
S2 = 89ABCDEF01234567
S3 = A5A5A5A5A5A5A5A5
S4 = 5A5A5A5A5A5A5A5A

Observed Outputs:
S0 = 0121052509290D2D
S1 = 2406604224066042
S2 = D2D2D2D2D2D2D2D2
S3 = 8888888888888888
S4 = 5B7B5F7FDBFBDFFF

Result:
PASS


## round.v

Status:
PASS

Description:
Single ASCON round implementation.

Architecture:
pC -> pS -> pL

Modules Used:
- round_constant.v
- substitution_layer.v
- diffusion.v

Verification:
- Functional simulation
- GTKWave inspection
- Round constant variation test

Result:
PASS

## permutation.v

Status:
PASS

Architecture:
Iterative permutation engine

Supported Modes:
- P12 (rounds 0-11)
- P8  (rounds 4-11)

Verification:
- Functional simulation
- GTKWave inspection
- P12 execution verified
- P8 execution verified
- Done signal verified
- State evolution verified

Result:
PASS