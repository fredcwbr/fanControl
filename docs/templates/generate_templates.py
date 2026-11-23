#!/usr/bin/env python3
"""
Generate 1:1 Scale Printable Stripboard Templates
Dimensions: 33.0 mm x 72.0 mm (12 Columns x 28 Rows, 2.54 mm pitch)
Features: Staggered / Alternating Column Identification Labels (C01, C03... / C02, C04...)
"""

import os
import math
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

# Exact Board Dimensions
BOARD_W_MM = 33.0
BOARD_H_MM = 72.0
COLS = 12
ROWS = 28
PITCH_MM = 2.54

# Margins to center the 12x28 grid inside 33.0 x 72.0 mm
GRID_W_MM = (COLS - 1) * PITCH_MM   # 27.94 mm
GRID_H_MM = (ROWS - 1) * PITCH_MM   # 68.58 mm
MARGIN_X_MM = (BOARD_W_MM - GRID_W_MM) / 2.0  # 2.53 mm
MARGIN_Y_MM = (BOARD_H_MM - GRID_H_MM) / 2.0  # 1.71 mm

# Hole coordinates for SVG (Y=0 at top, increasing downwards)
def get_hole_coords_svg(col, row, mirrored=False):
    if mirrored:
        c_idx = (COLS - col)
    else:
        c_idx = (col - 1)
    r_idx = (row - 1)
    x = MARGIN_X_MM + c_idx * PITCH_MM
    y = MARGIN_Y_MM + r_idx * PITCH_MM
    return x, y

# Hole coordinates for PDF (Y=0 at bottom, increasing upwards; R01 at top)
def get_hole_coords_pdf(col, row, mirrored=False):
    if mirrored:
        c_idx = (COLS - col)
    else:
        c_idx = (col - 1)
    r_idx = (row - 1)
    x = MARGIN_X_MM + c_idx * PITCH_MM
    y = BOARD_H_MM - (MARGIN_Y_MM + r_idx * PITCH_MM)
    return x, y

