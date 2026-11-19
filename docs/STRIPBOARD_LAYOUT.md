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
4. **Dedicated CH340 & Decoupling Zone (Rows R21 to R26):**
   - The 6-pin female socket header for the CH340 USB module, the auto-reset DTR coupling capacitor, the 5V logic decoupling capacitor, and the 12V bulk electrolytic capacitor are grouped cleanly along Rows R21 to R26.

---

## 2. Complete Physical Board Matrix (28 Rows $\times$ 12 Columns = 336 Holes)

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
       ═══════════════════════════════════════════════════════════════════════════  [CUT 1] R16/C12
 R16:  (GND)     ────────────────── [ 1-ROW SPACER GAP ] ───────────────────────   ─────
 R17:  (GND)     PWM 1 In ──►   Pin 1 ──► [  ULN2003A  ] ◄── Pin 16 (OUT 1) ──────►(+12V)
 R18:  (GND)     PWM 2 In ──►   Pin 2 ──► [   DIP-16   ] ◄── Pin 15 (OUT 2) ──────►(+12V)
 R19:  (GND)     PWM 3 In ──►   Pin 3 ──► [  Rows 17-24] ◄── Pin 14 (OUT 3) ──────►(+12V)
 R20:  (GND)     PWM 4 In ──►   Pin 4 ──► [   PINS:    ] ◄── Pin 13 (OUT 4) ──────►(+12V)
       ────────────────── [ CH340 & DECOUPLING ZONE: ROWS R21-R26 ] ─────────────
 R21:  (GND)     [CH340 Pin 1: DTR] [CUT 2] [C_DTR 100nF] ──► (ULN Pin 5: Unused) (+12V)
 R22:  (GND)     [CH340 Pin 2: RXD] ───────────────────────► (ULN Pin 6: Unused) (+12V)
 R23:  (GND)     [CH340 Pin 3: TXD] ───────────────────────► (ULN Pin 7: Unused) (+12V)
 R24:  (GND)     [CH340 Pin 4: VCC] [CUT 3] [C2 100nF] ────► (ULN Pin 8: GND)    (+12V)
 R25:  (GND)     [CH340 Pin 5: CTS (NC)] ── [C1 100uF 25V Electrolytic] ────────► (+12V)
 R26:  (GND)     [CH340 Pin 6: GND] ────► [Bridge to C01] ──► (Fans +12V Bus)    (+12V)
                 ───[CUT 4: R27/R28]───                  ───[CUT 5: R27/R28]───
 R27:  (GND)     [F1 SwGND: C02] [F2 SwGND: C04]         [F3 SwGND: C08] [F4 SwGND: C10] (+12V)
 R28:  (GND)     [F1 Tach : C02] [F2 Tach : C04]         [F3 Tach : C08] [F4 Tach : C10] (+12V)
```

---

## 3. Detailed CH340 6-Pin Socket Header & Decoupling Area (Rows R21 to R26)

The 6-pin female socket header (1x6, 2.54 mm pitch) is soldered into **Column C02 across Rows R21 to R26**.

```
                           DETAILED COMPONENT & TRACE CUT MAP
                           Rows R21 to R26 (Columns C01 to C12)

        C01         C02            C03            C04            C05          C06       C07      C12
       (GND)                                                                 (+5V)     (GND)    (+12V)
R21:    │     [CH340 Pin 1: DTR] ──[CUT 2]── [C_DTR 100nF leg 2]                  │         │        │
        │             │                              │                            │         │        │
        │             └── [C_DTR 100nF leg 1]        └── Jumper wire to ATmega    │         │        │
        │                                                Pin 1 (/RESET at R02)    │         │        │
        │                                                                         │         │        │
R22:    │     [CH340 Pin 2: RXD] ─────────────────────── Jumper wire to ATmega    │         │        │
        │                                                Pin 3 (TXD at R04)       │         │        │
        │                                                                         │         │        │
R23:    │     [CH340 Pin 3: TXD] ─────────────────────── Jumper wire to ATmega    │         │        │
        │                                                Pin 2 (RXD at R03)       │         │        │
        │                                                                         │         │        │
R24:    │     [CH340 Pin 4: VCC] ──[CUT 3]── [C2 100nF] ────► [ULN Pin 8: GND] ───┴──► +5V  │        │
        │             │                                               │                     │        │
        │             └── Wire jumper to C06 (+5V Rail)               └── Jumper to C01 GND │        │
        │                                                                                   │        │
R25:    │     [CH340 Pin 5: CTS (NC)]                                                       │        │
        │             (Unconnected / Floating)                                              │        │
        │                                                                                   │        │
R26:    │     [CH340 Pin 6: GND] ── (Solder bridge to C01)                                  │        │
        │             │                                                                     │        │
        │             └── Negative leg of C1 (100uF) ────────────── Positive leg of C1 ─────┴──────►│
        ▼                                                                                            ▼
