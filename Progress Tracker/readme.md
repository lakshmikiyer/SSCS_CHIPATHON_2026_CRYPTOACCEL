 # ASCON AEAD 128: Progress Tracker
---
## 1. Specification & Idea Decision
| Task | Target / Completion Date | Ownership | Status | Comments |
| :--- | :--- | :--- | :--- | :--- |
| Finalize Cryptographic Hardware Accelerator Domain | May 19, 2026 | Team | ✅ Completed | - |
| ASCON Algorithm Idea Finalized | May 26, 2026 | Team | ✅ Completed | - |

## 2. Architecture & RTL (Design + Verification)
| Task | Target / Completion Date | Ownership | Status | Comments |
| :--- | :--- | :--- | :--- | :--- |
| ASCON Core (Design + Arch) | Jun 4, 2026 | Lakshmi & Tarun | ✅ Completed | AEAD128a variant |
| ASCON Core Design Verification (RTL) | Jun 9, 2026 | Yash | ✅ Completed | Verilog TB + py based CocoTB |
| AXI-LITE Slave & Master (RTL) | Jun 30, 2026 | Lakshmi | ✅ Completed | - |
| SPI Slave (RTL) | Jun 30, 2026 onwards | Lakshmi | 🔄 In Progress | - |
| NIST-Based KAT Verification | Jul 6, 2026 | Yash | ✅ Completed | Added as per reviewer comment (1089 cases passed) |

## 3. Synthesis (Running & Verification)
| Task | Target / Completion Date | Ownership | Status | Comments |
| :--- | :--- | :--- | :--- | :--- |
| ASCON Core Verification (Post-syn timing) | Jun 29, 2026 | Yash | ✅ Completed | - |
| AXI-LITE Slave & Master (Post-syn timing) | TBD | Yash & Tarun |  ⏳ Pending  | - |
| SPI Slave (Post-syn timing) | TBD | Yash & Tarun | ⏳ Pending | To be completed |
| Chip_top IO cell integration (Post-syn timing) | TBD | Lakshmi, Yash, Tarun | ⏳ Pending | To be completed |

## 4. Physical Design (LibreLane & ORFS)
| Task | Target / Completion Date | Ownership | Status | Comments |
| :--- | :--- | :--- | :--- | :--- |
| ORFS Setup & Initial Prototyping | started Jun 16, 2026 | Tarun & Yash | 🔄 In Progress | Setup done, prototyping started |
| LibreLane Setup & Prototyping | started Jun 27, 2026 | Yash | 🔄 In Progress | Setup done, prototyping started |
| Chip_top IO cell integration (PNR flow) | TBD | Lakshmi, Yash, Tarun | ⏳ Pending | To be completed |
| Chip_top Final (DRC & LVS Check) | TBD | Lakshmi, Yash, Tarun | ⏳ Pending | To be completed |

## 5. Documentation & Presentations
| Task | Target / Completion Date | Ownership | Status | Comments |
| :--- | :--- | :--- | :--- | :--- |
| Proposal Documentation | Jun 2, 2026 | Yash & Lakshmi | ✅ Completed | - |
| Proposal Live Presentation | Jun 11, 2026 | Lakshmi | ✅ Completed | Presented on June 12 |
| Schematic Round Review (PPT + Video) | Jul 4, 2026 | Lakshmi | ✅ Completed | Submitted |
