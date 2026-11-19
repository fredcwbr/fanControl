# Stripboard Physical Matrix & Coordinate System
## Based on `custoStripBoard.ods` (33x71 mm Breadboard-Style Protoboard)
### Configuration: Locked-in Option A (Bottom Edge Fan Bank) + R16/C12 Trace Cut

---

## 1. Key Architectural Decisions

1. **The R16 / C12 Copper Trace Cut:**
   - A single clean cut on **Column C12 at Row R16** separates the rail into two independent voltage zones:
     - **Upper C12 (Rows R02 to R15):** Connected to **+5V Logic** (from CH340 VCC / Motherboard USB).
     - **Lower C12 (Rows R17 to R28):** Connected to **+12V Power** (from PC PSU Molex/SATA Yellow wire).
2. **Direct Horizontal Tachometer Pull-Ups:**
   - Because Upper C12 is energized with +5V, the four $10\text{k}\Omega$ pull-up resistors (**R1 to R4**) mount horizontally across **Columns C11 and C12** directly adjacent to ATmega Port C pins (Rows R04 to R07). **Zero crossover jumper wires are needed for pull-ups!**
3. **Locked-in Option A (Bottom Edge Fan Bank):**
   - All 4 fan connectors are grouped at the **bottom edge of the board (Rows R26 to R28)**.
   - All fan cables exit toward the bottom of the PC chassis for clean, unified cable management.

---

## 2. Physical Board Matrix Diagram (28 Rows $\times$ 12 Columns = 336 Holes)

```
        C01       C02  C03  C04  C05      C06    C07      C08  C09  C10  C11       C12
       (GND)     (--- LEFT BANK ---)     (+5V)  (GND)    (--- RIGHT BANK ---)     (RAIL)
 R01:  ─────────────────── [ NET 1: TOP AUXILIARY RAIL ] ───────────────────────  ─────
 R02:  (GND)     CH340 DTR-Cap  Pin 1 ──► [ ATmega328P ] ◄── Pin 28                (+5V )
 R03:  (GND)     CH340 TXD  ──► Pin 2 ──► [    DIP-28  ] ◄── Pin 27                (+5V )
 R04:  (GND)     CH340 RXD  ◄── Pin 3 ──► [  Rows 2-15 ] ◄── Pin 26 ──[10kΩ R4]──► (+5V )
 R05:  (GND)     Fan 1 Tach ──► Pin 4 ──► [            ] ◄── Pin 25 ──[10kΩ R3]──► (+5V )
 R06:  (GND)     Fan 4 PWM  ──► Pin 5 ──► [   PINS:    ] ◄── Pin 24 ──[10kΩ R2]──► (+5V )
 R07:  (GND)                    Pin 6 ──► [ Left: 1-14 ] ◄── Pin 23 ──[10kΩ R1]──► (+5V )
 R08:  (GND)     Bridge to +5V  Pin 7 ──► [   (in C05) ] ◄── Pin 22 (Bridge to GND)(+5V )
 R09:  (GND)     Bridge to GND  Pin 8 ──► [            ] ◄── Pin 21 (AREF 100nF)   (+5V )
 R10:  (GND)     22pF to GND ── Pin 9 ──► [ Right:28-15] ◄── Pin 20 (AVCC to +5V)  (+5V )
 R11:  (GND)     22pF to GND ── Pin 10──► [   (in C08) ] ◄── Pin 19                (+5V )
 R12:  (GND)                    Pin 11──► [            ] ◄── Pin 18                (+5V )
 R13:  (GND)                    Pin 12──► [            ] ◄── Pin 17 (Fan 3 PWM Out)(+5V )
 R14:  (GND)                    Pin 13──► [            ] ◄── Pin 16 (Fan 2 PWM Out)(+5V )
 R15:  (GND)                    Pin 14──► [            ] ◄── Pin 15 (Fan 1 PWM Out)(+5V )
       ═══════════════════════════════════════════════════════════════════════════  [CUT] R16/C12
 R16:  (GND)     ────────────────── [ 1-ROW SPACER GAP ] ───────────────────────   ─────
 R17:  (GND)     PWM 1 In ──►   Pin 1 ──► [  ULN2003A  ] ◄── Pin 16 (OUT 1) ──────►(+12V)
 R18:  (GND)     PWM 2 In ──►   Pin 2 ──► [   DIP-16   ] ◄── Pin 15 (OUT 2) ──────►(+12V)
 R19:  (GND)     PWM 3 In ──►   Pin 3 ──► [  Rows 17-24] ◄── Pin 14 (OUT 3) ──────►(+12V)
 R20:  (GND)     PWM 4 In ──►   Pin 4 ──► [   PINS:    ] ◄── Pin 13 (OUT 4) ──────►(+12V)
 R21:  (GND)                    Pin 5 ──► [ Left: 1-8  ] ◄── Pin 12                (+12V)
 R22:  (GND)                    Pin 6 ──► [   (in C05) ] ◄── Pin 11                (+12V)
 R23:  (GND)                    Pin 7 ──► [ Right:16-9 ] ◄── Pin 10                (+12V)
 R24:  (GND)     Jumper to GND  Pin 8 ──► [   (in C08) ] ◄── Pin 9 (COM) ─────────►(+12V)
 R25:  (GND)     ── [ CH340 6-Pin Socket Header & Decoupling Area ] ─────────────  (+12V)
 R26:  (GND)     [ FAN 1 & 2 +12V Bus (Net 38) ]         [ FAN 3 & 4 +12V Bus (Net 63) ] (+12V)
                 ───[CUT R27/R28]───                     ───[CUT R27/R28]───
 R27:  (GND)     [F1 SwGND: C02] [F2 SwGND: C04]         [F3 SwGND: C08] [F4 SwGND: C10] (+12V)
 R28:  (GND)     [F1 Tach : C02] [F2 Tach : C04]         [F3 Tach : C08] [F4 Tach : C10] (+12V)
```

