# Physical Design
---

For this tapeout, we are working with open source tool chain.
For completing the RTL to GDS flow, we are using automated flows like LibreLane and ORFS as recommended by IEEE SSCS chipathon committee.

---

### Setup of Librelane:
<img width="800" height="229" alt="image" src="https://github.com/user-attachments/assets/c2751568-7423-4082-9576-022610acff57" />

```
Setup:
- Installed docker desktop
- Installed klayout
- Installed vscxrv (Xlaunch) for running gui.
- Used IIC-OSIC-TOOLS Docker container – downloaded the image from
hpretl/iic-osic-tools docker image – contains librelane flow along with needed PDK -
gf180
- Initialization: launched docker container and mounted it to windows by creating “eda”
directory → foss/designs
- Example Testing: Ran counter_demo, with a custom config.yaml ( analogous to
config.mk from ORFS) and constraint.sdc
- Files used to run this example: FOLDER: counter_demo → FILES: counter.v,
config.yaml, constraint.sdc
- Launched docker desktop, opened container’s terminal, and ran the flow with the
command: librelane config.yaml --pdk gf180mcuD --pdk-root /foss/pdks --run-tag
counter_run

 We utilized LibreLane, a Python-based RTL-to-GDSII flow that orchestrates Yosys, OpenROAD, and Magic, chosen for its seamless Docker integration via IIC-OSIC-TOOLS.
```

---

### Current Progress:
`Note: Current progress is based on the design of ASCON core only.`
#### RTL used: Non-Pipelined
Once all of the files are setup, we moved to running the flow in Docker terminal:
` librelane config.yaml --pdk gf180mcuD --pdk-root /foss/pdks --manual-pdk
--run-tag ascon_run_final `

Run Summary: before getting a completed run , i ran the script 3-4 times, where the
average time of run is 40 minutes. Here is a summary of the failed documented runs:

- 1. run 1 - failed after 37mins — reduced setup and hold constraints from 3,3ns to
1,0.25ns
- 2. run 2 - failed after 44:35mins - during detailed routing due to clock buffer
insertion— reduced target density from 0.7 to 0.6
- 3. run 3 - failed after ~30mins - during detailed routing due to 5-micron power straps
physically crushing the standard cell pins (a setting copied over from the
counter_demo config YAML) — so i reduced PDN vertical/horizontal widths from
5.0µm down to 1.6µm.

The working run needed about 43:13 mins to complete all 80 stages of the flow.

##### Our conditions for the flow were:
- Clock freq: 50Mhz
- Clock period: 20ns
- Target Density: 0.6
- Die size: 1100x1100

### GDS Visualization:
<img width="1251" height="744" alt="image" src="https://github.com/user-attachments/assets/f15daf77-dcb3-4daa-b75a-c21d978ce7ef" />
<img width="1158" height="824" alt="image" src="https://github.com/user-attachments/assets/b889524a-9d9c-41bf-994c-56495800d9a7" />

using mattven's librelane-summary script:
<img width="1240" height="197" alt="image" src="https://github.com/user-attachments/assets/fde6b56f-4f82-478c-a0cc-63e594d6c610" />
As we can see from this summary table, Slow corner max_ss_125c is failing.
There is a setup violation, and the WNS is around -10.91 ns. 
We are currently working on improving this, with changes in clock speed and pipelining in rtl, along with tweaking routing parameters.

### Preliminary Results

| **Category** | **Metric / Check** | **Condition / PVT Corner** | **Result** | **Status** |
|:------------|:-------------------|:---------------------------|:----------:|:----------:|
| **Physical Characteristics** | Standard Cell Count | — | 15,811 | — |
|  | Core Area | — | 1.19 mm² | — |
|  | Target Density | — | 60% | — |
|  | Total Power | — | ~181 mW | — |
| **Physical Verification (Signoff)** | Design Rule Check (DRC) | — | 0 Errors | ✅ PASS |
|  | Antenna Violations | — | 0 Errors | ✅ PASS |
|  | LVS (Layout vs Schematic) | — | 0 Errors | ✅ PASS |
|  | Power Grid Violations | — | 0 Errors | ✅ PASS |
| **Timing Analysis** | Setup Slack | Nominal *(nom_tt_025C_3v30)* | +3.43 ns | ✅ Pass |
|  | Hold Slack | Nominal *(nom_tt_025C_3v30)* | +1.04 ns | ✅ Pass |
|  | Setup Slack | Fast *(min_ff_n40C_3v60)* | +9.15 ns | ✅ Pass |
|  | Hold Slack | Fast *(min_ff_n40C_3v60)* | +0.48 ns | ✅ Pass |
|  | Setup Slack | Slow *(max_ss_125C_3v00)* | -10.91 ns | ❌ Violation |
|  | Hold Slack | Slow *(max_ss_125C_3v00)* | +0.64 ns | ✅ Pass |
