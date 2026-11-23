# Custom Stripboard Rev 1.1 & Rev 1.1a — Complete Engineering Specification & Technical Manual

This document consolidates all technical notes, electrical specifications, mechanical constraints, layout design rules, assembly options, fabrication guidelines, and production cost models for **Custom Stripboard Rev 1.1** and **Rev 1.1a**.

---

## 1. Architectural Overview & Design Philosophy

The **Custom Stripboard Rev 1.1 / Rev 1.1a** is a modular industrial prototyping and fan control platform built around standard Eurocard/Vector plugboard dimensions, designed within the open-source **Lepton-EDA** + **`pcb-rnd`** toolchain.

### Fundamental Engineering Principles:
1. **Through-Hole Technology (THT) as the Mandatory Default**:
   - Surface Mount Device (SMD) mounting is strictly an optional alternative.
   - The primary and native manufacturing standard is **100% Through-Hole (THT / PTH)** with plated drill holes.
   - All discrete passives (ceramic disc/monolithic and electrolytic capacitors, axial 1/4W resistors), dual-in-line integrated circuits (DIP), linear voltage regulators (TO-220 upright), screw terminal blocks, and interface headers use plated through-hole pins.
2. **Standardized High-Reliability Pad Sizes ($\ge 80\text{ mil}$)**:
   - All stripboard tie points, terminal block pass-thrus, IC headers, and regulator pads feature an outer copper diameter $\ge 80.00\text{ mil}$ ($2.032\text{ mm}$), a $35.00\text{ mil}$ ($0.889\text{ mm}$) finished drill hole, and an $86.00\text{ mil}$ ($2.184\text{ mm}$) solder mask opening.
   - Scratch-pad prototyping pads feature a $90.00\text{ mil}$ ($2.286\text{ mm}$) pad diameter with an exact $10.00\text{ mil}$ ($0.254\text{ mm}$) copper gap.
3. **Single-Sided Bottom Copper with Industrial Card Edge Connector**:
   - All electrical copper routing resides exclusively on the **bottom solder layer (`Layer 6 "bottom"` / `onsolder`)**.
   - The 44-pin card-edge tongue ($2.54\text{ mm}$ / $100\text{ mil}$ pitch, Sullins/Vector standard) features contact fingers and open solder jumpers solely on the bottom face, leaving the top face unclad FR4 laminate to eliminate short-circuit risks in single-sided card cages.

---

## 2. Mechanical Geometry & M3 Mounting Hole Alignment

### Physical Dimensions:
- **Board Body Width:** $3500.00\text{ mil}$ ($88.90\text{ mm}$)
- **Total Board Length:** $5050.00\text{ mil}$ ($128.27\text{ mm}$)
- **Card-Edge Tongue Width:** $2700.00\text{ mil}$ ($68.58\text{ mm}$), spanning $X = 400.00\text{ mil}$ to $3100.00\text{ mil}$.
- **Tongue Insertion Depth:** $310.00\text{ mil}$ ($7.87\text{ mm}$), from $Y = 4740.00\text{ mil}$ to $5050.00\text{ mil}$.
- **Mechanical Stop Shoulders:** $400.00\text{ mil}$ ($10.16\text{ mm}$) lateral steps at $Y = 4740.00\text{ mil}$.
- **Lead-in Chamfers:** $40.00\text{ mil} \times 45^\circ$ beveling on the bottom tongue corners for smooth card-cage insertion.

