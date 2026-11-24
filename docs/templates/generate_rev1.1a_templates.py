#!/usr/bin/env python3
"""
generate_rev1.1a_templates.py
Generates 1:1 Scale Printable Templates and Circuit Assembly Visualizations
for Custom Stripboard Rev 1.1a (Eurocard 88.90 mm x 128.27 mm / 3500 x 5050 mil).

Outputs generated in docs/templates/:
1. circuit_assembly_rev1.1a_top_view.svg & .png (300 DPI)
2. circuit_assembly_rev1.1a_bottom_view.svg & .png (300 DPI)
3. stripboard_rev1.1a_1to1_printout.pdf (A4 1:1 Printable Assembly Sheet)
"""

import os
import math
import subprocess
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

# Board Geometry
BOARD_W_MM = 88.90    # 3500 mil
BOARD_H_MM = 128.27   # 5050 mil
MIL_TO_MM = 0.0254

# Mounting Holes (M3, 3.2mm drill, 6.1mm pad)
MOUNTING_HOLES_MIL = [
    ("MH101", 200.0, 200.0),
    ("MH102", 3300.0, 200.0),
    ("MH103", 200.0, 2000.0),
    ("MH104", 3300.0, 2700.0),
    ("MH105", 200.0, 4600.0),
    ("MH106", 3300.0, 4600.0),
]

# 8 Vertical Power Rails (40 pins each, Y=800 to 4700 mil)
RAILS_MIL = [
    (1, "Rail 1", 500.0, "#999999", "Aux 1"),
    (2, "Rail 2", 600.0, "#999999", "Aux 2"),
    (3, "Rail 3", 700.0, "#999999", "Aux 3"),
    (4, "Rail 4 (GND)", 1700.0, "#333333", "GND"),
    (5, "Rail 5 (+5V)", 1800.0, "#e65100", "+5V"),
    (6, "Rail 6 (+12V)", 2800.0, "#c62828", "+12V"),
    (7, "Rail 7 (+12V)", 2900.0, "#c62828", "+12V"),
    (8, "Rail 8 (GND)", 3000.0, "#333333", "GND"),
]

# Prototyping Rows: 32 rows, Y = 800 to 3900 mil, step 100 mil
ROWS_Y_MIL = [800.0 + i * 100.0 for i in range(32)]
LEFT_COLS_X_MIL = [800.0 + i * 100.0 for i in range(9)]    # 800..1600 mil
RIGHT_COLS_X_MIL = [1900.0 + i * 100.0 for i in range(9)]  # 1900..2700 mil

# Scratch-pad Prototyping Area: 14 rows x 4 cols (X=3100..3400, Y=3000..4300)
SCRATCH_X_MIL = [3100.0, 3200.0, 3300.0, 3400.0]
SCRATCH_Y_MIL = [3000.0 + i * 100.0 for i in range(14)]

def mil2mm(x_mil, y_mil):
    return x_mil * MIL_TO_MM, y_mil * MIL_TO_MM