```

### A. Pin-by-Pin Wiring Schedule for CH340 Header

| Pin # | CH340 Label | Location | Exact Connection & Jumper Routing |
| :---: | :---: | :---: | :--- |
| **Pin 1** | **DTR** | **Row R21, Col C02** | **Auto-Reset Circuit:**<br>• Make **[CUT 2]** between C02 and C03 on Row R21.<br>• Solder **C_DTR ($100\text{nF}$ ceramic)** with leg 1 in C02 and leg 2 in C03.<br>• Run a jumper wire from **Row R21, Col C03** up to **Row R02, Col C03** (ATmega Pin 1 / /RESET). |
| **Pin 2** | **RXD** | **Row R22, Col C02** | **UART Receive (from MCU):**<br>• Row R22 Left Bank (Net 34) is free (ULN Pin 6 is unused).<br>• Run a jumper wire from **Row R22, Col C03** up to **Row R04, Col C04** (ATmega Pin 3 / PD1 / TXD). |
| **Pin 3** | **TXD** | **Row R23, Col C02** | **UART Transmit (to MCU):**<br>• Row R23 Left Bank (Net 35) is free (ULN Pin 7 is unused).<br>• Run a jumper wire from **Row R23, Col C03** up to **Row R03, Col C04** (ATmega Pin 2 / PD0 / RXD). |
| **Pin 4** | **VCC (+5V)** | **Row R24, Col C02** | **USB 5V Power Entry & Decoupling:**<br>• On Row R24, Col C05 holds ULN Pin 8 (GND). To prevent shorting VCC to GND, make **[CUT 3]** between C03 and C04 on Row R24.<br>• Run a jumper wire from **Row R24, Col C02** to **Column C06 (+5V Rail)**.<br>• Solder **C2 ($100\text{nF}$ ceramic)** directly across CUT 3 (leg 1 in C03 = +5V, leg 2 in C04 = GND) for zero-lead-length bypass filtering! |
| **Pin 5** | **CTS** | **Row R25, Col C02** | **Clear to Send:**<br>• Leave unconnected (NC / Floating). |
| **Pin 6** | **GND** | **Row R26, Col C02** | **Logic & Signal Ground:**<br>• Connect via a short solder bridge or 1-hole jumper from **Row R26, Col C02** directly to **Column C01 (GND Bus)**. |

---

### B. Decoupling Capacitors in this Area

1. **C_DTR ($100\text{nF}$ Ceramic Disc / Monolithic):**
   - **Location:** Row R21 across **[CUT 2]** (Hole C02 to Hole C03).
   - **Role:** Differentiates the DTR level drop from Linux into a sharp 1ms negative spike to reset the ATmega328P automatically before serial code flashing.
2. **C2 ($100\text{nF}$ Ceramic Bypass Capacitor):**
   - **Location:** Row R24 across **[CUT 3]** (Hole C03 to Hole C04).
   - **Role:** High-frequency noise suppression right at the USB +5V power input.
3. **C1 ($100\mu\text{F}$ 25V Electrolytic Bulk Capacitor):**
   - **Location:** Row R25 / R26.
   - **Positive (+) lead:** Inserted into **Row R25, Column C12 (+12V Rail)**.
   - **Negative (-) lead:** Inserted into **Row R25, Column C07 (GND)** or Column C01 (GND).
   - **Role:** Stabilizes the +12V power rail and absorbs inductive voltage dips/spikes when all 4 cooling fans start up or switch duty cycles.

---

## 4. Track Cuts in the CH340 Area

| Cut ID | Coordinate | Method | Purpose |
| :---: | :---: | :---: | :--- |
| **[CUT 2]** | **Row R21 (between C02 and C03)** | Twist 3mm drill bit on copper side | Isolates CH340 DTR pin so $100\text{nF}$ AC capacitor C_DTR can be inserted in-line. |
| **[CUT 3]** | **Row R24 (between C03 and C04)** | Twist 3mm drill bit on copper side | Isolates CH340 VCC (+5V in C02/C03) from ULN Pin 8 (GND in C04/C05). C2 bypass cap mounts directly across this cut! |

---

## 5. Summary of All Track Cuts on the Entire Board

Only **7 tiny track cuts** across the whole 336-hole board:
1. **Cut 1 (Rail Split):** Row **R16, Column C12** (Separates Upper +5V Logic from Lower +12V Fan Power).
2. **Cut 2 (DTR Isolation):** Row **R21, between C02 and C03** (For in-line DTR auto-reset capacitor).
3. **Cut 3 (VCC/GND Split):** Row **R24, between C03 and C04** (Separates CH340 5V from ULN GND; mounts C2 bypass cap).
4. **Cut 4 (Fan 1 Pin Split):** Column **C02, between R27 and R28** (Separates Fan 1 GND from Tach).
5. **Cut 5 (Fan 2 Pin Split):** Column **C04, between R27 and R28** (Separates Fan 2 GND from Tach).
6. **Cut 6 (Fan 3 Pin Split):** Column **C08, between R27 and R28** (Separates Fan 3 GND from Tach).
7. **Cut 7 (Fan 4 Pin Split):** Column **C10, between R27 and R28** (Separates Fan 4 GND from Tach).
