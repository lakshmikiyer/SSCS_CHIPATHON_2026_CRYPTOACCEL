# SSCS_CHIPATHON_2026_CRYPTOACCEL
# CryptoAccel

Team CryptoAccel's Repository for IEEE SSCS Chipathon 2026:
- **Team Lead** - [*Lakshmi Iyer*](https://www.linkedin.com/in/lakshmi-iyer-27020b40/) - IIT Bombay
- [*Yashvardhan Singh*](https://www.linkedin.com/in/yvs373/) - STMicroelectronics, MIT Manipal
- [*Tarun R S*](https://www.linkedin.com/in/r-s-tarun-279807310/) - IIIT Bangalore
- [*Harshitha Shetty*](https://www.linkedin.com/in/harshitha-shetty-3a4749213/) - PES Bangalore

---
Link to project proposal:  [Click Here ↗](https://docs.google.com/document/d/e/2PACX-1vQ7hXiJkHFsaxKhHVbuH3Zd8qZDoJdL6WpXG3n53tD7aNz_2QSCsUlUvai5AVLdPrBWiSDReBhnfogW/pub)

--- 
<img width="2352" height="480" alt="cryptoaccel_logo" src="https://github.com/user-attachments/assets/9e05458b-7662-42a9-9287-e7aeeaf4b6a3" />

# CryptoAccel: ASCON AEAD128 Cryptographic Hardware Accelerator

**IEEE SSCS PICO Chipathon 2026 (Track A)** | **Target PDK:** GF180MCU

## About the Project

Team CryptoAccel proposes a fully open-source, lightweight cryptographic hardware accelerator IP implementing the ASCON128 Authenticated Encryption with Associated Data (AEAD) algorithm (NIST SP 800-232). Designed as a drop-in peripheral IP for modern System-on-Chip (SoC) architectures, this IP provides a unified security primitive for Root of Trust (RoT), secure boot, and IoT/Edge communication applications.

To the best of our knowledge, this project represents the first standalone ASCON cryptographic accelerator comprehensively designed, verified, and taped out on the GF180MCU PDK utilizing a 100% open-source EDA toolchain.

## Key Features

* **NIST-Standardized Security:** Implements the ASCON lightweight cryptographic standard, providing both encryption and authentication in a single core.
* **Plug-and-Play SoC Integration:** Wrapped in a standard AXI4-Lite slave interface, allowing seamless memory-mapped integration with RISC-V host processors (e.g., Ibex, PicoRV32).
* **Ultra-Low Footprint:** Built on an iterative 1-round-per-cycle permutation engine (~7 kGE), optimizing Power, Performance, and Area (PPA) for resource-constrained edge devices.
* **Open-Source RTL-to-GDSII:** Fully synthesizable Verilog design utilizing an end-to-end open-source physical design flow (Yosys, OpenROAD/OpenLane, KLayout) for a DRC/LVS-clean layout.

---