---

## 3. Bottom Edge Fan Connector Bank (Detailed Pinout)

Each standard 3-pin PC fan connector has:
- **Pin 1:** Switched Ground (Black wire)
- **Pin 2:** +12V Power (Red/Yellow wire)
- **Pin 3:** Tachometer / RPM Pulse (Yellow/Green wire)

By making four tiny 1 mm track cuts between **Row R27 and Row R28** (under C02, C04, C08, C10), the 4 fan headers mount as standard 3-pin vertical headers:

### Left Bank (Fans 1 & 2):
```
        Column C02 (Fan 1 Header)           Column C04 (Fan 2 Header)
       ┌─────────────────────────┐         ┌─────────────────────────┐
 R26:  │ Pin 2: +12V Power Bus   │   R26:  │ Pin 2: +12V Power Bus   │  (Jumper to Lower C12)
 R27:  │ Pin 1: Switched GND 1   │   R27:  │ Pin 1: Switched GND 2   │  (From ULN OUT 1 & OUT 2)
 R28:  │ Pin 3: Tachometer 1     │   R28:  │ Pin 3: Tachometer 2     │  (To ATmega PC0 & PC1)
       └─────────────────────────┘         └─────────────────────────┘
```

### Right Bank (Fans 3 & 4):
```
        Column C08 (Fan 3 Header)           Column C10 (Fan 4 Header)
       ┌─────────────────────────┐         ┌─────────────────────────┐
 R26:  │ Pin 2: +12V Power Bus   │   R26:  │ Pin 2: +12V Power Bus   │  (Jumper to Lower C12)
 R27:  │ Pin 1: Switched GND 3   │   R27:  │ Pin 1: Switched GND 4   │  (From ULN OUT 3 & OUT 4)
 R28:  │ Pin 3: Tachometer 3     │   R28:  │ Pin 3: Tachometer 4     │  (To ATmega PC2 & PC3)
       └─────────────────────────┘         └─────────────────────────┘
```

---

## 4. Signal Interconnect Schedule

| Fan | Pin 1 (Switched GND) | Pin 2 (+12V Power) | Pin 3 (Tachometer) | Pull-Up Resistor ($10\text{k}\Omega$) |
| :---: | :---: | :---: | :---: | :---: |
| **Fan 1** | Row R27, Col C02 $\leftarrow$ Jumper from ULN Pin 16 (R17, C09) | Row R26, Col C02 $\leftarrow$ Jumper to Lower C12 (+12V) | Row R28, Col C02 $\rightarrow$ Wire to ATmega Pin 23 (R07, C09) | Row R07: Spans C11 to Upper C12 (+5V) |
| **Fan 2** | Row R27, Col C04 $\leftarrow$ Jumper from ULN Pin 15 (R18, C09) | Row R26, Col C04 $\leftarrow$ Jumper to Lower C12 (+12V) | Row R28, Col C04 $\rightarrow$ Wire to ATmega Pin 24 (R06, C09) | Row R06: Spans C11 to Upper C12 (+5V) |
| **Fan 3** | Row R27, Col C08 $\leftarrow$ Jumper from ULN Pin 14 (R19, C09) | Row R26, Col C08 $\leftarrow$ Jumper to Lower C12 (+12V) | Row R28, Col C08 $\rightarrow$ Wire to ATmega Pin 25 (R05, C09) | Row R05: Spans C11 to Upper C12 (+5V) |
| **Fan 4** | Row R27, Col C10 $\leftarrow$ Jumper from ULN Pin 13 (R20, C09) | Row R26, Col C10 $\leftarrow$ Jumper to Lower C12 (+12V) | Row R28, Col C10 $\rightarrow$ Wire to ATmega Pin 26 (R04, C09) | Row R04: Spans C11 to Upper C12 (+5V) |

---

## 5. Track Cuts Checklist (Summary)

Only **5 easy track cuts** in total on the entire board:
1. **[CRITICAL] Cut 1:** Row **R16, Column C12** (Separates Upper +5V Logic from Lower +12V Fan Power).
2. **Cut 2:** Between Row R27 and R28 under Column C02 (Isolates Fan 1 Pin 1 from Pin 3).
3. **Cut 3:** Between Row R27 and R28 under Column C04 (Isolates Fan 2 Pin 1 from Pin 3).
4. **Cut 4:** Between Row R27 and R28 under Column C08 (Isolates Fan 3 Pin 1 from Pin 3).
5. **Cut 5:** Between Row R27 and R28 under Column C10 (Isolates Fan 4 Pin 1 from Pin 3).

*(No track cuts under the ATmega328P or ULN2003A sockets!)*