def generate_svg(filename, mode="cuts", mirrored=False):
    pad_x = 14.0 # mm padding on left/right for row labels
    pad_y = 16.0 # mm padding on top/bottom for staggered column labels
    total_w = BOARD_W_MM + 2 * pad_x
    total_h = BOARD_H_MM + 2 * pad_y

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{total_w}mm" height="{total_h}mm" viewBox="0 0 {total_w} {total_h}">')
    svg.append('<style>')
    svg.append('  text { font-family: "DejaVu Sans", "Helvetica", Arial, sans-serif; font-size: 1.3px; text-anchor: middle; dominant-baseline: central; }')
    svg.append('  .label-axis { font-size: 1.2px; fill: #000000; font-weight: bold; }')
    svg.append('  .title { font-size: 2.3px; font-weight: bold; fill: #111111; }')
    svg.append('  .subtitle { font-size: 1.25px; fill: #444444; }')
    svg.append('  .board-outline { fill: #fdfaf2; stroke: #000000; stroke-width: 0.45; }')
    svg.append('  .copper-track { fill: #e6b87d; stroke: #c99355; stroke-width: 0.15; opacity: 0.85; }')
    svg.append('  .copper-rail { fill: #d4a366; stroke: #b58045; stroke-width: 0.15; opacity: 0.90; }')
    svg.append('  .hole { fill: #ffffff; stroke: #333333; stroke-width: 0.18; }')
    svg.append('  .hole-cross { stroke: #666666; stroke-width: 0.12; }')
    svg.append('  .cut-box { fill: #ff1111; stroke: #880000; stroke-width: 0.25; }')
    svg.append('  .cut-cross { stroke: #ffffff; stroke-width: 0.4; stroke-linecap: round; }')
    svg.append('  .guide-line { stroke: #555555; stroke-width: 0.18; stroke-dasharray: 0.4, 0.4; }')
    svg.append('  .ruler-tick { stroke: #111111; stroke-width: 0.25; }')
    svg.append('  .ruler-subtick { stroke: #666666; stroke-width: 0.15; }')
    svg.append('</style>')

    # Background
    svg.append(f'<rect width="{total_w}" height="{total_h}" fill="#ffffff" />')

    # Group for board offset
    bx = pad_x
    by = pad_y
    svg.append(f'<g transform="translate({bx}, {by})">')

    # Physical Board Outline
    svg.append(f'  <rect x="0" y="0" width="{BOARD_W_MM}" height="{BOARD_H_MM}" rx="1.0" ry="1.0" class="board-outline" />')

    # Millimeter Ruler Ticks along Left Edge (0 to 72 mm)
    for mm_i in range(int(BOARD_H_MM) + 1):
        if mm_i % 10 == 0:
            svg.append(f'  <line x1="-2.0" y1="{mm_i}" x2="0" y2="{mm_i}" class="ruler-tick" />')
            svg.append(f'  <text x="-4.2" y="{mm_i}" class="label-axis" style="text-anchor: end; font-size: 1.1px;">{mm_i}</text>')
        elif mm_i % 5 == 0:
            svg.append(f'  <line x1="-1.3" y1="{mm_i}" x2="0" y2="{mm_i}" class="ruler-tick" />')
        else:
            svg.append(f'  <line x1="-0.8" y1="{mm_i}" x2="0" y2="{mm_i}" class="ruler-subtick" />')

    # Draw Copper Tracks based on custoStripBoard.ods
    track_w = 1.9 # mm width of copper tracks
    hole_r = 0.55 # mm hole radius
    pad_r = 1.05  # mm copper pad radius

    if mode == "cuts":
        # 1. Row R01 horizontal bus across C01..C12
        x1, y1 = get_hole_coords_svg(1, 1, mirrored)
        x2, y2 = get_hole_coords_svg(12, 1, mirrored)
        xmin, xmax = min(x1, x2), max(x1, x2)
        svg.append(f'  <rect x="{xmin - pad_r:.3f}" y="{y1 - track_w/2:.3f}" width="{xmax - xmin + 2*pad_r:.3f}" height="{track_w:.3f}" rx="{track_w/2:.3f}" class="copper-rail" />')

        # 2. Vertical Rails (C01, C06, C07, C12) from R02 to R28
        for col in [1, 6, 7, 12]:
            x_top, y_top = get_hole_coords_svg(col, 2, mirrored)
            x_bot, y_bot = get_hole_coords_svg(col, 28, mirrored)
            svg.append(f'  <rect x="{x_top - track_w/2:.3f}" y="{y_top - pad_r:.3f}" width="{track_w:.3f}" height="{y_bot - y_top + 2*pad_r:.3f}" rx="{track_w/2:.3f}" class="copper-rail" />')

        # 3. Horizontal 4-hole strips (Rows R02 to R26)
        for r in range(2, 27):
            x1, y1 = get_hole_coords_svg(2, r, mirrored)
            x2, y2 = get_hole_coords_svg(5, r, mirrored)
            xmin, xmax = min(x1, x2), max(x1, x2)
            svg.append(f'  <rect x="{xmin - pad_r:.3f}" y="{y1 - track_w/2:.3f}" width="{xmax - xmin + 2*pad_r:.3f}" height="{track_w:.3f}" rx="{track_w/2:.3f}" class="copper-track" />')

            x3, y3 = get_hole_coords_svg(8, r, mirrored)
            x4, y4 = get_hole_coords_svg(11, r, mirrored)
            xmin, xmax = min(x3, x4), max(x3, x4)
            svg.append(f'  <rect x="{xmin - pad_r:.3f}" y="{y3 - track_w/2:.3f}" width="{xmax - xmin + 2*pad_r:.3f}" height="{track_w:.3f}" rx="{track_w/2:.3f}" class="copper-track" />')

        # 4. Vertical 2-hole pairs (Rows R27 to R28) on C02..C05 and C08..C11
        for col in [2, 3, 4, 5, 8, 9, 10, 11]:
            x_top, y_top = get_hole_coords_svg(col, 27, mirrored)
            x_bot, y_bot = get_hole_coords_svg(col, 28, mirrored)
            svg.append(f'  <rect x="{x_top - track_w/2:.3f}" y="{y_top - pad_r:.3f}" width="{track_w:.3f}" height="{y_bot - y_top + 2*pad_r:.3f}" rx="{track_w/2:.3f}" class="copper-track" />')

    # Draw Holes (all 28 rows x 12 cols)
    for r in range(1, ROWS + 1):
        for c in range(1, COLS + 1):
            hx, hy = get_hole_coords_svg(c, r, mirrored)
            svg.append(f'  <circle cx="{hx:.3f}" cy="{hy:.3f}" r="{hole_r}" class="hole" />')
            svg.append(f'  <line x1="{hx-0.3:.3f}" y1="{hy:.3f}" x2="{hx+0.3:.3f}" y2="{hy:.3f}" class="hole-cross" />')
            svg.append(f'  <line x1="{hx:.3f}" y1="{hy-0.3:.3f}" x2="{hx:.3f}" y2="{hy+0.3:.3f}" class="hole-cross" />')

    # Draw CUTS in RED (if mode == 'cuts')
    if mode == "cuts":
        cuts = [
            (12, 16, "CUT 1: R16/C12 (+5V/+12V rail split)"),
            (2.5, 21, "CUT 2: R21 between C02 and C03 (DTR cap)"),
            (3.5, 24, "CUT 3: R24 between C03 and C04 (VCC/GND split)"),
            (2, 27.5, "CUT 4: C02 between R27 and R28 (Fan 1)"),
            (4, 27.5, "CUT 5: C04 between R27 and R28 (Fan 2)"),
            (8, 27.5, "CUT 6: C08 between R27 and R28 (Fan 3)"),
            (10, 27.5, "CUT 7: C10 between R27 and R28 (Fan 4)"),
        ]

        for c_spec in cuts:
            c_val, r_val = c_spec[0], c_spec[1]
            if mirrored:
                c_idx = (COLS - c_val)
            else:
                c_idx = (c_val - 1)
            cx = MARGIN_X_MM + c_idx * PITCH_MM
            cy = MARGIN_Y_MM + (r_val - 1) * PITCH_MM

            sz = 1.8 # size of red cut indicator
            svg.append(f'  <!-- {c_spec[2]} -->')
            svg.append(f'  <rect x="{cx - sz/2:.3f}" y="{cy - sz/2:.3f}" width="{sz}" height="{sz}" rx="0.3" class="cut-box" />')
            svg.append(f'  <line x1="{cx - sz*0.35:.3f}" y1="{cy - sz*0.35:.3f}" x2="{cx + sz*0.35:.3f}" y2="{cy + sz*0.35:.3f}" class="cut-cross" />')
            svg.append(f'  <line x1="{cx + sz*0.35:.3f}" y1="{cy - sz*0.35:.3f}" x2="{cx - sz*0.35:.3f}" y2="{cy + sz*0.35:.3f}" class="cut-cross" />')

    # STAGGERED / ALTERNATING COLUMN LABELS (C01, C03... on row 1; C02, C04... on row 2)
    # Top Staggered Labels:
    # Odd cols: y = -4.2 mm, Even cols: y = -1.5 mm
    for c in range(1, COLS + 1):
        hx, _ = get_hole_coords_svg(c, 1, mirrored)
        col_name = f'C{c:02d}'
        if c % 2 == 1:
            lbl_y = -4.5
            svg.append(f'  <line x1="{hx:.3f}" y1="{lbl_y + 1.0:.3f}" x2="{hx:.3f}" y2="0" class="guide-line" />')
        else:
            lbl_y = -1.6
            svg.append(f'  <line x1="{hx:.3f}" y1="{lbl_y + 0.9:.3f}" x2="{hx:.3f}" y2="0" class="ruler-tick" />')
        svg.append(f'  <text x="{hx:.3f}" y="{lbl_y:.3f}" class="label-axis">{col_name}</text>')

    # Bottom Staggered Labels:
    # Even cols: y = BOARD_H_MM + 1.8 mm, Odd cols: y = BOARD_H_MM + 4.8 mm
    for c in range(1, COLS + 1):
        hx, _ = get_hole_coords_svg(c, 1, mirrored)
        col_name = f'C{c:02d}'
        if c % 2 == 1:
            lbl_y = BOARD_H_MM + 4.8
            svg.append(f'  <line x1="{hx:.3f}" y1="{BOARD_H_MM}" x2="{hx:.3f}" y2="{lbl_y - 1.0:.3f}" class="guide-line" />')
        else:
            lbl_y = BOARD_H_MM + 1.8
            svg.append(f'  <line x1="{hx:.3f}" y1="{BOARD_H_MM}" x2="{hx:.3f}" y2="{lbl_y - 0.9:.3f}" class="ruler-tick" />')
        svg.append(f'  <text x="{hx:.3f}" y="{lbl_y:.3f}" class="label-axis">{col_name}</text>')

    # Row Labels (R01 to R28) on Left & Right
    for r in range(1, ROWS + 1):
        _, hy = get_hole_coords_svg(1, r, mirrored)
        row_name = f'R{r:02d}'
        svg.append(f'  <text x="{-1.2:.3f}" y="{hy:.3f}" class="label-axis" style="text-anchor: end; font-size: 0.95px;">{row_name}</text>')
        svg.append(f'  <text x="{BOARD_W_MM + 1.2:.3f}" y="{hy:.3f}" class="label-axis" style="text-anchor: start; font-size: 0.95px;">{row_name}</text>')

    svg.append('</g>') # close board group

    # Header Title
    title_text = "STRIPBOARD CUT TEMPLATE" if mode == "cuts" else "BOARD RULER &amp; ALIGNMENT INDICATOR"
    sub_text = "BOTTOM (DRILL / COPPER SIDE) - MIRRORED" if mirrored else "TOP (COMPONENT SIDE) - 1:1 TRUE SCALE"
    if mode == "cuts" and not mirrored:
        sub_text += " [ALL CUTS IN RED]"

    svg.append(f'<text x="{total_w/2:.2f}" y="4.2" class="title">{title_text}</text>')
    svg.append(f'<text x="{total_w/2:.2f}" y="7.0" class="subtitle">{sub_text} | Exact: {BOARD_W_MM:.0f} mm x {BOARD_H_MM:.0f} mm</text>')

    svg.append('</svg>')

    with open(filename, 'w') as f:
        f.write('\n'.join(svg))
    print(f"Generated SVG: {filename}")

