# Custom PC Fan Controller (Linux Controlled)

A complete hardware, firmware, and software system for integrating custom fan control inside a PC desktop case, powered by an **ATmega328P** + **ULN2003A/ULN7003A** Darlington array driving up to 4 cooling fans (e.g., 4x Akasa 90mm and Arctic P8) and controlled dynamically by a **Linux systemd daemon**.

---

## Architecture Overview

```
 PC Case Interior:
 ┌──────────────────────────────────────────────┐
 │ PC Motherboard                               │
 │  └── Internal USB 2.0 9-pin Header           │
 │        │ (D+, D-, 5V, GND)                   │
 │        ▼                                     │
 │ Custom Controller Board                      │
 │  ├── ATmega328P Microcontroller (16 MHz)     │
 │  │    └── UART, 4x Hardware PWM, 4x Tach     │
 │  │                                           │
 │  ├── ULN2003A / ULN7003A Darlington Driver   │
 │  │    └── Low-side Ground Switching          │
 │  │                                           │
 │  └── Power In from PSU SATA/Molex (+12V, GND)│
 │        │                                     │
 │        ▼                                     │
 │ 4x Fans (Akasa 90mm / Arctic P8)             │
 └──────────────────────────────────────────────┘
```

---

## Directory Structure

- **`firmware/`**: AVR C firmware for ATmega328P.
  - Generates low-side PWM for 3-pin fans or 25kHz for 4-pin fans.
  - Reads fan tachometer RPM using interrupts.
  - Implements a hardware/software 5-second failsafe watchdog (spins fans to 70% if Linux freezes).
  - Serial command parser (115200 baud).
- **`daemon/`**: Linux C service (`fancontrold`) and CLI tool.
  - Reads CPU/GPU temperatures directly from `/sys/class/hwmon`.
  - Calculates dynamic silent fan curves.
  - Transmits PWM speeds over USB serial (`/dev/fancontrol`).
  - Includes `fancontrol.service` (systemd) and `99-fancontrol.rules` (udev).
- **`docs/`**: Hardware integration guide:
  - `docs/PC_CASE_WIRING.md`: Complete pinout, Molex/SATA wiring, internal USB header mapping, and flyback clamp diode protection.

---

## Quick Start

### 1. Build Everything
```bash
make
```

### 2. Flash Firmware to ATmega328P
```bash
cd firmware
make flash PORT=/dev/ttyUSB0
```

### 3. Test Controller from Linux
```bash
# Query available temperature sensors on host
./daemon/fancontrold --list-hwmon

# Check controller status (PWM & RPM)
./daemon/fancontrold -p /dev/ttyUSB0 --status

# Set fan speed manually
./daemon/fancontrold -p /dev/ttyUSB0 --setall 150
```

### 4. Install Linux Service
```bash
cd daemon
sudo make install
sudo systemctl enable --now fancontrol.service
```