### M3 Plated Mounting Holes (Drill: $126.00\text{ mil}$ / $3.20\text{ mm}$, Pad: $240.00\text{ mil}$, Keepout: $300.00\text{ mil}$):
| Identifier | Coordinates $(X, Y)$ | Mechanical Positioning & Clearance Rationale |
| :---: | :---: | :--- |
| **MH101** | $(200.00, 200.00\text{ mil})$ | Top-left perimeter. Ample clearance to DC Power Jack 1 and VR101 module. |
| **MH102** | $(3300.00, 200.00\text{ mil})$ | Top-right perimeter. Maintains $>150\text{ mil}$ isolation to the TB101 terminal block body ($Y = 600\text{ mil}$). |
| **MH103** | $(200.00, 2000.00\text{ mil})$ | **Relocated to $Y = 2000\text{ mil}$**. Positioned midway between LM2596 Module #1 (`VR101`, ending at $Y = 1200\text{ mil}$) and Module #2 (`VR102`, starting at $Y = 2800\text{ mil}$). The $300\text{ mil}$ screw keepout ($Y \in [1850, 2150]$) offers $>650\text{ mil}$ of clearance to both modules. |
| **MH104** | $(3300.00, 2700.00\text{ mil})$ | **Adjusted to $Y = 2700\text{ mil}$**. Maintains $80\text{ mil}$ pad clearance to the bottom of the TB101 terminal block body ($Y = 2500\text{ mil}$) and $135\text{ mil}$ copper clearance to the scratch-pad area ($Y = 2955\text{ mil}$). |
| **MH105** | $(200.00, 4600.00\text{ mil})$ | Bottom-left perimeter. The bottom edge of the copper pad ring ($Y = 4720\text{ mil}$) aligns with the bottom baseline of the prototyping matrix ($Y = 4728\text{ mil}$), ensuring $140\text{ mil}$ clearance to the tongue shoulder ($Y = 4740\text{ mil}$). |
| **MH106** | $(3300.00, 4600.00\text{ mil})$ | Bottom-right perimeter, symmetrically aligned with MH105. |

---

## 3. Top Margin Power Subsystem: DC Barrel Jacks & Dual LM317 Regulators

### 3.1 DC Barrel Jacks & Breakout SIP3 Headers
To accommodate central linear regulators and heat sinks without mechanical interference, the two 2.1mm $\times$ 5.5mm DC barrel jacks were spread towards the board edges:
- **DC Jack 1 (`CONN117`):** Located at $(X = 800.00\text{ mil}, Y = 200.00\text{ mil})$.
  - Dedicated 3-pin breakout SIP3 headers (`CONN119..121`) located at $X = 500, 600, 700\text{ mil}$ ($Y = 200, 300, 400\text{ mil}$).
  - Center pin ($+V$), middle switch contact, and ground sleeve routed exclusively with **$40\text{ mil}$ copper traces (`Layer 6 "bottom"`)** for low impedance up to 5A continuous.
- **DC Jack 2 (`CONN118`):** Located at $(X = 2400.00\text{ mil}, Y = 200.00\text{ mil})$.
  - Dedicated 3-pin breakout SIP3 headers (`CONN122..124`) located at $X = 2800, 2900, 3000\text{ mil}$ ($Y = 200, 300, 400\text{ mil}$).
  - Routed exclusively with **$40\text{ mil}$ copper traces**.

### 3.2 Dual LM317 Linear Voltage Regulators (TI Datasheet, Page 1)
Centered between the two DC barrel jacks ($X = 1400\text{ mil}$ to $X = 2100\text{ mil}$, $Y = 200..700\text{ mil}$), two independent, full-featured LM317 linear regulator circuits are implemented following the Texas Instruments datasheet:

$$V_{OUT} = 1.25\,\text{V} \times \left(1 + \frac{R_2}{R_1}\right) + I_{ADJ} \times R_2$$

```
                         LM317 REGULATOR CIRCUIT (TI Datasheet Page 1)
                              ┌──────────────┐
                  VIN o───────┤ 3 (VIN)      │
                              │   LM317      │
                    ┌─────────┤ 1 (ADJ)    2 ├──┬───────────────o VOUT
                    │         └──────────────┘  │
                    │               │           │
                   [R2]            [R1 240Ω]   [C2 1.0µF]
                    │ (Adjust)      │           │
                    │               └───────────┘
                    │
           GND o────┴───────────────────────────────────────────o GND (Common)
               (C1 0.1µF input bypass decoupling cap)
```

