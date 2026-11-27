#!/usr/bin/env python3
"""
generate_rev1.0_4pin_assembly_guide.py
Generates a complete, comprehensive, 4-Page PDF Assembly Guide & 1:1 Printable Template
for Custom Stripboard Rev 1.0 (33.0 x 72.0 mm / 27 Physical Rows x 12 Columns)
configured for 4-Pin Akasa DFC9225120 PWM Fan Coolers and HW-597B V2.1 USB-TTL module.

Pages:
1. 1:1 Printable Templates (Top Component Assembly & Mirrored Bottom Solder/Drill with cuts)
2. Enlarged Color Wiring & Component Assembly Diagram
3. Complete Wire Jumpers Schedule, Cuts Table & Pinout Map
4. Step-by-Step Assembly Instructions & Quality Checklist
"""

import os
import subprocess
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

# Geometry for Rev 1.0 Stripboard
BOARD_W_MM = 33.0
BOARD_H_MM = 70.0  # 27 rows @ 2.54mm = 66.04mm grid, centered in ~70mm board
COLS = 12
ROWS = 27
PITCH_MM = 2.54

GRID_W_MM = (COLS - 1) * PITCH_MM  # 27.94 mm
GRID_H_MM = (ROWS - 1) * PITCH_MM  # 66.04 mm
MARGIN_X_MM = (BOARD_W_MM - GRID_W_MM) / 2.0  # 2.53 mm
MARGIN_Y_MM = (BOARD_H_MM - GRID_H_MM) / 2.0  # 1.98 mm

def get_hole_coords(col, row, ox, oy, bh, mirrored=False):
    """
    Returns ReportLab (x, y) on canvas in pt/mm.
    col: 1..12
    row: 1..27 (R01 at top, R27 at bottom)
    """
    if mirrored:
        c_idx = COLS - col
    else:
        c_idx = col - 1
    r_idx = row - 1
    x = ox + (MARGIN_X_MM + c_idx * PITCH_MM) * mm
    y = oy + bh - (MARGIN_Y_MM + r_idx * PITCH_MM) * mm
    return x, y

def draw_header_footer(c, page_num, total_pages, title, subtitle):
    c.saveState()
    # Header
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(colors.HexColor("#1b5e20"))
    c.drawString(20 * mm, 282 * mm, "FAN CONTROLLER • REV 1.0 (AKASA 4-PIN PWM & HW-597B)")
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.HexColor("#555555"))
    c.drawRightString(190 * mm, 282 * mm, "Stripboard Assembly & Verification Guide")
    c.setStrokeColor(colors.HexColor("#4caf50"))
    c.setLineWidth(1)
    c.line(20 * mm, 279 * mm, 190 * mm, 279 * mm)

    # Title & Subtitle banner
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.HexColor("#212121"))
    c.drawString(20 * mm, 271 * mm, title)
    c.setFont("Helvetica-Oblique", 8.5)
    c.setFillColor(colors.HexColor("#616161"))
    c.drawString(20 * mm, 266 * mm, subtitle)

    # Footer
    c.setStrokeColor(colors.HexColor("#e0e0e0"))
    c.setLineWidth(0.5)
    c.line(20 * mm, 14 * mm, 190 * mm, 14 * mm)
    c.setFont("Helvetica", 7.5)
    c.setFillColor(colors.HexColor("#757575"))
    c.drawString(20 * mm, 10 * mm, "Plataforma Stripboard Rev 1.0 (27 Linhas x 12 Colunas) • ATmega328P-PU Standalone @ 16 MHz")
    c.drawRightString(190 * mm, 10 * mm, f"Página {page_num} de {total_pages}")
    c.restoreState()

def draw_calibration_ruler(c, x, y):
    c.saveState()
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.5)
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 6)

    # 50mm ruler
    c.rect(x, y, 50 * mm, 4 * mm, fill=0, stroke=1)
    for i in range(51):
        h = 4 * mm if (i % 10 == 0) else (2.5 * mm if (i % 5 == 0) else 1.5 * mm)
        c.line(x + i * mm, y, x + i * mm, y + h)
        if i % 10 == 0:
            c.drawCentredString(x + i * mm, y + 5 * mm, f"{i}mm")
    c.setFont("Helvetica", 6.5)
    c.drawString(x, y - 4 * mm, "Aferição de Escala: 50 mm exatos (Verificar com régua física antes de cortar)")
    c.restoreState()

