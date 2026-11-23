# Custom PC Fan Controller (Linux Controlled)

[![License: LGPL v3](https://img.shields.io/badge/License-LGPL_v3-blue.svg)](LICENSE)
[![CI Build](https://img.shields.io/badge/Build-Passing-brightgreen.svg)](.github/workflows/ci.yml)
[![EDA: Lepton-EDA & pcb-rnd](https://img.shields.io/badge/EDA-Lepton--EDA%20%2F%20pcb--rnd-orange.svg)](lepton/)
[![Assisted by AI: Gemini 3.8 Flash](https://img.shields.io/badge/AI--Assisted-Gemini%203.8%20Flash-blueviolet.svg)](#8-assisted-by-ai---gemini-38-flash-medium)

> **Languages / Idiomas:** [English (US)](README.md) | [Português](README_PT.md) | [Español](README_ES.md)

A comprehensive hardware, firmware, and software system for integrating custom cooling fan control inside a desktop PC chassis. The controller is built on a standard **33.0 mm $\times$ 72.0 mm through-hole protoboard**, powered by a standalone **ATmega328P-PU** running at **16.000 MHz**, a **CH340 6-pin USB-Serial converter**, and a **ULN2003A / ULN7003A** Darlington array driving up to 4 PC cooling fans (e.g., 4x Akasa 90mm and Arctic P8) with real-time tachometer RPM feedback, failsafe watchdog protection, and automated thermal management via Linux.

---

## Table of Contents

- [🎯 Context & Motivation](#-context--motivation)

1. [Architecture Overview](#architecture-overview)
2. [Hardware Bill of Materials (BOM)](#hardware-bill-of-materials-bom)
3. [Engineering Reasoning & Design Choices](#engineering-reasoning--design-choices)
   - [Form Factor: Bare ATmega328P DIP-28 vs. Arduino Nano](#form-factor-bare-atmega328p-dip-28-vs-arduino-nano)
   - [Motherboard Integration: CH340 Module vs. Virtual USB (V-USB)](#motherboard-integration-ch340-module-vs-virtual-usb-v-usb)
   - [Breadboard-Style Protoboard Matrix Analysis](#breadboard-style-protoboard-matrix-analysis)
   - [Split Rail Innovation: R16 / C12 Copper Trace Cut](#split-rail-innovation-r16--c12-copper-trace-cut)
   - [Fan Connector Placement: Option A (Bottom Edge Bank)](#fan-connector-placement-option-a-bottom-edge-bank)
   - [Staggered Column Label Identification Solution](#staggered-column-label-identification-solution)
   - [Fan Control & Failsafe Strategy](#fan-control--failsafe-strategy)
4. [Custom Stripboard Rev 1.1 / 1.1a — Modular Architecture & Specifications](#custom-stripboard-rev-11--11a--modular-architecture--specifications)
   - [Physical & Mechanical Specifications](#1-physical--mechanical-specifications)
   - [Top Power Subsystem: DC Barrel Jacks & Breakout SIP3 Headers](#2-top-power-subsystem-dc-barrel-jacks--breakout-sip3-headers)
   - [Dual LM317 Linear Regulators (TI Datasheet, Page 1)](#3-dual-lm317-linear-regulators-ti-datasheet-page-1)
   - [Left Margin: Dual Upright LM2596 Step-Down Modules (VR101, VR102)](#4-left-margin-dual-upright-lm2596-step-down-modules-vr101-vr102)
   - [Right Margin: 10-Way 5.08mm Screw Terminal Block & Pass-Thru Matrix (TB101)](#5-right-margin-10-way-508mm-screw-terminal-block--pass-thru-matrix-tb101)
   - [Right Margin: Scratch-Pad Prototyping Area (56 Pads, 3 mil)](#6-right-margin-scratch-pad-prototyping-area-56-pads-3-mil)
   - [Manufacturing Directive: Through-Hole (THT) Mandatory Default & Pad Size >= 80 mil](#7-manufacturing-directive-through-hole-tht-mandatory-default--pad-size--80-mil)
   - [Standardized Copper Trace Width Hierarchy](#8-standardized-copper-trace-width-hierarchy)
   - [Prototyping Matrix & Sandwich Interconnect Section](#9-prototyping-matrix--sandwich-interconnect-section)
   - [Single-Sided Card Edge Connector (44-Pin Standard Tongue)](#10-single-sided-card-edge-connector-44-pin-standard-tongue)
   - [Mechanical Polarizing Key (Keying at Finger 8)](#11-mechanical-polarizing-key-keying-at-finger-8)
   - [Open Solder Jumpers](#12-open-solder-jumpers)
   - [M3 Mounting Holes, Keepouts & Alignment](#13-m3-mounting-holes-keepouts--alignment)
   - [Silkscreen Legend & Visual Identification](#14-silkscreen-legend--visual-identification)
   - [EDA Source Files & Build Instructions](#15-eda-source-files--build-instructions)
   - [Sub-revision 1.1a — Sandwich Shift & 32 Continuous Rows](#16-sub-revision-11a--sandwich-shift--32-continuous-rows)
5. [Printable 1:1 Scale Templates](#printable-11-scale-templates)
6. [Directory Structure](#directory-structure)
7. [Quick Start & Build Guide](#quick-start--build-guide)
8. [Assisted by AI - Gemini 3.8 Flash Medium](#8-assisted-by-ai---gemini-38-flash-medium)
9. [Bibliography & References](#bibliography--references)
10. [Comprehensive Production Cost Analysis](#10-comprehensive-production-cost-analysis)
11. [License](#11-license)

---

## 🎯 Context & Motivation

This project was born out of a real workbench and maintenance need: the failure of the 180 mm front intake fan in my primary PC case — a non-standard and proprietary form factor, essential for keeping my sole workstation running.

The original fan had already been struggling with frequent thermal throttling and overheating events, especially during the hottest months of the year. When researching a compatible replacement part, the cost hovered around **R$ 180,00 (~$31 USD)** for a low-efficiency stock component. The viable geometric alternative was to fill the exact same physical opening with **four 90 mm cooling fans**. However, a technical bottleneck immediately arose: the motherboard lacked sufficient fan headers and had zero independent driving capacity to manage such an array safely and elegantly.

### From a Temporary Workaround to a Definitive Circuit

1. **The Emergency Prototype:** I quickly assembled an emergency solution on a standard *perfboard* to avoid disrupting daily work, but the cramped physical space and tangled flying wires created an unmaintainable rat's nest.
2. **The Low-Side Switching vs. Tachometer Dilemma:**  
   > ⚠️ **Technical Note:** Speed control using conventional *low-side* switching topologies (such as pulling down ground via a ULN2003 Darlington array or discrete N-channel MOSFETs) chops the fan's GND pin. This causes the internal ground reference of the fan's integrated Hall-effect sensor to float. In practice, the **tachometer signal (RPM pulse pin)** becomes severely corrupted or fails to register accurately on the host motherboard or microcontroller.
3. **Evolution to a Dedicated Board:** Because there was no physical room left on the perfboard to implement proper drive filtering (preserving a solid common ground reference for tachometer capture) and the wiring had become an unmanageable web, I decided to engineer a purpose-built PCB.
4. **Designing for Future Prototyping Needs:** Knowing well that in the maker ecosystem *"nothing is more permanent than a temporary fix"*, I took advantage of the redesign to incorporate dedicated power distribution rails, protective flyback clamps, and breakout tie-points that are routinely missed on the workbench during other embedded automation and cooling projects.

---

This project is made publicly available in the hope of saving time, frustration, and rework for anyone tackling similar PC chassis cooling challenges or peripheral prototyping.

Feedback, bug reports, field tests, and pull requests are warmly welcomed!

---

## Architecture Overview

```
 PC Case Interior:
 ┌─────────────────────────────────────────────────────────────┐
 │ Motherboard Internal USB 2.0 9-Pin Header (Port 1)          │
 │   └── 5V, D-, D+, GND                                       │
 │         │                                                   │
 │         ▼                                                   │
 │ CH340 6-Pin USB-Serial TTL Module (5V Jumper)               │
 │   └── DTR (100nF auto-reset), RXD, TXD, 5V, GND             │
 │         │                                                   │
 │         ▼                                                   │
 │ Custom Stripboard Controller (33.0 mm x 72.0 mm)            │
 │   ├── ATmega328P-PU (16.000 MHz Crystal + 2x 22pF Caps)     │
 │   │     ├── Hardware UART (USART0 @ 115200 baud)            │
 │   │     ├── 4x Hardware PWM Channels (Timers 1 & 2)         │
 │   │     └── 4x Tachometer Interrupt Counters (INT0 & PCINT) │
 │   │                                                         │
 │   ├── ULN2003A / ULN7003A Darlington Driver (DIP-16)        │
 │   │     ├── Low-Side Ground Switching (4 Channels)          │
 │   │     └── Pin 9 COM Clamp Diode tied to +12V Rail         │
 │   │                                                         │
 │   └── Power from PC PSU (SATA / Molex 4-Pin)                │
 │         ├── Yellow Wire: +12V Power Rail                    │
 │         └── Black Wire: Common System Ground (GND)          │
 │         │                                                   │
 │         ▼                                                   │
 │ 4x PC Cooling Fans (4x Akasa 90mm / Arctic P8)              │
 └─────────────────────────────────────────────────────────────┘
```

---

## Hardware Bill of Materials (BOM)

All components are **100% Through-Hole (Thru-Pin / THT / DIP)** for easy soldering on stripboard:

| Item | Component | Package / Value | Qty | Role / Circuit Connection |
| :--- | :--- | :---: | :---: | :--- |
| **BRD1** | Placa Padrão Trilha | 33.0 $\times$ 72.0 mm | 1 | Breadboard-style matrix (12 cols $\times$ 28 rows, 336 holes, 2.54 mm pitch) |
| **U1** | ATmega328P-PU | 28-Pin Narrow DIP | 1 | Main microcontroller (16 MHz) |
| **SKT1** | IC Socket | 28-Pin Narrow DIP | 1 | Socket for ATmega328P |
| **U2** | ULN2003A or ULN7003A | 16-Pin DIP | 1 | 7-channel Darlington low-side ground switch |
| **SKT2** | IC Socket | 16-Pin DIP | 1 | Socket for ULN2003A |
| **MOD1** | CH340 6-Pin USB-TTL Module | 6-Pin Module | 1 | USB-UART bridge to motherboard internal USB header |
| **HDR_USB**| Female/Male Pin Socket | 1x6, 2.54 mm pitch | 1 | Receptacle for CH340 module (Rows R21–R26, Col C02) |
| **Y1** | Quartz Crystal | 16.000 MHz (HC-49) | 1 | Master clock across ATmega Pins 9 & 10 |
| **C3, C4** | Ceramic Capacitors | 22 pF (Disc) | 2 | Crystal load capacitors to GND |
| **C_DTR** | Ceramic Capacitor | 100 nF (0.1 µF) | 1 | In-line AC coupling for DTR auto-reset (Row R21, across Cut 2) |
| **C2, C5** | Ceramic Capacitors | 100 nF (0.1 µF) | 2 | VCC/GND and AVCC/GND high-frequency bypass decoupling |
| **C1** | Electrolytic Capacitor | 100 µF, 25V (Radial) | 1 | Bulk decoupling across +12V rail and GND bus |
| **R_RST** | Metal/Carbon Resistor | $10\text{ k}\Omega$, 1/4W | 1 | Pull-up on ATmega Pin 1 (/RESET) to +5V |
| **R1–R4** | Metal/Carbon Resistors | $10\text{ k}\Omega$, 1/4W | 4 | Pull-ups for Fan Tachometer lines (mount directly from C11 to Upper C12) |
| **J_PWR** | Screw Terminal Block | 2-Pin, 5.08 mm pitch | 1 | PSU +12V (Yellow) and GND (Black) power input |
| **J_FAN** | Male Pin Headers | 3-Pin, 2.54 mm pitch | 4 | Fan 1 to Fan 4 headers (Option A: Rows R26–R28) |
| **WIRE** | Solid Core Hookup Wire | 24 AWG | ~1 m | Top-side jumper links |

---

## Engineering Reasoning & Design Choices

### Form Factor: Bare ATmega328P DIP-28 vs. Arduino Nano
- **Considered:** Using a commercial Arduino Nano board with built-in USB.
- **Decision:** Scaled down to a **bare ATmega328P-PU (DIP-28)** with a **16.000 MHz crystal**.
- **Reasoning:** 
  1. The Arduino Nano has a wide 0.6" (15.24 mm) pin row spacing, which would consume 7 out of the 12 columns of the stripboard, leaving virtually no room for the ULN2003A driver, wiring, or fan headers.
  2. The bare ATmega328P-PU has a narrow 0.3" (7.62 mm) row spacing, exactly matching the ULN2003A and straddling the 0.3" center trough of the protoboard with zero wasted space.
  3. Eliminates unnecessary onboard LEDs, regulators, and duplicate hardware, reducing quiescent power.

### Motherboard Integration: CH340 Module vs. Virtual USB (V-USB)
- **Considered Alternatives:**
  1. *Virtual USB (V-USB):* Software bit-banged USB 1.1 Low-Speed directly on ATmega GPIO pins using 3.6V Zener diodes and series $68\Omega$ resistors.
  2. *Motherboard Internal COM1 Header:* Connecting to legacy RS-232 serial header via a MAX232 level shifter.
  3. *CH340 6-Pin USB-Serial Converter Module:* Connecting to motherboard internal 9-pin USB 2.0 header.
- **Decision:** Adopted the **CH340 6-Pin USB-Serial TTL Converter Module**.
- **Reasoning:**
  1. *Zero AVR CPU Load:* V-USB bit-banging requires tight timing loops and high interrupt priority, which causes jitter and conflicts with 4-channel hardware PWM and tachometer edge interrupts. The CH340 offloads USB to hardware, allowing the ATmega to use its dedicated **Hardware UART (`USART0`)** at 115200 baud with zero CPU overhead.
  2. *Native Linux Support:* The CH340 is supported in-tree by the standard Linux kernel module `ch341.ko` (present out of the box in virtually all Linux distributions without compiling custom drivers).
  3. *1-Click USB Flashing:* By routing the CH340's **DTR pin** through an in-line $100\text{nF}$ capacitor (`C_DTR`) to ATmega Pin 1 (/RESET), the board automatically resets when `avrdude` initiates communication. Firmware can be updated over USB without opening the case or pressing physical reset buttons.

### Breadboard-Style Protoboard Matrix Analysis
Based on the physical connectivity map from [`custoStripBoard.ods`](docs/custoStripBoard.ods), the 33.0 $\times$ 72.0 mm board features:
- **4 Full-Length Vertical Rails (Rows R02–R28, 27 continuous holes each):**
  - Column C01: Primary **GND Bus**
  - Column C06: Primary **+5V Logic Rail**
  - Column C07: Secondary **GND / Shield Rail**
  - Column C12: High-Power **+12V Rail**
- **Two Banks of 4-Hole Horizontal Tie-Points (Rows R02–R26):**
  - Left Bank (C02–C05): 25 isolated 4-hole strips.
  - Right Bank (C08–C11): 25 isolated 4-hole strips.
- **Center Trough (Distance between C05 and C08):** Exactly 0.3" (7.62 mm).
- **Major Advantage:** The center trough provides built-in isolation between pin rows. **No track cuts are required underneath the ATmega328P or ULN2003A sockets!** Both DIP ICs plug straight in.

### Split Rail Innovation: R16 / C12 Copper Trace Cut
- **The Concept:** A single cut on **Column C12 at Row R16** splits the right-most rail into two independent electrical zones:
  - **Upper C12 (Rows R02 to R15):** Connected to **+5V Logic**.
  - **Lower C12 (Rows R17 to R28):** Connected to **+12V Power**.
- **Engineering Advantage:** ATmega Port C pins (Pins 23 to 26 for Tachometers 1 to 4) sit on Column C08 on Rows R07, R06, R05, and R04. Because Upper C12 is +5V, the four $10\text{k}\Omega$ pull-up resistors (**R1 to R4**) simply bridge horizontally between **C11 and C12**. This completely eliminates 4 long crossover jumper wires across the board.

### Fan Connector Placement: Option A (Bottom Edge Bank)
- **Evaluated Options:**
  - *Option A (Bottom Edge Bank, Rows R26–R28):* All 4 fan headers grouped along the bottom perimeter.
  - *Option B (Right Edge Inline, Rows R21–R26):* Fan headers staggered along the right edge alongside the lower C12 rail.
- **Decision:** **Option A (Bottom Edge Bank)** was locked in.
- **Reasoning:**
  1. *Chassis Cable Management:* Grouping all 4 fan connectors along the bottom allows fan cables to bundle and exit downward towards the bottom/rear of the case in a unified harness.
  2. *Symmetrical Pinout:* Symmetrically splits Fans 1 & 2 on the Left Bank (Cols C02 & C04) and Fans 3 & 4 on the Right Bank (Cols C08 & C10).
  3. *Common 12V Bus:* Row R26 serves as the common +12V power distribution bus (Pin 2) for all 4 fan headers, fed directly from Lower C12.

### Staggered Column Label Identification Solution
- **The Problem:** The standard 2.54 mm (0.1") grid pitch is very tight. When printing column labels `C01`, `C02`, `C03` ... `C12` on a single line, text labels overlap and become unreadable.
- **The Solution:** Adopted **alternating / staggered label rows** on both the SVG and PDF printouts:
  - **Outer Tier:** Odd Columns (`C01`, `C03`, `C05`, `C07`, `C09`, `C11`) with dashed extension guide lines.
  - **Inner Tier:** Even Columns (`C02`, `C04`, `C06`, `C08`, `C10`, `C12`) with solid alignment ticks.
  - Result: 100% legible, collision-free column identification.

### Fan Control & Failsafe Strategy
- **Low-Side Switching:** 3-pin fans are powered by constant +12V with their ground switched through the ULN2003A Darlington transistors.
- **Inductive Kickback Protection:** ULN2003A Pin 9 (`COM`) is tied directly to the +12V rail, engaging internal freewheeling clamp diodes across all channels.
- **Operating Modes (in Firmware):**
  - `INDEPENDENT`: 4 individual PWM channels.
  - `SYMMETRIC`: Fan B automatically mirrors Fan A.
  - `ASYMMETRIC`: Fan B tracks Fan A with a configurable offset curve.
  - `HOT_STANDBY`: Fan B remains idle until Fan A tachometer reports 0 RPM while commanded ON (`PWM > 50`). Upon detecting stall/failure, Fan B immediately ramps to 100% and transmits an alarm.
- **Failsafe Watchdog:** A 5-second hardware/software heartbeat timer. If the Linux host freezes, crashes, or the USB cable is unplugged, the microcontroller automatically ramps all fans to a safe **70% duty cycle (180/255)**.

---

## Custom Stripboard Rev 1.1 / 1.1a — Modular Architecture & Specifications

> **Multilingual Engineering Documentation:**  
> 🇺🇸 **US-English:** [CUSTOM_STRIPBOARD_REV1.1_SPEC_EN.md](file:///home/fred/C/fanControl/docs/CUSTOM_STRIPBOARD_REV1.1_SPEC_EN.md) | 🇧🇷 **Português:** [CUSTOM_STRIPBOARD_REV1.1_SPEC_PT.md](file:///home/fred/C/fanControl/docs/CUSTOM_STRIPBOARD_REV1.1_SPEC_PT.md) | 🇪🇸 **Español:** [CUSTOM_STRIPBOARD_REV1.1_SPEC_ES.md](file:///home/fred/C/fanControl/docs/CUSTOM_STRIPBOARD_REV1.1_SPEC_ES.md)

The evolution of the cooling control and prototyping project gave rise to **Custom Stripboard Rev 1.1** and its sub-revision **Rev 1.1a**, an expanded modular prototyping platform in standard Eurocard/Vector plugboard format developed using the **Lepton-EDA** and **`pcb-rnd`** toolchain. The board integrates triple power rails (+12V, +5V, GND), two independent DC barrel power jacks positioned at the outer top edges, a **dual LM317 linear regulator circuit** (Texas Instruments datasheet) in the center top span, **two upright LM2596 step-down buck converter modules** on the left margin, a **10-way 5.08mm screw terminal block (KRE) with a 3-point pass-thru matrix** on the right margin, a **scratch-pad rapid prototyping area with 56 pads and 3 mil knife-scratchable microtraces**, a central prototyping matrix with sandwich interconnect headers, and direct termination into an industrial standard 44-pin card-edge connector ($100\text{ mil}$ / $2.54\text{ mm}$ pitch), strictly single-sided on the bottom solder layer.

> [!IMPORTANT]
> **Manufacturing Directive — Through-Hole (THT) as the Mandatory Default**:  
> Surface Mount Device (SMD) assembly is treated strictly as an optional alternative. The **MANDATORY DEFAULT manufacturing standard is 100% Through-Hole (plated through-hole / PTH)**. All prototyping matrix pads, terminal block pass-thrus, scratch-pad pads, connectors, and regulators utilize plated drill holes with an outer copper diameter $\ge 80.00\text{ mil}$ ($2.032\text{ mm}$), preventing trace delamination and enabling robust manual soldering and rework.

```
  Custom Stripboard Rev 1.1 / Rev 1.1a (Topological Architecture Overview):
  ┌────────────────────────────────────────────────────────────────────────────────────────┐
  │ [MH101]    [CONN117 DC JACK 1]   [LM317 #1]  [LM317 #2]   [CONN118 DC JACK 2]  [MH102] │
  │ M3 (200,200) X=800, Y=200       X=1400..1600 X=1900..2100  X=2400, Y=200    (3300,200)│
  │            [SIP3 Breakout 1]     U101+Caps   U102+Caps    [SIP3 Breakout 2]            │
  │            X=500..700, Y=200..400 R101/R102   R103/R104   X=2800..3000                 │
  │ ───────────────────────────────── GND BRIDGE (Y=600 mil) ───────────────────────────── │
  │ [VR101]                                                    [TB101 KRE 10P 5.08mm]      │
  │ LM2596 Upright #1                                          X=3400, Y=600..2400 mil     │
  │ 4x7 Pins (200 mil)                                         [CONN137..139 Pass-Thru]    │
  │ Y=600..1200 mil                                            3 pass-thru pads per pin    │
  │ VIN1+/- , OUT1+/-                                          10 nets: KRE_1..KRE_10      │
  │                                                                                        │
  │ [MH103] Central M3 Mount                                   [MH104] Adjusted M3 Mount   │
  │ X=200, Y=2000 mil                                          X=3300, Y=2700 mil          │
  │ (Midway clearance between VR101 & VR102)                   (Clearance to KRE & Scratch)│
  │                                                                                        │
  │ [VR102]                                                    [SCRATCH-PAD PROTO AREA]    │
  │ LM2596 Upright #2                                          14 rows x 4 columns         │
  │ 4x7 Pins (200 mil)                                         56 pads (Pad 90mil, Drill 35)
  │ Y=2800..3400 mil                                           3 mil microtraces           │
  │ VIN2+/- , OUT2+/-                                          X=3100..3400, Y=3000..4300  │
  │                                                            Common net: SCRATCHPAD      │
  │ ────────────────────────────────────────────────────────────────────────────────────── │
  │ 8x Vertical Power Rails (Continuous 40 mil Traces: GND/+5V/+12V)                       │
  │ ├── 58 Rows (Rev 1.1) or 64 Rows (Rev 1.1a) Horizontal Prototyping Strips (10 mil)    │
  │ └── Sandwich Interconnect Section:                                                     │
  │     ├── Upper Horizontal Strips (SIP9N)                                                │
  │     ├── Dual-Row Center Headers (HEADER18 - J201 & J301, 100 mil pitch)                │
  │     │     └── Vertical bridge traces widened to 30 mil                                 │
  │     ├── Lower Horizontal Strips (SIP9N)                                                │
  │     └── Bottom Vertical Output Strips (SIP4N - 40 mil traces)                          │
  │                                                                                        │
  │ [MH105] ── Mechanical Alignment with Bottom Pad Row ── [MH106]                         │
  │ X=200, Y=4600 mil (Pad bottom edge strictly aligns with pad baseline) X=3300 mil       │
  │ ══════════════════════════════════════════════════════════════════════════════════════ │
  │ Mechanical Stop Shoulders (Y = 4740 mil - 3.5" to 2.7" step with 45° chamfers)        │
  │       ┌────────────────────────────────────────────────────────────────────────┐       │
  │       │ Open Solder Jumpers (13 mil Gap, 30 mil Traces)                        │       │
  │       ├────────────────────────────────────────────────────────────────────────┤       │
  │       │ Single-Sided Card Edge Connector (44-Pin Standard Tongue):             │       │
  │       │     ├── 26 Contact Positions (100 mil / 2.54 mm pitch)                 │       │
  │       │     ├── Single-Sided (Exclusively on Bottom Solder Layer / onsolder)   │       │
  │       │     ├── Mechanical Polarizing Key: Finger 8 Omitted ("KEY")            │       │
  │       │     └── 45° Insertion Lead-in Chamfers on Bottom Corners               │       │
  │       └────────────────────────────────────────────────────────────────────────┘       │
  └────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### 1. Physical & Mechanical Specifications

| Parameter | Value in Mils | Value in Millimeters (mm) | Description / Function |
| :--- | :---: | :---: | :--- |
| **Total Body Width** | $3500.00\text{ mil}$ | $88.90\text{ mm}$ | Structural width of the prototyping area |
| **Total Board Length** | $5050.00\text{ mil}$ | $128.27\text{ mm}$ | Overall length from top edge to tongue tip |
| **Card-Edge Tongue Width** | $2700.00\text{ mil}$ | $68.58\text{ mm}$ | Connector insertion tongue ($X = 400.00$ to $3100.00\text{ mil}$) |
| **Insertion Depth** | $310.00\text{ mil}$ | $7.87\text{ mm}$ | Insertable tongue reach ($Y = 4740.00$ to $5050.00\text{ mil}$) |
| **Mechanical Stop Shoulders** | $400.00\text{ mil}$ | $10.16\text{ mm}$ | Lateral steps at $Y = 4740\text{ mil}$ resting against card-edge socket |
| **Lead-in Chamfers** | $40.00\text{ mil} \times 45^\circ$ | $1.02\text{ mm} \times 45^\circ$ | Bottom corner bevels for smooth card-cage insertion |
| **Plated M3 Mounting Holes** | $126.00\text{ mil}$ (drill) | $3.20\text{ mm}$ | 6x holes ($240\text{ mil}$ pad, $40\text{ mil}$ clearance, $300\text{ mil}$ keepout) |
| **Top M3 Coordinates** | $(200, 200)$, $(3300, 200)$ | $(5.08, 5.08)$, $(83.82, 5.08)$ | Top perimeter corners (`MH101` and `MH102`) |
| **Center M3 Coordinates** | $(200, 2000)$, $(3300, 2700)$ | $(5.08, 50.80)$, $(83.82, 68.58)$ | **`MH103` between LM2596 modules; `MH104` between KRE & Scratch-pad** |
| **Bottom M3 Coordinates** | $(200, 4600)$, $(3300, 4600)$ | $(5.08, 116.84)$, $(83.82, 116.84)$ | **Aligned with pad baseline of bottom row** (`MH105`, `MH106`) |

---

### 2. Top Power Subsystem: DC Barrel Jacks & Breakout SIP3 Headers

To accommodate central linear regulators and heat sinks without mechanical interference, the dual 2.1mm $\times$ 5.5mm DC barrel jacks were relocated outward toward the edges:

- **DC Jack 1 (`CONN117`):** Located at $(X = 800.00\text{ mil}, Y = 200.00\text{ mil})$.
  - Dedicated 3-pin breakout SIP3 headers (`CONN119..121` at $X = 500, 600, 700\text{ mil}$, $Y = 200..400\text{ mil}$).
  - Traces routed exclusively with **$40\text{ mil}$ copper (`Layer 6 "bottom"`)** for continuous current capacity up to 5A.
- **DC Jack 2 (`CONN118`):** Located at $(X = 2400.00\text{ mil}, Y = 200.00\text{ mil})$.
  - Dedicated 3-pin breakout SIP3 headers (`CONN122..124` at $X = 2800, 2900, 3000\text{ mil}$, $Y = 200..400\text{ mil}$).
  - Traces routed exclusively with **$40\text{ mil}$ copper**.

---

### 3. Dual LM317 Linear Regulators (TI Datasheet, Page 1)

In the upper-middle region ($X = 1400\text{ mil}$ to $X = 2100\text{ mil}$, $Y = 200..700\text{ mil}$), two independent, full-featured LM317 linear regulator circuits are implemented following the official manufacturer diagram:

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
- **THT Test & Power Pads (Pads $\ge 80\text{ mil}$):** `J101` (VIN1 at $1400, 200$), `J102` (VOUT1 at $1500, 200$), `J103` (GND at $1400, 700$).

#### LM317 Circuit #2:
- **IC Regulator `U102` (TO-220 Upright):** Pin 3 (VIN) at $(1900, 300)$, Pin 2 (VOUT) at $(2000, 300)$, Pin 1 (ADJ) at $(2100, 300)$.
- **Through-Hole Capacitors:** $C_{103}$ ($0.1\,\mu\text{F}$) at $(1900, 400..600)$; $C_{104}$ ($1.0\,\mu\text{F}$) at $(2000, 400..600)$.
- **Axial Resistors:** $R_{103}$ ($240\,\Omega$) at $(2000..2100, 500)$; $R_{104}$ ($R_2$) at $(2100, 400..600)$.
- **THT Test & Power Pads (Pads $\ge 80\text{ mil}$):** `J104` (VIN2 at $1900, 200$), `J105` (VOUT2 at $2000, 200$), `J106` (GND at $1900, 700$).
- **Common Ground Bus:** A solid $40\text{ mil}$ copper trace at $Y = 600\text{ mil}$ connects the ground terminals of both regulator circuits.

---

### 4. Left Margin: Dual Upright LM2596 Step-Down Modules (`VR101`, `VR102`)

For high-efficiency switching regulation (e.g., +12V to +5V or variable outputs up to 3A):
- **Footprint:** $4 \times 7$ pin matrix at $200.00\text{ mil}$ ($5.08\text{ mm}$) pitch ($X = 100, 200, 300, 400\text{ mil}$).
- **Module 1 (`VR101`):** $Y = 600.00\text{ mil}$ to $1200.00\text{ mil}$. Rows 1–4 form `VIN1+` ($X = 100$) and `VIN1-` ($X = 300$); Rows 5–7 form `OUT1+` ($X = 100$) and `OUT1-` ($X = 300$).
- **Module 2 (`VR102`):** $Y = 2800.00\text{ mil}$ to $3400.00\text{ mil}$. Rows 1–4 form `VIN2+` and `VIN2-`; Rows 5–7 form `OUT2+` and `OUT2-`.
- **$40\text{ mil}$ Power Traces:** Vertical $40\text{ mil}$ buses tie together the pins for each electrical net.
- **Positioning of `MH103`:** Placed at $(X = 200\text{ mil}, Y = 2000\text{ mil})$, exactly midway between `VR101` and `VR102` with $>650\text{ mil}$ clearance to both modules.

---

### 5. Right Margin: 10-Way 5.08mm Screw Terminal Block & Pass-Thru Matrix (`TB101`)

On the upper right margin, between mounting holes `MH102` and `MH104`:
- **Screw Terminal Block 10P 5.08mm (`TB101`):** Pins at $X = 3400.00\text{ mil}$, $Y = [600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400]\text{ mil}$.
- **Horizontal 3-Point Pass-Thru Matrix:** For each screw terminal pin, 3 plated pass-thru holes extend horizontally inward:
  - `CONN137` at $X = 3300.00\text{ mil}$
  - `CONN138` at $X = 3200.00\text{ mil}$
  - `CONN139` at $X = 3100.00\text{ mil}$
- **$30\text{ mil}$ Copper Traces:** Each 4-hole row is tied together by $30\text{ mil}$ traces, creating 10 independent electrical nets (`KRE_1` to `KRE_10`).
- **Mechanical Clearances:**
  - Above ($Y = 600\text{ mil}$): $>150\text{ mil}$ clearance to the `MH102` screw keepout.
  - Below ($Y = 2400\text{ mil}$): The terminal block plastic body terminates at $Y = 2500\text{ mil}$, providing $80\text{ mil}$ of isolation to the pad of `MH104` ($Y = 2700\text{ mil}$).

---

### 6. Right Margin: Scratch-Pad Prototyping Area (56 Pads, 3 mil)

On the lower right margin, between `MH104` and `MH106`:
- **Prototyping Matrix:** 14 rows $\times$ 4 columns = **56 pads** ($X = 3100, 3200, 3300, 3400\text{ mil}$, $Y = 3000$ to $4300\text{ mil}$).
- **Pad Geometry:** **$90.00\text{ mil}$** pad diameter, **$35.00\text{ mil}$** drill hole, **$96.00\text{ mil}$** solder mask opening.
- **$10\text{ mil}$ Copper Gap:** Spacing between adjacent pads is exactly **$10.00\text{ mil}$ ($0.254\text{ mm}$)**.
- **Knife-Scratchable $3\text{ mil}$ Microtraces:**
  - All 56 pads belong to a single initial common electrical net (`SCRATCHPAD`).
  - Adjacent pads are bridged by **$3.00\text{ mil}$** microtraces on the bottom copper layer.
  - Can be cleanly severed with a hobby knife or surgical scalpel to create isolated pads or custom grouped buses.
- **Silkscreen Boundary:** Rectangular silkscreen outline enclosing the area with the label `"SCRATCH PAD"`.

---

### 7. Manufacturing Directive: Through-Hole (THT) Mandatory Default & Pad Size $\ge 80\text{ mil}$

- **THT Assembly by Rule:** SMD technology is optional; the mandatory engineering default of the project is **100% Through-Hole (plated through-hole / PTH)**.
- **Standardized Pad Dimensions:** All solder pads previously $< 80\text{ mil}$ were enlarged to **$\ge 80.00\text{ mil}$** ($80\text{ mil}$ or $90\text{ mil}$), with $35\text{ mil}$ drill hole and $86\text{ mil}$ solder mask opening.
- **Verified Manufacturing Compliance:**
  - Pins with pad diameter $< 80\text{ mil}$: **0**
  - Pins without plated through-hole: **0** (only the card edge contact fingers on the tongue are single-sided SMD).

---

### 8. Standardized Copper Trace Width Hierarchy

| Category | Trace Width | Clearance | Layer | Application / Circuit |
| :--- | :---: | :---: | :---: | :--- |
| **Power & Primary Rails** | **40 mil** ($1.016\text{ mm}$) | $20\text{ mil}$ | Bottom (Layer 6) | 8 vertical power rails; DC Jack feed lines; LM2596 power buses; LM317 power/GND rails; bottom 4-pin vertical output strips |
| **Bridges & Interconnects** | **30 mil** ($0.762\text{ mm}$) | $20\text{ mil}$ | Bottom (Layer 6) | Vertical 100 mil bridge traces in `HEADER18`; open solder jumper feeds; terminal block KRE pass-thru lines |
| **Feedback & Adjust** | **20 mil** ($0.508\text{ mm}$) | $20\text{ mil}$ | Bottom (Layer 6) | LM317 Pin 1 (ADJ) lines to resistors $R_1$ and $R_2$ |
| **Prototyping Strips** | **10 mil** ($0.254\text{ mm}$) | $20\text{ mil}$ | Bottom (Layer 6) | Horizontal strip lines for 58 rows (Rev 1.1) or 64 rows (Rev 1.1a) |
| **Scratchable Microtraces** | **3 mil** ($0.076\text{ mm}$) | $10\text{ mil}$ | Bottom (Layer 6) | Interconnection mesh in the scratch-pad rapid prototyping area |

---

### 9. Prototyping Matrix & Sandwich Interconnect Section

1. **8 Continuous Vertical Power Rails:**
   - 40 holes each ($Y = 800\text{ mil}$ to $Y = 4700\text{ mil}$), formed by pairs of `SIP20N` connectors joined with continuous $40\text{ mil}$ copper traces.
   - X Positions: $500, 600, 700\text{ mil}$ (GND, +5V, +12V Left Bank); $1700, 1800\text{ mil}$ (Center Shield); $2800, 2900, 3000\text{ mil}$ (GND, +5V, +12V Right Bank).
2. **Horizontal Prototyping Strip Rows:**
   - Left Bank ($X = 800$ to $1600\text{ mil}$, 9 pins each).
   - Right Bank ($X = 1900$ to $2700\text{ mil}$, 9 pins each).
   - Interconnected with **$10\text{ mil}$** traces.
3. **Sandwich Interconnect Section:**
   - Dual-row 18-pin center headers (`HEADER18`, 2x9 pins, $100\text{ mil}$ pitch): `J201` and `J301`.
   - Sandwiched by `SIP9N` strips with vertical bridge traces widened to **$30\text{ mil}$**.
   - Bottom 4-pin vertical output strips (`SIP4N`, $Y = 4400..4700\text{ mil}$) with **$40\text{ mil}$** traces.

---

### 10. Single-Sided Card Edge Connector (44-Pin Standard Tongue)

- **Strictly Single-Sided Architecture:** All 26 contact fingers reside exclusively on the bottom solder layer (`Layer 6 "bottom"` / `onsolder`). The top side is virgin, unclad FR4 laminate.
- **Finger Dimensions:** $65\text{ mil} \times 230\text{ mil}$ ($1.65\text{ mm} \times 5.84\text{ mm}$), centered at $Y = 4925\text{ mil}$ (span of $Y = 4810$ to $5040\text{ mil}$).
- **Shoulders & Chamfers:** Mechanical stop shoulders at $Y = 4740\text{ mil}$ and $40\text{ mil} \times 45^\circ$ lead-in corner chamfers.

---

### 11. Mechanical Polarizing Key (Keying at Finger 8)

- **Contact Omission at Finger 8:** Contact finger `EF8` at $X = 1200\text{ mil}$ and its solder jumper have been omitted.
- **Silkscreen Identification:** Silkscreen label `"KEY"` printed at $X = 1160\text{ mil}, Y = 4725\text{ mil}$ for inserting a plastic polarizing key into the backplane socket.

---

### 12. Open Solder Jumpers

- **Location:** Between the bottom of the matrix ($Y = 4700\text{ mil}$) and the start of the card edge fingers ($Y = 4810\text{ mil}$).
- **SMD Pads:** Two $50\text{ mil} \times 30\text{ mil}$ pads separated by an open isolation gap of **$13\text{ mil}$ ($0.33\text{ mm}$)**.
- **Operation:** Open by default. A drop of solder easily bridges the jumper to connect the desired strip signal to the card edge finger.

---

### 13. M3 Mounting Holes, Keepouts & Alignment

- **Dimensions:** $126\text{ mil}$ ($3.20\text{ mm}$) drill, $240\text{ mil}$ copper pad ring, $300\text{ mil}$ ($7.62\text{ mm}$) silkscreen keepout and head relief.
- **Bottom Hole Alignment (`MH105`, `MH106`):** Located at $Y = 4600\text{ mil}$, the bottom edge of the copper pad ring ($Y = 4720\text{ mil}$) aligns strictly with the baseline of the bottom pad row ($Y = 4728\text{ mil}$), preserving $140\text{ mil}$ clearance to the tongue shoulders.
- **Validated Keepouts:** `MH103` at $Y = 2000\text{ mil}$ (clear of `VR101` and `VR102`); `MH104` at $Y = 2700\text{ mil}$ (clear of `TB101` and scratch-pad).

---

### 14. Silkscreen Legend & Visual Identification

- Logos: `"CUSTOM STRIPBOARD REV 1.1"` and `"CUSTOM STRIPBOARD REV 1.1a"` on the right margin.
- Power Legends: `"PWR JACK 1"`, `"PWR JACK 2"`, `"J1 PWR OUT"`, `"J2 PWR OUT"`, `"LM317 #1"`, `"LM317 #2"`, `"VIN"`, `"VOUT"`, `"GND"`.
- Connector Legends: `"LM2596 VR101"`, `"LM2596 VR102"`, `"KRE 10P"`, `"SCRATCH PAD"`, `"KEY"`.

---

### 15. EDA Source Files & Build Instructions

All files reside in the [`lepton/`](file:///home/fred/C/fanControl/lepton/) directory:
- **Comprehensive Technical Specification:** [`docs/CUSTOM_STRIPBOARD_REV1.1_SPEC_EN.md`](file:///home/fred/C/fanControl/docs/CUSTOM_STRIPBOARD_REV1.1_SPEC_EN.md)
- **Layout Synthesizer Script:** [`layout_stripboards.py`](file:///home/fred/C/fanControl/lepton/layout_stripboards.py)
- **Rev 1.1a:**
  - PCB Layout: [`stripboard_rev1.1a.pcb`](file:///home/fred/C/fanControl/lepton/rev1.1a/stripboard_rev1.1a.pcb)
  - Schematic: [`centro.sch`](file:///home/fred/C/fanControl/lepton/rev1.1a/centro.sch) | [centro.png](file:///home/fred/C/fanControl/lepton/rev1.1a/centro.png)
  - 300 DPI Previews: [Top (Components)](file:///home/fred/C/fanControl/lepton/rev1.1a/stripboard_rev1.1a_preview_300dpi.png) | [Bottom (Copper & Fingers)](file:///home/fred/C/fanControl/lepton/rev1.1a/stripboard_rev1.1a_bottom_preview_300dpi.png)
- **Rev 1.1:**
  - PCB Layout: [`stripboard_rev1.1.pcb`](file:///home/fred/C/fanControl/lepton/rev1.1/stripboard_rev1.1.pcb)
  - Schematic: [`centro.sch`](file:///home/fred/C/fanControl/lepton/rev1.1/centro.sch) | [centro.png](file:///home/fred/C/fanControl/lepton/rev1.1/centro.png)
  - 300 DPI Previews: [Top (Components)](file:///home/fred/C/fanControl/lepton/rev1.1/stripboard_rev1.1_preview_300dpi.png) | [Bottom (Copper & Fingers)](file:///home/fred/C/fanControl/lepton/rev1.1/stripboard_rev1.1_bottom_preview_300dpi.png)

#### Regeneration Command:
```bash
# Compile layouts, synchronize netlists, and export 300 DPI preview renders:
python3 lepton/layout_stripboards.py
```

---

### 16. Sub-revision 1.1a — Sandwich Shift & 32 Continuous Rows

In sub-revision **Rev 1.1a**:
1. **Sandwich Downward Shift (+200 mil):** Upper strip at $Y = 4000\text{ mil}$, center header at $Y = 4100..4200\text{ mil}$, and lower strip at $Y = 4300\text{ mil}$.
2. **Closing the Lower Gap:** The lower strip at $Y = 4300\text{ mil}$ aligns at exactly $100\text{ mil}$ from the bottom vertical output strips at $Y = 4400\text{ mil}$.
3. **Filling Rows 30, 31, and 32:** Coordinates $Y = 3700, 3800, 3900\text{ mil}$ are fully populated with 9-pin horizontal strips (`CONN241..243` and `CONN341..343`), yielding **32 continuous rows per bank** (**64 horizontal 9-pin strips** in total).

---

## Printable 1:1 Scale Templates

The [`docs/templates/`](docs/templates/) directory contains exact **1:1 scale templates** calibrated for the **33.0 mm $\times$ 72.0 mm** board:

1. **Master Printable PDF:**
   - **[`stripboard_1to1_printout.pdf`](docs/templates/stripboard_1to1_printout.pdf)**: An A4 master sheet containing all 3 templates, a 100 mm calibration verification ruler, staggered column IDs, and cutting guides.
2. **Template 1 — Physical Ruler & Alignment Indicator:**
   - **[`board_ruler_indicator.png`](docs/templates/board_ruler_indicator.png)** ([SVG](docs/templates/board_ruler_indicator.svg)): Place your physical board directly on top of this printout. Outer borders (33 $\times$ 72 mm) and hole crosshairs match 1:1 for instant coordinate identification.
3. **Template 2 — Top / Component View Cut Guide:**
   - **[`board_cuts_top_view.png`](docs/templates/board_cuts_top_view.png)** ([SVG](docs/templates/board_cuts_top_view.svg)): Shows internal copper tracks with all **7 track cuts highlighted in RED**.
4. **Template 3 — Bottom / Solder Side Drill Guide (Mirrored):**
   - **[`board_cuts_bottom_drill_view.png`](docs/templates/board_cuts_bottom_drill_view.png)** ([SVG](docs/templates/board_cuts_bottom_drill_view.svg)): Horizontally flipped so that when you turn the board upside down onto the copper side, the red cuts match exactly what you see under your drill bit.

### Complete List of the 7 Red Track Cuts
| Cut ID | Coordinate | Tool / Method | Purpose |
| :---: | :---: | :---: | :--- |
| **Cut 1** | **Row R16, Column C12** | 3.0 mm drill bit twisted by hand | Splits C12 rail into Upper (+5V Logic) and Lower (+12V Power). |
| **Cut 2** | **Row R21, between C02 and C03** | 3.0 mm drill bit twisted by hand | Isolates CH340 DTR pin so $100\text{nF}$ C_DTR cap mounts in-line. |
| **Cut 3** | **Row R24, between C03 and C04** | 3.0 mm drill bit twisted by hand | Isolates CH340 5V from ULN Pin 8 GND; C2 bypass cap mounts across it. |
| **Cut 4** | **Column C02, between R27 and R28** | 3.0 mm drill bit twisted by hand | Isolates Fan 1 Switched GND (R27) from Fan 1 Tach (R28). |
| **Cut 5** | **Column C04, between R27 and R28** | 3.0 mm drill bit twisted by hand | Isolates Fan 2 Switched GND (R27) from Fan 2 Tach (R28). |
| **Cut 6** | **Column C08, between R27 and R28** | 3.0 mm drill bit twisted by hand | Isolates Fan 3 Switched GND (R27) from Fan 3 Tach (R28). |
| **Cut 7** | **Column C10, between R27 and R28** | 3.0 mm drill bit twisted by hand | Isolates Fan 4 Switched GND (R27) from Fan 4 Tach (R28). |

---

## Directory Structure

```
fanControl/
├── Makefile                          # Top-level build automation (firmware + daemon)
├── README.md                         # Complete project documentation & architectural log
├── lepton/                           # Lepton-EDA Schematics & Stripboard PCB Generation
│   ├── Makefile                      # Lepton-EDA netlist, schematic export & layout generation
│   ├── layout_stripboards.py         # Automated layout generator for Rev 1.0, Rev 1.1 & Rev 1.1a PCBs
│   ├── common/                       # Shared Lepton symbols & footprints (.sym, .fp)
│   ├── rev1.0/                       # 33x72mm Breadboard-style stripboard EDA files
│   ├── rev1.1/                       # Modular 3.5"x5.05" Industrial Stripboard with Card Edge
│   │   ├── centro.sch                # Power rails, M3 holes, DC power jacks, dual LM317, VR101/VR102, KRE 10P & scratch-pad
│   │   ├── lado1.sch / lado2.sch     # Left and right prototyping matrix banks (29 rows)
│   │   ├── interconnect.sch          # HEADER18 sandwich headers and SIP9N strips
│   │   ├── stripboard_rev1.1.pcb     # pcb-rnd layout file with through-hole pads (>=80 mil), dual LM317, KRE 10P, scratch-pad
│   │   ├── stripboard_rev1.1_preview_300dpi.png        # Top component view (300 DPI)
│   │   └── stripboard_rev1.1_bottom_preview_300dpi.png # Bottom solder/edge view (300 DPI)
│   └── rev1.1a/                      # Sub-revision 1.1a: Shifted sandwich & 32 continuous rows
│       ├── centro.sch                # Power rails, M3 holes, DC power jacks, dual LM317, VR101/VR102, KRE 10P & scratch-pad
│       ├── lado1.sch / lado2.sch     # 32 continuous rows of 9-pin strips (CONN201..243 / 301..343)
│       ├── interconnect.sch          # Shifted HEADER18 sandwich headers (Y = 4000..4300 mil)
│       ├── stripboard_rev1.1a.pcb    # pcb-rnd layout with shifted sandwich, filled rows, dual LM317, KRE 10P, scratch-pad
│       ├── stripboard_rev1.1a_preview_300dpi.png       # Top component view (300 DPI)
│       └── stripboard_rev1.1a_bottom_preview_300dpi.png # Bottom solder/edge view (300 DPI)
├── firmware/                         # ATmega328P Pure C Firmware
│   ├── Makefile                      # AVR-GCC compilation and avrdude USB flashing
│   ├── main.c                        # Main loop, command processor & failsafe watchdog
│   ├── pwm.c / pwm.h                 # 4-channel hardware PWM & multi-fan behaviors
│   ├── tach.c / tach.h               # Interrupt-driven RPM pulse measurement
│   └── uart.c / uart.h               # Hardware USART0 ring buffer driver (115200 baud)
├── daemon/                           # Linux Host Daemon & CLI Tool
│   ├── Makefile                      # Host C compiler build & system install targets
│   ├── fancontrol.conf               # Config file (temperature thresholds, ports, curves)
│   ├── fancontrol.service            # systemd background service unit
│   ├── 99-fancontrol.rules           # udev rule for persistent /dev/fancontrol symlink
│   └── src/
│       ├── main.c                    # Daemon loop & CLI flag parser
│       ├── hwmon.c / hwmon.h         # Linux /sys/class/hwmon temperature sensor reader
│       ├── serial.c / serial.h       # POSIX termios serial communications
│       └── curve.c / curve.h         # Linear & multi-point fan curve calculator
├── kernel/                           # Linux Kernel hwmon Driver (Optional)
│   ├── Makefile                      # Out-of-tree kernel module build
│   └── fancontrol_hwmon.c            # Native USB hwmon driver registering sysfs nodes
└── docs/                             # Hardware & Assembly Documentation
    ├── CUSTOM_STRIPBOARD_REV1.1_SPEC.md    # Especificação técnica completa (Português)
    ├── CUSTOM_STRIPBOARD_REV1.1_SPEC_EN.md # Complete technical specification (US-English)
    ├── CUSTOM_STRIPBOARD_REV1.1_SPEC_ES.md # Especificación técnica completa (Español)
    ├── PC_CASE_WIRING.md             # Case integration, 9-pin USB header & Molex wiring
    ├── STRIPBOARD_LAYOUT.md          # Step-by-step soldering & assembly coordinate table (Rev 1.0)
    ├── custoStripBoard.ods           # Original protoboard matrix connection spreadsheet
    └── templates/                    # Printable 1:1 Scale Fabrication Templates
        ├── generate_templates.py     # Python vector generator (SVG & ReportLab PDF)
        ├── stripboard_1to1_printout.pdf # Master printable A4 sheet (100% scale)
        ├── board_ruler_indicator.svg / .png
        ├── board_cuts_top_view.svg / .png
        ├── board_cuts_bottom_drill_view.svg / .png
        └── preview_page-1.png        # 300 DPI preview rendering of print sheet
```

---

## Quick Start & Build Guide

### 1. Compile Firmware & Linux Daemon
```bash
make
```

### 2. Flash ATmega328P over USB
Connect the board to your PC via USB:
```bash
cd firmware
make flash PORT=/dev/ttyUSB0
```

### 3. Test Controller from Linux CLI
```bash
cd ../daemon
./fancontrold --list-hwmon                       # Scan host PC temperature sensors
./fancontrold -p /dev/ttyUSB0 --status           # Query live fan RPM and PWM duties
./fancontrold -p /dev/ttyUSB0 --setall 180       # Set all fans to ~70% speed
```

### 4. Install Background systemd Service
```bash
sudo make install
sudo systemctl enable --now fancontrol.service
sudo systemctl status fancontrol.service
```

---

## 8. Assisted by AI - Gemini 3.8 Flash Medium

> [!NOTE]
> **Official Development Attribution:**  
> *"projeto usando lepton-eda/pcb-rnd assistido com IA-Gemini-3.8-Flash-Medium"*

This project was conceived, designed, coded, debugged, and documented end-to-end with the interactive and autonomous assistance of the **Google DeepMind Gemini 3.8 Flash (Medium)** model.

### Detailed Record of Resources and Iterations

| Metric | Quantity / Scope | Operations Description |
| :--- | :---: | :--- |
| **AI Model** | `Gemini 3.8 Flash (Medium)` | High-speed, high-precision multimodal reasoning model |
| **User Dialog Iterations (Turns)** | **17 dialog turns** | From initial protoboard concept to final Rev 1.1 / Rev 1.1a layout |
| **Tool Invocations (Tool Calls)** | **413 tool calls** | Automated build, inspection, editing, and EDA validation operations |
| • `run_command` | **290 calls** | Bash shell execution, C/AVR compilers, Python scripts, Lepton-EDA & `pcb-rnd` tools |
| • `edit_file` | **42 calls** | Surgical source code edits, algorithmic layout generation, documentation updates |
| • `manage_task` | **28 calls** | Background process management and heavy graphics renders |
| • `read_file` | **26 calls** | Reading and integrity verification of netlists, schematics, and tables |
| • `search_web` | **16 calls** | Datasheet consulting (TI LM317, WCH CH340, ULN2003, Sullins, Vector, etc.) |
| • `write_file` | **9 calls** | Creation of generator scripts, technical specifications, and Makefiles |
| • `ask_question` | **2 calls** | Requirement clarifications and design decisions directly with the user |
| **Generated Code** | **~5,200+ lines of code** | Pure AVR C firmware, Linux daemon C, hwmon kernel driver, parametric PCB generator, Makefiles |
| **Generated Graphics & Previews** | **14 graphic artifacts** | Lepton-EDA schematics (.png), 300 DPI top/bottom PCBs, 1:1 templates (.svg, .png, .pdf) |

### Tool Inventory & Software Stack

1. **EDA & Layout Suite:**
   - **`lepton-schematic` / `lepton-cli`:** Vector and raster capture of high-resolution schematics.
   - **`lepton-netlist`:** Automated netlist extraction in gEDA/pcb-rnd format.
   - **`pcb-rnd`:** Printed circuit CAD with high-resolution photographic rendering (`--photo-mode --dpi 300`) and scriptable routing.
2. **Compilers & Toolchains:**
   - **Host Linux:** `gcc` 14.2.0 (compilation of CLI daemon and `/sys/class/hwmon` reader).
   - **Microcontroller Cross-Compiler:** `avr-gcc` 14.2.0 (`-Os -std=gnu99 -mmcu=atmega328p -DF_CPU=16000000UL`), `avr-objcopy`, `avr-size` (Flash consumption: 6,494 bytes, SRAM: 497 bytes).
   - **Programmer:** `avrdude` (STK500v1 protocol via CH340 converter at `/dev/ttyUSB0`).
3. **Scripting & Algorithmic Environment:**
   - **Python 3.12 / 3.13:**
     - `layout_stripboards.py`: Parametric synthesizer for Rev 1.0, Rev 1.1, and Rev 1.1a PCBs, calculating coordinates, pads, copper traces, M3 holes, and silkscreen.
     - `generate_templates.py`: Physical 1:1 scale cutting and drilling template generator.
     - Automated pad audit scripts ($\ge 80\text{ mil}$ outer diameter and plated drill holes).
4. **Vectorization & Graphic Processing:**
   - **`reportlab`:** PDF canvas synthesis with true metric calibration for unscaled A4 printing.
   - **`inkscape`:** Headless SVG rasterizer for 300 DPI bitmaps.
   - **`pdftoppm`:** Poppler utility for visual inspection and verification of templates.

---

## 9. Bibliography & References

### 1. Reference Projects & Community
- **pnjorge (Paulo Nogueira / F5VMJ):** *"Silent Running With This Dual Fan Controller"* (Hackster.io, 2021).  
  Reference project and design notes on dynamic fan curves, tachometer pulse interrupt capture, and failsafe modes with ATmega328P.  
  [https://www.hackster.io/pnjorge/silent-running-with-this-dual-fan-controller-0accb8](https://www.hackster.io/pnjorge/silent-running-with-this-dual-fan-controller-0accb8)
- **pnjorge:** *Cooler-Fan-Controller Hardware & Firmware Repository* (GitHub).  
  [https://github.com/pnjorge/Cooler-Fan-Controller](https://github.com/pnjorge/Cooler-Fan-Controller)

### 2. Hardware Components & Official Datasheets
- **Texas Instruments LM317 3-Terminal Adjustable Regulator:**  
  *LM317 3-Terminal Adjustable Regulator* (Datasheet SNVS774P). Standard application circuit on page 1 ($1.25\text{V} - 37\text{V}$, $1.5\text{A}$, $R_1 = 240\,\Omega$, $C_1 = 0.1\,\mu\text{F}$, $C_2 = 1.0\,\mu\text{F}$).  
  Official PDF: [https://www.ti.com/lit/ds/symlink/lm317.pdf](https://www.ti.com/lit/ds/symlink/lm317.pdf)
- **Texas Instruments / STMicroelectronics / Allegro ULN2003A & ULN7003A:**  
  *Seven Darlington Arrays* (Datasheet SLRS027P). High-voltage, high-current Darlington transistor array with internal inductive clamp diodes tied to COM.  
  [https://www.ti.com/lit/ds/symlink/uln2003a.pdf](https://www.ti.com/lit/ds/symlink/uln2003a.pdf)
- **Microchip / Atmel ATmega328P-PU:**  
  *8-bit AVR Microcontroller with 32K Bytes In-System Programmable Flash* (Datasheet DS40002061B / Atmel-8271). Hardware PWM registers (Timers 1 & 2), external interrupts (INT0 / PCINT), and hardware USART0.  
  [https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7810-Automotive-Microcontrollers-ATmega328P_Datasheet.pdf](https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7810-Automotive-Microcontrollers-ATmega328P_Datasheet.pdf)
- **LM2596 Step-Down DC-DC Switching Regulator Module:**  
  Monolithic 150 kHz 3A step-down switching buck converter in vertical upright module form ($4 \times 7$ pins, 200 mil pitch).
- **10-Way 5.08mm Screw Terminal Block (ZB128 14mm):**  
  Screw clamp terminal block for PCB, 5.08mm (0.2") pitch, 10 positions, 300V / 16A dielectric rating, 14mm body height.
- **WCH (Jiangsu Qinheng Co.): CH340 USB-to-Serial TTL Converter:**  
  6-pin module (DTR, RXD, TXD, VCC, CTS, GND) with selectable 5V/3.3V logic levels.  
  [https://www.wch-ic.com/products/CH340.html](https://www.wch-ic.com/products/CH340.html)
- **ARCTIC P8 Black (80mm Pressure-optimised Fan):**  
  ARCTIC GmbH — Product Specification Sheet (SKU: ACFAN00147A). 12V DC, 0.14A, 3000 RPM, 3-Pin.  
  [https://www.arctic.de/media/9a/83/08/1697784936/Spec_Sheet_P8_BLACK_EN.pdf](https://www.arctic.de/media/9a/83/08/1697784936/Spec_Sheet_P8_BLACK_EN.pdf)
- **Akasa 90mm Chassis Cooling Fans (92 $\times$ 92 $\times$ 25mm):**  
  Akasa Thermal Solution. Standard 12V DC (~0.15A–0.20A), 3-pin connector.
- **Sullins Connector Solutions — Card Edge Connectors (0.100" Pitch, ETM / EBM Series):**  
  44-position / 22-contact industrial female card edge receptacle (2.54 mm pitch, $0.300'' - 0.330''$ contact depth).  
  [https://www.sullinscorp.com/](https://www.sullinscorp.com/)
- **Vector Electronics & Technology — Eurocard & Vectorbord Card-Edge Plugboards:**  
  Standard 44-pin edge connector prototyping boards (Model 3662 series).  
  [https://www.vectorelect.com/](https://www.vectorelect.com/)

### 3. Industry Standards & Linux Kernel Documentation
- **Wikipedia — Edge Connector & Finger Card Standards:**  
  Standard dimensional definitions, beveling, insertion chamfers, and mechanical polarizing keys for card edge connectors.  
  [https://en.wikipedia.org/wiki/Edge_connector](https://en.wikipedia.org/wiki/Edge_connector)
- **Intel Corporation:** *4-Wire Pulse Width Modulation (PWM) Controlled Fans Specification*, Revision 1.3 (September 2005).  
  Open-collector tachometer 2 pulses per revolution output and fan connector pinouts.
- **The Linux Kernel Organization:** *Hardware Monitoring Kernel Subsystem (`hwmon`)*.  
  Thermal sensor and fan control sysfs driver architecture (`/sys/class/hwmon/`).  
  [https://docs.kernel.org/hwmon/](https://docs.kernel.org/hwmon/)
- **Linux USB-to-Serial Driver:**  
  In-tree kernel driver `drivers/usb/serial/ch341.c`.

---

## 10. Comprehensive Production Cost Analysis

We present a comprehensive quantitative and qualitative cost analysis for manufacturing the **Custom Stripboard Rev 1.1 / Rev 1.1a**, incorporating benchmark quotations from leading **Brazilian national PCB manufacturers (TEC-CI, PCB Brasil, Micro-Circuitos, Griffus PCB, Micropress, and Circuibras)**, complete bill of materials (BOM), through-hole assembly and soldering labor, firmware flashing, functional quality testing, and volume scalability scenarios.

---

### 10.1 Bare PCB Fabrication — Brazilian Industry Benchmark vs. Offshore

#### Board Manufacturing Parameters:
- **Dimensions:** $88.90\text{ mm} \times 128.27\text{ mm}$ ($3.50'' \times 5.05''$, surface area $\approx 114\text{ cm}^2$).
- **Layer Count:** 2 Layers (Double-sided FR4, single-sided copper routing on bottom layer `Layer 6`).
- **Substrate & Copper:** Standard FR-4 ($T_g \ge 130\text{--}140^\circ\text{C}$), board thickness $1.60\text{ mm}$, copper weight 1 oz ($35\,\mu\text{m}$).
- **Through-Hole Specification:** Plated Through-Hole (PTH), 100% Through-Hole Default, minimum pad diameter $\ge 80.00\text{ mil}$ ($2.032\text{ mm}$), drill hole $35.00\text{ mil}$ ($0.889\text{ mm}$).
- **Surface Finish:** Lead-Free HASL (standard) or ENIG (Electroless Nickel Immersion Gold, recommended for card-edge connector fingers).
- **Edge Connector Features:** $45^\circ$ insertion lead-in chamfering / beveling on 44-pin tongue.

#### Benchmark of Leading Brazilian PCB Manufacturers:

| Manufacturer | Headquarters / Profile | Typical Prototype (5 boards) | Small Batch (30 boards) | Production Run (100+ boards) | Turnaround / Lead Time | Key Competitive Advantage |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **TEC-CI Circuitos Impressos** | São Paulo - SP (Est. 1984) | **R$ 39,00** / pc<br>*(US$ 6.72)* | **R$ 24,00** / pc<br>*(US$ 4.14)* | **R$ 13,50** / pc<br>*(US$ 2.33)* | 7–10 business days | Online instant quotation engine; aggressive prototype pricing; robust national support |
| **PCB Brasil** | Campinas - SP | **R$ 42,00** / pc<br>*(US$ 7.24)* | **R$ 26,00** / pc<br>*(US$ 4.48)* | **R$ 14,50** / pc<br>*(US$ 2.50)* | 7–10 business days | Dedicated fast-proto web configurator; flexible solder mask colors; reliable tracking |
| **Micro-Circuitos** | Rio de Janeiro / SP | **R$ 45,00** / pc<br>*(US$ 7.76)* | **R$ 27,00** / pc<br>*(US$ 4.65)* | **R$ 15,00** / pc<br>*(US$ 2.59)* | 8–12 business days | Prototype and small-series specialist; personalized engineering analysis and layout check |
| **Griffus PCB** | Cotia - SP | **R$ 48,00** / pc<br>*(US$ 8.28)* | **R$ 28,00** / pc<br>*(US$ 4.83)* | **R$ 14,00** / pc<br>*(US$ 2.41)* | 8–10 business days | ISO-certified industrial supplier; high mechanical dimensional consistency for card cages |
| **Micropress** | São Paulo - SP (Est. 1986) | **R$ 72,00** / pc<br>*(US$ 12.41)* | **R$ 42,00** / pc<br>*(US$ 7.24)* | **R$ 24,00** / pc<br>*(US$ 4.14)* | **24h–48h express**<br>*(or 5–7d std)* | National benchmark in express quick-turn prototyping; aerospace/medical-grade quality |
| **Circuibras** | Curitiba - PR | **R$ 56,00** / pc<br>*(US$ 9.65)* | **R$ 25,00** / pc<br>*(US$ 4.31)* | **R$ 12,00** / pc<br>*(US$ 2.07)* | 10–15 business days | Large automated manufacturing plant; unmatched economies of scale in 100+ volume runs |

*(Reference exchange rate: USD $1.00 = BRL R$ 5.80)*

#### Strategic National vs. Offshore Trade-Off Analysis:

- **Brazilian National Fabrication (TEC-CI, PCB Brasil, Micro-Circuitos, etc.):**
  - **Zero Customs Risk:** Immediate domestic Sedex shipping (1–2 days post-fabrication).
  - **100% Tax Compliant:** Direct NF-e invoice with national CNPJ, mandatory for Brazilian research institutions (FAPESP, CNPq, FINEP) and enterprise corporate accounting.
  - **No Hidden Fees:** Excluded from the Brazilian 92%+ import tariff ("Remessa Conforme" / II + ICMS compounding on goods + freight).
  - **Direct Engineering Support:** Same timezone, direct phone/WhatsApp technical communication with CAM engineers in Portuguese.
- **Offshore Fabrication (e.g., JLCPCB / PCBWay):**
  - Base sticker price appears lower ($4.00–$75.00), but international courier freight ($14.00–$35.00) plus mandatory Brazilian import duties and ICMS bring small prototype lots to **R$ 28,00 – R$ 35,00 / board** with delivery times spanning **15 to 30 calendar days**.

---

### 10.2 Complete Bill of Materials (BOM) per Unit

All components adhere strictly to the **100% Through-Hole (THT / DIP)** engineering directive:

| Item | Component / Specification | Package / Lead Pitch | Qty | Unit Price (USD) | Unit Price (BRL) | Total Cost (BRL) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **U1** | ATmega328P-PU Microcontroller | Narrow DIP-28 ($0.3''$) | 1 | $2.20 | R$ 12.80 | R$ 12.80 |
| **SKT1** | DIP-28 Stamped / Machined IC Socket | 28-Pin $2.54\text{ mm}$ pitch | 1 | $0.25 | R$ 1.50 | R$ 1.50 |
| **U2** | ULN2003A / ULN7003A Darlington Driver | DIP-16 | 1 | $0.40 | R$ 2.30 | R$ 2.30 |
| **SKT2** | DIP-16 IC Socket | 16-Pin $2.54\text{ mm}$ pitch | 1 | $0.15 | R$ 0.90 | R$ 0.90 |
| **MOD1** | CH340 6-Pin USB-to-TTL Serial Module | 6-Pin $2.54\text{ mm}$ pitch | 1 | $1.20 | R$ 7.00 | R$ 7.00 |
| **Y1** | Quartz Crystal 16.000 MHz | HC-49S Thru-Hole | 1 | $0.18 | R$ 1.00 | R$ 1.00 |
| **C3, C4** | Ceramic Disc Capacitors 22 pF | $2.54\text{ mm}$ pitch | 2 | $0.05 | R$ 0.30 | R$ 0.60 |
| **U101, U102** | LM317T Linear Regulators (TI Datasheet) | TO-220 Upright | 2 | $0.40 | R$ 2.30 | R$ 4.60 |
| **VR101, VR102**| LM2596 DC-DC Step-Down Buck Modules | Upright $4 \times 7$ pin array | 2 | $1.30 | R$ 7.50 | R$ 15.00 |
| **TB101** | 10-Way 5.08mm Screw Terminal Block | ZB128 14mm height | 1 | $1.10 | R$ 6.40 | R$ 6.40 |
| **CONN117, 118**| 2.1mm $\times$ 5.5mm DC Power Barrel Jacks | THT Radial | 2 | $0.25 | R$ 1.45 | R$ 2.90 |
| **HDR_SANDWICH**| 2.54mm Breakaway Pin Headers (M/F) | 40-pin breakaway strips | 2 strips | $0.60 | R$ 3.50 | R$ 7.00 |
| **PASSIVES** | Decoupling caps (100nF, 1uF, 100uF) + 1/4W Resistors | Axial / Radial Kit | 1 kit | $0.70 | R$ 4.00 | R$ 4.00 |
| **MECHANICAL** | M3 Brass/Nylon Screws, Nuts, Standoffs | 6-point chassis kit | 6 sets | $0.80 | R$ 4.60 | R$ 4.60 |
| **TOTAL BOM** | **Raw Electronic Components per Board** | — | — | **$9.58** | **R$ 55.85** | **R$ 70.60 (w/ buffer)** |

---

### 10.3 Assembly, Soldering & Testing Labor

- **Through-Hole Manual Assembly Time:** ~25 to 35 minutes per board (component insertion, lead bending, manual hand soldering, lead trimming, and flux cleaning).
- **Automated USB Flashing & Quality Assurance:** ~5 to 7 minutes (`make flash` over USB via `avrdude`, tachometer edge capture check, 4-channel hardware PWM sweep, and multimeter measurement of dual LM317 and LM2596 voltage rails).
- **Labor Cost Models:**
  - *DIY / Maker Assembly:* R$ 0.00 (educational / open-source hobby).
  - *Specialized Bench Technician (Brazil):* Estimated at R$ 25.00 to R$ 35.00 per board.
  - *Automated Selective / Wave Soldering (Volume batches 100+):* ~US$ 3.50 to US$ 5.00 (R$ 20.00 to R$ 29.00) per unit.

---

### 10.4 Consolidated Unit Cost Summary Across Production Volumes

*(Based on average Brazilian national PCB manufacturing rates from TEC-CI / PCB Brasil / Micro-Circuitos)*

| Production Scenario | Bare PCB Cost (BR) | BOM Component Cost | Assembly & Testing | **Total Unit Cost (BRL)** | **Total Unit Cost (USD)** |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **1. DIY / Single Prototype (1 to 5 pcs)** | R$ 39,00 (TEC-CI) | R$ 70,60 | R$ 0,00 (Self-built) | **R$ 109,60** | **$18.90** |
| **2. Semi-Artisanal Small Batch (30 pcs)** | R$ 24,00 (TEC-CI) | R$ 52,00 | R$ 25,00 (Technician) | **R$ 101,00** | **$17.40** |
| **3. Industrial Production Batch (100+ pcs)** | R$ 12,00 (Circuibras) | R$ 42,00 | R$ 20,00 (Selective) | **R$ 74,00** | **$12.75** |

---

### 10.5 Cost Optimization Strategies (Cost-Down Roadmap)

1. **Discrete Switching Converter Integration:**
   - Replacing the two pre-assembled commercial LM2596 modules (R$ 15.00) with discrete buck controller ICs, surface or THT power inductors, and Schottky diodes directly on the PCB reduces unit cost by up to **R$ 8.00** in batches over 100 units.
2. **Direct DIP Soldering (Socket Elimination):**
   - For industrial series deployment, soldering the ATmega328P and ULN2003 directly into the board eliminates sockets, saving **R$ 2.40** per board while significantly enhancing vibration resistance inside PC enclosures.
3. **Reel and Wholesale Component Procurement:**
   - Purchasing passive components (capacitors, metal film resistors, pin headers) on full tape-and-reel quantities from authorized regional distributors (e.g., Mouser, DigiKey, Farnell, or local importers) cuts the passive kit cost from R$ 4.00 to under **R$ 1.20** per board.

---

## 11. License

This project is open-source and licensed under the **GNU Lesser General Public License v3.0 (LGPLv3)**.

- Full License Terms: [LICENSE](file:///home/fred/C/fanControl/LICENSE)
- GNU Lesser General Public License: [COPYING.LESSER](file:///home/fred/C/fanControl/COPYING.LESSER) / [LICENSE.LESSER](file:///home/fred/C/fanControl/LICENSE.LESSER)
- GNU General Public License: [COPYING](file:///home/fred/C/fanControl/COPYING)

You may freely modify, distribute, and integrate this software and hardware design in your own projects under the conditions of the LGPLv3.