#### LM317 Circuit #1:
- **IC Regulator `U101` (TO-220 Upright):** Pin 3 (VIN) at $(1400, 300)$, Pin 2 (VOUT) at $(1500, 300)$, Pin 1 (ADJ) at $(1600, 300)$.
- **Through-Hole Capacitors:** $C_{101}$ ($0.1\,\mu\text{F}$ ceramic disc) at $(1400, 400..600)$; $C_{102}$ ($1.0\,\mu\text{F}$ tantalum/electrolytic) at $(1500, 400..600)$.
- **Axial Resistors:** $R_{101}$ ($240\,\Omega$, 1/4W) at $(1500..1600, 500)$; $R_{102}$ ($R_2$, fixed or multi-turn trimpot) at $(1600, 400..600)$.
- **THT Interface / Test Pads (Pads $\ge 80\text{ mil}$):** `J101` (VIN1 at $1400, 200$), `J102` (VOUT1 at $1500, 200$), `J103` (GND at $1400, 700$).

#### LM317 Circuit #2:
- **IC Regulator `U102` (TO-220 Upright):** Pin 3 (VIN) at $(1900, 300)$, Pin 2 (VOUT) at $(2000, 300)$, Pin 1 (ADJ) at $(2100, 300)$.
- **Through-Hole Capacitors:** $C_{103}$ ($0.1\,\mu\text{F}$) at $(1900, 400..600)$; $C_{104}$ ($1.0\,\mu\text{F}$) at $(2000, 400..600)$.
- **Axial Resistors:** $R_{103}$ ($240\,\Omega$) at $(2000..2100, 500)$; $R_{104}$ ($R_2$) at $(2100, 400..600)$.
- **THT Interface / Test Pads (Pads $\ge 80\text{ mil}$):** `J104` (VIN2 at $1900, 200$), `J105` (VOUT2 at $2000, 200$), `J106` (GND at $1900, 700$).
- **Common Ground Bus:** A solid $40\text{ mil}$ copper trace at $Y = 600.00\text{ mil}$ joins the ground terminals of both circuits ($X = 1400$ to $X = 2100\text{ mil}$).

---

## 4. Left Margin: Dual Upright LM2596 Step-Down Buck Modules (`VR101`, `VR102`)

For high-efficiency switching step-down regulation (e.g., +12V to +5V or +3.3V up to 3A):
- **Footprint:** $4 \times 7$ pin matrix at $200.00\text{ mil}$ ($5.08\text{ mm}$) pitch ($X = 100, 200, 300, 400\text{ mil}$).
- **Module 1 (`VR101`):** $Y = 600.00\text{ mil}$ to $1200.00\text{ mil}$. Rows 1–4 form `VIN1+` ($X = 100$) and `VIN1-` ($X = 300$); Rows 5–7 form `OUT1+` ($X = 100$) and `OUT1-` ($X = 300$).
- **Module 2 (`VR102`):** $Y = 2800.00\text{ mil}$ to $3400.00\text{ mil}$. Rows 1–4 form `VIN2+` and `VIN2-`; Rows 5–7 form `OUT2+` and `OUT2-`.
- **Power Rails:** Continuous $40\text{ mil}$ copper tracks group the vertical pin arrays into functional power nets.
- **Mounting Hole `MH103`:** Placed at $(X = 200\text{ mil}, Y = 2000\text{ mil})$, perfectly isolated in the gap between `VR101` and `VR102` with $>650\text{ mil}$ clearance.

---

## 5. Right Margin: 10-Position Screw Terminal Block (5.08mm KRE) & Pass-Thru Matrix

