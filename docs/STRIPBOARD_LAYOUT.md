# 100% Through-Hole (THT) Stripboard Assembly Guide
## Bare ATmega328P + Virtual USB (V-USB) + ULN2003A
### Board: Placa Padrão Trilha 33x71 mm (12 Pistas x 27 Furos, 324 Furos)

This guide documents the **all-through-hole (thru-pin / THT / DIP)** hardware design. It integrates directly with a desktop PC motherboard's **internal USB 2.0 9-pin header** using **V-USB** (software-based Low-Speed USB on ATmega328P @ 16MHz) with zero surface-mount parts.

---

## 1. 100% Through-Pin Bill of Materials (BOM)

All components are standard through-hole leaded parts with 2.54 mm (0.1") pitch or standard axial/radial packages:

| Component | Package / Type | Qty | Purpose |
| :--- | :--- | :---: | :--- |
| **BRD1** | Placa Padrão Trilha 33x71 mm (12 tracks x 27 holes) | 1 | Circuit base |
| **U1** | **ATmega328P-PU** (28-pin narrow DIP, 0.3" row spacing) | 1 | Microcontroller running V-USB stack |
| **SKT1** | 28-pin DIP Socket (narrow 0.3") | 1 | Socket for ATmega328P |
| **U2** | **ULN2003A or ULN7003A** (16-pin DIP) | 1 | 7-channel Darlington low-side driver |
| **SKT2** | 16-pin DIP Socket | 1 | Socket for ULN2003A |
| **Y1** | **16.000 MHz Quartz Crystal** (HC-49 through-hole) | 1 | Master clock for V-USB cycle timing |
| **C3, C4** | **22 pF** Ceramic Disc Capacitors (Through-hole) | 2 | Crystal load capacitors to GND |
| **D1, D2** | **3.6V Zener Diodes** (DO-35 axial leaded: 1N5227B or BZX55C3V6) | 2 | Clamp 5V AVR outputs to 3.3V USB logic |
| **R_USB1,2**| **$68\Omega$**, 1/4W Metal/Carbon Film Resistors (Axial) | 2 | USB D+ and D- series impedance match |
| **R_PULL** | **$1.5\text{k}\Omega$**, 1/4W Resistor (Axial) | 1 | Pull-up on USB D- (Signals USB Low-Speed) |
| **R_RST** | **$10\text{k}\Omega$**, 1/4W Resistor (Axial) | 1 | Pull-up for ATmega Pin 1 (/RESET) |
| **R1–R4** | **$10\text{k}\Omega$**, 1/4W Resistors (Axial) | 4 | Pull-ups for Fan Tachometer lines |
| **C1** | **$100\mu\text{F}$ 25V** Electrolytic (Radial through-hole) | 1 | Bulk decoupling on 12V fan power rail |
| **C2, C5** | **$100\text{nF}$** (0.1µF) Ceramic Disc/Monolithic (Radial) | 2 | VCC and AVCC bypass decoupling to GND |
| **J_USB** | **4-pin 2.54mm Male Header** (Through-hole) | 1 | Plugs into internal Motherboard USB cable |
| **J_PWR** | **2-pin 5.08mm Screw Terminal Block** (Through-hole) | 1 | +12V (Yellow) and GND (Black) from PSU |
| **J_FAN** | **3-pin 2.54mm Male Header pins** (Through-hole) | 4 | Fan 1 to Fan 4 headers |
| **WIRE** | 24 AWG Solid Core Hookup Wire | ~1 m | Jumpers on top side |

---

## 2. Through-Hole V-USB Schematic to Motherboard Header

```
 Motherboard USB 2.0                                             ATmega328P-PU
 Internal 9-Pin Header                                           (DIP-28 @ 16MHz)
 ─────────────────────                                           ────────────────
 Pin 1 (+5V) ──────────────────────────────────────────────────► Pin 7 (VCC) & Pin 20 (AVCC)
                                   +5V Rail
                                      │
                                    [1.5kΩ Axial] (Signals Low-Speed USB to host)
                                      │
 Pin 3 (USB D-) ────[ 68Ω Axial ]─────┴────────────────────────► Pin 5 (PD3)
                         │
                   [3.6V Zener] (Cathode to line, Anode to GND)
                         │
 Pin 7 (GND) ────────────┴─────────────────────────────────────► Pin 8 (GND) & Pin 22 (GND)
                         │
                   [3.6V Zener] (Cathode to line, Anode to GND)
                         │
 Pin 5 (USB D+) ────[ 68Ω Axial ]──────────────────────────────► Pin 4 (PD2 / INT0)
```

---

## 3. ATmega328P Pin Mapping for V-USB & Fans

| ATmega328P Pin | Label | Thru-Pin Connection | Function |
| :---: | :---: | :---: | :--- |
| **Pin 1** | PC6 (/RESET) | $10\text{k}\Omega$ resistor to +5V | Hardware Reset |
| **Pin 4** | PD2 (INT0) | Series $68\Omega$ resistor $\rightarrow$ USB D+ & 3.6V Zener | **USB Data Plus (Interrupt)** |
| **Pin 5** | PD3 | Series $68\Omega$ $\rightarrow$ USB D- & $1.5\text{k}\Omega$ pull-up & 3.6V Zener | **USB Data Minus** |
| **Pin 7** | VCC | Connected to +5V (from Motherboard Pin 1) | Logic Power (+5V) |
| **Pin 8** | GND | Connected to Common Ground | Logic Ground |
| **Pin 9** | PB6 (XTAL1) | 16.000 MHz Quartz Crystal + 22pF capacitor to GND | Master Clock |
| **Pin 10**| PB7 (XTAL2) | 16.000 MHz Quartz Crystal + 22pF capacitor to GND | Master Clock |
| **Pin 12**| PD6 (OC0A) | $\rightarrow$ ULN2003A Pin 4 (IN4) | **Fan 4 PWM** |
| **Pin 15**| PB1 (OC1A) | $\rightarrow$ ULN2003A Pin 1 (IN1) | **Fan 1 PWM** |
| **Pin 16**| PB2 (OC1B) | $\rightarrow$ ULN2003A Pin 2 (IN2) | **Fan 2 PWM** |
| **Pin 17**| PB3 (OC2A) | $\rightarrow$ ULN2003A Pin 3 (IN3) | **Fan 3 PWM** |
| **Pin 20**| AVCC | Connected to +5V via $100\text{nF}$ filter cap | Analog VCC |
| **Pin 22**| GND | Connected to Common Ground | Logic Ground |
| **Pin 23**| PC0 (PCINT8) | $\rightarrow$ Fan 1 Tach (Pin 3) with $10\text{k}\Omega$ pull-up | **Fan 1 RPM Sense** |
| **Pin 24**| PC1 (PCINT9) | $\rightarrow$ Fan 2 Tach (Pin 3) with $10\text{k}\Omega$ pull-up | **Fan 2 RPM Sense** |
| **Pin 25**| PC2 (PCINT10)| $\rightarrow$ Fan 3 Tach (Pin 3) with $10\text{k}\Omega$ pull-up | **Fan 3 RPM Sense** |
| **Pin 26**| PC3 (PCINT11)| $\rightarrow$ Fan 4 Tach (Pin 3) with $10\text{k}\Omega$ pull-up | **Fan 4 RPM Sense** |

---

## 4. Stripboard Physical Layout (33x71 mm Grid)

```
Column:   01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 | 16 | 17 18 19 20 21 22 23 24 | 25 26 27
Row A  ───[              GND BUS (PSU GND & USB Pin 7)                   ]────────────
Row B  ───[              +12V RAIL (PSU 12V Yellow & ULN Pin 9 COM)      ]────────────
Row C  ───○ [ ATmega328P Pins 1 to 14 (Top Row) ] ──○ ──[CUT]─○ [ ULN Pins 1 to 8 ] ───○ ──[FAN 1-4]
Row D  ───○ ──(Track cut under IC)──────────────────○ ──[CUT]─○ ────────────────────────○ ──[FAN 1-4]
Row E  ───○ ──(Track cut under IC)──────────────────○ ──[CUT]─○ ────────────────────────○ ──[FAN 1-4]
Row F  ───○ [ ATmega328P Pins 28 to 15 (Bot Row)] ──○ ──[CUT]─○ [ ULN Pins 16 to 9 ] ──○ ──[FAN 1-4]
Row G  ───○ ──[ 16MHz Crystal + 22pF Caps ]─────────○ ───────○ ──(PWM Routing Jumpers)──○ ──[TACH 1-4]
Row H  ───○ ──[ V-USB: 68Ω Resistors & 3.6V Zeners]─○ ───────○ ────────────────────────○ ──[PULL-UPS]
Row I  ───○ ──[ V-USB: 1.5kΩ D- Pull-Up Resistor ]──○ ───────○ ────────────────────────○ ──[PULL-UPS]
Row J  ───○ ──[ J_USB: 4-Pin Header (5V, D-, D+, GND) ]──────○ ────────────────────────○ ──[PULL-UPS]
Row K  ───○ ──[ R_RST 10kΩ & Decoupling Caps ]──────○ ───────○ ────────────────────────○ ──[PULL-UPS]
Row L  ───[              +5V RAIL (Motherboard USB Pin 1 +5V)            ]────────────
```

### Copper Track Cuts:
1. **Column 16 (Tracks C, D, E, F):** Isolates the ATmega328P pin rows from the ULN2003A.
2. **Columns 3 to 14 (Tracks D, E):** Clears the intermediate stripboard tracks directly underneath the ATmega328P socket.
3. **Columns 17 to 24 (Tracks D, E):** Clears the intermediate stripboard tracks directly underneath the ULN2003A socket.

---

## 5. Linux Kernel Driver Integration

The Linux driver is provided in `kernel/fancontrol_hwmon.c`:
1. It binds directly to the V-USB device (`VID: 0x16c0 / PID: 0x05dc`).
2. When the internal USB cable is plugged into the motherboard, Linux automatically detects the device and registers it into the kernel **hwmon** subsystem.
3. Native Linux sysfs entries are created:
   - `/sys/class/hwmon/hwmonX/pwm1` to `pwm4`
   - `/sys/class/hwmon/hwmonX/fan1_input` to `fan4_input`
4. Standard Linux commands work out of the box:
   ```bash
   # Read fan speeds
   sensors
   # Output:
   # custom_fan-usb-0:
   #   fan1: 1450 RPM
   #   fan2: 1420 RPM
   #   fan3: 1800 RPM
   #   fan4: 1460 RPM

   # Manually set fan 1 speed to 60%
   echo 150 | sudo tee /sys/class/hwmon/hwmon2/pwm1
   ```
