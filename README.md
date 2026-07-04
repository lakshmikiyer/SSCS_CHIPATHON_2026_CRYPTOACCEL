# SSCS_CHIPATHON_2026_CRYPTOACCEL
---
Link to project proposal:  [Click Here ↗](https://docs.google.com/document/d/e/2PACX-1vQ7hXiJkHFsaxKhHVbuH3Zd8qZDoJdL6WpXG3n53tD7aNz_2QSCsUlUvai5AVLdPrBWiSDReBhnfogW/pub)

--- 
<img width="2352" height="480" alt="cryptoaccel_logo" src="https://github.com/user-attachments/assets/9e05458b-7662-42a9-9287-e7aeeaf4b6a3" />

# CryptoAccel: ASCON AEAD128a Cryptographic Hardware Accelerator
**IEEE SSCS PICO Chipathon 2026 (Track A)** | **Target PDK:** GF180MCU

## Overview

CryptoAccel is a lightweight hardware accelerator implementing the **ASCON-AEAD128a** authenticated encryption algorithm, standardized by NIST (SP 800-232). It is designed for resource-constrained applications such as IoT security, secure boot, and root-of-trust.

The accelerator is built in synthesizable Verilog and taken through a complete open-source RTL-to-GDSII flow using **OpenROAD Flow Scripts (ORFS)** targeting the **GlobalFoundries 180nm (GF180MCU)** process.

## Repository Structure

```
├── Proposal/               # Project proposal documents
├── docs/                   # Documentation and reports
├── rtl_verification/       # RTL source files and verification environment
├── LICENSE
└── README.md
```
```
> *Repository structure is being finalized. RTL, testbench, and ORFS flow directories will be organized into dedicated folders before tape-out.
```

## Architecture & Design (Lakshmi)

The design consists of three main blocks:

1. **ASCON Core (`ascon_core_adpt_encdec`)** — Implements the full ASCON-AEAD128a state machine: initialization, associated data processing, plaintext/ciphertext processing, finalization, and tag generation/verification. Supports both encryption and decryption modes.

2. **ASCON Round (`ascon_round`)** — A single purely combinational round of the ASCON permutation, comprising the round constant addition (pC), the 5-bit S-box layer (pS), and the linear diffusion layer (pL).

3. **AXI-Lite Wrapper (`ascon_axi_wrapper`)** — Provides a standard AXI4-Lite slave interface for system-level integration. A CPU or SoC master writes key, nonce, associated data, and plaintext through memory-mapped registers, and reads back ciphertext and the authentication tag.

<img width="1340" height="967" alt="image" src="https://github.com/user-attachments/assets/19bc8b5f-9126-45ad-8db6-b8464ad2b238" />


## Design Verification (Yashvardhan)
Functional verification of the ASCON core is performed using Cocotb (a Python-based verification framework) with Icarus Verilog as the simulator. A Python golden reference model generates expected outputs for comparison against the RTL.

The verification plan covers:

Encryption tests — Directed test vectors with varying AD and plaintext lengths (empty, partial block, full block, multi-block).
Decryption tests — Standalone decryption of known ciphertext with tag verification.
Full roundtrip tests — Encrypt-then-decrypt cycles confirming plaintext recovery and auth_ok assertion.
Authentication fault injection — Tampered ciphertext and tampered tag inputs to verify that the core correctly rejects forgeries, validating resistance to reverse-engineering of the ASCON state.
Randomized testing — Cocotb-driven random key/nonce/AD/plaintext generation to increase functional coverage across a wide input space.

## Physical Design — OpenROAD RTL-to-GDSII Flow (ORFS - Tarun, Librelane - Yashvardhan)
## ORFS:
### Development Environment

| Component           | Details                              |
|---------------------|--------------------------------------|
| Operating System    | Ubuntu 24.04 LTS (VM)               |
| Flow Framework      | OpenROAD Flow Scripts (ORFS)         |
| Technology Node     | GF180 MCU                            |
| Synthesis Tool      | Yosys                                |
| Place & Route Tool  | OpenROAD                             |
| Layout Viewer       | KLayout 0.28.16                      |
| Host Platform       | Apple Silicon with Ubuntu VM         |

### Design Configuration

**`config.mk`**
```makefile
export DESIGN_NAME     = ascon_core_adpt_encdec
export PLATFORM        = gf180
export VERILOG_FILES   = \
    $(DESIGN_HOME)/gf180/ascon/ascon_core_adpt_encdec.v \
    $(DESIGN_HOME)/gf180/ascon/ascon_round.v
export CLOCK_PORT      = clk
export CLOCK_PERIOD    = 10
export SDC_FILE        = $(DESIGN_HOME)/gf180/ascon/constraint.sdc
export CORE_UTILIZATION = 40
export PLACE_DENSITY   = 0.50
```

**`constraint.sdc`**
```tcl
create_clock -period 10 -name clk [get_ports clk]
set_input_delay  1 -clock clk [all_inputs]
set_output_delay 1 -clock clk [all_outputs]
```

### Flow Execution

The design was integrated into ORFS by creating a dedicated directory at `flow/designs/gf180/ascon/`. The complete flow was executed with:

```bash
cd flow
make DESIGN_CONFIG=./designs/gf180/ascon/config.mk
```

The following stages completed successfully:

1. RTL Elaboration
2. Logic Synthesis
3. Floorplanning
4. Power Distribution Network Generation
5. Global Placement
6. Detailed Placement
7. Clock Tree Synthesis
8. Global Routing
9. Detailed Routing
10. Fill Cell Insertion
11. Timing Analysis
12. Signoff Checks
13. GDSII Generation

### Pre-Silicon Functional Verification Results

| Test ID | Description                          | Status |
|---------|--------------------------------------|--------|
| TV-01   | Empty AD, Empty Plaintext            | PASS   |
| TV-02   | Empty AD, Plaintext = "Hello"        | PASS   |
| TV-03   | Encrypt-Decrypt Roundtrip            | PASS   |
| TV-04   | Associated Data + Secret Message     | PASS   |

All test vectors passed, confirming correct encryption, decryption, tag generation, and FSM state transitions.

### Floorplan

| Metric      | Value             |
|-------------|-------------------|

To be added

### Flow Runtime

| Metric             | Value       |
|--------------------|-------------|
| Flow Runtime       | 7 min 4 sec |
| Peak Memory Usage  | 465 MB      |

### Implementation Results (Preliminary — 100 MHz)

| Metric                       | Value              |
|-------------------------------|--------------------|
| Total Cell Count              | 5424               |
| Sequential Cells              | 596                |
| Synthesized Area              | 257,036 µm²       |
| Sequential Area               | 57,193 µm²        |
| Sequential Area Percentage    | 22.25%             |
| Final Design Area             | 305,271 µm²       |
| Core Utilization              | 48%                |
| Worst Slack                   | +3.26 ns           |
| Average IR Drop               | 5.62 × 10⁻⁴ V     |
| Worst Case IR Drop            | 1.53 × 10⁻³ V     |

> **Note:** These metrics correspond to the preliminary 100 MHz run. An additional 50 MHz run targeting a die size of 500 µm × 500 µm (0.25 mm², within the 0.64 mm² budget) is planned for simulational performance evaluation.

## Team

| Member        | Role                              |
|---------------|-----------------------------------|
| Lakshmi       | RTL Core Design & Architecture + RTL Design of Interface + Team Management  |
| Yashvardhan   | Design Verification + Post-Synth Verification + PD via Librelane + Documentation    |
| Tarun         | RTL Design + PD via ORFS   |
| Harshitha     | AXI-Lite Wrapper Design   |


## References

- [NIST SP 800-232 — ASCON Standard](https://csrc.nist.gov/pubs/sp/800/232/final)
- [ASCON Official Website](https://ascon.iaik.tugraz.at/)
- [OpenROAD Flow Scripts (ORFS)](https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts)
- [GlobalFoundries GF180MCU PDK](https://github.com/google/gf180mcu-pdk)
 