# =========================================================================
# PAGE 1: 1:1 Scale Printable Sheet
# =========================================================================
def build_page_1(c):
    draw_header_footer(c, 1, 4,
                       "1. Gabarito em Escala Real 1:1 para Impressão Direta (A4)",
                       "Configuração de impressão: 'Tamanho Real' ou 'Escala 100%' (NÃO usar 'Ajustar à página')")

    # Center two templates side by side
    # Board dimensions: 33.0 mm x 70.0 mm
    bw = BOARD_W_MM * mm
    bh = BOARD_H_MM * mm

    y_pos = 175 * mm
    x_top = 35 * mm
    x_bot = 115 * mm

    # Top View Template Label
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(colors.HexColor("#1b5e20"))
    c.drawCentredString(x_top + bw / 2.0, y_pos + bh + 8 * mm, "VISTA SUPERIOR (COMPONENTES)")
    c.setFont("Helvetica", 7)
    c.setFillColor(colors.HexColor("#424242"))
    c.drawCentredString(x_top + bw / 2.0, y_pos + bh + 4 * mm, "Escala 1:1 (Lado dos Componentes / Serigrafia)")

    # Bottom View Template Label
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(colors.HexColor("#b71c1c"))
    c.drawCentredString(x_bot + bw / 2.0, y_pos + bh + 8 * mm, "VISTA INFERIOR ESPELHADA (COBRE)")
    c.setFont("Helvetica", 7)
    c.setFillColor(colors.HexColor("#424242"))
    c.drawCentredString(x_bot + bw / 2.0, y_pos + bh + 4 * mm, "Escala 1:1 (Lado do Cobre / Guia de Cortes e Furação)")

    # Helper function to render a 1:1 board outline and pads
    def draw_board_base(ox, oy, mirrored=False):
        c.saveState()
        # Board contour
        c.setStrokeColor(colors.HexColor("#2e7d32") if not mirrored else colors.HexColor("#c62828"))
        c.setLineWidth(0.8)
        c.setFillColor(colors.HexColor("#e8f5e9") if not mirrored else colors.HexColor("#ffebee"))
        c.roundRect(ox, oy, bw, bh, 1.5 * mm, fill=1, stroke=1)

        # Rails lines
        c.setLineWidth(0.3)
        c.setStrokeColor(colors.HexColor("#a5d6a7") if not mirrored else colors.HexColor("#ef9a9a"))
        # Vertical rails: C01, C06, C07, C12
        for col in [1, 6, 7, 12]:
            hx1, hy1 = get_hole_coords(col, 1, ox, oy, bh, mirrored)
            hx2, hy2 = get_hole_coords(col, 27, ox, oy, bh, mirrored)
            c.line(hx1, hy1, hx2, hy2)

        # Horizontal strips (Left bank C02..C05, Right bank C08..C11)
        for r in range(1, 28):
            # Left bank
            hx1, hy1 = get_hole_coords(2, r, ox, oy, bh, mirrored)
            hx2, hy2 = get_hole_coords(5, r, ox, oy, bh, mirrored)
            c.line(hx1, hy1, hx2, hy2)
            # Right bank
            hx3, hy3 = get_hole_coords(8, r, ox, oy, bh, mirrored)
            hx4, hy4 = get_hole_coords(11, r, ox, oy, bh, mirrored)
            c.line(hx3, hy3, hx4, hy4)

        # Holes pads
        c.setFillColor(colors.white)
        c.setStrokeColor(colors.HexColor("#333333"))
        c.setLineWidth(0.2)
        for r in range(1, 28):
            for col in range(1, 13):
                hx, hy = get_hole_coords(col, r, ox, oy, bh, mirrored)
                c.circle(hx, hy, 0.45 * mm, fill=1, stroke=1)

        c.restoreState()

    # Draw bases
    draw_board_base(x_top, y_pos, mirrored=False)
    draw_board_base(x_bot, y_pos, mirrored=True)

    # ---------------- Overlay Top View Elements ----------------
    c.saveState()
    # ATmega328P Outline (Rows 4 to 17)
    ic_x1, ic_y_top = get_hole_coords(5, 4, x_top, y_pos, bh, mirrored=False)
    ic_x2, ic_y_bot = get_hole_coords(8, 17, x_top, y_pos, bh, mirrored=False)
    ic_w = (ic_x2 - ic_x1) + 2.54 * mm
    ic_h = (ic_y_top - ic_y_bot) + 2.54 * mm
    c.setStrokeColor(colors.HexColor("#1b5e20"))
    c.setFillColor(colors.HexColor("#2e7d32"))
    c.roundRect(ic_x1 - 1.27 * mm, ic_y_bot - 1.27 * mm, ic_w, ic_h, 1.0 * mm, fill=0, stroke=1)
    c.setFont("Helvetica-Bold", 5)
    c.setFillColor(colors.HexColor("#1b5e20"))
    c.drawCentredString(ic_x1 + ic_w / 2.0 - 1.27 * mm, ic_y_bot + ic_h / 2.0 - 1.27 * mm, "ATmega328P (DIP-28)")

    # 4 Fan Connectors (Rows 20..23)
    c.setFont("Helvetica-Bold", 4.5)
    c.setFillColor(colors.HexColor("#0d47a1"))
    c.setStrokeColor(colors.HexColor("#1565c0"))
    for f_name, col in [("F1", 2), ("F2", 5), ("F3", 8), ("F4", 11)]:
        fx, fy_top = get_hole_coords(col, 20, x_top, y_pos, bh, mirrored=False)
        _, fy_bot = get_hole_coords(col, 23, x_top, y_pos, bh, mirrored=False)
        fh = fy_top - fy_bot + 2.0 * mm
        c.rect(fx - 1.0 * mm, fy_bot - 1.0 * mm, 2.0 * mm, fh, fill=0, stroke=1)
        c.drawCentredString(fx, fy_bot - 2.5 * mm, f_name)

    # HW-597 Socket Header (Row 27, Cols 1..6)
    hw_x1, hw_y = get_hole_coords(1, 27, x_top, y_pos, bh, mirrored=False)
    hw_x2, _ = get_hole_coords(6, 27, x_top, y_pos, bh, mirrored=False)
    c.setStrokeColor(colors.HexColor("#e65100"))
    c.rect(hw_x1 - 1.0 * mm, hw_y - 1.0 * mm, (hw_x2 - hw_x1) + 2.0 * mm, 2.0 * mm, fill=0, stroke=1)
    c.setFont("Helvetica-Bold", 4.5)
    c.setFillColor(colors.HexColor("#e65100"))
    c.drawString(hw_x1, hw_y - 3.0 * mm, "HW-597B (SIP-6)")

    # Floppy 4-Pin Power Header (Row 27, Cols 8..11)
    flp_x1, flp_y = get_hole_coords(8, 27, x_top, y_pos, bh, mirrored=False)
    flp_x2, _ = get_hole_coords(11, 27, x_top, y_pos, bh, mirrored=False)
    c.setStrokeColor(colors.HexColor("#c62828"))
    c.rect(flp_x1 - 1.0 * mm, flp_y - 1.0 * mm, (flp_x2 - flp_x1) + 2.0 * mm, 2.0 * mm, fill=0, stroke=1)
    c.setFont("Helvetica-Bold", 4.5)
    c.setFillColor(colors.HexColor("#c62828"))
    c.drawString(flp_x1, flp_y - 3.0 * mm, "FLOPPY 4P PWR")
    c.restoreState()

    # ---------------- Overlay Bottom View Cuts ----------------
    c.saveState()
    # Draw CUTS with prominent RED X and text
    c.setStrokeColor(colors.HexColor("#d50000"))
    c.setLineWidth(1.2)
    c.setFillColor(colors.HexColor("#d50000"))
    c.setFont("Helvetica-Bold", 5)

    # Cut 1: Col 7, Row 19
    c1_x, c1_y = get_hole_coords(7, 19, x_bot, y_pos, bh, mirrored=True)
    c.line(c1_x - 1.5 * mm, c1_y - 1.5 * mm, c1_x + 1.5 * mm, c1_y + 1.5 * mm)
    c.line(c1_x - 1.5 * mm, c1_y + 1.5 * mm, c1_x + 1.5 * mm, c1_y - 1.5 * mm)
    c.drawString(c1_x + 2.0 * mm, c1_y - 1.0 * mm, "CORTE 1 (C07 R19)")

    # Cut 2: Between C03 & C04, Rows 20 & 21
    c2_x1, c2_y1 = get_hole_coords(3, 20, x_bot, y_pos, bh, mirrored=True)
    c2_x2, _ = get_hole_coords(4, 20, x_bot, y_pos, bh, mirrored=True)
    mid2_x = (c2_x1 + c2_x2) / 2.0
    _, c2_y2 = get_hole_coords(3, 21, x_bot, y_pos, bh, mirrored=True)
    c.rect(mid2_x - 0.4 * mm, c2_y2 - 0.8 * mm, 0.8 * mm, (c2_y1 - c2_y2) + 1.6 * mm, fill=1, stroke=0)
    c.drawRightString(mid2_x - 1.5 * mm, (c2_y1 + c2_y2)/2.0 - 1.0 * mm, "CORTE 2 (R20-21)")

    # Cut 3: Between C09 & C10, Rows 20 & 21
    c3_x1, c3_y1 = get_hole_coords(9, 20, x_bot, y_pos, bh, mirrored=True)
    c3_x2, _ = get_hole_coords(10, 20, x_bot, y_pos, bh, mirrored=True)
    mid3_x = (c3_x1 + c3_x2) / 2.0
    _, c3_y2 = get_hole_coords(9, 21, x_bot, y_pos, bh, mirrored=True)
    c.rect(mid3_x - 0.4 * mm, c3_y2 - 0.8 * mm, 0.8 * mm, (c3_y1 - c3_y2) + 1.6 * mm, fill=1, stroke=0)
    c.drawString(mid3_x + 1.5 * mm, (c3_y1 + c3_y2)/2.0 - 1.0 * mm, "CORTE 3 (R20-21)")

    c.restoreState()

    # Calibration Ruler & Printing instructions
    draw_calibration_ruler(c, 25 * mm, 148 * mm)

    # Lower Panel: Summary Quick Reference
    c.saveState()
    c.setFillColor(colors.HexColor("#f5f5f5"))
    c.setStrokeColor(colors.HexColor("#e0e0e0"))
    c.roundRect(20 * mm, 20 * mm, 170 * mm, 118 * mm, 2 * mm, fill=1, stroke=1)

    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(colors.HexColor("#1b5e20"))
    c.drawString(25 * mm, 130 * mm, "GUIA RÁPIDO DE IDENTIFICAÇÃO DAS 27 LINHAS E 12 COLUNAS")

    c.setFont("Helvetica", 8)
    c.setFillColor(colors.HexColor("#333333"))
    text_lines = [
        "• Dimensões Físicas: 33.0 mm de largura x 70.0 mm de comprimento (12 colunas x 27 linhas com passo padrão 2.54 mm / 100 mil).",
        "• Colunas: C01 (Trilha Aux 1), C02..C05 (Banco Esquerdo), C06 (Barramento GND), C07 (Barramento +12V), C08..C11 (Banco Direito), C12 (Aux 2).",
        "• Linhas 01 a 03: Livres / Área de folga superior.",
        "• Linhas 04 a 17: Soquete DIP-28 do microcontrolador ATmega328P-PU montado atravessando a fenda central.",
        "  - Lado Esquerdo (C05): Pinos 1 (/RESET na R04) até 14 (PB0 na R17).",
        "  - Lado Direito (C08): Pinos 15 (PB1 na R17) até 28 (PC5 na R04).",
        "• Linha 19: Corte na Coluna 7 (isola a parte superior da parte inferior da linha de +12V).",
        "• Linhas 20 e 21: Réguas de sinal PWM (R20) e Tacômetro TACH (R21), divididas em 4 canais de 2 ilhas cada pelos Cortes 2 e 3.",
        "• Linha 22: Barramento de +12V para os 4 coolers (alimentado diretamente pelo jumper WJ em R22C07).",
        "• Linha 23: Barramento de GND para os 4 coolers (alimentado diretamente pelo jumper WJ em R23C06).",
        "• Linhas 26 e 27: Conectadas verticalmente nas colunas 2, 3, 4, 5 e 8, 9, 10, 11.",
        "• Linha 27: Barra fêmea SIP-6 para conexão do módulo USB-Serial HW-597B V2.1 (CH340G).",
        "  - R27C01: +5V  |  R27C02: VCC (Jumper)  |  R27C03: +3.3V  |  R27C04: TxD  |  R27C05: RxD  |  R27C06: GND"
    ]
    cur_y = 122 * mm
    for tl in text_lines:
        c.drawString(25 * mm, cur_y, tl)
        cur_y -= 6.2 * mm

    c.restoreState()
    c.showPage()