Located on the upper right board perimeter between `MH102` and `MH104`:
- **Connector Model (`TB101`):** 10-Position Screw Terminal Block, $5.08\text{ mm}$ ($0.2''$) pitch (ZB128 series, 14mm height).
- **Pin Locations:** $X = 3400.00\text{ mil}$, $Y = [600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400]\text{ mil}$.
- **Horizontal 3-Point Pass-Thru Matrix:** For each terminal screw pin, 3 plated pass-thru holes extend horizontally inward:
  - Point 1: `CONN137` at $X = 3300.00\text{ mil}$
  - Point 2: `CONN138` at $X = 3200.00\text{ mil}$
  - Point 3: `CONN139` at $X = 3100.00\text{ mil}$
- **$30\text{ mil}$ Interconnect Traces:** Each 4-hole row is connected by $30\text{ mil}$ bottom copper traces, establishing 10 fully independent electrical nets (`KRE_1` to `KRE_10`).
- **Mechanical Clearances:**
  - Above ($Y = 600\text{ mil}$): $>150\text{ mil}$ clearance to the `MH102` screw keepout.
  - Below ($Y = 2400\text{ mil}$): Terminal block body ends at $Y = 2500\text{ mil}$, giving $80\text{ mil}$ clearance to the pad of `MH104` ($Y = 2700\text{ mil}$).

---

## 6. Right Margin: Scratch-Pad Prototyping Area (56 Pads, 3 mil Knife-Scratchable Traces)

Located on the lower right perimeter between `MH104` and `MH106`:
- **Matrix Geometry:** 14 rows $\times$ 4 columns = **56 pads** ($X = 3100, 3200, 3300, 3400\text{ mil}$, $Y = 3000$ to $4300\text{ mil}$).
- **Pad Specifications:** $90.00\text{ mil}$ pad diameter, $35.00\text{ mil}$ drill hole, $96.00\text{ mil}$ solder mask opening.
- **$10\text{ mil}$ Copper Gap:** Gap between adjacent pads is exactly **$10.00\text{ mil}$ ($0.254\text{ mm}$)**.
- **$3\text{ mil}$ Knife-Scratchable Traces:**
  - All 56 pads are initially tied into a common electrical net (`SCRATCHPAD`).
  - Adjacent pads are bridged by narrow **$3.00\text{ mil}$ ($0.0762\text{ mm}$)** copper microtraces on the bottom layer.
  - Users can slice through any trace with a hobby scalpel or X-Acto knife to isolate pads or create custom signal groupings.
- **Silkscreen Boundary:** Bounded by a dedicated silkscreen rectangle labeled `"SCRATCH PAD"`.

---

## 7. Standardized Copper Trace Width Hierarchy

| Trace Width | Clearance | Layer | Target Signals & Circuits |
| :---: | :---: | :---: | :--- |
| **$40.00\text{ mil}$** ($1.016\text{ mm}$) | $20.00\text{ mil}$ | Bottom | 8 Primary power rails (+12V, +5V, GND); DC Jack feed lines; LM2596 module power rails; LM317 power/GND rails; Bottom vertical output strips (`SIP4N`). |
| **$30.00\text{ mil}$** ($0.762\text{ mm}$) | $20.00\text{ mil}$ | Bottom | Vertical $100\text{ mil}$ bridge tracks in the `HEADER18` sandwich; Open solder jumper feeds; Terminal block KRE pass-thru lines. |
| **$20.00\text{ mil}$** ($0.508\text{ mm}$) | $20.00\text{ mil}$ | Bottom | LM317 Pin 1 (ADJ) feedback traces to resistors $R_1$ and $R_2$. |
| **$10.00\text{ mil}$** ($0.254\text{ mm}$) | $20.00\text{ mil}$ | Bottom | Horizontal prototyping strip lines (58 lines in Rev 1.1, 64 lines in Rev 1.1a). |
| **$3.00\text{ mil}$** ($0.076\text{ mm}$) | $10.00\text{ mil}$ | Bottom | Knife-scratchable microtraces in the scratch-pad prototyping area. |

---

## 8. Detailed Comparison: Rev 1.1 vs. Rev 1.1a

