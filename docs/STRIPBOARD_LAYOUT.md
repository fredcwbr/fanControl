# 100% Through-Hole Stripboard Assembly Guide
## Bare ATmega328P + CH340 6-Pin Serial Module + ULN2003A
### Board: Placa Padrão Trilha 33x71 mm (12 Pistas x 27 Furos, 324 Furos)

This guide documents the complete **through-pin (THT/DIP)** hardware build integrating:
- Bare **ATmega328P-PU (DIP-28)** with a **16.000 MHz** quartz crystal.
- **CH340 6-Pin USB-Serial TTL Converter Module** connecting to the motherboard internal USB header.
- **ULN2003A / ULN7003A (DIP-16)** 7-channel Darlington low-side fan driver.
- 4x Case Fan headers with tachometer RPM monitoring.

---

## 1. Bill of Materials (BOM)

| Item | Component | Qty | Description / Role |
| :--- | :--- | :---: | :--- |
| **BRD1** | Placa Padrão Trilha 33x71 mm (12 tracks x 27 holes) | 1 | Circuit base board |
| **U1** | **ATmega328P-PU** (28-pin narrow DIP, 0.3" row spacing) | 1 | Microcontroller |
| **SKT1** | 28-pin DIP Socket (narrow 0.3") | 1 | Socket for ATmega328P |
| **U2** | **ULN2003A or ULN7003A** (16-pin DIP) | 1 | Darlington low-side ground switch |
| **SKT2** | 16-pin DIP Socket | 1 | Socket for ULN2003A |
| **MOD1** | **CH340 6-Pin USB-to-TTL Serial Module** | 1 | Connects to PC Motherboard internal USB port |
| **HDR_CH340**| **6-pin 2.54mm Female (or Male) Socket Header** | 1 | Plugs into the CH340 module |
| **Y1** | **16.000 MHz Quartz Crystal** (HC-49 through-hole) | 1 | Master clock for ATmega328P |
| **C3, C4** | **22 pF** Ceramic Disc Capacitors (Through-hole) | 2 | Crystal load capacitors to GND |
| **C_DTR** | **100 nF** (0.1µF) Ceramic Capacitor | 1 | In-line AC coupling for DTR auto-reset |
| **R_RST** | **$10\text{k}\Omega$**, 1/4W Resistor | 1 | Pull-up on ATmega Pin 1 (/RESET) to +5V |
| **R1–R4** | **$10\text{k}\Omega$**, 1/4W Resistors | 4 | Pull-ups for Fan Tachometer lines (to +5V) |
| **C1** | **$100\mu\text{F}$ 25V** Electrolytic Capacitor (Radial) | 1 | 12V rail bulk filtering |
| **C2, C5** | **$100\text{nF}$** (0.1µF) Ceramic Capacitors | 2 | VCC/GND and AVCC/GND bypass decoupling |
| **J_PWR** | **2-pin 5.08mm Screw Terminal Block** | 1 | +12V (Yellow) and GND (Black) from PC PSU |
| **J_FAN** | **3-pin 2.54mm Male Header pins** | 4 | Fan 1 to Fan 4 headers |
| **WIRE** | 24 AWG Solid Core Hookup Wire | ~1 m | Jumpers on component side |

---

## 2. CH340 6-Pin Converter Interconnect

The 6-pin CH340 module connects the PC Motherboard USB to the ATmega328P hardware UART (`USART0`):

```
 PC Motherboard USB 2.0                 CH340 6-Pin Module                Stripboard / ATmega328P
 Internal 9-Pin Header                  (USB-Serial Bridge)               (DIP-28 @ 16 MHz)
 ──────────────────────                 ───────────────────               ───────────────────────
 Pin 1 (+5V) ──────────────────────────► USB VBUS
 Pin 3 (Data -)────────────────────────► USB D-
 Pin 5 (Data +)────────────────────────► USB D+
 Pin 7 (GND) ──────────────────────────► USB GND
                                        [ DTR ] ──────[ 100nF Cap ]─────► Pin 1 (PC6 / /RESET)
                                        [ RXD ] ◄──────────────────────── Pin 3 (PD1 / TXD)
                                        [ TXD ] ────────────────────────► Pin 2 (PD0 / RXD)
                                        [ VCC ] ────────────────────────► +5V Rail (Pins 7 & 20)
                                        [ CTS ] ── (NC)
                                        [ GND ] ────────────────────────► GND Rail (Pins 8 & 22)
```

> [!TIP]
> **Automatic Reset on Upload:**
> The `100 nF` capacitor between the CH340 **DTR** pin and ATmega **Pin 1 (/RESET)** produces a sharp low pulse when Linux opens the serial port. This enables 1-click flashing with `avrdude` directly over USB without pressing any manual buttons!

---

## 3. ATmega328P DIP-28 Complete Pinout

```
                         ATmega328P-PU
                         ┌───────∪───────┐
   CH340 DTR (via 100nF) ─┤  1        28 ├─ PC5 (SCL)
         CH340 TXD ─────►─┤  2 (RXD)  27 ├─ PC4 (SDA)
         CH340 RXD ◄──────┤  3 (TXD)  26 ├─ PC3
       Fan 1 Tach In ─────┤  4 (INT0) 25 ├─ PC2
   Fan 4 PWM ──► (ULN IN4)┤  5 (OC2B) 24 ├─ PC1
       Fan 2 Tach In ─────┤  6 (PD4)  23 ├─ PC0
               +5V VCC ───┤  7        22 ├─ GND
               GND Bus ───┤  8        21 ├─ AREF (100nF to GND)
        16MHz Crystal ────┤  9 (PB6)  20 ├─ AVCC (+5V via 100nF)
        16MHz Crystal ────┤ 10 (PB7)  19 ├─ PB5 (SCK)
       Fan 3 Tach In ─────┤ 11 (PD5)  18 ├─ PB4 (MISO)
       Fan 4 Tach In ─────┤ 12 (PD6)  17 ├─ PB3 (OC2A) ──► Fan 3 PWM (ULN IN3)
                          ┤ 13 (PD7)  16 ├─ PB2 (OC1B) ──► Fan 2 PWM (ULN IN2)
                          ┤ 14 (PB0)  15 ├─ PB1 (OC1A) ──► Fan 1 PWM (ULN IN1)
                         └───────────────┘
```

---

## 4. Stripboard Physical Matrix & Coordinate System

- **Board:** 12 copper tracks (**Rows A through L**) $\times$ 27 holes (**Columns 1 through 27**).
- Both DIP sockets are narrow 0.3" (spanning 4 holes across Rows C through F).

```
Column:   01 02 03 04 05 06 | 07 08 09 10 11 12 13 14 15 16 17 18 19 20 | 21 22 23 24 | 25 26 27
Row A  ───[                          GND BUS (Power Supply GND & CH340 GND)                       ]──
Row B  ───[                          +12V RAIL (Power Supply +12V Yellow & ULN Pin 9 COM)          ]──
Row C  ───○ [CH340 Header] ──○ ──○ [ ATmega328P Pins 1 to 14 (Top Row) ] ──[CUT]─○ [ULN Pins 1-8] ──[FANS]
Row D  ───○ [CH340 Header] ──○ ──○ ──(Track cut under ICs)──────────────────[CUT]─○ ───────────────[FANS]
Row E  ───○ [CH340 Header] ──○ ──○ ──(Track cut under ICs)──────────────────[CUT]─○ ───────────────[FANS]
Row F  ───○ [CH340 Header] ──○ ──○ [ ATmega328P Pins 28 to 15 (Bot Row)] ──[CUT]─○ [ULN Pins 16-9]─[FANS]
Row G  ───○ [CH340 Header] ──○ ──○ ──[ 16MHz Crystal Y1 + 22pF Caps ]──────────────(PWM Routing)───[TACH]
Row H  ───○ [CH340 Header] ──○ ──○ ──[ 10k Pull-Up Resistors (R1-R4) ]─────────────────────────────[TACH]
Row I  ───○ ─────────────────○ ──○ ──[ 100nF DTR Capacitor C_DTR ]─────────────────────────────────[TACH]
Row J  ───○ ─────────────────○ ──○ ──[ Reset Resistor R_RST ]──────────────────────────────────────[TACH]
Row K  ───○ ─────────────────○ ──○ ─────────────────────────────────────────────────────────────────[TACH]
Row L  ───[                          +5V RAIL (CH340 VCC & Motherboard 5V)                        ]──
```

### Copper Track Cuts (Bottom Side)
Use a 3.5 mm to 4.0 mm drill bit twisted by hand on the copper tracks:
1. **Column 6 (Tracks C, D, E, F, G, H):** Isolates the 6-pin CH340 header area from the ATmega pins.
2. **Column 20 (Tracks C, D, E, F):** Isolates the ATmega328P pin rows from the ULN2003A.
3. **Columns 8 to 19 (Tracks D, E):** Clears the intermediate stripboard tracks directly underneath the ATmega328P socket.
4. **Columns 21 to 24 (Tracks D, E):** Clears the intermediate stripboard tracks directly underneath the ULN2003A socket.

---

## 5. Wiring Connections

### A. Power Rails
- **Row A:** Connect to PSU Ground (Black wire) and CH340 GND.
- **Row B:** Connect to PSU +12V (Yellow wire), ULN Pin 9 (`COM`), and Fan Pin 2 (+12V).
- **Row L:** Connect to CH340 VCC (+5V), ATmega Pin 7 (`VCC`), ATmega Pin 20 (`AVCC`), and all $10\text{k}\Omega$ pull-up resistors.

### B. 16 MHz Quartz Crystal
- Solder crystal **Y1** across **Pin 9 (PB6)** and **Pin 10 (PB7)**.
- Connect one **22 pF cap (C3)** from Pin 9 to Row A (GND).
- Connect second **22 pF cap (C4)** from Pin 10 to Row A (GND).

### C. PWM Signal Links (ATmega $\rightarrow$ ULN2003A)
- **Fan 1 PWM:** ATmega Pin 15 (PB1/OC1A) $\rightarrow$ ULN Pin 1 (IN1)
- **Fan 2 PWM:** ATmega Pin 16 (PB2/OC1B) $\rightarrow$ ULN Pin 2 (IN2)
- **Fan 3 PWM:** ATmega Pin 17 (PB3/OC2A) $\rightarrow$ ULN Pin 3 (IN3)
- **Fan 4 PWM:** ATmega Pin 5  (PD3/OC2B) $\rightarrow$ ULN Pin 4 (IN4)

### D. ULN2003A to Fans (Low-Side Ground Switching)
- **ULN Pin 8 (GND):** Tied to Row A (GND Bus).
- **ULN Pin 9 (COM):** Tied to Row B (+12V Rail) — **Critical clamp diode protection**.
- **ULN Pin 16 (OUT 1):** $\rightarrow$ Fan 1 Negative (Pin 1)
- **ULN Pin 15 (OUT 2):** $\rightarrow$ Fan 2 Negative (Pin 1)
- **ULN Pin 14 (OUT 3):** $\rightarrow$ Fan 3 Negative (Pin 1)
- **ULN Pin 13 (OUT 4):** $\rightarrow$ Fan 4 Negative (Pin 1)

### E. Tachometer Inputs & $10\text{k}\Omega$ Pull-Ups
- **Fan 1 Tach (Pin 3):** Connects to ATmega Pin 4 (PD2/INT0) + $10\text{k}\Omega$ pull-up to Row L (+5V).
- **Fan 2 Tach (Pin 3):** Connects to ATmega Pin 6 (PD4/PCINT20) + $10\text{k}\Omega$ pull-up to Row L (+5V).
- **Fan 3 Tach (Pin 3):** Connects to ATmega Pin 11 (PD5/PCINT21) + $10\text{k}\Omega$ pull-up to Row L (+5V).
- **Fan 4 Tach (Pin 3):** Connects to ATmega Pin 12 (PD6/PCINT22) + $10\text{k}\Omega$ pull-up to Row L (+5V).

---

## 6. Linux Programming & Operation

With the CH340 module connected, Linux recognizes it immediately with its standard in-tree driver (`ch341.ko`):
```bash
# Check device creation:
ls -la /dev/ttyUSB*
# dmesg output: "ch341-uart converter now attached to ttyUSB0"

# Flash firmware directly with auto-reset over USB:
cd firmware
make flash PORT=/dev/ttyUSB0

# Query controller RPM and status from Linux CLI:
cd ../daemon
./fancontrold -p /dev/ttyUSB0 --status
```