def generate_circuit_assembly_svg(output_path, mirrored=False):
    """
    Renders the complete top or bottom view SVG of Rev 1.1a Stripboard
    populated with the Fan Controller Circuit.
    """
    margin = 10.0  # mm border padding
    w_total = BOARD_W_MM + 2 * margin
    h_total = BOARD_H_MM + 2 * margin

    def transform(x_mil, y_mil):
        x_mm = x_mil * MIL_TO_MM
        y_mm = y_mil * MIL_TO_MM
        if mirrored:
            x_mm = BOARD_W_MM - x_mm
        return margin + x_mm, margin + y_mm

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w_total}mm" height="{h_total}mm" viewBox="0 0 {w_total} {h_total}">')
    svg.append('<defs>')
    # Drop shadows & gradients
    svg.append('  <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%"><feDropShadow dx="0.4" dy="0.6" stdDeviation="0.4" flood-opacity="0.35"/></filter>')
    svg.append('  <filter id="ic-shadow" x="-10%" y="-5%" width="120%" height="110%"><feDropShadow dx="0.5" dy="0.8" stdDeviation="0.6" flood-opacity="0.45"/></filter>')
    svg.append('</defs>')

    svg.append('<style>')
    svg.append('  text { font-family: "DejaVu Sans", "Helvetica", Arial, sans-serif; text-anchor: middle; dominant-baseline: central; }')
    svg.append('  .board-body { fill: #1c3b2b; stroke: #0d1f16; stroke-width: 0.5; }') # Dark solder-mask green
    svg.append('  .copper-pad { fill: #e5a95d; stroke: #a36d2e; stroke-width: 0.08; }') # Gold plated pad
    svg.append('  .copper-track { fill: #2e6648; stroke: #1f4531; stroke-width: 0.15; }')
    svg.append('  .hole { fill: #111111; stroke: #333333; stroke-width: 0.08; }')
    svg.append('  .m3-pad { fill: #e5a95d; stroke: #8a581e; stroke-width: 0.2; }')
    svg.append('  .silkscreen { fill: #ffffff; font-size: 1.4px; font-weight: bold; }')
    svg.append('  .silk-sub { fill: #dddddd; font-size: 1.0px; }')
    svg.append('  .wire-pwr12 { stroke: #e53935; stroke-width: 0.7; stroke-linecap: round; fill: none; }')
    svg.append('  .wire-pwr5  { stroke: #fb8c00; stroke-width: 0.7; stroke-linecap: round; fill: none; }')
    svg.append('  .wire-gnd   { stroke: #212121; stroke-width: 0.7; stroke-linecap: round; fill: none; }')
    svg.append('  .wire-pwm   { stroke: #1e88e5; stroke-width: 0.6; stroke-linecap: round; fill: none; }')
    svg.append('  .wire-tach  { stroke: #43a047; stroke-width: 0.6; stroke-linecap: round; fill: none; }')
    svg.append('  .wire-uart  { stroke: #fdd835; stroke-width: 0.6; stroke-linecap: round; fill: none; }')
    svg.append('  .wire-rst   { stroke: #8e24aa; stroke-width: 0.6; stroke-linecap: round; fill: none; }')
    svg.append('</style>')

    # 1. PCB Body & Contour (Eurocard 88.9 x 128.3 mm with tongue)
    # Tongue: X=400..3100 mil, Y=4740..5050 mil
    p_tl = transform(0.0, 0.0)
    p_tr = transform(3500.0, 0.0)
    p_sr = transform(3500.0, 4740.0)
    p_tgr = transform(3100.0, 4740.0)
    p_br = transform(3100.0, 5050.0)
    p_bl = transform(400.0, 5050.0)
    p_tgl = transform(400.0, 4740.0)
    p_sl = transform(0.0, 4740.0)

    if not mirrored:
        path_board = f"M {p_tl[0]} {p_tl[1]} L {p_tr[0]} {p_tr[1]} L {p_sr[0]} {p_sr[1]} L {p_tgr[0]} {p_tgr[1]} L {p_br[0]} {p_br[1]} L {p_bl[0]} {p_bl[1]} L {p_tgl[0]} {p_tgl[1]} L {p_sl[0]} {p_sl[1]} Z"
    else:
        path_board = f"M {p_tr[0]} {p_tr[1]} L {p_tl[0]} {p_tl[1]} L {p_sl[0]} {p_sl[1]} L {p_tgl[0]} {p_tgl[1]} L {p_bl[0]} {p_bl[1]} L {p_br[0]} {p_br[1]} L {p_tgr[0]} {p_tgr[1]} L {p_sr[0]} {p_sr[1]} Z"

    svg.append(f'<path d="{path_board}" class="board-body" filter="url(#shadow)"/>')

    # 2. Silkscreen Headers and Markings
    c_x, c_y = transform(1750.0, 150.0)
    svg.append(f'<text x="{c_x}" y="{c_y}" class="silkscreen" font-size="2.6px">FAN CONTROLLER — CUSTOM STRIPBOARD REV 1.1a</text>')
    c_x, c_y = transform(1750.0, 260.0)
    svg.append(f'<text x="{c_x}" y="{c_y}" class="silk-sub" font-size="1.4px">High-Side Sziklai CFP (4x BC549 + BC328) • Autonomous ATX MOLEX Power</text>')

    # 3. M3 Mounting Holes
    for name, hx_mil, hy_mil in MOUNTING_HOLES_MIL:
        mx, my = transform(hx_mil, hy_mil)
        svg.append(f'<circle cx="{mx}" cy="{my}" r="3.05" class="m3-pad"/>')
        svg.append(f'<circle cx="{mx}" cy="{my}" r="1.60" class="hole"/>')
        tx, ty = transform(hx_mil, hy_mil + 190.0)
        svg.append(f'<text x="{tx}" y="{ty}" class="silk-sub" font-size="1.2px">{name}</text>')

    # 4. Vertical Power Rails (Copper strips + holes)
    for r_num, r_label, rx_mil, r_color, net_lbl in RAILS_MIL:
        x_mm, y_start = transform(rx_mil, 800.0)
        _, y_end = transform(rx_mil, 4700.0)
        y_top = min(y_start, y_end) - 1.016
        h_rail = abs(y_end - y_start) + 2.032
        # Rail copper background
        svg.append(f'<rect x="{x_mm - 1.016}" y="{y_top}" width="2.032" height="{h_rail}" rx="0.8" fill="{r_color}" opacity="0.35"/>')
        # Pads & Holes
        for y_mil in [800.0 + i * 100.0 for i in range(40)]:
            px, py = transform(rx_mil, y_mil)
            svg.append(f'<circle cx="{px}" cy="{py}" r="1.016" class="copper-pad"/>')
            svg.append(f'<circle cx="{px}" cy="{py}" r="0.445" class="hole"/>')
        # Rail Label at top
        lx, ly = transform(rx_mil, 700.0)
        svg.append(f'<text x="{lx}" y="{ly}" class="silk-sub" font-weight="bold" font-size="1.1px">{net_lbl}</text>')

    # 5. Prototyping Rows (Left Bank & Right Bank)
    for r_idx, ry_mil in enumerate(ROWS_Y_MIL):
        row_num = r_idx + 1
        # Left Bank copper strip
        lx_start, ly = transform(LEFT_COLS_X_MIL[0], ry_mil)
        lx_end, _ = transform(LEFT_COLS_X_MIL[-1], ry_mil)
        x_min_l = min(lx_start, lx_end) - 1.016
        w_l = abs(lx_end - lx_start) + 2.032
        svg.append(f'<rect x="{x_min_l}" y="{ly - 1.016}" width="{w_l}" height="2.032" rx="0.6" class="copper-track" opacity="0.45"/>')
        for cx_mil in LEFT_COLS_X_MIL:
            px, py = transform(cx_mil, ry_mil)
            svg.append(f'<circle cx="{px}" cy="{py}" r="1.016" class="copper-pad"/>')
            svg.append(f'<circle cx="{px}" cy="{py}" r="0.445" class="hole"/>')

        # Right Bank copper strip
        rx_start, ry = transform(RIGHT_COLS_X_MIL[0], ry_mil)
        rx_end, _ = transform(RIGHT_COLS_X_MIL[-1], ry_mil)
        x_min_r = min(rx_start, rx_end) - 1.016
        w_r = abs(rx_end - rx_start) + 2.032
        svg.append(f'<rect x="{x_min_r}" y="{ry - 1.016}" width="{w_r}" height="2.032" rx="0.6" class="copper-track" opacity="0.45"/>')
        for cx_mil in RIGHT_COLS_X_MIL:
            px, py = transform(cx_mil, ry_mil)
            svg.append(f'<circle cx="{px}" cy="{py}" r="1.016" class="copper-pad"/>')
            svg.append(f'<circle cx="{px}" cy="{py}" r="0.445" class="hole"/>')

        # Row Numbers on margins
        lbl_lx, lbl_ly = transform(380.0, ry_mil)
        svg.append(f'<text x="{lbl_lx}" y="{lbl_ly}" class="silk-sub" font-size="1.1px">R{row_num:02d}</text>')
        lbl_rx, lbl_ry = transform(3120.0, ry_mil)
        svg.append(f'<text x="{lbl_rx}" y="{lbl_ry}" class="silk-sub" font-size="1.1px">R{row_num:02d}</text>')

    # 6. Scratch-pad Matrix (Right margin, 14 rows x 4 cols)
    for ry_mil in SCRATCH_Y_MIL:
        for cx_mil in SCRATCH_X_MIL:
            px, py = transform(cx_mil, ry_mil)
            svg.append(f'<circle cx="{px}" cy="{py}" r="1.143" class="copper-pad"/>')
            svg.append(f'<circle cx="{px}" cy="{py}" r="0.445" class="hole"/>')

    # 7. Edge Connector Tongue (44 Fingers on bottom layer)
    for finger_idx in range(22):
        fx_mil = 450.0 + finger_idx * 120.0
        fx, fy = transform(fx_mil, 4850.0)
        svg.append(f'<rect x="{fx - 1.0}" y="{fy - 3.5}" width="2.0" height="7.0" rx="0.4" fill="#d4af37" opacity="0.8"/>')

    # ==================== CIRCUIT COMPONENTS OVERLAY ====================
    # A. ATMEGA328P-PU (DIP-28)
    # Spans Left Bank X=1600 (Pins 1..14) to Right Bank X=1900 (Pins 15..28) across Rows 1..14 (Y=800..2100)
    ic_x1, ic_y1 = transform(1600.0, 800.0)
    ic_x2, ic_y2 = transform(1900.0, 2100.0)
    ic_left = min(ic_x1, ic_x2) - 0.5
    ic_top = min(ic_y1, ic_y2) - 1.8
    ic_w = abs(ic_x2 - ic_x1) + 1.0
    ic_h = abs(ic_y2 - ic_y1) + 3.6

    svg.append(f'<rect x="{ic_left}" y="{ic_top}" width="{ic_w}" height="{ic_h}" rx="1.2" fill="#151515" stroke="#333333" stroke-width="0.3" filter="url(#ic-shadow)"/>')
    # Notch at pin 1
    notch_x = (ic_x1 + ic_x2) / 2.0
    svg.append(f'<circle cx="{notch_x}" cy="{ic_top}" r="1.2" fill="#2b2b2b"/>')
    # Chip Label
    svg.append(f'<text x="{notch_x}" y="{(ic_y1+ic_y2)/2.0 - 3.0}" fill="#e0e0e0" font-size="1.8px" font-weight="bold">ATmega328P</text>')
    svg.append(f'<text x="{notch_x}" y="{(ic_y1+ic_y2)/2.0}" fill="#9e9e9e" font-size="1.2px">16MHz AVR MCU</text>')
    svg.append(f'<text x="{notch_x}" y="{(ic_y1+ic_y2)/2.0 + 3.0}" fill="#e53935" font-size="1.1px">● Pin 1</text>')

    # B. Crystal Y1 & Load Capacitors (C3, C4)
    # Y1 at Left Bank Rows 9-10 (X=1300, Y=1600..1700)
    yx, y_mid = transform(1300.0, 1650.0)
    svg.append(f'<rect x="{yx - 1.5}" y="{y_mid - 2.8}" width="3.0" height="5.6" rx="1.5" fill="#c0c0c0" stroke="#777777" stroke-width="0.25" filter="url(#shadow)"/>')
    svg.append(f'<text x="{yx}" y="{y_mid}" fill="#111111" font-size="1.1px" font-weight="bold" transform="rotate(-90 {yx} {y_mid})">16 MHz</text>')
    # C3, C4 22pF Discs (between X=1200 and Rail 4 GND X=1700)
    c3x, c3y = transform(1450.0, 1600.0)
    svg.append(f'<circle cx="{c3x}" cy="{c3y}" r="1.6" fill="#00897b" stroke="#004d40" stroke-width="0.2"/>')
    svg.append(f'<text x="{c3x}" y="{c3y}" fill="#ffffff" font-size="0.9px">C3</text>')
    c4x, c4y = transform(1450.0, 1700.0)
    svg.append(f'<circle cx="{c4x}" cy="{c4y}" r="1.6" fill="#00897b" stroke="#004d40" stroke-width="0.2"/>')
    svg.append(f'<text x="{c4x}" y="{c4y}" fill="#ffffff" font-size="0.9px">C4</text>')

    # C. Tachometer Pull-Up Resistors (R4..R7 across Left Bank to Rail 5 +5V)
    for r_lbl, row_mil in [("R4 (T1)", 1100.0), ("R5 (T2)", 1300.0), ("R6 (T3)", 1800.0), ("R7 (T4)", 1900.0)]:
        rx_start, ry = transform(1500.0, row_mil)
        rx_end, _ = transform(1800.0, row_mil)
        rx_mid = (rx_start + rx_end) / 2.0
        svg.append(f'<line x1="{rx_start}" y1="{ry}" x2="{rx_end}" y2="{ry}" stroke="#d7ccc8" stroke-width="0.4"/>')
        svg.append(f'<rect x="{rx_mid - 2.0}" y="{ry - 0.9}" width="4.0" height="1.8" rx="0.4" fill="#d7ccc8" stroke="#5d4037" stroke-width="0.2"/>')
        # Resistor color bands (10k: Brown, Black, Orange, Gold)
        svg.append(f'<line x1="{rx_mid - 1.2}" y1="{ry - 0.9}" x2="{rx_mid - 1.2}" y2="{ry + 0.9}" stroke="#5d4037" stroke-width="0.3"/>')
        svg.append(f'<line x1="{rx_mid - 0.4}" y1="{ry - 0.9}" x2="{rx_mid - 0.4}" y2="{ry + 0.9}" stroke="#212121" stroke-width="0.3"/>')
        svg.append(f'<line x1="{rx_mid + 0.4}" y1="{ry - 0.9}" x2="{rx_mid + 0.4}" y2="{ry + 0.9}" stroke="#ff9800" stroke-width="0.3"/>')
        svg.append(f'<line x1="{rx_mid + 1.2}" y1="{ry - 0.9}" x2="{rx_mid + 1.2}" y2="{ry + 0.9}" stroke="#ffd700" stroke-width="0.3"/>')
        svg.append(f'<text x="{rx_mid}" y="{ry - 1.8}" fill="#ffffff" font-size="0.9px">{r_lbl}</text>')

    # D. Reset Pull-Up (R_RST) and DTR Capacitor (C_DTR)
    rrx_start, rry = transform(1500.0, 800.0)
    rrx_end, _ = transform(1800.0, 800.0)
    rrx_mid = (rrx_start + rrx_end) / 2.0
    svg.append(f'<rect x="{rrx_mid - 2.0}" y="{rry - 0.9}" width="4.0" height="1.8" rx="0.4" fill="#d7ccc8" stroke="#5d4037" stroke-width="0.2"/>')
    svg.append(f'<text x="{rrx_mid}" y="{rry - 1.8}" fill="#ffffff" font-size="0.9px">R_RST 10k</text>')

    # C_DTR at Row 27 (X=1100..1300, Y=3400)
    cdx, cdy = transform(1200.0, 3400.0)
    svg.append(f'<circle cx="{cdx}" cy="{cdy}" r="1.5" fill="#fbc02d" stroke="#f57f17" stroke-width="0.2"/>')
    svg.append(f'<text x="{cdx}" y="{cdy}" fill="#000000" font-size="0.8px" font-weight="bold">C_DTR</text>')

    # E. CH340 Female Socket (Rows 27..32 at X=1000 mil)
    s_x, s_y1 = transform(1000.0, 3400.0)
    _, s_y2 = transform(1000.0, 3900.0)
    svg.append(f'<rect x="{s_x - 1.5}" y="{s_y1 - 1.8}" width="3.0" height="{abs(s_y2 - s_y1) + 3.6}" rx="0.8" fill="#212121" stroke="#424242" stroke-width="0.3" filter="url(#shadow)"/>')
    svg.append(f'<text x="{s_x}" y="{(s_y1 + s_y2)/2.0}" fill="#ffffff" font-size="1.2px" font-weight="bold" transform="rotate(-90 {s_x} {(s_y1 + s_y2)/2.0})">CH340 USB (6P)</text>')

    # F. MOLEX ATX Power Entry Connector (Row 30, Y=3700 mil, connecting Rails 4, 5, 6, 8)
    mx1, my = transform(1700.0, 3700.0)
    mx2, _ = transform(3000.0, 3700.0)
    mol_left = min(mx1, mx2) - 2.5
    mol_w = abs(mx2 - mx1) + 5.0
    svg.append(f'<rect x="{mol_left}" y="{my - 3.2}" width="{mol_w}" height="6.4" rx="1.5" fill="#f5f5f5" stroke="#9e9e9e" stroke-width="0.4" filter="url(#shadow)"/>')
    svg.append(f'<text x="{(mx1+mx2)/2.0}" y="{my - 4.5}" fill="#ffffff" font-size="1.3px" font-weight="bold">CONN_MOLEX (ATX 4-PIN: +12V / GND / GND / +5V)</text>')
    # Pins
    for p_num, px_mil, p_col, p_name in [(1, 2800.0, "#e53935", "+12V"), (2, 3000.0, "#212121", "GND"), (3, 1700.0, "#212121", "GND"), (4, 1800.0, "#fb8c00", "+5V")]:
        px, py = transform(px_mil, 3700.0)
        svg.append(f'<circle cx="{px}" cy="{py}" r="1.4" fill="{p_col}" stroke="#333333" stroke-width="0.2"/>')

    # Bulk Cap C1 (100uF 25V) & Logic Decoupling C2 (100nF)
    c1x, c1y = transform(2900.0, 3500.0)
    svg.append(f'<circle cx="{c1x}" cy="{c1y}" r="2.8" fill="#1e88e5" stroke="#0d47a1" stroke-width="0.3" filter="url(#shadow)"/>')
    svg.append(f'<text x="{c1x}" y="{c1y}" fill="#ffffff" font-size="1.0px" font-weight="bold">C1 100uF</text>')

    c2x, c2y = transform(1750.0, 3500.0)
    svg.append(f'<circle cx="{c2x}" cy="{c2y}" r="1.6" fill="#fbc02d" stroke="#f57f17" stroke-width="0.2"/>')
    svg.append(f'<text x="{c2x}" y="{c2y}" fill="#000000" font-size="0.9px" font-weight="bold">C2</text>')

    # C_REF at Right Bank Row 8 (X=1900, Y=1500 mil)
    crx, cry = transform(2000.0, 1500.0)
    svg.append(f'<circle cx="{crx}" cy="{cry}" r="1.5" fill="#fbc02d" stroke="#f57f17" stroke-width="0.2"/>')
    svg.append(f'<text x="{crx}" y="{cry}" fill="#000000" font-size="0.8px" font-weight="bold">C_REF</text>')

    # G. 4x SZIKLAI HIGH-SIDE DRIVER CHANNELS (Rows 17 to 28 on Right Bank)
    channels_info = [
        (1, 17, 2400.0, "DRV1 (FAN 1)"),
        (2, 20, 2700.0, "DRV2 (FAN 2)"),
        (3, 23, 3000.0, "DRV3 (FAN 3)"),
        (4, 26, 3300.0, "DRV4 (FAN 4)")
    ]

    for ch_num, r_base, y_base_mil, ch_label in channels_info:
        r_npn = y_base_mil
        r_mid = y_base_mil + 100.0
        r_pnp = y_base_mil + 200.0

        # Subcircuit boundary box
        bx1, by1 = transform(1950.0, r_npn - 40.0)
        bx2, by2 = transform(3050.0, r_pnp + 40.0)
        b_left = min(bx1, bx2)
        b_top = min(by1, by2)
        b_w = abs(bx2 - bx1)
        b_h = abs(by2 - by1)
        svg.append(f'<rect x="{b_left}" y="{b_top}" width="{b_w}" height="{b_h}" rx="1.0" fill="#2e7d32" fill-opacity="0.10" stroke="#388e3c" stroke-width="0.2" stroke-dasharray="1.0, 0.8"/>')
        svg.append(f'<text x="{b_left + b_w/2.0}" y="{b_top - 1.2}" fill="#81c784" font-size="1.0px" font-weight="bold">{ch_label}</text>')

        # 1. R1 (1.5k base NPN) across X=2000..2300 at Row r_npn
        r1x1, r1y = transform(2000.0, r_npn)
        r1x2, _ = transform(2300.0, r_npn)
        r1_mid = (r1x1 + r1x2) / 2.0
        svg.append(f'<line x1="{r1x1}" y1="{r1y}" x2="{r1x2}" y2="{r1y}" stroke="#d7ccc8" stroke-width="0.3"/>')
        svg.append(f'<rect x="{r1_mid - 1.6}" y="{r1y - 0.7}" width="3.2" height="1.4" rx="0.3" fill="#d7ccc8" stroke="#5d4037" stroke-width="0.15"/>')
        svg.append(f'<text x="{r1_mid}" y="{r1y - 1.3}" fill="#ffffff" font-size="0.8px">R1 1.5k</text>')

        # 2. Q1 (BC549 NPN TO-92) at X=2400 (Row r_npn Base, Row r_mid Collector, Rail 4 GND Emitter)
        q1x, q1y = transform(2400.0, r_npn + 50.0)
        svg.append(f'<path d="M {q1x - 1.3} {q1y - 1.0} A 1.4 1.4 0 0 1 {q1x + 1.3} {q1y - 1.0} L {q1x + 1.3} {q1y + 1.0} L {q1x - 1.3} {q1y + 1.0} Z" fill="#212121" stroke="#424242" stroke-width="0.2"/>')
        svg.append(f'<text x="{q1x}" y="{q1y}" fill="#ffffff" font-size="0.7px">BC549</text>')
        # Emitter connection to Rail 4 GND
        em_x1, em_y = transform(1700.0, r_npn)
        svg.append(f'<line x1="{em_x1}" y1="{em_y}" x2="{q1x - 1.3}" y2="{r1y}" class="wire-gnd" stroke-width="0.4"/>')

        # 3. R2 (4.7k Pull-up +12V) between X=2500 and Rail 6 (+12V, X=2800) at Row r_mid
        r2x1, r2y = transform(2500.0, r_mid)
        r2x2, _ = transform(2800.0, r_mid)
        r2_mid = (r2x1 + r2x2) / 2.0
        svg.append(f'<line x1="{r2x1}" y1="{r2y}" x2="{r2x2}" y2="{r2y}" stroke="#d7ccc8" stroke-width="0.3"/>')
        svg.append(f'<rect x="{r2_mid - 1.6}" y="{r2y - 0.7}" width="3.2" height="1.4" rx="0.3" fill="#d7ccc8" stroke="#5d4037" stroke-width="0.15"/>')
        svg.append(f'<text x="{r2_mid}" y="{r2y - 1.3}" fill="#ffffff" font-size="0.8px">R2 4.7k</text>')

        # 4. R3 (680R series base drive) vertical between Row r_mid (X=2300) and Row r_pnp (X=2300)
        r3x, r3y1 = transform(2300.0, r_mid)
        _, r3y2 = transform(2300.0, r_pnp)
        r3_mid = (r3y1 + r3y2) / 2.0
        svg.append(f'<line x1="{r3x}" y1="{r3y1}" x2="{r3x}" y2="{r3y2}" stroke="#d7ccc8" stroke-width="0.3"/>')
        svg.append(f'<rect x="{r3x - 0.7}" y="{r3_mid - 1.6}" width="1.4" height="3.2" rx="0.3" fill="#d7ccc8" stroke="#5d4037" stroke-width="0.15"/>')
        svg.append(f'<text x="{r3x - 1.4}" y="{r3_mid}" fill="#ffffff" font-size="0.7px" transform="rotate(-90 {r3x-1.4} {r3_mid})">R3 680R</text>')

        # 5. Q2 (BC328 PNP TO-92, 800mA) at Row r_pnp (Base X=2400, Collector X=2500, Emitter Rail 6 X=2800)
        q2x, q2y = transform(2450.0, r_pnp)
        svg.append(f'<path d="M {q2x - 1.4} {q2y - 1.2} A 1.5 1.5 0 0 1 {q2x + 1.4} {q2y - 1.2} L {q2x + 1.4} {q2y + 1.2} L {q2x - 1.4} {q2y + 1.2} Z" fill="#1565c0" stroke="#0d47a1" stroke-width="0.2"/>')
        svg.append(f'<text x="{q2x}" y="{q2y}" fill="#ffffff" font-size="0.75px" font-weight="bold">BC328</text>')
        # Emitter to Rail 6 +12V
        q2e_x, q2e_y = transform(2800.0, r_pnp)
        svg.append(f'<line x1="{q2x + 1.4}" y1="{q2y}" x2="{q2e_x}" y2="{q2e_y}" class="wire-pwr12" stroke-width="0.4"/>')

        # 6. D1 (1N4007 Flyback Diode) between Row r_pnp Collector (X=2600) and Rail 8 GND (X=3000)
        d1x1, d1y = transform(2600.0, r_pnp)
        d1x2, _ = transform(3000.0, r_pnp)
        d1_mid = (d1x1 + d1x2) / 2.0
        svg.append(f'<line x1="{d1x1}" y1="{d1y}" x2="{d1x2}" y2="{d1y}" stroke="#424242" stroke-width="0.4"/>')
        svg.append(f'<rect x="{d1_mid - 2.0}" y="{d1y - 0.9}" width="4.0" height="1.8" rx="0.3" fill="#212121" stroke="#000000" stroke-width="0.2"/>')
        # Silver cathode band towards collector
        svg.append(f'<line x1="{d1_mid - 1.2}" y1="{d1y - 0.9}" x2="{d1_mid - 1.2}" y2="{d1y + 0.9}" stroke="#eeeeee" stroke-width="0.5"/>')
        svg.append(f'<text x="{d1_mid}" y="{d1y + 1.8}" fill="#ffffff" font-size="0.8px">1N4007</text>')

    # H. 4x PC FAN CONNECTORS (FAN1..FAN4 on Right Margin X=3400 mil)
    fan_headers = [
        ("FAN1", 600.0),
        ("FAN2", 1000.0),
        ("FAN3", 1400.0),
        ("FAN4", 1800.0),
    ]

    for fan_name, y_fan in fan_headers:
        fx, fy1 = transform(3400.0, y_fan)
        _, fy2 = transform(3400.0, y_fan + 100.0)
        _, fy3 = transform(3400.0, y_fan + 200.0)
        # Plastic body with locking tab
        f_top = min(fy1, fy3) - 1.6
        f_h = abs(fy3 - fy1) + 3.2
        svg.append(f'<rect x="{fx - 2.5}" y="{f_top}" width="5.0" height="{f_h}" rx="0.8" fill="#eeeeee" stroke="#757575" stroke-width="0.3" filter="url(#shadow)"/>')
        # Locking ramp
        svg.append(f'<rect x="{fx + 1.6}" y="{f_top + 1.0}" width="1.0" height="{f_h - 2.0}" rx="0.2" fill="#bdbdbd"/>')
        svg.append(f'<text x="{fx - 4.5}" y="{(fy1+fy3)/2.0}" fill="#ffffff" font-size="1.2px" font-weight="bold">{fan_name}</text>')
        # Pin labels
        svg.append(f'<text x="{fx}" y="{fy1}" fill="#212121" font-size="0.8px">G</text>')
        svg.append(f'<text x="{fx}" y="{fy2}" fill="#c62828" font-size="0.8px">+</text>')
        svg.append(f'<text x="{fx}" y="{fy3}" fill="#2e7d32" font-size="0.8px">T</text>')

    # I. Jumper Wires & Interconnects (Color coded, realistic curve/line paths)
    # Output from each Q2 to FAN Pin 2 (+12V Switched)
    for ch_idx, (ch_num, r_base, y_base_mil, _) in enumerate(channels_info):
        q2_out_x, q2_out_y = transform(2700.0, y_base_mil + 200.0)
        fan_in_x, fan_in_y = transform(3400.0, fan_headers[ch_idx][1] + 100.0)
        svg.append(f'<path d="M {q2_out_x} {q2_out_y} C {q2_out_x + 8.0} {q2_out_y}, {fan_in_x - 8.0} {fan_in_y}, {fan_in_x} {fan_in_y}" class="wire-pwr12" stroke-width="0.55"/>')

    # Fan GND lines (from Rail 8 GND X=3000 mil to Fan Pin 1)
    for fan_name, y_fan in fan_headers:
        gnd_x, gnd_y = transform(3000.0, y_fan)
        fan_g_x, fan_g_y = transform(3400.0, y_fan)
        svg.append(f'<line x1="{gnd_x}" y1="{gnd_y}" x2="{fan_g_x}" y2="{fan_g_y}" class="wire-gnd" stroke-width="0.55"/>')

    # Tachometer lines from Fan Pin 3 to MCU Pins 4, 6, 11, 12
    tach_routes = [
        (600.0 + 200.0, 1100.0), # FAN1 Tach -> MCU Pin 4 (Row 4)
        (1000.0 + 200.0, 1300.0),# FAN2 Tach -> MCU Pin 6 (Row 6)
        (1400.0 + 200.0, 1800.0),# FAN3 Tach -> MCU Pin 11 (Row 11)
        (1800.0 + 200.0, 1900.0),# FAN4 Tach -> MCU Pin 12 (Row 12)
    ]
    for fan_y, mcu_y in tach_routes:
        tx1, ty1 = transform(3400.0, fan_y)
        tx2, ty2 = transform(1600.0, mcu_y)
        svg.append(f'<path d="M {tx1} {ty1} C {tx1 - 15.0} {ty1}, {tx2 + 15.0} {ty2}, {tx2} {ty2}" class="wire-tach" stroke-width="0.5" stroke-dasharray="1.2, 0.6"/>')

    # MCU PWM routes (PB1, PB2, PB3, PD3) to DRV1..4
    pwm_routes = [
        (2100.0, 2400.0), # PB1 (Row 14) -> DRV1 (Row 17)
        (2000.0, 2700.0), # PB2 (Row 13) -> DRV2 (Row 20)
        (1900.0, 3000.0), # PB3 (Row 12) -> DRV3 (Row 23)
        (1200.0, 3300.0), # PD3 (Row 5)  -> DRV4 (Row 26)
    ]
    for mcu_pwm_y, drv_pwm_y in pwm_routes:
        px1, py1 = transform(1900.0 if mcu_pwm_y > 1500.0 else 1600.0, mcu_pwm_y)
        px2, py2 = transform(2000.0, drv_pwm_y)
        svg.append(f'<path d="M {px1} {py1} C {px1 + 8.0} {py1}, {px2 - 8.0} {py2}, {px2} {py2}" class="wire-pwm" stroke-width="0.55"/>')

    # Legend / Key
    leg_x, leg_y = transform(1750.0, 4400.0)
    svg.append(f'<rect x="{leg_x - 38.0}" y="{leg_y - 2.5}" width="76.0" height="5.0" rx="0.8" fill="#111111" opacity="0.85" stroke="#444444" stroke-width="0.3"/>')
    svg.append(f'<line x1="{leg_x - 35.0}" y1="{leg_y}" x2="{leg_x - 29.0}" y2="{leg_y}" class="wire-pwr12" stroke-width="0.8"/>')
    svg.append(f'<text x="{leg_x - 25.0}" y="{leg_y}" fill="#ffffff" font-size="1.1px">+12V</text>')
    svg.append(f'<line x1="{leg_x - 19.0}" y1="{leg_y}" x2="{leg_x - 13.0}" y2="{leg_y}" class="wire-pwr5" stroke-width="0.8"/>')
    svg.append(f'<text x="{leg_x - 9.0}" y="{leg_y}" fill="#ffffff" font-size="1.1px">+5V</text>')
    svg.append(f'<line x1="{leg_x - 4.0}" y1="{leg_y}" x2="{leg_x + 2.0}" y2="{leg_y}" class="wire-gnd" stroke-width="0.8"/>')
    svg.append(f'<text x="{leg_x + 6.0}" y="{leg_y}" fill="#ffffff" font-size="1.1px">GND</text>')
    svg.append(f'<line x1="{leg_x + 11.0}" y1="{leg_y}" x2="{leg_x + 17.0}" y2="{leg_y}" class="wire-pwm" stroke-width="0.8"/>')
    svg.append(f'<text x="{leg_x + 21.0}" y="{leg_y}" fill="#ffffff" font-size="1.1px">PWM</text>')
    svg.append(f'<line x1="{leg_x + 26.0}" y1="{leg_y}" x2="{leg_x + 32.0}" y2="{leg_y}" class="wire-tach" stroke-width="0.8"/>')
    svg.append(f'<text x="{leg_x + 36.0}" y="{leg_y}" fill="#ffffff" font-size="1.1px">TACH</text>')

    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Generated SVG: {output_path}")

