# FanControl

A lightweight, modular C-based fan control utility and daemon for Linux using `sysfs`/`hwmon`.

## Features

- **hwmon Device Discovery**: Detect and inspect available temperature sensors and PWM controllers.
- **Dynamic Fan Curves**: Linear interpolation curve between customizable minimum and maximum temperature thresholds.
- **Fail-safe Operation**: Graceful handling of `SIGINT` / `SIGTERM` with automatic restoration of fan control mode.
- **Configurable**: Simple key-value config file (`fancontrol.conf`).

## Project Layout

```
.
├── include/
│   ├── config.h       # Configuration loading and fan curve calculations
│   ├── fan.h          # PWM read/write and mode switching
│   ├── fancontrol.h   # Core definitions and logging macros
│   └── sensor.h       # Temperature sensor readings and discovery
├── src/
│   ├── config.c
│   ├── fan.c
│   ├── main.c
│   └── sensor.c
├── fancontrol.conf    # Example configuration file
├── Makefile           # Build system
├── README.md
└── .gitignore
```

## Building

```bash
# Compile release build
make

# Compile with AddressSanitizer and debug symbols
make debug

# Clean build artifacts
make clean
```

## Usage

```bash
# Discover detected sensors and fan devices
./fancontrol --discover

# Perform a single temperature and PWM calculation check
./fancontrol --once

# Run continuous control daemon
./fancontrol --config fancontrol.conf
```
