# Stripboard Physical Matrix & Coordinate System
## Based on `custoStripBoard.ods` (33x71 mm Breadboard-Style Protoboard)

This revised guide uses the exact **breadboard-style protoboard copper track matrix** defined in [docs/custoStripBoard.ods](file:///home/fred/C/fanControl/docs/custoStripBoard.ods).

---

## 1. Physical Board Matrix Analysis (28 Rows $\times$ 12 Columns = 336 Holes)

The protoboard has a **solderless breadboard layout** with **4 full-length vertical bus rails** and **two banks of 4-hole horizontal tie-point strips** separated by a standard 0.3" center trough.

```
       C01   C02 C03 C04 C05   C06   C07   C08 C09 C10 C11   C12
R01:  [=================== NET 1: TOP HORIZONTAL RAIL ===================]
R02:  |RAIL| [ Net 14 (4 pts)] |RAIL |RAIL| [ Net 39 (4 pts)] |RAIL|
R03:  | 2  | [ Net 15 (4 pts)] | 4   | 5  | [ Net 40 (4 pts)] | 3  |
...   |    | [     ...       ] |     |    | [     ...       ] |    |
R15:  |GND | [ Net 27 (4 pts)] |+5V  |GND | [ Net 52 (4 pts)] |+12V|
R16:  |BUS | [ Net 28 (4 pts)] |LOGIC|SEC | [ Net 53 (4 pts)] |RAIL|
R17:  |    | [ Net 29 (4 pts)] |RAIL |RAIL| [ Net 54 (4 pts)] |    |
...   |    | [     ...       ] |     |    | [     ...       ] |    |
R26:  |    | [ Net 38 (4 pts)] |     |    | [ Net 63 (4 pts)] |    |
R27:  |    | [N6] [N7] [N8][N9]|     |    |[N10][N11][N12][N13]   |
R28:  |    | [N6] [N7] [N8][N9]|     |    |[N10][N11][N12][N13]   |
```

### Dedicated Continuous Bus Rails:
- **Column C01 (Net 2, 27 holes, R02–R28):** **GND Bus** (Common Ground for PSU, CH340, ATmega, and Fans).
- **Column C06 (Net 4, 27 holes, R02–R28):** **+5V Logic Rail** (Supplied by CH340 VCC / Motherboard USB Pin 1).
- **Column C07 (Net 5, 27 holes, R02–R28):** **Secondary GND / Shield Rail**.
- **Column C12 (Net 3, 27 holes, R02–R28):** **+12V Power Rail** (From PC PSU Yellow wire; powers Fans & ULN Pin 9 `COM`).
- **Row R01 (Net 1, 12 holes, C01–C12):** Top auxiliary bus.

### Horizontal Component Tie-Points:
- **Left Bank (Columns C02, C03, C04, C05):**
  - Rows R02 to R26: 25 individual 4-hole horizontal strips (Nets 14 to 38).
- **Right Bank (Columns C08, C09, C10, C11):**
  - Rows R02 to R26: 25 individual 4-hole horizontal strips (Nets 39 to 63).
- **Center Spacing:**
  - The gap between **C05** and **C08** spans exactly **0.3" (7.62 mm)** across center rails C06 and C07.
  - **Zero Track Cuts Needed!** Narrow DIP ICs (ATmega328P-PU and ULN2003A) straddle C05 and C08 directly with built-in electrical isolation!

---

## 2. Component Placement on the Matrix

```
       C01       C02  C03  C04  C05      C06    C07      C08  C09  C10  C11       C12
      (GND)     (--- LEFT BANK ---)     (+5V)  (GND)    (--- RIGHT BANK ---)     (+12V)
R01:  ─────────────────── [ NET 1: TOP AUXILIARY RAIL ] ──────────────────────
R02:  (GND)     CH340 DTR-Cap  Pin 1 ──► [ ATmega328P ] ◄── Pin 28                (+12V)
R03:  (GND)     CH340 TXD  ──► Pin 2 ──► [    DIP-28  ] ◄── Pin 27                (+12V)
R04:  (GND)     CH340 RXD  ◄── Pin 3 ──► [  Rows 2-15 ] ◄── Pin 26 (Tach 4 In)    (+12V)
R05:  (GND)     (Fan 1 Tach In)Pin 4 ──► [            ] ◄── Pin 25 (Tach 3 In)    (+12V)
R06:  (GND)     (Fan 4 PWM Out)Pin 5 ──► [   PINS:    ] ◄── Pin 24 (Tach 2 In)    (+12V)
R07:  (GND)                    Pin 6 ──► [ Left: 1-14 ] ◄── Pin 23 (Tach 1 In)    (+12V)
R08:  (GND)     Jumper to +5V  Pin 7 ──► [   (in C05) ] ◄── Pin 22 (Jumper to GND)(+12V)
R09:  (GND)     Jumper to GND  Pin 8 ──► [            ] ◄── Pin 21 (AREF 100nF)   (+12V)
R10:  (GND)     22pF Cap ──►   Pin 9 ──► [ Right:28-15] ◄── Pin 20 (AVCC to +5V)  (+12V)
R11:  (GND)     22pF Cap ──►   Pin 10──► [   (in C08) ] ◄── Pin 19                (+12V)
R12:  (GND)                    Pin 11──► [            ] ◄── Pin 18                (+12V)
R13:  (GND)                    Pin 12──► [            ] ◄── Pin 17 (Fan 3 PWM Out)(+12V)
R14:  (GND)                    Pin 13──► [            ] ◄── Pin 16 (Fan 2 PWM Out)(+12V)
R15:  (GND)                    Pin 14──► [            ] ◄── Pin 15 (Fan 1 PWM Out)(+12V)
R16:  (GND)     ────────────────── [ 1-ROW SPACER GAP ] ───────────────────────   (+12V)
R17:  (GND)     PWM 1 In ──►   Pin 1 ──► [  ULN2003A  ] ◄── Pin 16 ──► Fan 1 (-)  (+12V)
R18:  (GND)     PWM 2 In ──►   Pin 2 ──► [   DIP-16   ] ◄── Pin 15 ──► Fan 2 (-)  (+12V)
R19:  (GND)     PWM 3 In ──►   Pin 3 ──► [  Rows 17-24] ◄── Pin 14 ──► Fan 3 (-)  (+12V)
R20:  (GND)     PWM 4 In ──►   Pin 4 ──► [   PINS:    ] ◄── Pin 13 ──► Fan 4 (-)  (+12V)
R21:  (GND)                    Pin 5 ──► [ Left: 1-8  ] ◄── Pin 12                (+12V)
R22:  (GND)                    Pin 6 ──► [   (in C05) ] ◄── Pin 11                (+12V)
R23:  (GND)                    Pin 7 ──► [ Right:16-9 ] ◄── Pin 10                (+12V)
R24:  (GND)     Jumper to GND  Pin 8 ──► [   (in C08) ] ◄── Pin 9  ──► To +12V Rail(+12V)
R25:  (GND)     ── [ CH340 6-Pin Socket Header / Jumper Terminal Area ] ──────    (+12V)
R26:  (GND)     ── [ 10kΩ Tach Pull-ups / Decoupling Capacitors ] ───────────     (+12V)
R27:  (GND)     [Net 6] [Net 7] [Net 8] [Net 9] | | [N10] [N11] [N12] [N13]       (+12V)
R28:  (GND)     [─────── 4x FAN HEADERS ──────] | | [── 12V / GND POWER IN ──]    (+12V)
```

---

## 3. Exact Pin-by-Pin Wiring Schedule

### A. Power Distribution
- **PSU +12V Yellow Wire:** Connects to **C12 (Row R28)**.
- **PSU GND Black Wire:** Connects to **C01 (Row R28)**.
- **CH340 VCC (+5V from USB):** Jumpered to **C06 (+5V Rail)**.
- **CH340 GND:** Jumpered to **C01 (GND Bus)**.
- **Bulk Capacitor C1 ($100\mu\text{F}$ 25V):** Spans across C12 (+12V) and C01 (GND) near R28.
- **Decoupling Capacitor C2 ($100\text{nF}$):** Spans across C06 (+5V) and C07 (GND) near R08.

### B. ATmega328P DIP-28 (Rows R02 to R15)
- **R02, C05 (Pin 1 /RESET):**
  - Resistor $10\text{k}\Omega$ (R_RST) from C04 to C06 (+5V).
  - Ceramic capacitor $100\text{nF}$ (C_DTR) from C03 to CH340 DTR pin.
- **R03, C05 (Pin 2 / RXD):** Connects to CH340 TXD pin via C04.
- **R04, C05 (Pin 3 / TXD):** Connects to CH340 RXD pin via C04.
- **R05, C05 (Pin 4 / INT0):** Fan 1 Tach input from C04.
- **R06, C05 (Pin 5 / OC2B):** Fan 4 PWM output. Jumper wire from C04 down to **R20, C04** (ULN Pin 4).
- **R08, C05 (Pin 7 / VCC):** Short wire jumper from C05 to C06 (+5V rail).
- **R09, C05 (Pin 8 / GND):** Short wire jumper from C05 to C01 (GND rail).
- **R10, C05 (Pin 9 / XTAL1):** 16MHz Crystal lead 1 in C04; 22pF capacitor from C03 to C01 (GND).
- **R11, C05 (Pin 10 / XTAL2):** 16MHz Crystal lead 2 in C04; 22pF capacitor from C03 to C01 (GND).
- **R15, C08 (Pin 15 / OC1A):** Fan 1 PWM output. Jumper wire from C09 down to **R17, C04** (ULN Pin 1).
- **R14, C08 (Pin 16 / OC1B):** Fan 2 PWM output. Jumper wire from C09 down to **R18, C04** (ULN Pin 2).
- **R13, C08 (Pin 17 / OC2A):** Fan 3 PWM output. Jumper wire from C09 down to **R19, C04** (ULN Pin 3).
- **R10, C08 (Pin 20 / AVCC):** Short wire jumper from C08 to C06 (+5V rail).
- **R09, C08 (Pin 21 / AREF):** $100\text{nF}$ capacitor from C09 to C07 (GND).
- **R08, C08 (Pin 22 / GND):** Short wire jumper from C08 to C07 (GND).
- **R07, C08 (Pin 23 / PC0):** Fan 1 Tach input ($10\text{k}\Omega$ pull-up to +5V).
- **R06, C08 (Pin 24 / PC1):** Fan 2 Tach input ($10\text{k}\Omega$ pull-up to +5V).
- **R05, C08 (Pin 25 / PC2):** Fan 3 Tach input ($10\text{k}\Omega$ pull-up to +5V).
- **R04, C08 (Pin 26 / PC3):** Fan 4 Tach input ($10\text{k}\Omega$ pull-up to +5V).

### C. ULN2003A DIP-16 (Rows R17 to R24)
- **R17, C05 (Pin 1 / IN1):** $\leftarrow$ Jumper from ATmega Pin 15 (PWM 1).
- **R17, C08 (Pin 16 / OUT1):** $\rightarrow$ Switched Ground to Fan 1 Pin 1.
- **R18, C05 (Pin 2 / IN2):** $\leftarrow$ Jumper from ATmega Pin 16 (PWM 2).
- **R18, C08 (Pin 15 / OUT2):** $\rightarrow$ Switched Ground to Fan 2 Pin 1.
- **R19, C05 (Pin 3 / IN3):** $\leftarrow$ Jumper from ATmega Pin 17 (PWM 3).
- **R19, C08 (Pin 14 / OUT3):** $\rightarrow$ Switched Ground to Fan 3 Pin 1.
- **R20, C05 (Pin 4 / IN4):** $\leftarrow$ Jumper from ATmega Pin 5 (PWM 4).
- **R20, C08 (Pin 13 / OUT4):** $\rightarrow$ Switched Ground to Fan 4 Pin 1.
- **R24, C05 (Pin 8 / GND):** Wire jumper from C04 to **C01 (GND Bus)**.
- **R24, C08 (Pin 9 / COM):** Wire jumper from C09 to **C12 (+12V Rail)** (Crucial inductive flyback clamp).

---

## 4. Why This Matrix Is Superior
1. **Zero Mechanical Track Cuts:** Because the protoboard has a built-in 0.3" center split (isolated between C05 and C08), both the ATmega328P and ULN2003A sockets drop straight in without needing a drill bit to break tracks!
2. **Dedicated Continuous Power Buses:** The 4 long vertical rails (C01 = GND, C06 = +5V, C07 = GND, C12 = +12V) provide clean, low-impedance power distribution directly adjacent to every IC pin.
3. **Plentiful Component Tie-Points:** 3 free holes per pin (C02–C04 on the left, C09–C11 on the right) allow neat top-side jumper routing, resistor placement, and probe test points.