def generate_pdf_templates(output_path):
    """
    Generates exact 1:1 scale printable PDF assembly templates on A4 paper
    using ReportLab. Includes Millimetric calibration rulers and crosshairs.
    """
    c = canvas.Canvas(output_path, pagesize=A4)
    page_w, page_h = A4

    # Target board dimensions
    bw = BOARD_W_MM * mm
    bh = BOARD_H_MM * mm

    # Center board on A4 page
    ox = (page_w - bw) / 2.0
    oy = (page_h - bh) / 2.0

    # 1. Page Title & Calibration Note
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(page_w / 2.0, page_h - 18 * mm, "Custom Stripboard Rev 1.1a — Gabarito de Montagem 1:1 (Scale 100%)")
    c.setFont("Helvetica", 9)
    c.setFillColor(colors.HexColor("#444444"))
    c.drawCentredString(page_w / 2.0, page_h - 23 * mm, "IMPORTANTE: Imprimir em escala 100% ('Tamanho Real' / 'Sem Redimensionamento') em folha A4.")
    c.drawCentredString(page_w / 2.0, page_h - 27 * mm, "Verifique os calibradores milimétricos laterais antes de furar ou cortar os componentes.")

    # 2. Calibration Crosshairs & Precision 50mm Rulers
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.5)

    # 50 mm Horizontal Calibration Ruler
    ruler_x = ox
    ruler_y = oy - 14 * mm
    c.line(ruler_x, ruler_y, ruler_x + 50 * mm, ruler_y)
    for mm_i in range(51):
        tick_h = 3 * mm if mm_i % 10 == 0 else (2 * mm if mm_i % 5 == 0 else 1 * mm)
        c.line(ruler_x + mm_i * mm, ruler_y, ruler_x + mm_i * mm, ruler_y + tick_h)
        if mm_i % 10 == 0:
            c.setFont("Helvetica", 6)
            c.drawCentredString(ruler_x + mm_i * mm, ruler_y - 3 * mm, f"{mm_i}mm")
    c.setFont("Helvetica-Bold", 8)
    c.drawString(ruler_x + 54 * mm, ruler_y, "◄── 50.0 mm Régua de Calibração Horizontal")

    # 50 mm Vertical Calibration Ruler
    vruler_x = ox - 12 * mm
    vruler_y = oy
    c.line(vruler_x, vruler_y, vruler_x, vruler_y + 50 * mm)
    for mm_i in range(51):
        tick_w = 3 * mm if mm_i % 10 == 0 else (2 * mm if mm_i % 5 == 0 else 1 * mm)
        c.line(vruler_x, vruler_y + mm_i * mm, vruler_x + tick_w, vruler_y + mm_i * mm)
        if mm_i % 10 == 0:
            c.setFont("Helvetica", 6)
            c.drawRightString(vruler_x - 1 * mm, vruler_y + mm_i * mm - 1 * mm, f"{mm_i}mm")

    # 3. Board Outline (Eurocard 88.90 x 128.27 mm)
    c.setStrokeColor(colors.HexColor("#0d1f16"))
    c.setFillColor(colors.HexColor("#f4f9f4"))
    c.setLineWidth(0.8)

    # Coords relative to bottom-left:
    # Tongue: X=400..3100 mil (10.16..78.74 mm), Y from bottom (5050 - 4740 = 310 mil = 7.87 mm)
    p = c.beginPath()
    p.moveTo(ox, oy + bh)                                 # Top-left
    p.lineTo(ox + bw, oy + bh)                            # Top-right
    p.lineTo(ox + bw, oy + 7.87 * mm)                     # Right shoulder
    p.lineTo(ox + 78.74 * mm, oy + 7.87 * mm)             # Tongue right step
    p.lineTo(ox + 78.74 * mm, oy)                         # Tongue bottom-right
    p.lineTo(ox + 10.16 * mm, oy)                         # Tongue bottom-left
    p.lineTo(ox + 10.16 * mm, oy + 7.87 * mm)             # Tongue left step
    p.lineTo(ox, oy + 7.87 * mm)                          # Left shoulder
    p.close()
    c.drawPath(p, fill=1, stroke=1)

    # 4. M3 Holes
    c.setFillColor(colors.white)
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.4)
    for name, hx_mil, hy_mil in MOUNTING_HOLES_MIL:
        hx = ox + hx_mil * MIL_TO_MM * mm
        hy = oy + bh - hy_mil * MIL_TO_MM * mm
        c.circle(hx, hy, 1.6 * mm, fill=1, stroke=1)
        # Crosshair
        c.line(hx - 2.5 * mm, hy, hx + 2.5 * mm, hy)
        c.line(hx, hy - 2.5 * mm, hx, hy + 2.5 * mm)
        c.setFont("Helvetica-Bold", 6)
        c.drawString(hx + 2.2 * mm, hy + 1.5 * mm, name)

    # 5. Rails (Y=800..4700 mil, from top)
    for r_num, r_label, rx_mil, r_color, net_lbl in RAILS_MIL:
        rx = ox + rx_mil * MIL_TO_MM * mm
        c.setStrokeColor(colors.HexColor("#b0bec5"))
        c.setLineWidth(0.2)
        y_top = oy + bh - 800.0 * MIL_TO_MM * mm
        y_bot = oy + bh - 4700.0 * MIL_TO_MM * mm
        c.line(rx, y_top, rx, y_bot)
        c.setFont("Helvetica-Bold", 5)
        c.setFillColor(colors.HexColor(r_color))
        c.drawCentredString(rx, y_top + 1.5 * mm, net_lbl)

    # 6. Prototyping Rows & Holes Grid
    c.setStrokeColor(colors.HexColor("#78909c"))
    c.setLineWidth(0.15)
    for ry_mil in ROWS_Y_MIL:
        ry = oy + bh - ry_mil * MIL_TO_MM * mm
        # Left Bank line
        c.line(ox + LEFT_COLS_X_MIL[0]*MIL_TO_MM*mm, ry, ox + LEFT_COLS_X_MIL[-1]*MIL_TO_MM*mm, ry)
        # Right Bank line
        c.line(ox + RIGHT_COLS_X_MIL[0]*MIL_TO_MM*mm, ry, ox + RIGHT_COLS_X_MIL[-1]*MIL_TO_MM*mm, ry)

    # Drill points (0.4mm circles for precision centering drill bit)
    c.setFillColor(colors.black)
    for ry_mil in ROWS_Y_MIL:
        ry = oy + bh - ry_mil * MIL_TO_MM * mm
        for cx_mil in LEFT_COLS_X_MIL + RIGHT_COLS_X_MIL:
            cx = ox + cx_mil * MIL_TO_MM * mm
            c.circle(cx, ry, 0.4 * mm, fill=1, stroke=0)

    # Rail Drill points
    for _, _, rx_mil, _, _ in RAILS_MIL:
        rx = ox + rx_mil * MIL_TO_MM * mm
        for y_mil in [800.0 + i * 100.0 for i in range(40)]:
            ry = oy + bh - y_mil * MIL_TO_MM * mm
            c.circle(rx, ry, 0.4 * mm, fill=1, stroke=0)

    # 7. IC DIP-28 Silk Outline
    ic_x = ox + 1600.0 * MIL_TO_MM * mm
    ic_y = oy + bh - 2100.0 * MIL_TO_MM * mm - 1.0 * mm
    ic_w = (1900.0 - 1600.0) * MIL_TO_MM * mm
    ic_h = (2100.0 - 800.0) * MIL_TO_MM * mm + 2.0 * mm
    c.setStrokeColor(colors.HexColor("#1b5e20"))
    c.setLineWidth(0.8)
    c.roundRect(ic_x, ic_y, ic_w, ic_h, 1.0 * mm, fill=0, stroke=1)
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(colors.HexColor("#1b5e20"))
    c.drawCentredString(ic_x + ic_w / 2.0, ic_y + ic_h / 2.0, "U1 ATmega328P")

    # 8. Fan Connectors Outline (FAN1..FAN4)
    for fan_name, y_fan in [("FAN1", 600.0), ("FAN2", 1000.0), ("FAN3", 1400.0), ("FAN4", 1800.0)]:
        fx = ox + 3400.0 * MIL_TO_MM * mm - 1.5 * mm
        fy = oy + bh - (y_fan + 200.0) * MIL_TO_MM * mm - 1.0 * mm
        fw = 3.0 * mm
        fh = 200.0 * MIL_TO_MM * mm + 2.0 * mm
        c.setStrokeColor(colors.HexColor("#c62828"))
        c.setLineWidth(0.6)
        c.rect(fx, fy, fw, fh, fill=0, stroke=1)
        c.setFont("Helvetica-Bold", 6)
        c.drawString(fx + fw + 1.0 * mm, fy + fh / 2.0 - 1.5 * mm, fan_name)

    c.showPage()
    c.save()
    print(f"Generated PDF: {output_path}")