| Parameter / Feature | Custom Stripboard Rev 1.1 | Custom Stripboard Rev 1.1a |
| :--- | :--- | :--- |
| **Horizontal Prototyping Lines** | 29 rows per bank (Rows 1–29, total 58 9-pin strips) | **32 rows per bank (Rows 1–32, total 64 9-pin strips)** |
| **Sandwich Interconnect Section Placement** | $Y = 3800\text{ mil}$ (`SIP9N`), $Y = 3900..4000\text{ mil}$ (`HEADER18`), $Y = 4100\text{ mil}$ (`SIP9N`) | **Shifted $+200\text{ mil}$ down:** $Y = 4000\text{ mil}$ (`SIP9N`), $Y = 4100..4200\text{ mil}$ (`HEADER18`), $Y = 4300\text{ mil}$ (`SIP9N`) |
| **Utilization of Rows $Y = 3700, 3800, 3900\text{ mil}$** | Open transition gap | **100% Filled:** 9-pin strips `CONN241..243` and `CONN341..343` with $10\text{ mil}$ traces |
| **Clearance to Bottom Output Strips ($Y = 4400\text{ mil}$)** | $300\text{ mil}$ unutilized gap ($Y = 4100$ to $4400\text{ mil}$) | **Seamless:** Bottom sandwich strip at $Y = 4300\text{ mil}$, exactly $100\text{ mil}$ from output strips |
| **Dual LM2596 Upright Modules (`VR101`, `VR102`)** | Present on left margin ($4 \times 7$ pins) | Present on left margin ($4 \times 7$ pins) |
| **Dual LM317 Linear Regulators (`U101`, `U102`)** | Present between DC jacks with THT test pads | Present between DC jacks with THT test pads |
| **10-Way KRE Terminal Block + Pass-Thru** | Present on right margin (`TB101` + 30 pass-thrus) | Present on right margin (`TB101` + 30 pass-thrus) |
| **Scratch-Pad Prototyping Area ($3\text{ mil}$ traces)** | Present between `MH104` and `MH106` | Present between `MH104` and `MH106` |
| **Silkscreen Title** | `"CUSTOM STRIPBOARD REV 1.1"` | `"CUSTOM STRIPBOARD REV 1.1a"` |

---

## 9. Card Edge Connector & Open Solder Jumpers

- **Strictly Single-Sided Architecture:** All 26 edge contact fingers are located on the bottom solder side (`Layer 6 "bottom"` / `onsolder`). The top side is unclad FR4 laminate.
- **Finger Dimensions:** $65.00\text{ mil} \times 230.00\text{ mil}$ ($1.65\text{ mm} \times 5.84\text{ mm}$), centered at $Y = 4925\text{ mil}$ ($Y = 4810$ to $5040\text{ mil}$).
- **Mechanical Keying at Finger 8:** Contact finger 8 ($X = 1200\text{ mil}$) and its solder jumper are intentionally omitted and marked with silkscreen `"KEY"` for card-cage polarizing keys.
- **Open Solder Jumpers:** Positioned between $Y = 4700\text{ mil}$ and $Y = 4810\text{ mil}$ with a **$13\text{ mil}$ ($0.33\text{ mm}$)** open isolation gap. Bridged with a drop of solder to route any strip signal to the edge connector.

---

## 10. Production Cost Analysis (Comprehensive Breakdown)

*(Reference Exchange Rate: USD $1.00 = BRL R$ 5.80)*

### 10.1 Bare PCB Fabrication Costs (FR4, 2-Layer, $45^\circ$ Edge Beveling)
| Production Batch | Fabrication (e.g., JLCPCB / PCBWay) | Freight & Import Duty (BR) | Unit PCB Cost (USD) | Unit PCB Cost (BRL) |
| :---: | :---: | :---: | :---: | :---: |
| **Prototype Batch (5 pcs)** | $4.00 base + $6.00 beveling | $14.00 | **$4.80** | **R$ 28.00** |
| **Small Batch (30 pcs)** | $28.00 base + $10.00 beveling | $22.00 | **$2.00** | **R$ 11.60** |
| **Volume Run (100 pcs)** | $75.00 base + $15.00 ENIG/beveling | $35.00 | **$1.25** | **R$ 7.25** |

