# Custom PC Fan Controller (Linux Controlled)

[![License: LGPL v3](https://img.shields.io/badge/License-LGPL_v3-blue.svg)](LICENSE)
[![CI Build](https://img.shields.io/badge/Build-Passing-brightgreen.svg)](.github/workflows/ci.yml)
[![EDA: Lepton-EDA & pcb-rnd](https://img.shields.io/badge/EDA-Lepton--EDA%20%2F%20pcb--rnd-orange.svg)](lepton/)
[![Assisted by AI: Gemini 3.8 Flash](https://img.shields.io/badge/AI--Assisted-Gemini%203.8%20Flash-blueviolet.svg)](#8-assisted-by-ai---gemini-38-flash-medius)

A comprehensive hardware, firmware, and software system for integrating custom cooling fan control inside a desktop PC chassis. The controller is built on a standard **33.0 mm $\times$ 72.0 mm through-hole protoboard**, powered by a standalone **ATmega328P-PU** running at **16.000 MHz**, a **CH340 6-pin USB-Serial converter**, and a **ULN2003A / ULN7003A** Darlington array driving up to 4 PC cooling fans (e.g., 4x Akasa 90mm and Arctic P8) with real-time tachometer RPM feedback, failsafe watchdog protection, and automated thermal management via Linux.

---

## Table of Contents

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
4. [Custom Stripboard Rev 1.1 / 1.1a — Arquitetura Modular & Especificações](#custom-stripboard-rev-11--11a--arquitetura-modular--especificações)
   - [Especificações Físicas e Mecânicas](#1-especificações-físicas-e-mecânicas)
   - [Subsistema de Força de Topo: Entradas DC Jack & Breakouts SIP3](#2-subsistema-de-força-de-topo-entradas-dc-jack--breakouts-sip3)
   - [Duplo Regulador Linear LM317 (Datasheet TI, Página 1)](#3-duplo-regulador-linear-lm317-datasheet-ti-página-1)
   - [Margem Esquerda: Módulos Step-Down LM2596 Upright (VR101, VR102)](#4-margem-esquerda-módulos-step-down-lm2596-upright-vr101-vr102)
   - [Margem Direita: Borne KRE 10 Vias 5.08mm & Matriz Pass-Thru (TB101)](#5-margem-direita-borne-kre-10-vias-508mm--matriz-pass-thru-tb101)
   - [Margem Direita: Área de Prototipagem Rápida Scratch-Pad (56 Ilhas, 3 mil)](#6-margem-direita-área-de-prototipagem-rápida-scratch-pad-56-ilhas-3-mil)
   - [Diretriz de Fabricação: Padrão Thru-Hole (THT) Obrigatório & Pad Size >= 80 mil](#7-diretriz-de-fabricação-padrão-thru-hole-tht-obrigatório--pad-size--80-mil)
   - [Hierarquia de Largura de Trilhas de Cobre (Trace Width Hierarchy)](#8-hierarquia-de-largura-de-trilhas-de-cobre-trace-width-hierarchy)
   - [Matriz de Prototipagem & Seção de Interconexão em Sanduíche](#9-matriz-de-prototipagem--seção-de-interconexão-em-sanduíche)
   - [Conector de Borda Single-Sided (Card Edge Tongue 44-Pin Standard)](#10-conector-de-borda-single-sided-card-edge-tongue-44-pin-standard)
   - [Chave de Polarização Mecânica (Keying na Coluna 8)](#11-chave-de-polarização-mecânica-keying-na-coluna-8)
   - [Jumpers de Solda Abertos (Open Solder Jumpers)](#12-jumpers-de-solda-abertos-open-solder-jumpers)
   - [Furos de Fixação Mecânica M3, Keepouts e Alinhamento](#13-furos-de-fixação-mecânica-m3-keepouts-e-alinhamento)
   - [Serigrafia e Identificação Visual](#14-serigrafia-e-identificação-visual)
   - [Arquivos EDA e Instruções de Compilação](#15-arquivos-eda-e-instruções-de-compilação)
   - [Sub-revisão 1.1a — Otimização do Sanduíche e 32 Linhas Contínuas](#16-sub-revisão-11a--otimização-do-sanduíche-e-32-linhas-contínuas)
5. [Printable 1:1 Scale Templates](#printable-11-scale-templates)
6. [Directory Structure](#directory-structure)
7. [Quick Start & Build Guide](#quick-start--build-guide)
8. [Assisted by AI - Gemini 3.8 Flash Medius](#assisted-by-ai---gemini-38-flash-medius)
9. [Bibliography & References](#bibliography--references)
10. [Avaliação Detalhada de Custo de Produção (Production Cost Analysis)](#10-avaliação-detalhada-de-custo-de-produção-production-cost-analysis)
11. [License](#11-license)

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

## Custom Stripboard Rev 1.1 / 1.1a — Arquitetura Modular & Especificações

> **Documentação Multilíngue / Multilingual Engineering Documentation:**  
> 🇧🇷 **Português:** [CUSTOM_STRIPBOARD_REV1.1_SPEC.md](file:///home/fred/C/fanControl/docs/CUSTOM_STRIPBOARD_REV1.1_SPEC.md) | 🇺🇸 **US-English:** [CUSTOM_STRIPBOARD_REV1.1_SPEC_EN.md](file:///home/fred/C/fanControl/docs/CUSTOM_STRIPBOARD_REV1.1_SPEC_EN.md) | 🇪🇸 **Español:** [CUSTOM_STRIPBOARD_REV1.1_SPEC_ES.md](file:///home/fred/C/fanControl/docs/CUSTOM_STRIPBOARD_REV1.1_SPEC_ES.md)

A evolução do projeto de controle de arrefecimento e prototipagem originou a **Custom Stripboard Rev 1.1** e sua sub-revisão **Rev 1.1a**, uma plataforma modular expandida de prototipagem em formato padrão Eurocard/Vector desenvolvida no fluxo **Lepton-EDA** e **`pcb-rnd`**. A placa incorpora barramentos triplos de alimentação (+12V, +5V, GND), duas fontes independentes de força via DC barrel jacks afastadas nas extremidades, **duplo circuito regulador linear LM317** (TI Datasheet) no vão central, **dois módulos conversores step-down LM2596 verticais** na margem esquerda, um **borne terminal de parafusos KRE 10 vias 5.08mm com matriz de 3 pass-thrus** na borda direita, uma **área de prototipagem rápida tipo scratch-pad com 56 ilhas e microtrilhas raspáveis de 3 mil**, matriz central de prototipagem com headers de interconexão tipo sanduíche, e terminação direta em conector de borda (*card-edge connector*) industrial padrão 44 pinos (passo de $100\text{ mil}$ / $2.54\text{ mm}$), estritamente de face única (*single-sided* na camada inferior).

> [!IMPORTANT]
> **Diretriz de Fabricação — Padrão Thru-Hole (THT) como Default Obrigatório**:
> A montagem em tecnologia SMD é tratada como opção secundária. O **padrão DEFAULT de fabricação é 100% Through-Hole (furo passante metalizado)**. Todas as ilhas da matriz de tiras, pass-thrus do KRE, scratch-pad, conectores e reguladores utilizam furação metalizada com diâmetro externo $\ge 80.00\text{ mil}$ ($2.032\text{ mm}$), eliminando problemas de delaminação e viabilizando soldagem e retrabalho manual robustos.

```
  Custom Stripboard Rev 1.1 / Rev 1.1a (Vista Geral da Arquitetura Topológica):
  ┌────────────────────────────────────────────────────────────────────────────────────────┐
  │ [MH101]    [CONN117 DC JACK 1]   [LM317 #1]  [LM317 #2]   [CONN118 DC JACK 2]  [MH102] │
  │ M3 (200,200) X=800, Y=200       X=1400..1600 X=1900..2100  X=2400, Y=200    (3300,200)│
  │            [SIP3 Breakout 1]     U101+Caps   U102+Caps    [SIP3 Breakout 2]            │
  │            X=500..700, Y=200..400 R101/R102   R103/R104   X=2800..3000                 │
  │ ───────────────────────────────── GND BRIDGE (Y=600 mil) ───────────────────────────── │
  │ [VR101]                                                    [TB101 KRE 10P 5.08mm]      │
  │ LM2596 Upright #1                                          X=3400, Y=600..2400 mil     │
  │ 4x7 Pinos (200mil)                                         [CONN137..139 Pass-Thru]    │
  │ Y=600..1200 mil                                            3 ilhas passantes por pino  │
  │ VIN1+/- , OUT1+/-                                          10 redes: KRE_1..KRE_10     │
  │                                                                                        │
  │ [MH103] M3 Fixação Central                                 [MH104] M3 Ajustado         │
  │ X=200, Y=2000 mil                                          X=3300, Y=2700 mil          │
  │ (Espaço livre entre VR101 e VR102)                         (Folga KRE e Scratch-Pad)   │
  │                                                                                        │
  │ [VR102]                                                    [SCRATCH-PAD PROTO AREA]    │
  │ LM2596 Upright #2                                          14 linhas x 4 colunas       │
  │ 4x7 Pinos (200mil)                                         56 ilhas (Pad 90mil, Broca 35)
  │ Y=2800..3400 mil                                           Microtrilhas de 3 mil       │
  │ VIN2+/- , OUT2+/-                                          X=3100..3400, Y=3000..4300  │
  │                                                            Net comum: SCRATCHPAD       │
  │ ────────────────────────────────────────────────────────────────────────────────────── │
  │ 8x Barramentos Verticais de Alimentação (Trilhas Contínuas de 40 mil: GND/+5V/+12V)   │
  │ ├── 58 Linhas (Rev 1.1) ou 64 Linhas (Rev 1.1a) Horizontais de Prototipagem (10 mil)  │
  │ └── Seção de Interconexão em Sanduíche:                                                │
  │     ├── Réguas Horizontais Superiores (SIP9N)                                          │
  │     ├── Headers Centrais Dupla Barra (HEADER18 - J201 e J301, passo 100 mil)           │
  │     │     └── Pontes de Interligação Vertical alargadas para 30 mil                    │
  │     ├── Réguas Horizontais Inferiores (SIP9N)                                          │
  │     └── Réguas Verticais Inferiores de Saída (SIP4N - Trilhas de 40 mil)               │
  │                                                                                        │
  │ [MH105] ── Alinhamento Mecânico com a Última Linha de Ilhas ── [MH106]                 │
  │ X=200, Y=4600 mil (Base do anel alinha rigorosamente com a base dos pads) X=3300 mil   │
  │ ══════════════════════════════════════════════════════════════════════════════════════ │
  │ Ombros Mecânicos de Encosto (Y = 4740 mil - degrau de 3.5" para 2.7" com chanfros 45°) │
  │       ┌────────────────────────────────────────────────────────────────────────┐       │
  │       │ Jumpers de Solda Abertos (Open Solder Jumpers, Gap 13 mil, Trilhas 30m)│       │
  │       ├────────────────────────────────────────────────────────────────────────┤       │
  │       │ Conector de Borda Single-Sided (Card Edge Tongue 44-Pin Standard):     │       │
  │       │     ├── 26 Posições de Contato (Passo 100 mil / 2.54 mm)               │       │
  │       │     ├── Face Única (Exclusivo na Camada de Solda Inferior / onsolder)  │       │
  │       │     ├── Chave de Polarização Mecânica: Dedo 8 Omitido ("KEY")          │       │
  │       │     └── Chanfros de Inserção a 45° nos Cantos Inferiores               │       │
  │       └────────────────────────────────────────────────────────────────────────┘       │
  └────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### 1. Especificações Físicas e Mecânicas

| Parâmetro | Valor em Mils | Valor em Milímetros (mm) | Descrição / Função |
| :--- | :---: | :---: | :--- |
| **Largura Total do Corpo** | $3500.00\text{ mil}$ | $88.90\text{ mm}$ | Largura estrutural da área de prototipagem |
| **Comprimento Total da Placa** | $5050.00\text{ mil}$ | $128.27\text{ mm}$ | Comprimento do topo mecânico até a borda da lingueta |
| **Largura da Lingueta de Borda** | $2700.00\text{ mil}$ | $68.58\text{ mm}$ | Largura de inserção do conector ($X = 400.00$ a $3100.00\text{ mil}$) |
| **Profundidade de Inserção** | $310.00\text{ mil}$ | $7.87\text{ mm}$ | Extensão inserível da lingueta ($Y = 4740.00$ a $5050.00\text{ mil}$) |
| **Ombros Mecânicos de Apoio** | $400.00\text{ mil}$ | $10.16\text{ mm}$ | Degraus em $Y = 4740\text{ mil}$ para encosto no soquete do conector |
| **Chanfros de Inserção (Lead-in)** | $40.00\text{ mil} \times 45^\circ$ | $1.02\text{ mm} \times 45^\circ$ | Chanfros nos cantos inferiores para entrada suave no slot |
| **Furos de Fixação (M3 Banhados)** | $126.00\text{ mil}$ (broca) | $3.20\text{ mm}$ | 6x furos (pad $240\text{ mil}$, clearance $40\text{ mil}$, alívio $300\text{ mil}$) |
| **Posicionamento M3 Superior** | $(200, 200)$, $(3300, 200)$ | $(5.08, 5.08)$, $(83.82, 5.08)$ | Margens laterais superiores (`MH101` e `MH102`) |
| **Posicionamento M3 Central** | $(200, 2000)$, $(3300, 2700)$ | $(5.08, 50.80)$, $(83.82, 68.58)$ | **`MH103` entre LM2596; `MH104` entre KRE e Scratch-pad** |
| **Posicionamento M3 Inferior** | $(200, 4600)$, $(3300, 4600)$ | $(5.08, 116.84)$, $(83.82, 116.84)$ | **Alinhado com a base da última linha de ilhas** (`MH105`, `MH106`) |

---

### 2. Subsistema de Força de Topo: Entradas DC Jack & Breakouts SIP3

Para acomodar os circuitos reguladores centrais e permitir dissipadores térmicos sem interferência, os conectores DC Barrel Jack 2.1mm $\times$ 5.5mm foram afastados para as laterais:

- **DC Jack 1 (`CONN117`):** Posicionado em $(X = 800.00\text{ mil}, Y = 200.00\text{ mil})$.
  - Ao seu lado esquerdo, conector breakout SIP3 (`CONN119..121` em $X = 500, 600, 700\text{ mil}$, $Y = 200..400\text{ mil}$).
  - Interligações roteadas exclusivamente com **trilhas de 40 mil (`Layer 6 "bottom"`)** para suportar correntes contínuas de até 5A.
- **DC Jack 2 (`CONN118`):** Posicionado em $(X = 2400.00\text{ mil}, Y = 200.00\text{ mil})$.
  - Ao seu lado direito, conector breakout SIP3 (`CONN122..124` em $X = 2800, 2900, 3000\text{ mil}$, $Y = 200..400\text{ mil}$).
  - Interligações roteadas exclusivamente com **trilhas de 40 mil**.

---

### 3. Duplo Regulador Linear LM317 (Datasheet TI, Página 1)

No espaço central superior da placa ($X = 1400\text{ mil}$ a $X = 2100\text{ mil}$, $Y = 200..700\text{ mil}$), foram implementados dois circuitos reguladores independentes e completos, conforme o diagrama oficial do fabricante:

$$V_{OUT} = 1.25\,\text{V} \times \left(1 + \frac{R_2}{R_1}\right) + I_{ADJ} \times R_2$$

```
                         CIRCUITO REGULADOR LM317 (Datasheet TI Página 1)
                              ┌──────────────┐
                  VIN o───────┤ 3 (VIN)      │
                              │   LM317      │
                    ┌─────────┤ 1 (ADJ)    2 ├──┬───────────────o VOUT
                    │         └──────────────┘  │
                    │               │           │
                   [R2]            [R1 240Ω]   [C2 1.0µF]
                    │ (Ajuste)      │           │
                    │               └───────────┘
                    │
           GND o────┴───────────────────────────────────────────o GND (Comum)
               (C1 0.1µF desacoplamento na entrada VIN)
```

#### LM317 Circuito #1:
- **CI Regulador `U101` (TO-220 Upright):** Pino 3 (VIN) em $(1400, 300)$, Pino 2 (VOUT) em $(1500, 300)$, Pino 1 (ADJ) em $(1600, 300)$.
- **Capacitores Passantes:** $C_{101}$ ($0.1\,\mu\text{F}$ disco cerâmico) em $(1400, 400..600)$; $C_{102}$ ($1.0\,\mu\text{F}$ tântalo/eletrolítico) em $(1500, 400..600)$.
- **Resistores Axiais:** $R_{101}$ ($240\,\Omega$, 1/4W) em $(1500..1600, 500)$; $R_{102}$ ($R_2$, resistor fixo ou trimpot) em $(1600, 400..600)$.
- **Ilhas de Teste e Alimentação THT (Pads 80 mil):** `J101` (VIN1 em $1400, 200$), `J102` (VOUT1 em $1500, 200$), `J103` (GND em $1400, 700$).

#### LM317 Circuito #2:
- **CI Regulador `U102` (TO-220 Upright):** Pino 3 (VIN) em $(1900, 300)$, Pino 2 (VOUT) em $(2000, 300)$, Pino 1 (ADJ) em $(2100, 300)$.
- **Capacitores Passantes:** $C_{103}$ ($0.1\,\mu\text{F}$) em $(1900, 400..600)$; $C_{104}$ ($1.0\,\mu\text{F}$) em $(2000, 400..600)$.
- **Resistores Axiais:** $R_{103}$ ($240\,\Omega$) em $(2000..2100, 500)$; $R_{104}$ ($R_2$) em $(2100, 400..600)$.
- **Ilhas de Teste e Alimentação THT (Pads 80 mil):** `J104` (VIN2 em $1900, 200$), `J105` (VOUT2 em $2000, 200$), `J106` (GND em $1900, 700$).
- **Barramento de Terra Comum:** Trilha de cobre de $40\text{ mil}$ em $Y = 600\text{ mil}$ interligando o terra de ambos os circuitos reguladores.

---

### 4. Margem Esquerda: Módulos Step-Down LM2596 Upright (`VR101`, `VR102`)

Para conversão de alta eficiência de fontes chaveadas (ex: +12V para +5V ou tensões ajustáveis sob correntes de até 3A):
- **Footprint:** $4 \times 7$ pinos em passo de $200.00\text{ mil}$ ($5.08\text{ mm}$), colunas $X = 100, 200, 300, 400\text{ mil}$.
- **Módulo 1 (`VR101`):** $Y = 600.00\text{ mil}$ a $1200.00\text{ mil}$. Linhas 1-4 formam `VIN1+` ($X = 100$) e `VIN1-` ($X = 300$); Linhas 5-7 formam `OUT1+` ($X = 100$) e `OUT1-` ($X = 300$).
- **Módulo 2 (`VR102`):** $Y = 2800.00\text{ mil}$ a $3400.00\text{ mil}$. Linhas 1-4 formam `VIN2+` e `VIN2-`; Linhas 5-7 formam `OUT2+` e `OUT2-`.
- **Trilhas de Potência de $40\text{ mil}$:** Barramentos verticais de $40\text{ mil}$ unem os pinos em cada função elétrica.
- **Posicionamento de `MH103`:** Posicionado estrategicamente em $(X = 200\text{ mil}, Y = 2000\text{ mil})$, ficando exatamente a meia distância entre `VR101` e `VR102`, com folga mecânica superior a $650\text{ mil}$ para o parafuso M3.

---

### 5. Margem Direita: Borne KRE 10 Vias 5.08mm & Matriz Pass-Thru (`TB101`)

Na borda superior direita, entre os furos `MH102` e `MH104`:
- **Conector Borne KRE 10P 5.08mm (`TB101`):** Pinos em $X = 3400.00\text{ mil}$, nas cotas $Y = [600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400]\text{ mil}$.
- **Matriz Pass-Thru Horizontal de 3 Pontos:** Para cada pino do conector, estendem-se 3 ilhas passantes em direção ao centro da placa:
  - `CONN137` em $X = 3300.00\text{ mil}$
  - `CONN138` em $X = 3200.00\text{ mil}$
  - `CONN139` em $X = 3100.00\text{ mil}$
- **Trilhas de Cobre de $30\text{ mil}$:** Cada linha de 4 ilhas é unida por trilhas de $30\text{ mil}$, formando 10 redes elétricas isoladas (`KRE_1` a `KRE_10`).
- **Folgas Mecânicas Seguras:**
  - Acima ($Y = 600\text{ mil}$): Folga $>150\text{ mil}$ para o keepout do parafuso `MH102`.
  - Abaixo ($Y = 2400\text{ mil}$): O corpo plástico do borne termina em $Y = 2500\text{ mil}$, proporcionando $80\text{ mil}$ de isolamento até o pad de `MH104` ($Y = 2700\text{ mil}$).

---

### 6. Margem Direita: Área de Prototipagem Rápida Scratch-Pad (56 Ilhas, 3 mil)

Na margem direita inferior, entre `MH104` e `MH106`:
- **Matriz de Prototipagem:** 14 linhas $\times$ 4 colunas = **56 ilhas** ($X = 3100, 3200, 3300, 3400\text{ mil}$, $Y = 3000$ a $4300\text{ mil}$).
- **Geometria dos Pads:** Pad de **$90.00\text{ mil}$**, broca passante de **$35.00\text{ mil}$**, máscara de **$96.00\text{ mil}$**.
- **Gap de Cobre de $10\text{ mil}$:** Espaçamento entre pads de apenas **$10.00\text{ mil}$ ($0.254\text{ mm}$)**.
- **Microtrilhas Raspáveis de $3\text{ mil}$ (Knife-Scratchable):**
  - Todas as 56 ilhas pertencem à mesma rede elétrica inicial (`SCRATCHPAD`).
  - As ilhas vizinhas são unidas por microtrilhas de **$3.00\text{ mil}$** na camada de cobre inferior.
  - Podem ser facilmente seccionadas com estilete ou bisturi cirúrgico para criar ilhas isoladas ou pequenos barramentos personalizados.
- **Caixa de Serigrafia:** Contorno retangular silkscreen delimitando a área com a legenda `"SCRATCH PAD"`.

---

### 7. Diretriz de Fabricação: Padrão Thru-Hole (THT) Obrigatório & Pad Size $\ge 80\text{ mil}$

- **Montagem THT como Regra:** A tecnologia de montagem SMD é opcional; o padrão default de engenharia do projeto é **100% Through-Hole (furo passante metalizado)**.
- **Dimensão dos Pads Padronizada:** Todas as ilhas de solda que antes mediam $< 80\text{ mil}$ foram ampliadas para **$\ge 80.00\text{ mil}$** ($80\text{ mil}$ ou $90\text{ mil}$), com broca de $35\text{ mil}$ e máscara de $86\text{ mil}$.
- **Conformidade Verificada nos Arquivos de Fabricação:**
  - Pinos com diâmetro $< 80\text{ mil}$: **0**
  - Pinos sem furo passante metalizado: **0** (apenas os dedos de conector de borda na lingueta são SMD na face inferior).

---

### 8. Hierarquia de Largura de Trilhas de Cobre (Trace Width Hierarchy)

| Categoria | Largura da Trilha | Clearance | Camada | Aplicação / Conexão |
| :--- | :---: | :---: | :---: | :--- |
| **Potência & Barramentos** | **40 mil** ($1.016\text{ mm}$) | $20\text{ mil}$ | Bottom (Layer 6) | 8 barramentos verticais; trilhas dos Jacks DC; barramentos de potência dos módulos LM2596; alimentação/terra dos LM317; réguas verticais inferiores de 4 pinos |
| **Pontes & Interconexões** | **30 mil** ($0.762\text{ mm}$) | $20\text{ mil}$ | Bottom (Layer 6) | Pontes verticais de 100 mil no `HEADER18`; trilhas dos jumpers de solda abertos; trilhas do Borne KRE para a matriz pass-thru |
| **Feedback e Ajuste** | **20 mil** ($0.508\text{ mm}$) | $20\text{ mil}$ | Bottom (Layer 6) | Linhas do pino 1 (ADJ) dos reguladores LM317 até resistores $R_1$ e $R_2$ |
| **Trilhas de Prototipagem** | **10 mil** ($0.254\text{ mm}$) | $20\text{ mil}$ | Bottom (Layer 6) | Trilhas horizontais das 58 linhas (Rev 1.1) ou 64 linhas (Rev 1.1a) |
| **Microtrilhas Raspáveis** | **3 mil** ($0.076\text{ mm}$) | $10\text{ mil}$ | Bottom (Layer 6) | Malha de união da área de prototipagem rápida *scratch-pad* |

---

### 9. Matriz de Prototipagem & Seção de Interconexão em Sanduíche

1. **8 Barramentos Verticais Contínuos (Power Rails):**
   - 40 furos contínuos cada ($Y = 800\text{ mil}$ a $Y = 4700\text{ mil}$), divididos em pares de conectores `SIP20N` interligados por trilhas de 40 mil.
   - Posições em X: $500, 600, 700\text{ mil}$ (GND, +5V, +12V Banco Esquerdo); $1700, 1800\text{ mil}$ (Blindagem Central); $2800, 2900, 3000\text{ mil}$ (GND, +5V, +12V Banco Direito).
2. **Linhas Horizontais de Prototipagem:**
   - Banco Esquerdo ($X = 800$ a $1600\text{ mil}$, 9 pinos cada).
   - Banco Direito ($X = 1900$ a $2700\text{ mil}$, 9 pinos cada).
   - Interligadas com trilhas de **10 mil**.
3. **Seção de Interconexão em Sanduíche:**
   - Headers centrais dupla barra de 18 pinos (`HEADER18`, 2x9 pinos, passo $100\text{ mil}$): `J201` e `J301`.
   - Ensanduichados por réguas `SIP9N` com pontes verticais alargadas para **30 mil**.
   - Réguas verticais inferiores de 4 pinos (`SIP4N`, $Y = 4400..4700\text{ mil}$) com trilhas de **40 mil**.

---

### 10. Conector de Borda Single-Sided (Card Edge Tongue 44-Pin Standard)

- **Arquitetura Estritamente Single-Sided:** Todos os 26 dedos de contato residem exclusivamente na face inferior (`Layer 6 "bottom"` / `onsolder`). A face superior é laminado FR4 virgem e isolado.
- **Dimensões dos Dedos:** $65\text{ mil} \times 230\text{ mil}$ ($1.65\text{ mm} \times 5.84\text{ mm}$), centrados em $Y = 4925\text{ mil}$ (alcance de $Y = 4810$ a $5040\text{ mil}$).
- **Ombros e Chanfros:** Degraus de apoio mecânico em $Y = 4740\text{ mil}$ e chanfros de $40\text{ mil} \times 45^\circ$ nos cantos.

---

### 11. Chave de Polarização Mecânica (Keying na Coluna 8)

- **Omissão do Contato na Coluna 8:** O dedo `EF8` em $X = 1200\text{ mil}$ e seu solder jumper foram removidos.
- **Indicação em Serigrafia:** Legenda `"KEY"` gravada em $X = 1160\text{ mil}, Y = 4725\text{ mil}$ para inserção de chaveta plástica no soquete do backplane.

---

### 12. Jumpers de Solda Abertos (Open Solder Jumpers)

- **Localização:** Entre a base da matriz ($Y = 4700\text{ mil}$) e o início dos dedos de borda ($Y = 4810\text{ mil}$).
- **Pads SMD:** Dois pads de $50\text{ mil} \times 30\text{ mil}$ com gap aberto de **$13\text{ mil}$ ($0.33\text{ mm}$)**.
- **Operação:** Aberto por default. Uma simples gota de estanho fecha o contato com o dedo de borda desejado.

---

### 13. Furos de Fixação Mecânica M3, Keepouts e Alinhamento

- **Dimensões:** Broca $126\text{ mil}$ ($3.20\text{ mm}$), anel $240\text{ mil}$, keepout de serigrafia e alívio de $300\text{ mil}$ ($7.62\text{ mm}$).
- **Alinhamento dos Furos Inferiores (`MH105`, `MH106`):** Posicionados em $Y = 4600\text{ mil}$, a borda inferior do anel de cobre ($Y = 4720\text{ mil}$) alinha-se perfeitamente com a base da última linha de ilhas ($Y = 4728\text{ mil}$), mantendo $140\text{ mil}$ de folga dos ombros da lingueta.
- **Keepouts Validados:** `MH103` em $Y = 2000\text{ mil}$ (livre de `VR101` e `VR102`); `MH104` em $Y = 2700\text{ mil}$ (livre de `TB101` e do *scratch-pad*).

---

### 14. Serigrafia e Identificação Visual

- Logotipos: `"CUSTOM STRIPBOARD REV 1.1"` e `"CUSTOM STRIPBOARD REV 1.1a"` na margem direita.
- Legendas de Força: `"PWR JACK 1"`, `"PWR JACK 2"`, `"J1 PWR OUT"`, `"J2 PWR OUT"`, `"LM317 #1"`, `"LM317 #2"`, `"VIN"`, `"VOUT"`, `"GND"`.
- Legendas de Conectores: `"LM2596 VR101"`, `"LM2596 VR102"`, `"KRE 10P"`, `"SCRATCH PAD"`, `"KEY"`.

---

### 15. Arquivos EDA e Instruções de Compilação

Todos os arquivos residem no diretório [`lepton/`](file:///home/fred/C/fanControl/lepton/):
- **Documento Técnico de Especificação Completa:** [`docs/CUSTOM_STRIPBOARD_REV1.1_SPEC.md`](file:///home/fred/C/fanControl/docs/CUSTOM_STRIPBOARD_REV1.1_SPEC.md)
- **Script Gerador de Layout:** [`layout_stripboards.py`](file:///home/fred/C/fanControl/lepton/layout_stripboards.py)
- **Rev 1.1a:**
  - Layout PCB: [`stripboard_rev1.1a.pcb`](file:///home/fred/C/fanControl/lepton/rev1.1a/stripboard_rev1.1a.pcb)
  - Esquemático: [`centro.sch`](file:///home/fred/C/fanControl/lepton/rev1.1a/centro.sch) | [centro.png](file:///home/fred/C/fanControl/lepton/rev1.1a/centro.png)
  - Previews 300 DPI: [Topo (Componentes)](file:///home/fred/C/fanControl/lepton/rev1.1a/stripboard_rev1.1a_preview_300dpi.png) | [Fundo (Cobre e Dedos)](file:///home/fred/C/fanControl/lepton/rev1.1a/stripboard_rev1.1a_bottom_preview_300dpi.png)
- **Rev 1.1:**
  - Layout PCB: [`stripboard_rev1.1.pcb`](file:///home/fred/C/fanControl/lepton/rev1.1/stripboard_rev1.1.pcb)
  - Esquemático: [`centro.sch`](file:///home/fred/C/fanControl/lepton/rev1.1/centro.sch) | [centro.png](file:///home/fred/C/fanControl/lepton/rev1.1/centro.png)
  - Previews 300 DPI: [Topo (Componentes)](file:///home/fred/C/fanControl/lepton/rev1.1/stripboard_rev1.1_preview_300dpi.png) | [Fundo (Cobre e Dedos)](file:///home/fred/C/fanControl/lepton/rev1.1/stripboard_rev1.1_bottom_preview_300dpi.png)

#### Comandos de Regeneração:
```bash
# Compilar layouts, atualizar netlists e exportar imagens 300 DPI:
python3 lepton/layout_stripboards.py
```

---

### 16. Sub-revisão 1.1a — Otimização do Sanduíche e 32 Linhas Contínuas

Na sub-revisão **Rev 1.1a**:
1. **Deslocamento do Sanduíche (+200 mil para baixo):** Régua superior em $Y = 4000\text{ mil}$, header central em $Y = 4100..4200\text{ mil}$, e régua inferior em $Y = 4300\text{ mil}$.
2. **Fechamento da Lacuna Inferior:** A régua inferior em $Y = 4300\text{ mil}$ alinha-se a exatamente $100\text{ mil}$ das réguas verticais de saída em $Y = 4400\text{ mil}$.
3. **Preenchimento das Linhas 30, 31 e 32:** As cotas $Y = 3700, 3800, 3900\text{ mil}$ foram preenchidas com réguas horizontais de 9 pinos (`CONN241..243` e `CONN341..343`), totalizando **32 linhas contínuas por banco** (**64 tiras horizontais de 9 pinos** no total).

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

## 8. Assisted by AI - Gemini 3.8 Flash Medius

> [!NOTE]
> **Identificação Oficial de Desenvolvimento:**  
> *"projeto usando lepton-eda/pcb-rnd assistido com IA-Gemini-3.8-Flash-Medium"*

Este projeto foi totalmente concebido, projetado, codificado, depurado e documentado de ponta a ponta com a assistência interativa e autônoma do modelo **Google DeepMind Gemini 3.8 Flash (Medium)**.

### Registro Detalhado de Recursos e Iterações

| Métrica | Quantidade / Escopo | Descrição das Operações |
| :--- | :---: | :--- |
| **Modelo de IA** | `Gemini 3.8 Flash (Medium)` | Modelo de raciocínio multimodal de alta velocidade e precisão |
| **Iterações com Usuário (Turns)** | **17 turnos de diálogo** | Da concepção inicial da protoboard até a revisão e layout final Rev 1.1 / Rev 1.1a |
| **Execuções de Ferramental (Tool Calls)** | **413 invocações de ferramentas** | Operações automatizadas de compilação, inspeção, edição e validação EDA |
| • `run_command` | **290 chamadas** | Execução de shell bash, compiladores C/AVR, scripts Python, ferramentas Lepton-EDA e `pcb-rnd` |
| • `edit_file` | **42 chamadas** | Edições cirúrgicas e contíguas de código-fonte, layout algorítmico e documentação |
| • `manage_task` | **28 chamadas** | Gerenciamento de processos em background e renderizações gráficas pesadas |
| • `read_file` | **26 chamadas** | Leitura e verificação de integridade de netlists, esquemáticos e tabelas |
| • `search_web` | **16 chamadas** | Consulta de datasheets (TI LM317, WCH CH340, ULN2003, Sullins, Vector, etc.) |
| • `write_file` | **9 chamadas** | Criação de novos scripts geradores, especificações técnicas completas e Makefiles |
| • `ask_question` | **2 chamadas** | Alinhamento e esclarecimento direto de requisitos com o usuário |
| **Código Gerado** | **~5.200+ linhas de código** | Firmware AVR C puro, Daemon Linux C, módulo Kernel hwmon, gerador paramétrico PCB, Makefiles e documentação |
| **Gráficos e Previews Gerados** | **14 artefatos gráficos** | Esquemas Lepton-EDA (.png), PCBs topo/fundo 300 DPI, gabaritos 1:1 (.svg, .png, .pdf) |

### Inventário do Ferramental Utilizado

1. **Suíte EDA & Layout:**
   - **`lepton-schematic` / `lepton-cli`:** Captura e exportação vetorial/rasterizada de esquemas elétricos em alta resolução.
   - **`lepton-netlist`:** Extração automatizada de netlists no formato PCB gEDA/pcb-rnd.
   - **`pcb-rnd`:** CAD de circuito impresso com motor de renderização fotográfica de alta definição (`--photo-mode --dpi 300`) e roteamento por script.
2. **Compiladores e Toolchains:**
   - **Host Linux:** `gcc` 14.2.0 (compilação do daemon CLI e leitor `/sys/class/hwmon`).
   - **Cross-Compiler Microcontrolador:** `avr-gcc` 14.2.0 (`-Os -std=gnu99 -mmcu=atmega328p -DF_CPU=16000000UL`), `avr-objcopy`, `avr-size` (consumo de Flash: 6.494 bytes, SRAM: 497 bytes).
   - **Gravador:** `avrdude` (protocolo STK500v1 via conversor CH340 /dev/ttyUSB0).
3. **Ambiente de Scripting e Algoritmos:**
   - **Python 3.12 / 3.13:**
     - `layout_stripboards.py`: Sintetizador paramétrico das placas Rev 1.0, Rev 1.1 e Rev 1.1a, calculando coordenadas, pads, trilhas de cobre, furos M3 e serigrafia.
     - `generate_templates.py`: Gerador de gabaritos físicos de corte e furação em escala 1:1.
     - Scripts de auditoria automatizada de pads (espessura $\ge 80\text{ mil}$ e furação passante).
4. **Vetorização e Processamento Gráfico:**
   - **`reportlab`:** Síntese de canvas PDF com calibração métrica para impressão A4 sem distorção.
   - **`inkscape`:** Renderizador headless de SVGs para bitmaps rasterizados de 300 DPI.
   - **`pdftoppm`:** Utilitário Poppler para inspeção visual e conferência de gabaritos.

---

## 9. Bibliography & References

### 1. Projetos de Referência & Comunidade
- **pnjorge (Paulo Nogueira / F5VMJ):** *"Silent Running With This Dual Fan Controller"* (Hackster.io, 2021).  
  Artigo e projeto de referência sobre curvas térmicas dinâmicas, filtragem de pulsos de tacômetro e modos failsafe com ATmega328P.  
  [https://www.hackster.io/pnjorge/silent-running-with-this-dual-fan-controller-0accb8](https://www.hackster.io/pnjorge/silent-running-with-this-dual-fan-controller-0accb8)
- **pnjorge:** *Cooler-Fan-Controller Hardware & Firmware Repository* (GitHub).  
  [https://github.com/pnjorge/Cooler-Fan-Controller](https://github.com/pnjorge/Cooler-Fan-Controller)

### 2. Componentes de Hardware & Datasheets Oficiais
- **Texas Instruments LM317 3-Terminal Adjustable Regulator:**  
  *LM317 3-Terminal Adjustable Regulator* (Datasheet SNVS774P). Circuito padrão de aplicação da página 1 ($1.25\text{V} - 37\text{V}$, $1.5\text{A}$, $R_1 = 240\,\Omega$, $C_1 = 0.1\,\mu\text{F}$, $C_2 = 1.0\,\mu\text{F}$).  
  PDF Oficial: [https://www.ti.com/lit/ds/symlink/lm317.pdf](https://www.ti.com/lit/ds/symlink/lm317.pdf)
- **Texas Instruments / STMicroelectronics / Allegro ULN2003A & ULN7003A:**  
  *Seven Darlington Arrays* (Datasheet SLRS027P). Matriz de transistores Darlington com diodos de supressão indutiva integrados no pino COM.  
  [https://www.ti.com/lit/ds/symlink/uln2003a.pdf](https://www.ti.com/lit/ds/symlink/uln2003a.pdf)
- **Microchip / Atmel ATmega328P-PU:**  
  *8-bit AVR Microcontroller with 32K Bytes In-System Programmable Flash* (Datasheet DS40002061B / Atmel-8271). Registradores de PWM (Timer 1 e 2), interrupções de tacômetro (INT0/PCINT) e USART0 hardware.  
  [https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7810-Automotive-Microcontrollers-ATmega328P_Datasheet.pdf](https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7810-Automotive-Microcontrollers-ATmega328P_Datasheet.pdf)
- **LM2596 Step-Down DC-DC Switching Regulator Module:**  
  Módulo conversor buck chaveado 150 kHz 3A em configuração vertical (upright $4 \times 7$ pinos, passo de 200 mil).
- **Conector Borne KRE 10 Vias 5.08mm (ZB128 14mm):**  
  Terminal block de parafusos para circuito impresso, passo 5.08mm (0.2"), 10 posições, isolação 300V / 16A, altura 14mm.
- **WCH (Jiangsu Qinheng Co.): CH340 USB-to-Serial TTL Converter:**  
  Módulo de 6 pinos (DTR, RXD, TXD, VCC, CTS, GND) com níveis lógicos selecionáveis 5V/3.3V.  
  [https://www.wch-ic.com/products/CH340.html](https://www.wch-ic.com/products/CH340.html)
- **ARCTIC P8 Black (80mm Pressure-optimised Fan):**  
  ARCTIC GmbH — Product Specification Sheet (SKU: ACFAN00147A). 12V DC, 0.14A, 3000 RPM, 3-Pin.  
  [https://www.arctic.de/media/9a/83/08/1697784936/Spec_Sheet_P8_BLACK_EN.pdf](https://www.arctic.de/media/9a/83/08/1697784936/Spec_Sheet_P8_BLACK_EN.pdf)
- **Akasa 90mm Chassis Cooling Fans (92 $\times$ 92 $\times$ 25mm):**  
  Akasa Thermal Solution. Padrão 12V DC (~0.15A–0.20A), 3 pinos.
- **Sullins Connector Solutions — Card Edge Connectors (0.100" Pitch, ETM / EBM Series):**  
  Conector de borda fêmea industrial de 44 posições (passo 2.54 mm, profundidade de contato $0.300'' - 0.330''$ com orelhas de montagem).  
  [https://www.sullinscorp.com/](https://www.sullinscorp.com/)
- **Vector Electronics & Technology — Eurocard & Vectorbord Card-Edge Plugboards:**  
  Placas de prototipagem com conector de borda 44 pinos (Model 3662 series).  
  [https://www.vectorelect.com/](https://www.vectorelect.com/)

### 3. Padrões Industriais & Documentação do Kernel Linux
- **Wikipedia — Edge Connector & Finger Card Standards:**  
  Documentação normativa de dimensões de conectores de borda, chanfros e chavetas mecânicas de polarização.  
  [https://en.wikipedia.org/wiki/Edge_connector](https://en.wikipedia.org/wiki/Edge_connector)
- **Intel Corporation:** *4-Wire Pulse Width Modulation (PWM) Controlled Fans Specification*, Revision 1.3 (September 2005).  
  Especificação de controle PWM, leitura de 2 pulsos por rotação em coletor aberto e pinagem de ventiladores de PC.
- **The Linux Kernel Organization:** *Hardware Monitoring Kernel Subsystem (`hwmon`)*.  
  Interface de drivers de sensores térmicos e controle de ventiladores do Linux (`/sys/class/hwmon/`).  
  [https://docs.kernel.org/hwmon/](https://docs.kernel.org/hwmon/)
- **Linux USB-to-Serial Driver:**  
  Driver nativo in-tree do kernel `drivers/usb/serial/ch341.c`.

---

## 10. Avaliação Detalhada de Custo de Produção (Production Cost Analysis)

Apresentamos a análise quantitativa e qualitativa de custo para produção da **Custom Stripboard Rev 1.1 / Rev 1.1a**, abrangendo a fabricação de circuito impresso (PCB), lista completa de materiais (BOM), montagem, soldagem, controle de qualidade e três cenários de escala.

### 10.1 Custos de Fabricação do PCB (Placa Virgem FR4)

- **Parâmetros Técnicos do PCB:**
  - Dimensões: $88.90\text{ mm} \times 128.27\text{ mm}$ ($3.5'' \times 5.05''$).
  - Camadas: 2 Camadas (Top / Bottom, com roteamento single-sided na camada inferior).
  - Material: FR4 padrão (Tg 130–140°C), espessura $1.60\text{ mm}$, cobre 1 oz ($35\,\mu\text{m}$).
  - Acabamento de Superfície: HASL Lead-Free (ou ENIG / Ouro Químico recomendado para longevidade dos dedos de borda).
  - Borda / Lingueta: Chanfro de inserção a $45^\circ$ (*Gold Finger Chamfering / Beveling*).

| Lote / Quantidade | Custo Fabricações (Ex: JLCPCB / PCBWay) | Frete + Impostos (BR) | Custo Unitário do PCB (USD) | Custo Unitário do PCB (BRL R$) |
| :---: | :---: | :---: | :---: | :---: |
| **Protótipo (5 placas)** | US\$ 4.00 (base) + US\$ 6.00 (chanfro) | US\$ 14.00 | **US\$ 4.80** | **R\$ 28,00** |
| **Pequeno Lote (30 placas)** | US\$ 28.00 + US\$ 10.00 (chanfro) | US\$ 22.00 | **US\$ 2.00** | **R\$ 11,60** |
| **Lote Médio (100 placas)** | US\$ 75.00 + US\$ 15.00 (ENIG/chanfro) | US\$ 35.00 | **US\$ 1.25** | **R\$ 7,25** |

---

### 10.2 Lista Completa de Materiais (Bill of Materials - BOM) por Placa

Todos os componentes são **Through-Hole (THT / DIP)** conforme a diretriz de fabricação:

| Item | Componente / Especificação | Qtd | Preço Unit. (USD) | Preço Unit. (BRL R$) | Custo Total (BRL R$) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **U1** | ATmega328P-PU (DIP-28 Estreito) | 1 | US\$ 2.20 | R\$ 12,80 | R\$ 12,80 |
| **SKT1** | Soquete DIP-28 Estampado / Torneado | 1 | US\$ 0.25 | R\$ 1,50 | R\$ 1,50 |
| **U2** | ULN2003A ou ULN7003A (DIP-16) | 1 | US\$ 0.40 | R\$ 2,30 | R\$ 2,30 |
| **SKT2** | Soquete DIP-16 | 1 | US\$ 0.15 | R\$ 0,90 | R\$ 0,90 |
| **MOD1** | Módulo Conversor USB-Serial TTL CH340 (6 pinos) | 1 | US\$ 1.20 | R\$ 7,00 | R\$ 7,00 |
| **Y1** | Cristal de Quartzo 16.000 MHz HC-49S | 1 | US\$ 0.18 | R\$ 1,00 | R\$ 1,00 |
| **C3, C4** | Capacitores Cerâmicos 22 pF (disco) | 2 | US\$ 0.05 | R\$ 0,30 | R\$ 0,60 |
| **U101, U102** | CI Regulador LM317T (TO-220 Upright) | 2 | US\$ 0.40 | R\$ 2,30 | R\$ 4,60 |
| **VR101, VR102**| Módulos Step-Down LM2596 DC-DC (Upright) | 2 | US\$ 1.30 | R\$ 7,50 | R\$ 15,00 |
| **TB101** | Conector Borne KRE 10 Vias 5.08mm (ZB128 14mm) | 1 | US\$ 1.10 | R\$ 6,40 | R\$ 6,40 |
| **CONN117, 118**| Conector Jack DC Fêmea 2.1 $\times$ 5.5mm THT | 2 | US\$ 0.25 | R\$ 1,45 | R\$ 2,90 |
| **HDR_SANDWICH**| Conectores Barra de Pinos 2.54mm (Macho + Fêmea) | 2 barras | US\$ 0.60 | R\$ 3,50 | R\$ 7,00 |
| **PASSIVOS** | Caps 100nF, 1uF, 100uF + Resistores 1/4W (conjunto) | 1 kit | US\$ 0.70 | R\$ 4,00 | R\$ 4,00 |
| **MECÂNICA** | Parafusos, porcas e espaçadores M3 de nylon/latão | 6 kits | US\$ 0.80 | R\$ 4,60 | R\$ 4,60 |
| **TOTAL BOM** | **Soma dos Componentes Eletrônicos por Unidade** | — | **US\$ 9.58** | **R\$ 55,85** | **R\$ 70,60 (c/ margem)** |

---

### 10.3 Custos de Montagem, Soldagem e Testes Funcionais

- **Tempo Médio de Montagem Manual (Through-Hole):** ~25 a 35 minutos por placa (inserção de componentes, soldagem manual de pinos, corte de terminais e inspeção visual).
- **Gravação de Firmware & Teste Funcional:** ~5 a 7 minutos (gravação via USB `make flash`, validação de leitura de tacômetros, acionamento PWM nos 4 canais e medição das tensões de saída dos reguladores).
- **Custo de Mão de Obra Técnica:**
  - *DIY / Montagem Própria:* R\$ 0,00 (hobby/estudo).
  - *Técnico Especializado (Brasil):* Estimado em R\$ 25,00 a R\$ 40,00 por placa montada e testada.
  - *Montagem Automatizada em Fábrica (SMD + THT seletivo em lote de 100+):* ~US\$ 5.00 a US\$ 8.00 (R\$ 29,00 a R\$ 46,00) por unidade.

---

### 10.4 Comparativo de Custo Total por Unidade nos Três Cenários

*(Considerando taxa de câmbio referencial US\$ 1.00 = R\$ 5,80)*

| Cenário de Produção | Custo PCB Unit. | Custo BOM Unit. | Mão de Obra / Teste | **Custo Unitário Total (BRL)** | **Custo Unitário Total (USD)** |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **1. Protótipo Avulso / DIY (1 a 5 un)** | R\$ 28,00 | R\$ 70,60 | R\$ 0,00 (DIY) | **R\$ 98,60** | **US\$ 17.00** |
| **2. Pequeno Lote Semi-Artesanal (30 un)** | R\$ 11,60 | R\$ 52,00 | R\$ 25,00 (montagem) | **R\$ 88,60** | **US\$ 15.30** |
| **3. Lote Industrial (100+ un)** | R\$ 7,25 | R\$ 42,00 | R\$ 20,00 (lote) | **R\$ 69,25** | **US\$ 11.95** |

### 10.5 Oportunidades de Otimização de Custo (Cost Reduction)

1. **Substituição de Módulos Prontos por Circuitos Discretos:**
   - A substituição dos dois módulos conversores LM2596 comerciais (R\$ 15,00) por CIs conversores chaveados e indutores montados diretamente na placa pode reduzir em até R\$ 8,00 o custo por unidade em lotes acima de 100 peças.
2. **Eliminação de Soquetes DIP:**
   - Em produção seriada final, a soldagem direta do ATmega328P e do ULN2003 economiza R\$ 2,40 por placa e aumenta a imunidade mecânica contra vibração em chassis de alta rotação.
3. **Compra em Carretéis / Fitas (Volume):**
   - Capacitores, resistores e barras de pinos comprados no atacado reduzem o kit de passivos de R\$ 4,00 para menos de R\$ 1,20 por unidade.

---

## 11. License

This project is open-source and licensed under the **GNU Lesser General Public License v3.0 (LGPLv3)**.

- Full License Terms: [LICENSE](file:///home/fred/C/fanControl/LICENSE)
- GNU Lesser General Public License: [COPYING.LESSER](file:///home/fred/C/fanControl/COPYING.LESSER) / [LICENSE.LESSER](file:///home/fred/C/fanControl/LICENSE.LESSER)
- GNU General Public License: [COPYING](file:///home/fred/C/fanControl/COPYING)

You may freely modify, distribute, and integrate this software and hardware design in your own projects under the conditions of the LGPLv3.