def main():
    templates_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(templates_dir, exist_ok=True)

    # 1. Generate Top Assembly SVG
    svg_top_path = os.path.join(templates_dir, "circuit_assembly_rev1.1a_top_view.svg")
    generate_circuit_assembly_svg(svg_top_path, mirrored=False)

    # 2. Generate Bottom Solder SVG
    svg_bot_path = os.path.join(templates_dir, "circuit_assembly_rev1.1a_bottom_view.svg")
    generate_circuit_assembly_svg(svg_bot_path, mirrored=True)

    # 3. Export 300 DPI PNGs using rsvg-convert
    png_top_path = os.path.join(templates_dir, "circuit_assembly_rev1.1a_top_view.png")
    png_bot_path = os.path.join(templates_dir, "circuit_assembly_rev1.1a_bottom_view.png")

    for s_path, p_path in [(svg_top_path, png_top_path), (svg_bot_path, png_bot_path)]:
        try:
            subprocess.run(["rsvg-convert", "-d", "300", "-p", "300", "-o", p_path, s_path], check=True)
            print(f"Rendered 300 DPI PNG: {p_path}")
        except Exception as e:
            print(f"Warning: rsvg-convert failed ({e}), trying inkscape...")
            try:
                subprocess.run(["inkscape", s_path, "--export-filename=" + p_path, "--export-dpi=300"], check=True)
                print(f"Rendered 300 DPI PNG with Inkscape: {p_path}")
            except Exception as e2:
                print(f"Failed to export PNG: {e2}")

    # 4. Generate 1:1 Scale Printable PDF Sheet
    pdf_path = os.path.join(templates_dir, "stripboard_rev1.1a_1to1_printout.pdf")
    generate_pdf_templates(pdf_path)

    # 5. Copy top view PNG to docs/ for easy linking
    docs_dir = os.path.dirname(templates_dir)
    shutil_dest = os.path.join(docs_dir, "circuit_assembly_rev1.1a_top_view.png")
    import shutil
    shutil.copyfile(png_top_path, shutil_dest)
    print(f"Copied top view to docs root: {shutil_dest}")

if __name__ == "__main__":
    main()
