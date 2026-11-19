# Stripboard Assembly Guide (33x71 mm, 12 Tracks x 27 Holes)

This document provides the complete **Bill of Materials (BOM)** and exact **Stripboard Layout** (coordinates, track cuts, and jumper wires) to assemble the **ATmega328P + ULN2003A/ULN7003A** 4-channel PC fan controller on a standard single-sided copper stripboard (Placa Padrão 33x71 mm, 324 furos).

---

## 1. Bill of Materials (BOM)

| Item | Description | Qty | Purpose |
| :--- | :--- | :---: | :--- |
| **BRD1** | Placa Padrão Trilha 33x71 mm (12 pistas x 27 furos, pitch 2.54 mm) | 1 | Circuit base board |
| **U1** | Arduino Nano (ATmega328P, 16MHz, USB Mini/Micro/C) | 1 | Microcontroller & USB-UART interface |
| **SKT1** | 15-pin 2.54mm Female Header Sockets (or direct solder) | 2 | Socket for Arduino Nano |
| **U2** | ULN2003A or ULN7003A (DIP-16 package) | 1 | 7-channel Darlington driver |
| **SKT2** | 16-pin DIP IC Socket | 1 | Socket for ULN2003A |
| **R1–R4**| $10\text{k}\Omega$, 1/4W Resistors | 4 | Pull-up resistors for Tachometer inputs |
| **C1** | $100\mu\text{F}$ 25V Electrolytic Capacitor | 1 | Bulk decoupling on 12V fan power rail |
| **C2** | $100\text{nF}$ (0.1µF) Ceramic Capacitor | 1 | High-frequency noise bypass |
| **J_PWR**| 2-pin Screw Terminal Block (5.0 mm or 2.54 mm pitch) | 1 | 12V & GND input from PSU (Molex/SATA) |
| **J_FAN**| 3-pin / 4-pin 2.54mm Male Header pins | 4 | Fan 1, Fan 2, Fan 3, Fan 4 headers |
| **WIRE** | 22–24 AWG Solid Core Hookup Wire | ~1 m | Jumpers on component side |

---

## 2. Stripboard Grid Coordinate System

- **Rows A to L** (12 horizontal copper tracks running from Column 1 to Column 27):
  - Row A = Top track
  - Row L = Bottom track
- **Columns 1 to 27** (Vertical hole positions along each track).

```
        Col 01 02 03 04 05 ... 25 26 27
Row A  ───○──○──○──○──○───────○──○──○─── (Track 1)
Row B  ───○──○──○──○──○───────○──○──○─── (Track 2)
Row C  ───○──○──○──○──○───────○──○──○─── (Track 3)
Row D  ───○──○──○──○──○───────○──○──○─── (Track 4)
Row E  ───○──○──○──○──○───────○──○──○─── (Track 5)
Row F  ───○──○──○──○──○───────○──○──○─── (Track 6)
Row G  ───○──○──○──○──○───────○──○──○─── (Track 7)
Row H  ───○──○──○──○──○───────○──○──○─── (Track 8)
Row I  ───○──○──○──○──○───────○──○──○─── (Track 9)
Row J  ───○──○──○──○──○───────○──○──○─── (Track 10)
Row K  ───○──○──○──○──○───────○──○──○─── (Track 11)
Row L  ───○──○──○──○──○───────○──○──○─── (Track 12)
```

---

## 3. Dedicated Power Buses

- **Row A (Top Track):** **GND Bus** (Common Ground for PSU, Nano GND, ULN Pin 8, and Fan Grounds).
- **Row B (Second Track):** **+12V Rail** (From PSU 12V Yellow wire $\rightarrow$ Fan positive pins and ULN Pin 9 `COM`).
- **Row L (Bottom Track):** **+5V Rail** (From Nano 5V pin $\rightarrow$ Tachometer $10\text{k}\Omega$ pull-up resistors).

---

## 4. Copper Track Cuts (Required Isolations)

> [!IMPORTANT]
> Because stripboard tracks run continuously, you must cut the copper under DIP ICs and between partitioned components.
> **How to cut tracks:** Use a 3.5 mm or 4.0 mm drill bit twisted gently by hand directly over the hole on the copper (bottom) side until the copper ring is neatly broken.

| Cut ID | Coordinate | Track | Purpose |
| :---: | :---: | :---: | :--- |
| **X01** | Column 18, Row D | Track D | Isolates ULN Pin 1 from Pin 16 |
| **X02** | Column 18, Row E | Track E | Isolates ULN Pin 2 from Pin 15 |
| **X03** | Column 18, Row F | Track F | Isolates ULN Pin 3 from Pin 14 |
| **X04** | Column 18, Row G | Track G | Isolates ULN Pin 4 from Pin 13 |
| **X05** | Column 18, Row H | Track H | Isolates ULN Pin 5 from Pin 12 |
| **X06** | Column 18, Row I | Track I | Isolates ULN Pin 6 from Pin 11 |
| **X07** | Column 18, Row J | Track J | Isolates ULN Pin 7 from Pin 10 |
| **X08** | Column 18, Row K | Track K | Isolates ULN Pin 8 from Pin 9 |
| **X09** | Column 15, Row C | Track C | Isolates Nano Left Bank from Right Bank |
| **X10** | Column 15, Row D | Track D | Isolates Nano D12 from ULN Input |
| **X11** | Column 15, Row E | Track E | Isolates Nano D11 from ULN Input |
| **X12** | Column 15, Row F | Track F | Isolates Nano D10 from ULN Input |