### 10.2 Bill of Materials (BOM) per Unit (100% Through-Hole THT)
| Item | Component / Description | Qty | Unit Price (USD) | Unit Price (BRL) | Total Cost (BRL) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **U1** | ATmega328P-PU (Narrow DIP-28) | 1 | $2.20 | R$ 12.80 | R$ 12.80 |
| **SKT1** | DIP-28 IC Socket | 1 | $0.25 | R$ 1.50 | R$ 1.50 |
| **U2** | ULN2003A / ULN7003A Darlington (DIP-16) | 1 | $0.40 | R$ 2.30 | R$ 2.30 |
| **SKT2** | DIP-16 IC Socket | 1 | $0.15 | R$ 0.90 | R$ 0.90 |
| **MOD1** | CH340 6-Pin USB-to-TTL Serial Module | 1 | $1.20 | R$ 7.00 | R$ 7.00 |
| **Y1** | 16.000 MHz Crystal HC-49S | 1 | $0.18 | R$ 1.00 | R$ 1.00 |
| **C3, C4** | 22 pF Ceramic Disc Capacitors | 2 | $0.05 | R$ 0.30 | R$ 0.60 |
| **U101, U102** | LM317T Linear Regulator (TO-220 Upright) | 2 | $0.40 | R$ 2.30 | R$ 4.60 |
| **VR101, VR102**| LM2596 Upright DC-DC Step-Down Module | 2 | $1.30 | R$ 7.50 | R$ 15.00 |
| **TB101** | 10-Way 5.08mm Screw Terminal Block (ZB128) | 1 | $1.10 | R$ 6.40 | R$ 6.40 |
| **CONN117, 118**| 2.1mm $\times$ 5.5mm DC Power Jack THT | 2 | $0.25 | R$ 1.45 | R$ 2.90 |
| **HDR_SANDWICH**| 2.54mm Pin Headers (Male + Female Strips) | 2 strips | $0.60 | R$ 3.50 | R$ 7.00 |
| **PASSIVES** | Decoupling caps (100nF, 1uF, 100uF) + 1/4W Resistors | 1 kit | $0.70 | R$ 4.00 | R$ 4.00 |
| **MECHANICAL** | M3 Brass/Nylon Standoffs, Screws, Nuts | 6 sets | $0.80 | R$ 4.60 | R$ 4.60 |
| **TOTAL BOM** | **Raw Electronic Component Costs** | — | **$9.58** | **R$ 55.85** | **R$ 70.60 (w/ margin)** |

### 10.3 Assembly, Soldering & Testing Labor
- **Manual THT Soldering Time:** ~25 to 35 minutes per board.
- **Flashing & Functional Testing:** ~5 to 7 minutes (`make flash`, tachometer validation, 4-channel PWM exercise, voltage regulator verification).
- **Labor Cost Models:**
  - *DIY Builder:* $0.00
  - *Contract Technician (Brazil):* R$ 25.00 to R$ 40.00 per unit.
  - *Automated Wave/Selective Soldering (100+ pcs):* ~$5.00 to $8.00 (R$ 29.00 to R$ 46.00) per unit.

### 10.4 Unit Cost Summary Across Production Volumes

| Production Scenario | Bare PCB Cost | BOM Component Cost | Labor & Quality Test | **Total Unit Cost (BRL)** | **Total Unit Cost (USD)** |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **1. DIY / Prototype (1 to 5 pcs)** | R$ 28.00 | R$ 70.60 | R$ 0.00 (DIY) | **R$ 98.60** | **$17.00** |
| **2. Small Batch Assembly (30 pcs)** | R$ 11.60 | R$ 52.00 | R$ 25.00 | **R$ 88.60** | **$15.30** |
| **3. Volume Production (100+ pcs)** | R$ 7.25 | R$ 42.00 | R$ 20.00 | **R$ 69.25** | **$11.95** |

