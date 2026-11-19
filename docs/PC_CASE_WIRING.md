# Custom PC Fan Controller - Case Integration & Hardware Guide

This guide details how to build and mount the custom **ATmega328P + ULN2003A/ULN7003A** fan controller inside a desktop PC case and control it from Linux.

---

## 1. System Architecture

```mermaid
flowchart TD
    subgraph PC_MOTHERBOARD ["PC Motherboard & OS"]
        LINUX["Linux Host OS\n(hwmon / sysfs)"] -->|"Reads CPU/GPU Temp"| DAEMON["fancontrold Service"]
        DAEMON -->|"Serial Protocol (115200)"| USB_PORT["Motherboard Internal USB 2.0 Header\n(9-Pin Header)"]
    end

    subgraph POWER ["PC Power Supply (PSU)"]
        SATA_MOLEX["SATA / Molex Power Connector"]
        SATA_MOLEX -->|"+12V Rail (Yellow)"| FANS_PWR["Fan 12V Positive Pins"]
        SATA_MOLEX -->|"+12V Rail (Yellow)"| ULN_COM["ULN2003A Pin 9 (COM Clamp)"]
        SATA_MOLEX -->|"GND (Black)"| COMMON_GND["Common Ground"]
    end

    subgraph CONTROLLER ["Custom Controller Board (ATmega328P)"]
        USB_PORT -->|"D+, D-, 5V, GND"| MCU["ATmega328P (16MHz)"]
        MCU -->|"D9 (OC1A)"| ULN_IN1["ULN IN 1 (Pin 1)"]
        MCU -->|"D10 (OC1B)"| ULN_IN2["ULN IN 2 (Pin 2)"]
        MCU -->|"D11 (OC2A)"| ULN_IN3["ULN IN 3 (Pin 3)"]
        MCU -->|"D3 (OC2B)"| ULN_IN4["ULN IN 4 (Pin 4)"]
        
        MCU -->|"D2 (INT0)"| TACH1["Tachometer 1 Input"]
        MCU -->|"D4 (PCINT)"| TACH2["Tachometer 2 Input"]
        MCU -->|"D5 (PCINT)"| TACH3["Tachometer 3 Input"]
        MCU -->|"D6 (PCINT)"| TACH4["Tachometer 4 Input"]
    end

    subgraph DRIVER ["ULN2003A / ULN7003A Darlington Array"]
        ULN_IN1 --> ULN_OUT1["OUT 1 (Pin 16)"]
        ULN_IN2 --> ULN_OUT2["OUT 2 (Pin 15)"]
        ULN_IN3 --> ULN_OUT3["OUT 3 (Pin 14)"]
        ULN_IN4 --> ULN_OUT4["OUT 4 (Pin 13)"]
    end

    subgraph FANS ["PC Case Cooling Fans"]
        ULN_OUT1 -->|"Switched Ground"| FAN1["Akasa 90mm #1"]
        ULN_OUT2 -->|"Switched Ground"| FAN2["Akasa 90mm #2"]
        ULN_OUT3 -->|"Switched Ground"| FAN3["Akasa 90mm #3 / Arctic P8"]
        ULN_OUT4 -->|"Switched Ground"| FAN4["Akasa 90mm #4"]

        FAN1 -.->|"RPM Pulse (Yellow)"| TACH1
        FAN2 -.->|"RPM Pulse (Yellow)"| TACH2
    end
```

---

## 2. PC Case Connections

### A. Power Supply (Internal SATA / Molex)
Never power multiple 12V cooling fans from the motherboard 5V USB rail! Use an internal Molex (4-pin) or SATA power plug:
- **Yellow Wire**: `+12V DC` (Supplies power to all fans and `COM` Pin 9 of ULN).
- **Black Wires**: `GND` (Tie to ULN Pin 8 and ATmega328P Ground).
- **Red Wire**: `+5V DC` (Optional: can power ATmega328P VIN/5V, or let USB power the MCU).

### B. Motherboard Internal USB 2.0 Header (9-pin)
Most PC motherboards have 1 or 2 internal 9-pin USB 2.0 headers:
```
       Pin 1 (+5V)    [●] [●]  Pin 2 (+5V)
       Pin 3 (Data -) [●] [●]  Pin 4 (Data -)
       Pin 5 (Data +) [●] [●]  Pin 6 (Data +)
       Pin 7 (GND)    [●] [●]  Pin 8 (GND)
       Pin 9 (Key/NC) [ ] [●]  Pin 10 (NC / Shield)
                       Port 1   Port 2
```
To connect the ATmega328P (or Arduino Nano USB):
- Motherboard **Pin 1 (+5V)**  → USB VBUS (Red)
- Motherboard **Pin 3 (D-)**   → USB D- (White)
- Motherboard **Pin 5 (D+)**   → USB D+ (Green)
- Motherboard **Pin 7 (GND)**  → USB GND (Black)

---

## 3. ULN2003A / ULN7003A Pinout & Fan Wiring

```
                    ULN2003A / ULN7003A
                    ┌───────∪───────┐
  ATmega D9  ──> 1 ─┤ 1B        1C ├─ 16 ──> Fan 1 Negative (-)
  ATmega D10 ──> 2 ─┤ 2B        2C ├─ 15 ──> Fan 2 Negative (-)
  ATmega D11 ──> 3 ─┤ 3B        3C ├─ 14 ──> Fan 3 Negative (-)
  ATmega D3  ──> 4 ─┤ 4B        4C ├─ 13 ──> Fan 4 Negative (-)
                 5 ─┤ 5B        5C ├─ 12
                 6 ─┤ 6B        6C ├─ 11
                 7 ─┤ 7B        7C ├─ 10
  Common GND ──> 8 ─┤ GND      COM ├─ 9  ──> +12V Rail (CRITICAL)
                    └───────────────┘
```

> [!CAUTION]
> **Pin 9 (COM) must be connected to the +12V power rail!**
> Fans are inductive loads. When the Darlington transistors turn off, inductive flyback voltage can easily exceed 60V, which will destroy unprotected transistors. Pin 9 routes these spikes safely through the ULN's built-in clamp diodes back into the 12V rail.

### 3-Pin Fan Connector Pinout (Akasa / Arctic P8):
1. **Black (Pin 1 - GND)**: Connects to ULN Output (Pin 16, 15, 14, or 13).
2. **Red (Pin 2 - +12V)**: Connects directly to the PSU +12V rail (Yellow).
3. **Yellow (Pin 3 - Sense/Tach)**: Connects to ATmega tachometer pin (D2, D4, D5, D6) with a $10\text{k}\Omega$ pull-up resistor to 5V.

---

## 4. Hardware Watchdog & Fail-Safe

In an internal PC cooling setup, thermal safety is vital:
- The firmware contains an active **5-second heartbeat watchdog**.
- If the Linux host freezes, crashes, or the USB connection drops, the ATmega automatically sets all fans to **70% duty cycle (180/255)** after 5 seconds of silence.
- As soon as the Linux daemon resumes communication, smooth curve control automatically recovers.

---

## 5. Linux Installation & Systemd Service

1. **Install udev rule:**
   ```bash
   sudo cp daemon/99-fancontrol.rules /etc/udev/rules.d/
   sudo udevadm control --reload-rules && sudo udevadm trigger
   # Verifies device is now accessible at /dev/fancontrol
   ls -la /dev/fancontrol
   ```

2. **Build and install daemon:**
   ```bash
   cd daemon
   make
   sudo make install
   ```

3. **Start and enable systemd service:**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable --now fancontrol.service
   sudo systemctl status fancontrol.service
   ```