---

## 5. Component Layout (Top Side)

### A. Arduino Nano Sockets (Columns 2 to 16)
- **Top Row Header (Pins D13 down to TX):** Positioned along **Row C**, Columns 2 to 16.
- **Bottom Row Header (Pins D12 down to RAW):** Positioned along **Row J**, Columns 2 to 16.
- *Nano USB connector points left towards edge (Column 1) for easy cable access.*

### B. ULN2003A DIP-16 Socket (Columns 19 to 26)
- **Pins 1 to 8 (Inputs + GND):**
  - Pin 1 (IN 1): Row D, Col 19
  - Pin 2 (IN 2): Row E, Col 20
  - Pin 3 (IN 3): Row F, Col 21
  - Pin 4 (IN 4): Row G, Col 22
  - Pin 8 (GND):  Row K, Col 26 (Jumper to Row A Ground)
- **Pins 9 to 16 (COM + Outputs):**
  - Pin 9  (COM): Row K, Col 26 (Opposite side; tied to Row B +12V)
  - Pin 13 (OUT 4): Row G, Col 22
  - Pin 14 (OUT 3): Row F, Col 21
  - Pin 15 (OUT 2): Row E, Col 20
  - Pin 16 (OUT 1): Row D, Col 19

### C. Fan Headers (Columns 24 to 27)
Standard 3-pin headers (Pin 1: Switched GND, Pin 2: +12V, Pin 3: Tachometer):
- **Fan 1:** Col 24, Pins across Rows D (OUT 1), B (+12V), and L (+5V via Pull-up)
- **Fan 2:** Col 25, Pins across Rows E (OUT 2), B (+12V), and L (+5V via Pull-up)
- **Fan 3:** Col 26, Pins across Rows F (OUT 3), B (+12V), and L (+5V via Pull-up)
- **Fan 4:** Col 27, Pins across Rows G (OUT 4), B (+12V), and L (+5V via Pull-up)

### D. Pull-Up Resistors ($10\text{k}\Omega$)
- **R1 (Fan 1 Tach):** Spanning Row L (+5V) to Tach Signal Line
- **R2 (Fan 2 Tach):** Spanning Row L (+5V) to Tach Signal Line
- **R3 (Fan 3 Tach):** Spanning Row L (+5V) to Tach Signal Line
- **R4 (Fan 4 Tach):** Spanning Row L (+5V) to Tach Signal Line

---

## 6. Step-by-Step Soldering Sequence

1. **Mark & Cut Tracks:**
   - On the copper side, locate the 12 cut positions listed in Section 4.
   - Twist the drill bit until the copper track is clearly broken.
   - Use a continuity multimeter to confirm no shorts exist across each cut.
2. **Solder Wire Jumpers First:**
   - Install all flat wire jumpers on the component side before mounting sockets.
   - Connect Ground Bus (Row A) to Nano GND pin.
   - Connect +5V Bus (Row L) to Nano 5V pin.
   - Connect +12V Bus (Row B) to ULN Pin 9 (`COM`).
3. **Solder Resistors and Capacitors:**
   - Install R1–R4 ($10\text{k}\Omega$).
   - Install C2 ($100\text{nF}$) close to Nano 5V/GND.
   - Install C1 ($100\mu\text{F}$) across +12V (Row B) and GND (Row A) with correct electrolytic polarity.
4. **Solder IC Sockets:**
   - Solder the 16-pin socket for U2 and the two 15-pin female headers for the Nano.
5. **Solder Connectors:**
   - Install the 2-pin screw terminal for 12V/GND power input.
   - Install the four 3-pin fan connectors.

---

## 7. Pre-Power Checklist (Bench Test)

Before plugging the board into your PC power supply or connecting fans:

```
[ ] 1. Multimeter in Continuity / Resistance mode.
[ ] 2. Check resistance between +12V (Row B) and GND (Row A). Must be > 100kΩ (no short).
[ ] 3. Check resistance between +5V (Row L) and GND (Row A). Must be > 10kΩ.
[ ] 4. Check ULN Pin 9 (COM) has direct continuity (0Ω) to +12V (Row B).
[ ] 5. Insert Arduino Nano into socket. Connect USB cable to PC.
[ ] 6. Confirm Nano power LED lights up and no components get hot.
[ ] 7. Insert ULN2003A into its socket with Pin 1 notch facing the correct direction.
[ ] 8. Connect 12V bench power or SATA power. Test fan channels using Linux CLI:
       ./fancontrold -p /dev/ttyUSB0 --set 1 200
```