---

## 11. AI-Assisted Development Record

> [!NOTE]
> **Official Development Attribution:**  
> *"projeto usando lepton-eda/pcb-rnd assistido com IA-Gemini-3.8-Flash-Medium"*

- **AI Model:** Google DeepMind Gemini 3.8 Flash (Medium).
- **User Interaction Iterations:** **17 dialog turns**.
- **Automated Tool Executions:** **413 tool calls** (290 `run_command`, 42 `edit_file`, 28 `manage_task`, 26 `read_file`, 16 `search_web`, 9 `write_file`, 2 `ask_question`).
- **Engineering Toolchain:** Lepton-EDA (`lepton-schematic`, `lepton-netlist`, `lepton-cli`), `pcb-rnd` (photo-mode 300 DPI engine), `gcc` 14.2.0, `avr-gcc` 14.2.0, `avrdude`, Python 3.12/3.13, `reportlab` 4.x, `inkscape`, and `pdftoppm`.

---

## 12. References, Standards & Official Datasheets

1. **Texas Instruments LM317 3-Terminal Adjustable Regulator:**  
   Datasheet SNVS774P. Standard application circuit ($1.25\text{V} - 37\text{V}$, $1.5\text{A}$, $R_1 = 240\,\Omega$, $C_1 = 0.1\,\mu\text{F}$, $C_2 = 1.0\,\mu\text{F}$).  
   [https://www.ti.com/lit/ds/symlink/lm317.pdf](https://www.ti.com/lit/ds/symlink/lm317.pdf)
2. **Texas Instruments / STMicroelectronics ULN2003A & ULN7003A:**  
   Datasheet SLRS027P. Darlington transistor array with internal inductive clamp diodes.  
   [https://www.ti.com/lit/ds/symlink/uln2003a.pdf](https://www.ti.com/lit/ds/symlink/uln2003a.pdf)
3. **Microchip / Atmel ATmega328P-PU:**  
   Datasheet DS40002061B / Atmel-8271. PWM registers, tachometer interrupts, USART0.  
   [https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7810-Automotive-Microcontrollers-ATmega328P_Datasheet.pdf](https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7810-Automotive-Microcontrollers-ATmega328P_Datasheet.pdf)
4. **WCH: CH340 USB-to-Serial TTL Converter:**  
   Official technical product specifications.  
   [https://www.wch-ic.com/products/CH340.html](https://www.wch-ic.com/products/CH340.html)
5. **pnjorge (Paulo Nogueira / F5VMJ):**  
   *"Silent Running With This Dual Fan Controller"* (Hackster.io, 2021).  
   [https://www.hackster.io/pnjorge/silent-running-with-this-dual-fan-controller-0accb8](https://www.hackster.io/pnjorge/silent-running-with-this-dual-fan-controller-0accb8)  
   GitHub Repository: [https://github.com/pnjorge/Cooler-Fan-Controller](https://github.com/pnjorge/Cooler-Fan-Controller)
6. **Sullins Connector Solutions — Card Edge Connectors (0.100" Pitch, ETM / EBM Series):**  
   Standard 44-position / 22-contact single-sided card edge receptacles.  
   [https://www.sullinscorp.com/](https://www.sullinscorp.com/)
7. **Vector Electronics & Technology — Eurocard & Vectorbord Card-Edge Plugboards:**  
   Standard 44-pin plugboards (Model 3662 series).  
   [https://www.vectorelect.com/](https://www.vectorelect.com/)
8. **Intel Corporation:** *4-Wire Pulse Width Modulation (PWM) Controlled Fans Specification*, Rev 1.3.
9. **The Linux Kernel Organization:** *Hardware Monitoring Subsystem (`hwmon`)*.  
   [https://docs.kernel.org/hwmon/](https://docs.kernel.org/hwmon/)
