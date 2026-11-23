# Contributing to Custom PC Fan Controller

Thank you for your interest in contributing to the **Custom PC Fan Controller** project! We welcome code contributions, bug reports, feature suggestions, documentation enhancements, and PCB layout improvements.

---

## Code of Conduct

Please treat all community members and contributors with respect, courtesy, and professional consideration.

---

## How to Contribute

### 1. Reporting Bugs
- Before submitting a new issue, search the [existing issues](../../issues) to see if the bug has already been reported.
- When opening an issue, please use the provided **Bug Report** template and include:
  - Your Linux distribution, kernel version (`uname -r`), and hardware specs.
  - Motherboard internal USB header connection details (CH340 / USB port).
  - Exact error messages, dmesg output (`dmesg | grep -i ch34`), or daemon log output.
  - Steps to reliably reproduce the problem.

### 2. Suggesting Enhancements
- Feature requests are tracked via GitHub Issues using the **Feature Request** template.
- Please explain the engineering motivation, circuit impact, and expected benefits.

### 3. Pull Requests (PRs)
- Fork the repository and create a feature branch (`git checkout -b feature/my-new-feature`).
- Follow the project's coding and layout standards (see below).
- Verify that both the firmware and daemon compile cleanly with **zero warnings**:
  ```bash
  make clean && make
  ```
- If modifying Lepton-EDA schematics or PCB layouts, run:
  ```bash
  python3 lepton/layout_stripboards.py
  ```
- Commit your changes with clear, descriptive commit messages.
- Open a Pull Request referencing any related issues.

---

## Coding & Hardware Design Standards

### AVR Microcontroller Firmware (`firmware/`)
- Pure C conforming to `gnu99`.
- Target: ATmega328P @ 16.000 MHz.
- Keep interrupt service routines (ISRs) minimal and non-blocking.
- Maintain failsafe watchdog safety mechanisms at all times.

### Linux Host Daemon (`daemon/`)
- Modern, portable C conforming to `c11`.
- Follow Linux kernel coding style (K&R indentation, 4 or 8 spaces).
- Strictly non-root / unprivileged execution where possible (via udev rules).

### EDA & Hardware Layout (`lepton/`)
- Schematics created in **Lepton-EDA** (`lepton-schematic`).
- PCB layout generated or edited in **`pcb-rnd`**.
- **Through-Hole Priority**: Through-hole (THT) with plated drills is the default standard for all board components. All pad diameters must be $\ge 80\text{ mil}$ ($2.032\text{ mm}$).
- **Single-Sided Copper**: All traces must reside on the bottom layer (`Layer 6 "bottom"`).

---

## License

By contributing to this repository, you agree that your contributions will be licensed under the **GNU Lesser General Public License v3.0 (LGPLv3)**.