# =========================================================================
# PAGE 2: Enlarged Visual Assembly & Wiring Diagram
# =========================================================================
def build_page_2(c):
    draw_header_footer(c, 2, 4,
                       "2. Diagrama Visual Ampliado de Montagem e Roteamento",
                       "Posicionamento detalhado do ATmega328P, conectores, cortes e rotas dos Wire Jumpers")

    # Enlarged Stripboard visualization (scale factor ~2.2x)
    # Centered on left side
    scale = 2.0
    ox = 32 * mm
    oy = 24 * mm
    bw = BOARD_W_MM * scale * mm
    bh = BOARD_H_MM * scale * mm

    def get_hole_coords_p2(col, row):
        c_idx = col - 1
        r_idx = row - 1
        x = ox + (MARGIN_X_MM + c_idx * PITCH_MM) * scale * mm
        y = oy + bh - (MARGIN_Y_MM + r_idx * PITCH_MM) * scale * mm
        return x, y

    c.saveState()
    # Board base
    c.setFillColor(colors.HexColor("#1b3e2b")) # Solder mask dark green
    c.setStrokeColor(colors.HexColor("#0d2417"))
    c.setLineWidth(1)
    c.roundRect(ox, oy, bw, bh, 3 * mm, fill=1, stroke=1)

    # Prototyping copper strips (horizontal)
    c.setFillColor(colors.HexColor("#2a593e"))
    c.setStrokeColor(colors.HexColor("#1b3e2b"))
    c.setLineWidth(0.5)
    for r in range(1, 28):
        # Left bank
        x1, y1 = get_hole_coords_p2(2, r)
        x2, _ = get_hole_coords_p2(5, r)
        c.roundRect(x1 - 1.2 * scale * mm, y1 - 1.0 * scale * mm, (x2 - x1) + 2.4 * scale * mm, 2.0 * scale * mm, 0.5 * mm, fill=1, stroke=1)
        # Right bank
        x3, _ = get_hole_coords_p2(8, r)
        x4, _ = get_hole_coords_p2(11, r)
        c.roundRect(x3 - 1.2 * scale * mm, y1 - 1.0 * scale * mm, (x4 - x3) + 2.4 * scale * mm, 2.0 * scale * mm, 0.5 * mm, fill=1, stroke=1)

    # Vertical rails: C01, C06, C07, C12
    for col in [1, 6, 7, 12]:
        x1, y_top = get_hole_coords_p2(col, 1)
        _, y_bot = get_hole_coords_p2(col, 27)
        c.roundRect(x1 - 1.0 * scale * mm, y_bot - 1.2 * scale * mm, 2.0 * scale * mm, (y_top - y_bot) + 2.4 * scale * mm, 0.5 * mm, fill=1, stroke=1)

    # Pads & Holes
    c.setFont("Helvetica", 4.5)
    for r in range(1, 28):
        for col in range(1, 13):
            hx, hy = get_hole_coords_p2(col, r)
            c.setFillColor(colors.HexColor("#e5a95d")) # Gold copper pad
            c.circle(hx, hy, 0.8 * scale * mm, fill=1, stroke=0)
            c.setFillColor(colors.HexColor("#111111")) # Hole
            c.circle(hx, hy, 0.35 * scale * mm, fill=1, stroke=0)

    # Axis Labels
    c.setFont("Helvetica-Bold", 6.5)
    c.setFillColor(colors.white)
    # Column labels top
    for col in range(1, 13):
        hx, _ = get_hole_coords_p2(col, 1)
        c.drawCentredString(hx, oy + bh + 3.0 * mm, f"C{col:02d}")
    # Row labels left and right
    for r in range(1, 28):
        _, hy = get_hole_coords_p2(1, r)
        c.drawRightString(ox - 2.5 * mm, hy - 0.8 * mm, f"R{r:02d}")
        c.drawString(ox + bw + 2.5 * mm, hy - 0.8 * mm, f"R{r:02d}")

    # Cuts visualization
    c.setStrokeColor(colors.HexColor("#ff1744"))
    c.setFillColor(colors.HexColor("#ff1744"))
    c.setLineWidth(1.5)
    # Cut 1: C07 R19
    c1x, c1y = get_hole_coords_p2(7, 19)
    c.line(c1x - 2.5 * mm, c1y - 2.5 * mm, c1x + 2.5 * mm, c1y + 2.5 * mm)
    c.line(c1x - 2.5 * mm, c1y + 2.5 * mm, c1x + 2.5 * mm, c1y - 2.5 * mm)
    # Cut 2: R20-21 between C03 & C04
    c2x1, c2y1 = get_hole_coords_p2(3, 20)
    c2x2, _ = get_hole_coords_p2(4, 20)
    _, c2y2 = get_hole_coords_p2(3, 21)
    c.rect((c2x1+c2x2)/2.0 - 0.8 * mm, c2y2 - 1.2 * mm, 1.6 * mm, (c2y1 - c2y2) + 2.4 * mm, fill=1, stroke=0)
    # Cut 3: R20-21 between C09 & C10
    c3x1, c3y1 = get_hole_coords_p2(9, 20)
    c3x2, _ = get_hole_coords_p2(10, 20)
    _, c3y2 = get_hole_coords_p2(9, 21)
    c.rect((c3x1+c3x2)/2.0 - 0.8 * mm, c3y2 - 1.2 * mm, 1.6 * mm, (c3y1 - c3y2) + 2.4 * mm, fill=1, stroke=0)

    # ---------------- Draw IC ATmega328P Body ----------------
    ic_x1, ic_y_top = get_hole_coords_p2(5, 4)
    ic_x2, ic_y_bot = get_hole_coords_p2(8, 17)
    ic_w = (ic_x2 - ic_x1) + 2.54 * scale * mm
    ic_h = (ic_y_top - ic_y_bot) + 2.54 * scale * mm
    c.setFillColor(colors.HexColor("#263238"))
    c.setStrokeColor(colors.HexColor("#37474f"))
    c.roundRect(ic_x1 - 1.27 * scale * mm, ic_y_bot - 1.27 * scale * mm, ic_w, ic_h, 2.0 * mm, fill=1, stroke=1)
    # Notch on top
    c.setFillColor(colors.HexColor("#1b3e2b"))
    c.circle(ic_x1 - 1.27 * scale * mm + ic_w / 2.0, ic_y_top + 1.27 * scale * mm, 2.5 * mm, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(colors.white)
    c.drawCentredString(ic_x1 - 1.27 * scale * mm + ic_w / 2.0, ic_y_bot + ic_h / 2.0, "ATmega328P-PU")
    c.setFont("Helvetica", 6)
    c.setFillColor(colors.HexColor("#90a4ae"))
    c.drawCentredString(ic_x1 - 1.27 * scale * mm + ic_w / 2.0, ic_y_bot + ic_h / 2.0 - 4 * mm, "DIP-28 Socket (R04..R17)")

    # ---------------- Draw 4 Fan Connectors (Rows 20..23) ----------------
    c.setFont("Helvetica-Bold", 6.5)
    for fname, col, lbl in [("FAN 1", 2, "F1"), ("FAN 2", 5, "F2"), ("FAN 3", 8, "F3"), ("FAN 4", 11, "F4")]:
        fx, fy_top = get_hole_coords_p2(col, 20)
        _, fy_bot = get_hole_coords_p2(col, 23)
        c.setFillColor(colors.HexColor("#0d47a1"))
        c.roundRect(fx - 1.5 * scale * mm, fy_bot - 1.5 * scale * mm, 3.0 * scale * mm, (fy_top - fy_bot) + 3.0 * scale * mm, 1.0 * mm, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.drawCentredString(fx, (fy_top + fy_bot) / 2.0, lbl)

    # ---------------- Draw HW-597B Socket (Row 27, Cols 1..6) ----------------
    hx1, hy_hw = get_hole_coords_p2(1, 27)
    hx2, _ = get_hole_coords_p2(6, 27)
    c.setFillColor(colors.HexColor("#e65100"))
    c.roundRect(hx1 - 1.5 * scale * mm, hy_hw - 1.5 * scale * mm, (hx2 - hx1) + 3.0 * scale * mm, 3.0 * scale * mm, 1.0 * mm, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 6)
    c.drawCentredString((hx1 + hx2) / 2.0, hy_hw, "MÓDULO USB HW-597B (CH340)")

    # ---------------- Draw Floppy 4P Power Header (Row 27, Cols 8..11) ----------------
    px1, py_pwr = get_hole_coords_p2(8, 27)
    px2, _ = get_hole_coords_p2(11, 27)
    c.setFillColor(colors.HexColor("#c62828"))
    c.roundRect(px1 - 1.5 * scale * mm, py_pwr - 1.5 * scale * mm, (px2 - px1) + 3.0 * scale * mm, 3.0 * scale * mm, 1.0 * mm, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 6)
    c.drawCentredString((px1 + px2) / 2.0, py_pwr, "FLOPPY 4P PWR (+12V/GND/+5V)")

    # ---------------- Draw Wire Jumpers with distinctive curved tracks ----------------
    def draw_jumper(c, start_col, start_row, end_col, end_row, color, label=""):
        c.saveState()
        x1, y1 = get_hole_coords_p2(start_col, start_row)
        x2, y2 = get_hole_coords_p2(end_col, end_row)
        c.setStrokeColor(color)
        c.setLineWidth(1.6)
        c.line(x1, y1, x2, y2)
        # Solder points at ends
        c.setFillColor(color)
        c.circle(x1, y1, 1.5 * mm, fill=1, stroke=0)
        c.circle(x2, y2, 1.5 * mm, fill=1, stroke=0)
        c.restoreState()

    # 1. Power Jumpers
    draw_jumper(c, 7, 22, 7, 22, colors.HexColor("#d50000"), "WJ:R22C07") # +12V internal
    draw_jumper(c, 6, 23, 6, 23, colors.HexColor("#212121"), "WJ:R23C06") # GND internal

    # 2. PWM Jumpers (Blue)
    pwm_color = colors.HexColor("#00e5ff")
    draw_jumper(c, 8, 17, 3, 20, pwm_color) # PWM 1 (PB1 R17C08 -> R20C03)
    draw_jumper(c, 8, 16, 4, 20, pwm_color) # PWM 2 (PB2 R16C08 -> R20C04)
    draw_jumper(c, 8, 15, 9, 20, pwm_color) # PWM 3 (PB3 R15C08 -> R20C09)
    draw_jumper(c, 5, 8, 10, 20, pwm_color)  # PWM 4 (PD3 R08C05 -> R20C10)

    # 3. TACH Jumpers (Green)
    tach_color = colors.HexColor("#76ff03")
    draw_jumper(c, 5, 7, 3, 21, tach_color) # TACH 1 (PD2 R07C05 -> R21C03)
    draw_jumper(c, 5, 9, 4, 21, tach_color) # TACH 2 (PD4 R09C05 -> R21C04)
    draw_jumper(c, 5, 14, 9, 21, tach_color) # TACH 3 (PD5 R14C05 -> R21C09)
    draw_jumper(c, 5, 15, 10, 21, tach_color) # TACH 4 (PD6 R15C05 -> R21C10)

    # 4. UART Jumpers (Orange / Purple)
    draw_jumper(c, 4, 27, 5, 5, colors.HexColor("#ff9100")) # HW TX -> MCU RXD (R05C05)
    draw_jumper(c, 5, 27, 5, 6, colors.HexColor("#e040fb")) # HW RX -> MCU TXD (R06C05)

    c.restoreState()

    # ---------------- Right Panel: Legend & Detailed Net Callouts ----------------
    c.saveState()
    lx = 112 * mm
    ly = 24 * mm
    lw = 78 * mm
    lh = 238 * mm
    c.setFillColor(colors.HexColor("#f8f9fa"))
    c.setStrokeColor(colors.HexColor("#dee2e6"))
    c.roundRect(lx, ly, lw, lh, 2 * mm, fill=1, stroke=1)

    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(colors.HexColor("#1b5e20"))
    c.drawString(lx + 4 * mm, ly + lh - 8 * mm, "LEGENDA DE CORES & JUMPERS")

    # Legend color swatches
    swatches = [
        (colors.HexColor("#00e5ff"), "Sinais PWM (25 kHz dos Fans)", "PB1, PB2, PB3, PD3 -> Linha 20"),
        (colors.HexColor("#76ff03"), "Sinais Tacômetro (TACH)", "PD2, PD4, PD5, PD6 -> Linha 21"),
        (colors.HexColor("#ff9100"), "UART TXD (HW-597 -> ATmega RX)", "R27C04 -> R05C05"),
        (colors.HexColor("#e040fb"), "UART RXD (HW-597 -> ATmega TX)", "R27C05 -> R06C05"),
        (colors.HexColor("#ff1744"), "Cortes de Trilha (Track Cuts)", "3.0 mm drill bit (C07 R19, R20-21)"),
        (colors.HexColor("#d50000"), "Alimentação +12V Contínua", "Coluna 7 inferior e Linha 22"),
        (colors.HexColor("#212121"), "Barramento GND (Terra)", "Coluna 6 e Linha 23"),
    ]

    sy = ly + lh - 18 * mm
    for col, title, desc in swatches:
        c.setFillColor(col)
        c.roundRect(lx + 4 * mm, sy, 5 * mm, 5 * mm, 1 * mm, fill=1, stroke=0)
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(colors.HexColor("#212121"))
        c.drawString(lx + 11 * mm, sy + 2.5 * mm, title)
        c.setFont("Helvetica", 6.5)
        c.setFillColor(colors.HexColor("#616161"))
        c.drawString(lx + 11 * mm, sy - 1.5 * mm, desc)
        sy -= 9.5 * mm

    # Divider
    c.setStrokeColor(colors.HexColor("#cfd8dc"))
    c.setLineWidth(0.5)
    c.line(lx + 4 * mm, sy - 2 * mm, lx + lw - 4 * mm, sy - 2 * mm)
    sy -= 8 * mm

    # Details Box: Fan Connectors Pinout
    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(colors.HexColor("#0d47a1"))
    c.drawString(lx + 4 * mm, sy, "CONECTOR 4-PIN DOS COOLERS")
    sy -= 4 * mm
    c.setFont("Helvetica", 7)
    c.setFillColor(colors.HexColor("#333333"))
    fan_pin_desc = [
        "Padrão Molex KK 254 (4 Pinos Verticais):",
        "• Linha 20: Pino 4 - PWM (Controle 25 kHz)",
        "• Linha 21: Pino 3 - TACH (Pulso de RPM)",
        "• Linha 22: Pino 2 - +12V (Força Contínua)",
        "• Linha 23: Pino 1 - GND (0V Comum)"
    ]
    for l in fan_pin_desc:
        c.drawString(lx + 4 * mm, sy, l)
        sy -= 4 * mm

    sy -= 3 * mm
    c.line(lx + 4 * mm, sy, lx + lw - 4 * mm, sy)
    sy -= 6 * mm

    # Details Box: HW-597B Pinout
    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(colors.HexColor("#e65100"))
    c.drawString(lx + 4 * mm, sy, "MÓDULO HW-597B V2.1 (CH340)")
    sy -= 4 * mm
    c.setFont("Helvetica", 7)
    c.setFillColor(colors.HexColor("#333333"))
    hw_pin_desc = [
        "Barra Fêmea SIP-6 na Linha 27 (C01..C06):",
        "• R27C01: +5V (Alimentação USB)",
        "• R27C02: VCC (Jumper para 5V)",
        "• R27C03: +3.3V (Não Conectado / NC)",
        "• R27C04: TxD (Saída Serial -> MCU RXD)",
        "• R27C05: RxD (Entrada Serial <- MCU TXD)",
        "• R27C06: GND (Terra Comum)"
    ]
    for l in hw_pin_desc:
        c.drawString(lx + 4 * mm, sy, l)
        sy -= 4 * mm

    sy -= 3 * mm
    c.line(lx + 4 * mm, sy, lx + lw - 4 * mm, sy)
    sy -= 6 * mm

    # Details Box: Conector de Força Floppy
    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(colors.HexColor("#c62828"))
    c.drawString(lx + 4 * mm, sy, "ENTRADA DE FORÇA FLOPPY 4P (R27)")
    sy -= 4 * mm
    c.setFont("Helvetica", 7)
    c.setFillColor(colors.HexColor("#333333"))
    pwr_desc = [
        "Conector Berg 4-Pin / Mini-Molex (C08..C11):",
        "• R27C08 (Pino 4): +12V (Fio Amarelo) -> Jumper Coluna 7",
        "• R27C09 (Pino 3): GND (Fio Preto) -> Jumper Coluna 6",
        "• R27C10 (Pino 2): GND (Fio Preto) -> Terra Comum",
        "• R27C11 (Pino 1): +5V (Fio Vermelho) -> Barramento +5V MCU"
    ]
    for l in pwr_desc:
        c.drawString(lx + 4 * mm, sy, l)
        sy -= 4 * mm

    sy -= 3 * mm
    c.line(lx + 4 * mm, sy, lx + lw - 4 * mm, sy)
    sy -= 6 * mm

    # Details Box: Componentes Auxiliares
    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(colors.HexColor("#1b5e20"))
    c.drawString(lx + 4 * mm, sy, "CIRCUITO DO ATMEGA328P")
    sy -= 4 * mm
    c.setFont("Helvetica", 7)
    c.setFillColor(colors.HexColor("#333333"))
    aux_desc = [
        "• Y1 (Cristal 16 MHz): Entre R12 e R13",
        "• C_X1, C_X2 (22 pF): R12 -> GND, R13 -> GND",
        "• R_RST (10 kΩ): R04 (Pino 1) ao +5V",
        "• C_DEC (100 nF): Entre VCC (R10) e GND",
        "• Pinos de Terra: R11C05 e R10C08 ao GND",
        "• Pinos de VCC: R10C05 e R12C08 ao +5V"
    ]
    for l in aux_desc:
        c.drawString(lx + 4 * mm, sy, l)
        sy -= 4 * mm

    c.restoreState()
    c.showPage()

# =========================================================================
# PAGE 3: Comprehensive Wire Jumpers Schedule & Pinout Map
# =========================================================================
def build_page_3(c):
    draw_header_footer(c, 3, 4,
                       "3. Tabela Completa de Wire Jumpers, Cortes e Pinagem",
                       "Relação ponto a ponto de coordenadas para soldagem direta e conferência de continuidade")

    c.saveState()
    # Table 1: Wire Jumpers (WJ)
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(colors.HexColor("#1b5e20"))
    c.drawString(20 * mm, 252 * mm, "TABELA 1: CRONOGRAMA DE WIRE JUMPERS (WJ)")

    # Table header
    y = 244 * mm
    c.setFillColor(colors.HexColor("#e8f5e9"))
    c.rect(20 * mm, y - 2 * mm, 170 * mm, 6 * mm, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(colors.HexColor("#1b5e20"))
    c.drawString(22 * mm, y, "Ref")
    c.drawString(38 * mm, y, "Origem (De)")
    c.drawString(64 * mm, y, "Destino (Para)")
    c.drawString(94 * mm, y, "Sinal / Rede")
    c.drawString(124 * mm, y, "Cor")
    c.drawString(142 * mm, y, "Descrição Operacional")

    jumpers_data = [
        ("WJ01", "R17C08 (U1 Pin 15)", "R20C03 (FAN1 Pad)", "PWM1 (25 kHz)", "Azul", "Comando PWM Canal 1 (Timer 1 OC1A)"),
        ("WJ02", "R07C05 (U1 Pin 4)",  "R21C03 (FAN1 Pad)", "TACH1 (RPM)",   "Verde", "Leitura de Tacômetro Canal 1 (INT0)"),
        ("WJ03", "R16C08 (U1 Pin 16)", "R20C04 (FAN2 Pad)", "PWM2 (25 kHz)", "Azul", "Comando PWM Canal 2 (Timer 1 OC1B)"),
        ("WJ04", "R09C05 (U1 Pin 6)",  "R21C04 (FAN2 Pad)", "TACH2 (RPM)",   "Verde", "Leitura de Tacômetro Canal 2 (PCINT20)"),
        ("WJ05", "R15C08 (U1 Pin 17)", "R20C09 (FAN3 Pad)", "PWM3 (25 kHz)", "Azul", "Comando PWM Canal 3 (Timer 2 OC2A)"),
        ("WJ06", "R14C05 (U1 Pin 11)", "R21C09 (FAN3 Pad)", "TACH3 (RPM)",   "Verde", "Leitura de Tacômetro Canal 3 (PCINT21)"),
        ("WJ07", "R08C05 (U1 Pin 5)",  "R20C10 (FAN4 Pad)", "PWM4 (25 kHz)", "Azul", "Comando PWM Canal 4 (Timer 2 OC2B)"),
        ("WJ08", "R15C05 (U1 Pin 12)", "R21C10 (FAN4 Pad)", "TACH4 (RPM)",   "Verde", "Leitura de Tacômetro Canal 4 (PCINT22)"),
        ("WJ09", "R27C04 (HW TxD)",    "R05C05 (U1 Pin 2)",  "UART_RX",       "Laranja", "Comunicação Serial USB -> MCU RXD"),
        ("WJ10", "R27C05 (HW RxD)",    "R06C05 (U1 Pin 3)",  "UART_TX",       "Roxo", "Comunicação Serial MCU TXD -> USB"),
        ("WJ11", "R22C07 (Coluna 7)",  "R22 (Linha 22)",     "+12V_FAN",      "Vermelho", "Alimentação +12V Contínua para os 4 Coolers"),
        ("WJ12", "R23C06 (Coluna 6)",  "R23 (Linha 23)",     "GND_FAN",       "Preto", "Terra (0V) de Potência para os 4 Coolers"),
        ("WJ13", "R11C05 (U1 Pin 8)",  "C06 (Trilha GND)",   "GND_MCU",       "Preto", "Aterramento Lógico do Microcontrolador"),
        ("WJ14", "R10C08 (U1 Pin 22)", "C06 (Trilha GND)",   "GND_MCU",       "Preto", "Aterramento Analógico do Microcontrolador"),
        ("WJ15", "R10C05 (U1 Pin 7)",  "Barramento +5V",     "+5V_VCC",       "Vermelho", "Alimentação Lógica +5V do Microcontrolador"),
        ("WJ16", "R12C08 (U1 Pin 20)", "Barramento +5V",     "+5V_AVCC",      "Vermelho", "Alimentação Analógica AVCC do ATmega")
    ]

    c.setFont("Helvetica", 7)
    for ref, de, para, sinal, cor, desc in jumpers_data:
        y -= 4.8 * mm
        c.setFillColor(colors.HexColor("#212121"))
        c.drawString(22 * mm, y, ref)
        c.drawString(38 * mm, y, de)
        c.drawString(64 * mm, y, para)
        c.drawString(94 * mm, y, sinal)
        c.drawString(124 * mm, y, cor)
        c.drawString(142 * mm, y, desc)
        c.setStrokeColor(colors.HexColor("#eeeeee"))
        c.setLineWidth(0.3)
        c.line(20 * mm, y - 1 * mm, 190 * mm, y - 1 * mm)

    # Table 2: Trace Cuts
    y -= 10 * mm
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(colors.HexColor("#b71c1c"))
    c.drawString(20 * mm, y, "TABELA 2: ROTEIRO DE CORTES DE TRILHA (TRACK CUTS)")
    y -= 7 * mm

    c.setFillColor(colors.HexColor("#ffebee"))
    c.rect(20 * mm, y - 2 * mm, 170 * mm, 6 * mm, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(colors.HexColor("#b71c1c"))
    c.drawString(22 * mm, y, "Corte")
    c.drawString(40 * mm, y, "Coordenada Exata")
    c.drawString(75 * mm, y, "Ferramenta Recomendada")
    c.drawString(115 * mm, y, "Objetivo Elétrico e Isolamento")

    cuts_data = [
        ("CORTE 1", "Coluna 07 na Linha R19", "Broca 3.0 mm (girada à mão)", "Isola o barramento superior do +12V inferior (R20..R27)"),
        ("CORTE 2", "Linhas R20 e R21 entre C03 e C04", "Broca 3.0 mm ou estilete bisturi", "Separa os sinais de PWM e TACH do FAN 1 e FAN 2"),
        ("CORTE 3", "Linhas R20 e R21 entre C09 e C10", "Broca 3.0 mm ou estilete bisturi", "Separa os sinais de PWM e TACH do FAN 3 e FAN 4")
    ]
    c.setFont("Helvetica", 7)
    for c_id, coord, tool, purp in cuts_data:
        y -= 5.0 * mm
        c.setFillColor(colors.HexColor("#212121"))
        c.drawString(22 * mm, y, c_id)
        c.drawString(40 * mm, y, coord)
        c.drawString(75 * mm, y, tool)
        c.drawString(115 * mm, y, purp)
        c.setStrokeColor(colors.HexColor("#eeeeee"))
        c.setLineWidth(0.3)
        c.line(20 * mm, y - 1 * mm, 190 * mm, y - 1 * mm)

    # Table 3: ATmega328P Pinout Mapping on Stripboard Rev 1.0
    y -= 10 * mm
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(colors.HexColor("#0d47a1"))
    c.drawString(20 * mm, y, "TABELA 3: MAPA DE PINOS DO ATMEGA328P NA STRIPBOARD (R04 A R17)")
    y -= 7 * mm

    c.setFillColor(colors.HexColor("#e3f2fd"))
    c.rect(20 * mm, y - 2 * mm, 170 * mm, 6 * mm, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(colors.HexColor("#0d47a1"))
    c.drawString(22 * mm, y, "Linha")
    c.drawString(32 * mm, y, "Pino (Esq)")
    c.drawString(48 * mm, y, "Função MCU")
    c.drawString(75 * mm, y, "Conexão na Placa")
    c.drawString(108 * mm, y, "Pino (Dir)")
    c.drawString(124 * mm, y, "Função MCU")
    c.drawString(150 * mm, y, "Conexão na Placa")

    pinout_data = [
        ("R04", "Pin 1", "/RESET", "Pull-up 10k ao +5V / Botão", "Pin 28", "PC5 (ADC5)", "Livre / Expansão I2C (SCL)"),
        ("R05", "Pin 2", "PD0 (RXD)", "Jumper WJ09 (HW-597 TxD)", "Pin 27", "PC4 (ADC4)", "Livre / Expansão I2C (SDA)"),
        ("R06", "Pin 3", "PD1 (TXD)", "Jumper WJ10 (HW-597 RxD)", "Pin 26", "PC3 (ADC3)", "Livre"),
        ("R07", "Pin 4", "PD2 (INT0)", "Jumper WJ02 (FAN1 TACH)", "Pin 25", "PC2 (ADC2)", "Livre"),
        ("R08", "Pin 5", "PD3 (OC2B)", "Jumper WJ07 (FAN4 PWM)", "Pin 24", "PC1 (ADC1)", "Livre"),
        ("R09", "Pin 6", "PD4 (PCINT20)", "Jumper WJ04 (FAN2 TACH)", "Pin 23", "PC0 (ADC0)", "Livre"),
        ("R10", "Pin 7", "VCC (+5V)", "Alimentação +5V Lógica", "Pin 22", "GND (0V)", "Jumper WJ14 ao GND"),
        ("R11", "Pin 8", "GND (0V)", "Jumper WJ13 ao GND", "Pin 21", "AREF", "Capacitor 100nF ao GND"),
        ("R12", "Pin 9", "PB6 (XTAL1)", "Cristal 16MHz + 22pF", "Pin 20", "AVCC (+5V)", "Alimentação +5V Analógica"),
        ("R13", "Pin 10", "PB7 (XTAL2)", "Cristal 16MHz + 22pF", "Pin 19", "PB5 (SCK)", "Livre / ISP SCK"),
        ("R14", "Pin 11", "PD5 (PCINT21)", "Jumper WJ06 (FAN3 TACH)", "Pin 18", "PB4 (MISO)", "Livre / ISP MISO"),
        ("R15", "Pin 12", "PD6 (PCINT22)", "Jumper WJ08 (FAN4 TACH)", "Pin 17", "PB3 (OC2A)", "Jumper WJ05 (FAN3 PWM)"),
        ("R16", "Pin 13", "PD7", "Livre", "Pin 16", "PB2 (OC1B)", "Jumper WJ03 (FAN2 PWM)"),
        ("R17", "Pin 14", "PB0", "Livre", "Pin 15", "PB1 (OC1A)", "Jumper WJ01 (FAN1 PWM)")
    ]

    c.setFont("Helvetica", 6.5)
    for r, p_l, fn_l, con_l, p_r, fn_r, con_r in pinout_data:
        y -= 4.2 * mm
        c.setFillColor(colors.HexColor("#212121"))
        c.drawString(22 * mm, y, r)
        c.drawString(32 * mm, y, p_l)
        c.drawString(48 * mm, y, fn_l)
        c.drawString(75 * mm, y, con_l)
        c.drawString(108 * mm, y, p_r)
        c.drawString(124 * mm, y, fn_r)
        c.drawString(150 * mm, y, con_r)
        c.setStrokeColor(colors.HexColor("#f0f0f0"))
        c.setLineWidth(0.2)
        c.line(20 * mm, y - 0.8 * mm, 190 * mm, y - 0.8 * mm)

    c.restoreState()
    c.showPage()

# =========================================================================
# PAGE 4: Step-by-Step Instructions & Quality Checklist
# =========================================================================
def build_page_4(c):
    draw_header_footer(c, 4, 4,
                       "4. Instruções Passo a Passo de Montagem e Check-list",
                       "Roteiro de execução para montagem segura, inspeção a frio e validação funcional")

    c.saveState()
    y = 254 * mm

    steps = [
        ("FASE 1: CORTES DE TRILHA E VERIFICAÇÃO DE CONTINUIDADE", colors.HexColor("#b71c1c"), [
            ("[ ]", "Corte 1 (Coluna 07 na Linha 19): Cortar o cobre usando broca de 3.0 mm girada com a ponta dos dedos."),
            ("[ ]", "Teste de Continuidade 1: Verificar com multímetro que a Coluna 7 superior (R01..R18) NÃO conduz com a inferior (R20..R27)."),
            ("[ ]", "Corte 2 (Linhas 20 e 21 entre C03 e C04): Separar com bisturi/broca as ilhas do Canal 1 e Canal 2."),
            ("[ ]", "Corte 3 (Linhas 20 e 21 entre C09 e C10): Separar com bisturi/broca as ilhas do Canal 3 e Canal 4."),
            ("[ ]", "Teste de Continuidade 2: Confirmar isolamento elétrico entre C03-C04 e entre C09-C10 nas linhas 20 e 21 (> 1 MΩ).")
        ]),
        ("FASE 2: INSTALAÇÃO DOS WIRE JUMPERS (WJ) ISOLADOS", colors.HexColor("#e65100"), [
            ("[ ]", "WJ de Alimentação: Soldar WJ R23C06 (GND dos coolers ao GND comum) e WJ R22C07 (+12V dos coolers ao +12V inferior)."),
            ("[ ]", "Pontes Verticais R26-R27: Conectar verticalmente as colunas 2, 3, 4, 5 e 8, 9, 10, 11 entre as linhas 26 e 27."),
            ("[ ]", "Jumpers PWM (Fio Azul): Soldar WJ01 (R17C08->R20C03), WJ03 (R16C08->R20C04), WJ05 (R15C08->R20C09) e WJ07 (R08C05->R20C10)."),
            ("[ ]", "Jumpers TACH (Fio Verde): Soldar WJ02 (R07C05->R21C03), WJ04 (R09C05->R21C04), WJ06 (R14C05->R21C09) e WJ08 (R15C05->R21C10)."),
            ("[ ]", "Jumpers UART (Fio Laranja/Roxo): Soldar WJ09 (R27C04->R05C05 TxD->RXD) e WJ10 (R27C05->R06C05 RxD->TXD)."),
            ("[ ]", "Jumpers GND/VCC do MCU: Soldar pinos 8 e 22 ao GND (Coluna 6) e pinos 7 e 20 à linha de +5V.")
        ]),
        ("FASE 3: SOQUETES, BARRAS E CONECTORES", colors.HexColor("#0d47a1"), [
            ("[ ]", "Soquete DIP-28 do ATmega328P: Instalar entre as linhas R04 e R17 (chanfro voltado para a linha R01). NÃO inserir o chip ainda!"),
            ("[ ]", "Barra Fêmea SIP-6 para HW-597B: Soldar na Linha 27 (Colunas C01 a C06)."),
            ("[ ]", "Conectores Macho dos Coolers: Soldar 4x barras macho KK 254 (4 vias) em C02, C05, C08 e C11 (linhas 20 a 23).")
        ]),
        ("FASE 4: COMPONENTES PASSIVOS E OSCILADOR", colors.HexColor("#1b5e20"), [
            ("[ ]", "Oscilador a Cristal: Soldar cristal de 16.000 MHz entre R12 e R13, com capacitores de 22 pF de cada pino para a Coluna 6 (GND)."),
            ("[ ]", "Resistor de Reset: Soldar resistor de 10 kΩ entre R04 (Pino 1 /RESET) e a linha de +5V."),
            ("[ ]", "Capacitor de Desacoplamento: Soldar capacitor cerâmico de 100 nF próximo ao pino 7 (VCC) e pino 8 (GND).")
        ]),
        ("FASE 5: TESTE ELÉTRICO A FRIO (SEM CHIP / SEM ENERGIZAR)", colors.HexColor("#4a148c"), [
            ("[ ]", "Teste de Curto-Circuito: Com o multímetro na escala de continuidade, testar entre +12V e GND (deve dar circuito aberto)."),
            ("[ ]", "Teste +5V e GND: Verificar que NÃO há curto entre a linha de +5V e o GND."),
            ("[ ]", "Teste +12V e +5V: Confirmar isolamento total entre a linha de +12V dos coolers e o +5V lógico."),
            ("[ ]", "Conferência das Tensões nos Pinos do Soquete: Energizar momentaneamente sem o ATmega328P e medir com voltímetro:"),
            ("   ", "  -> Pino 7 e Pino 20 devem ter exatamente +5.0V. Pinos 8 e 22 devem ter 0.0V. Pino 1 deve ter +5.0V (pull-up)."),
            ("   ", "  -> Pinos 2 de todos os 4 conectores de cooler devem ter exatamente +12.0V.")
        ]),
        ("FASE 6: GRAVAÇÃO DO FIRMWARE E TESTE FUNCIONAL", colors.HexColor("#004d40"), [
            ("[ ]", "Encaixe do ATmega328P-PU gravado com o firmware compilado (`PWM_MODE_4PIN_25KHZ`)."),
            ("[ ]", "Encaixe do módulo HW-597B na barra fêmea da linha 27."),
            ("[ ]", "Conexão USB com o PC Linux: Executar `ls -l /dev/ttyUSB0` e `dmesg | tail` para confirmar detecção pelo kernel."),
            ("[ ]", "Comando de Teste Serial: Enviar comando `STATUS` a 115200 baud via terminal serial ou script Python."),
            ("[ ]", "Conexão dos Coolers Akasa DFC9225120: Ligar os 4 coolers e testar rampas de PWM (`SETALL 50`, `SETALL 150`, `SETALL 255`)."),
            ("[ ]", "Conferência do Tacômetro: Verificar que cada ventoinha reporta leituras reais de RPM estáveis e sem oscilações.")
        ])
    ]

    for phase_title, title_col, items in steps:
        c.setFont("Helvetica-Bold", 8.5)
        c.setFillColor(title_col)
        c.drawString(20 * mm, y, phase_title)
        y -= 4.2 * mm

        c.setFont("Helvetica", 7.2)
        c.setFillColor(colors.HexColor("#212121"))
        for chk, txt in items:
            c.drawString(23 * mm, y, chk)
            c.drawString(29 * mm, y, txt)
            y -= 3.8 * mm
        y -= 2.0 * mm

    c.restoreState()
    c.showPage()

def main():
    templates_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(templates_dir, exist_ok=True)
    pdf_path = os.path.join(templates_dir, "stripboard_rev1.0_4pin_assembly_guide.pdf")

    c = canvas.Canvas(pdf_path, pagesize=A4)
    c.setTitle("Fan Controller Rev 1.0 - 4-Pin Akasa PWM Assembly Guide")
    c.setAuthor("Frederico C Wilhelms & Antigravity")
    c.setSubject("Step-by-step Assembly, 1:1 Templates, Wire Jumpers Schedule and Verification Checklist")

    print("Generating Page 1: 1:1 Scale Printable Templates...")
    build_page_1(c)

    print("Generating Page 2: Visual Assembly & Wiring Diagram...")
    build_page_2(c)

    print("Generating Page 3: Wire Jumpers Schedule & Pinout Mapping...")
    build_page_3(c)

    print("Generating Page 4: Step-by-Step Instructions & Quality Checklist...")
    build_page_4(c)

    c.save()
    print(f"Successfully generated 4-page Assembly Guide PDF: {pdf_path}")

    # Render preview PNGs of all 4 pages
    prefix = os.path.join(templates_dir, "assembly_guide_page")
    print("Rendering PNG previews with pdftoppm...")
    subprocess.run(["pdftoppm", "-png", "-r", "150", pdf_path, prefix], check=True)
    print("All page previews rendered successfully!")

if __name__ == "__main__":
    main()