def generate_pdf():
    """
    Generate 1:1 exact scale printable A4 PDF with calibration checks and staggered labels.
    """
    pdf_filename = "docs/templates/stripboard_1to1_printout.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=A4)
    page_w, page_h = A4

    # Title Banner
    c.setFont("Helvetica-Bold", 13)
    c.drawString(18*mm, page_h - 15*mm, "Custom PC Fan Controller - 1:1 Scale Board Printout Templates")
    c.setFont("Helvetica", 8.5)
    c.setFillColor(colors.HexColor("#333333"))
    c.drawString(18*mm, page_h - 20*mm, "Precise Physical Size: 33.0 mm x 72.0 mm | Standard 2.54 mm (0.1\") Grid Pitch | 12 Columns x 28 Rows")
    c.drawString(18*mm, page_h - 24*mm, "Print Settings: Select 'Actual Size' or 100% scale (NO 'Fit to page'). Verify with calibration ruler below.")

    # 100 mm Calibration Ruler
    ruler_x = 18*mm
    ruler_y = page_h - 35*mm
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.8)
    c.line(ruler_x, ruler_y, ruler_x + 100*mm, ruler_y)
    for mm_i in range(101):
        tick_h = 4*mm if mm_i % 10 == 0 else (2.5*mm if mm_i % 5 == 0 else 1.5*mm)
        c.line(ruler_x + mm_i*mm, ruler_y, ruler_x + mm_i*mm, ruler_y + tick_h)
        if mm_i % 10 == 0:
            c.setFont("Helvetica", 6)
            c.drawCentredString(ruler_x + mm_i*mm, ruler_y + tick_h + 1.2*mm, f"{mm_i//10} cm")
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(ruler_x + 104*mm, ruler_y + 1*mm, "<-- Exactly 100 mm (Measure with physical ruler)")

    # Function to draw a 1:1 board on PDF
    def draw_board(origin_x, origin_y, mode="cuts", mirrored=False, title=""):
        c.saveState()
        c.translate(origin_x, origin_y)

        # Title above template
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(colors.black)
        c.drawCentredString(BOARD_W_MM*mm / 2.0, BOARD_H_MM*mm + 14*mm, title)
        c.setFont("Helvetica", 6.8)
        c.setFillColor(colors.HexColor("#555555"))
        subtitle = "BOTTOM (DRILL SIDE) - MIRRORED" if mirrored else "TOP (ALIGNMENT / RULER) - 1:1"
        c.drawCentredString(BOARD_W_MM*mm / 2.0, BOARD_H_MM*mm + 10.5*mm, subtitle)

        # Board Boundary
        c.setStrokeColor(colors.HexColor("#000000"))
        c.setLineWidth(0.6)
        c.setFillColor(colors.HexColor("#fdfaf2"))
        c.rect(0, 0, BOARD_W_MM*mm, BOARD_H_MM*mm, fill=1, stroke=1)

        # Millimeter ticks on board border
        c.setStrokeColor(colors.HexColor("#333333"))
        c.setLineWidth(0.2)
        for mm_i in range(int(BOARD_H_MM) + 1):
            t_len = 1.2*mm if mm_i % 10 == 0 else (0.8*mm if mm_i % 5 == 0 else 0.5*mm)
            c.line(0, mm_i*mm, t_len, mm_i*mm)
            c.line(BOARD_W_MM*mm - t_len, mm_i*mm, BOARD_W_MM*mm, mm_i*mm)

        for mm_i in range(int(BOARD_W_MM) + 1):
            t_len = 1.2*mm if mm_i % 10 == 0 else (0.8*mm if mm_i % 5 == 0 else 0.5*mm)
            c.line(mm_i*mm, 0, mm_i*mm, t_len)
            c.line(mm_i*mm, BOARD_H_MM*mm - t_len, mm_i*mm, BOARD_H_MM*mm)

        # Dimension labels
        c.setFont("Helvetica", 5.5)
        c.setFillColor(colors.HexColor("#666666"))
        c.drawCentredString(BOARD_W_MM*mm / 2.0, BOARD_H_MM*mm + 0.8*mm, "33.0 mm")
        c.drawString(BOARD_W_MM*mm + 1.2*mm, BOARD_H_MM*mm / 2.0, "72.0 mm")

        # Copper tracks
        track_w = 1.9 * mm
        pad_r = 1.05 * mm

        if mode == "cuts":
            c.setFillColor(colors.HexColor("#e6b87d"))
            c.setStrokeColor(colors.HexColor("#c99355"))
            c.setLineWidth(0.2)

            # Row 1 Top rail (R01 at top of board)
            x1, y1 = get_hole_coords_pdf(1, 1, mirrored)
            x2, y2 = get_hole_coords_pdf(12, 1, mirrored)
            xmin, xmax = min(x1, x2)*mm, max(x1, x2)*mm
            c.rect(xmin - pad_r, y1*mm - track_w/2, (xmax - xmin) + 2*pad_r, track_w, fill=1, stroke=1)

            # Vertical rails
            for col in [1, 6, 7, 12]:
                x_top, y_top = get_hole_coords_pdf(col, 2, mirrored)
                x_bot, y_bot = get_hole_coords_pdf(col, 28, mirrored)
                ymin, ymax = min(y_top, y_bot)*mm, max(y_top, y_bot)*mm
                c.rect(x_top*mm - track_w/2, ymin - pad_r, track_w, (ymax - ymin) + 2*pad_r, fill=1, stroke=1)

            # Horizontal 4-hole strips
            for r in range(2, 27):
                x1, y1 = get_hole_coords_pdf(2, r, mirrored)
                x2, y2 = get_hole_coords_pdf(5, r, mirrored)
                xmin, xmax = min(x1, x2)*mm, max(x1, x2)*mm
                c.rect(xmin - pad_r, y1*mm - track_w/2, (xmax - xmin) + 2*pad_r, track_w, fill=1, stroke=1)

                x3, y3 = get_hole_coords_pdf(8, r, mirrored)
                x4, y4 = get_hole_coords_pdf(11, r, mirrored)
                xmin, xmax = min(x3, x4)*mm, max(x3, x4)*mm
                c.rect(xmin - pad_r, y3*mm - track_w/2, (xmax - xmin) + 2*pad_r, track_w, fill=1, stroke=1)

            # Vertical 2-hole pairs
            for col in [2, 3, 4, 5, 8, 9, 10, 11]:
                x_top, y_top = get_hole_coords_pdf(col, 27, mirrored)
                x_bot, y_bot = get_hole_coords_pdf(col, 28, mirrored)
                ymin, ymax = min(y_top, y_bot)*mm, max(y_top, y_bot)*mm
                c.rect(x_top*mm - track_w/2, ymin - pad_r, track_w, (ymax - ymin) + 2*pad_r, fill=1, stroke=1)

        # Holes
        for r in range(1, ROWS + 1):
            for col in range(1, COLS + 1):
                hx, hy = get_hole_coords_pdf(col, r, mirrored)
                c.setFillColor(colors.white)
                c.setStrokeColor(colors.HexColor("#333333"))
                c.setLineWidth(0.25)
                c.circle(hx*mm, hy*mm, 0.55*mm, fill=1, stroke=1)
                # Crosshair
                c.setStrokeColor(colors.HexColor("#777777"))
                c.setLineWidth(0.12)
                c.line(hx*mm - 0.28*mm, hy*mm, hx*mm + 0.28*mm, hy*mm)
                c.line(hx*mm, hy*mm - 0.28*mm, hx*mm, hy*mm + 0.28*mm)

        # Red Cuts
        if mode == "cuts":
            cuts = [
                (12, 16),
                (2.5, 21),
                (3.5, 24),
                (2, 27.5),
                (4, 27.5),
                (8, 27.5),
                (10, 27.5),
            ]
            for c_val, r_val in cuts:
                if mirrored:
                    c_idx = (COLS - c_val)
                else:
                    c_idx = (c_val - 1)
                cx = (MARGIN_X_MM + c_idx * PITCH_MM) * mm
                cy = (BOARD_H_MM - (MARGIN_Y_MM + (r_val - 1) * PITCH_MM)) * mm
                sz = 1.8 * mm

                c.setFillColor(colors.HexColor("#ff1111"))
                c.setStrokeColor(colors.HexColor("#880000"))
                c.setLineWidth(0.35)
                c.rect(cx - sz/2, cy - sz/2, sz, sz, fill=1, stroke=1)

                c.setStrokeColor(colors.white)
                c.setLineWidth(0.45)
                c.line(cx - sz*0.35, cy - sz*0.35, cx + sz*0.35, cy + sz*0.35)
                c.line(cx + sz*0.35, cy - sz*0.35, cx - sz*0.35, cy + sz*0.35)

        # STAGGERED / ALTERNATING COLUMN LABELS (C01, C03... / C02, C04...)
        c.setFont("Helvetica-Bold", 4.5)
        c.setFillColor(colors.HexColor("#000000"))

        # Top Staggered Labels:
        # Odd cols: y = +5.2 mm, Even cols: y = +2.2 mm
        for col in range(1, COLS + 1):
            hx, _ = get_hole_coords_pdf(col, 1, mirrored)
            col_name = f"C{col:02d}"
            if col % 2 == 1:
                lbl_y = BOARD_H_MM*mm + 5.5*mm
                c.setStrokeColor(colors.HexColor("#666666"))
                c.setLineWidth(0.18)
                c.line(hx*mm, BOARD_H_MM*mm, hx*mm, lbl_y - 1.2*mm)
            else:
                lbl_y = BOARD_H_MM*mm + 2.2*mm
                c.setStrokeColor(colors.black)
                c.setLineWidth(0.25)
                c.line(hx*mm, BOARD_H_MM*mm, hx*mm, lbl_y - 1.0*mm)
            c.drawCentredString(hx*mm, lbl_y, col_name)

        # Bottom Staggered Labels:
        # Even cols: y = -2.2 mm, Odd cols: y = -5.5 mm
        for col in range(1, COLS + 1):
            hx, _ = get_hole_coords_pdf(col, 1, mirrored)
            col_name = f"C{col:02d}"
            if col % 2 == 1:
                lbl_y = -5.5*mm
                c.setStrokeColor(colors.HexColor("#666666"))
                c.setLineWidth(0.18)
                c.line(hx*mm, 0, hx*mm, lbl_y + 1.8*mm)
            else:
                lbl_y = -2.2*mm
                c.setStrokeColor(colors.black)
                c.setLineWidth(0.25)
                c.line(hx*mm, 0, hx*mm, lbl_y + 1.5*mm)
            c.drawCentredString(hx*mm, lbl_y, col_name)

        # Row Labels (R01 to R28) on Left & Right
        c.setFont("Helvetica-Bold", 3.8)
        for r in range(1, ROWS + 1):
            _, hy = get_hole_coords_pdf(1, r, mirrored)
            c.drawRightString(-1.4*mm, hy*mm - 1.2, f"R{r:02d}")
            c.drawString(BOARD_W_MM*mm + 1.4*mm, hy*mm - 1.2, f"R{r:02d}")

        c.restoreState()

    # Place 3 templates side by side on A4 page
    base_y = 75 * mm
    draw_board(18*mm, base_y, mode="ruler", mirrored=False, title="1. Physical Ruler & Alignment")
    draw_board(80*mm, base_y, mode="cuts", mirrored=False, title="2. Cut Guide (Component View)")
    draw_board(142*mm, base_y, mode="cuts", mirrored=True, title="3. Drill Guide (Copper/Bottom)")

    # Bottom Instructions & Legend Box
    c.setStrokeColor(colors.HexColor("#aaaaaa"))
    c.setLineWidth(0.5)
    c.setFillColor(colors.HexColor("#f8f9fa"))
    c.rect(18*mm, 10*mm, 174*mm, 52*mm, fill=1, stroke=1)

    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(colors.black)
    c.drawString(22*mm, 55*mm, "How to Use These 1:1 Scale Printout Templates:")

    c.setFont("Helvetica", 7.5)
    c.setFillColor(colors.HexColor("#333333"))
    instructions = [
        "1. Physical Verification: Place your physical 33.0 x 72.0 mm protoboard directly over Template 1. The outer black border and all hole crosshairs must line up exactly.",
        "2. Staggered Column Labels: Column IDs are alternated (C01, C03... / C02, C04...) so every column is clear, distinct, and easy to read.",
        "3. Top View Reference: Template 2 shows the internal copper tracks and all 7 required track cuts highlighted as RED squares with white crosses.",
        "4. Drill Guide (Mirrored): Template 3 is flipped horizontally! When turning the board over to drill the copper side, use Template 3 so cuts match what you see.",
        "5. How to Cut Tracks: Place the tip of a 3.0 mm or 3.5 mm drill bit into the red marked position and gently twist by hand until the copper foil is cleanly severed.",
        "6. Continuity Check: With a multimeter in continuity mode, verify 0 ohms across the track before cutting and infinite resistance (open circuit) after cutting.",
    ]
    for i, line in enumerate(instructions):
        c.drawString(22*mm, 49*mm - i*5*mm, line)

    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(22*mm, 18*mm, "Cut Locations:")
    c.setFont("Helvetica", 7)
    c.drawString(45*mm, 18*mm, "Cut 1: R16/C12 (+5V/+12V split) | Cut 2: R21 between C02 and C03 (DTR cap) | Cut 3: R24 between C03 and C04 (VCC/GND split)")
    c.drawString(45*mm, 14*mm, "Cut 4: C02 between R27 and R28 (Fan 1) | Cut 5: C04 between R27 and R28 (Fan 2) | Cut 6: C08 between R27 and R28 (Fan 3) | Cut 7: C10 between R27 and R28 (Fan 4)")

    c.showPage()
    c.save()
    print(f"Generated PDF: {pdf_filename}")

if __name__ == "__main__":
    generate_svg("docs/templates/board_ruler_indicator.svg", mode="ruler", mirrored=False)
    generate_svg("docs/templates/board_cuts_top_view.svg", mode="cuts", mirrored=False)
    generate_svg("docs/templates/board_cuts_bottom_drill_view.svg", mode="cuts", mirrored=True)
    generate_pdf()
