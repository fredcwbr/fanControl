#!/usr/bin/env python3
"""
layout_stripboards.py
Positions all elements in:
- lepton/rev1.0/stripboard_rev1.0.pcb
- lepton/rev1.1/stripboard_rev1.1.pcb
with widened margins for M3 mounting holes, dedicated clearance for power jacks,
thin clean tracks, and silkscreen labels properly positioned directly on/over connectors.
"""

import os
import shutil
import subprocess

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # ------------------ REV 1.1 ------------------
    # Board dimensions: Width = 3500.00 mil (88.9 mm), Height = 5000.00 mil (127.0 mm)
    w11 = 3500.0
    h11 = 5050.0

    p11_file = os.path.join(base_dir, "rev1.1/stripboard_rev1.1.pcb")
    with open(p11_file) as f:
        text11 = f.read()

    symbols_block11 = text11.split("PCB[")[1].split("Element[")[0]
    sym_idx11 = symbols_block11.find("Symbol[")
    symbols11 = symbols_block11[sym_idx11:]

    elems11 = []

    def kre10_v11(ref, x, y):
        # 10-pin KRE terminal block 5.08mm (200 mil pitch)
        # Pins at X=x, Y=y + i*200
        tx = 24.0
        ty = 60.0
        scale = 70
        res = [f"""Element["" "KRE10_508" "{ref}" "unknown" {x:.2f}mil {y:.2f}mil {tx:.2f}mil {ty:.2f}mil 3 {scale} ""]""", "("]
        for i in range(1, 11):
            py = (i - 1) * 200.0
            flag = "square" if i == 1 else ""
            res.append(f"""\tPin[0.0000 {py:.2f}mil 80.00mil 15.00mil 86.00mil 50.00mil "{i}" "{i}" "{flag}"]""")
        # Plastic body outline (ZB128)
        res.append("\tElementLine [-280.00mil -100.00mil  100.00mil -100.00mil 10.00mil]")
        res.append("\tElementLine [ 100.00mil -100.00mil  100.00mil 1900.00mil 10.00mil]")
        res.append("\tElementLine [ 100.00mil 1900.00mil -280.00mil 1900.00mil 10.00mil]")
        res.append("\tElementLine [-280.00mil 1900.00mil -280.00mil -100.00mil 10.00mil]")
        for i in range(1, 11):
            py = (i - 1) * 200.0
            res.append(f"\tElementLine [0.0000 {py-50.0:.2f}mil 90.00mil {py-50.0:.2f}mil 8.00mil]")
            res.append(f"\tElementLine [90.00mil {py-50.0:.2f}mil 90.00mil {py+50.0:.2f}mil 8.00mil]")
            res.append(f"\tElementLine [90.00mil {py+50.0:.2f}mil 0.0000 {py+50.0:.2f}mil 8.00mil]")
            res.append(f"\tElementArc [-100.00mil {py:.2f}mil 30.00mil 30.00mil 0 360 8.00mil]")
        res.append(")")
        return "\n".join(res)

    def sip10_200mil(ref, x, y):
        # 10-pin pass-thru column at 200 mil pitch (80 mil pad, 35 mil drill)
        tx = 24.0
        ty = 60.0
        scale = 60
        res = [f"""Element["" "SIP10_200MIL" "{ref}" "unknown" {x:.2f}mil {y:.2f}mil {tx:.2f}mil {ty:.2f}mil 3 {scale} ""]""", "("]
        for i in range(1, 11):
            py = (i - 1) * 200.0
            flag = "square" if i == 1 else ""
            res.append(f"""\tPin[0.0000 {py:.2f}mil 80.00mil 15.00mil 86.00mil 35.00mil "{i}" "{i}" "{flag}"]""")
        res.append(")")
        return "\n".join(res)

    def lm317_to220(ref, x, y):
        # x is Col 1 (e.g. 1400 or 1700)
        # Pins: Pin 3 (VIN) at x, Pin 2 (VOUT) at x+100, Pin 1 (ADJ) at x+200
        # Reference position at (x+100, y)
        tx = -50.0
        ty = -120.0
        res = [f"""Element["" "TO220_UPRIGHT" "{ref}" "LM317" {x+100.0:.2f}mil {y:.2f}mil {tx:.2f}mil {ty:.2f}mil 0 70 ""]""", "("]
        res.append("""\tPin[-100.00mil 0.0000 80.00mil 15.00mil 86.00mil 45.00mil \"3\" \"3\" \"\"]""")
        res.append("""\tPin[0.0000 0.0000 80.00mil 15.00mil 86.00mil 45.00mil \"2\" \"2\" \"\"]""")
        res.append("""\tPin[100.00mil 0.0000 80.00mil 15.00mil 86.00mil 45.00mil \"1\" \"1\" \"\"]""")
        # Tab at back (Y = -60 to -40 mil), Body (Y = -40 to +120 mil), Width = 400 mil (-200 to +200)
        res.append("\tElementLine [-200.00mil -60.00mil  200.00mil -60.00mil 12.00mil]")
        res.append("\tElementLine [-200.00mil -40.00mil  200.00mil -40.00mil  8.00mil]")
        res.append("\tElementLine [-200.00mil -40.00mil -200.00mil 120.00mil  8.00mil]")
        res.append("\tElementLine [ 200.00mil -40.00mil  200.00mil 120.00mil  8.00mil]")
        res.append("\tElementLine [-200.00mil 120.00mil  200.00mil 120.00mil  8.00mil]")
        res.append(")")
        return "\n".join(res)

    def cap_2pin_v(ref, val, x, y1, y2):
        cy = (y1 + y2) / 2.0
        dy = abs(y2 - y1) / 2.0
        tx = 25.0
        ty = -20.0
        res = [f"""Element["" "C_200MIL" "{ref}" "{val}" {x:.2f}mil {cy:.2f}mil {tx:.2f}mil {ty:.2f}mil 0 60 ""]""", "("]
        res.append(f"""\tPin[0.0000 {-dy:.2f}mil 80.00mil 15.00mil 86.00mil 35.00mil \"1\" \"1\" \"\"]""")
        res.append(f"""\tPin[0.0000 {dy:.2f}mil 80.00mil 15.00mil 86.00mil 35.00mil \"2\" \"2\" \"\"]""")
        res.append("\tElementArc [0.0000 0.0000 70.00mil 70.00mil 0 360 8.00mil]")
        res.append(")")
        return "\n".join(res)

    def res_2pin_h(ref, val, x1, x2, y):
        cx = (x1 + x2) / 2.0
        dx = abs(x2 - x1) / 2.0
        tx = -30.0
        ty = 25.0
        res = [f"""Element["" "R_100MIL" "{ref}" "{val}" {cx:.2f}mil {y:.2f}mil {tx:.2f}mil {ty:.2f}mil 0 60 ""]""", "("]
        res.append(f"""\tPin[{-dx:.2f}mil 0.0000 80.00mil 15.00mil 86.00mil 35.00mil \"1\" \"1\" \"\"]""")
        res.append(f"""\tPin[{dx:.2f}mil 0.0000 80.00mil 15.00mil 86.00mil 35.00mil \"2\" \"2\" \"\"]""")
        res.append("\tElementLine [-40.00mil -25.00mil  40.00mil -25.00mil 8.00mil]")
        res.append("\tElementLine [ 40.00mil -25.00mil  40.00mil  25.00mil 8.00mil]")
        res.append("\tElementLine [ 40.00mil  25.00mil -40.00mil  25.00mil 8.00mil]")
        res.append("\tElementLine [-40.00mil  25.00mil -40.00mil -25.00mil 8.00mil]")
        res.append(")")
        return "\n".join(res)

    def res_2pin_v(ref, val, x, y1, y2):
        cy = (y1 + y2) / 2.0
        dy = abs(y2 - y1) / 2.0
        tx = 25.0
        ty = -20.0
        res = [f"""Element["" "R_200MIL" "{ref}" "{val}" {x:.2f}mil {cy:.2f}mil {tx:.2f}mil {ty:.2f}mil 0 60 ""]""", "("]
        res.append(f"""\tPin[0.0000 {-dy:.2f}mil 80.00mil 15.00mil 86.00mil 35.00mil \"1\" \"1\" \"\"]""")
        res.append(f"""\tPin[0.0000 {dy:.2f}mil 80.00mil 15.00mil 86.00mil 35.00mil \"2\" \"2\" \"\"]""")
        res.append("\tElementLine [-25.00mil -60.00mil  25.00mil -60.00mil 8.00mil]")
        res.append("\tElementLine [ 25.00mil -60.00mil  25.00mil  60.00mil 8.00mil]")
        res.append("\tElementLine [ 25.00mil  60.00mil -25.00mil  60.00mil 8.00mil]")
        res.append("\tElementLine [-25.00mil  60.00mil -25.00mil -60.00mil 8.00mil]")
        res.append(")")
        return "\n".join(res)

    def single_pad(ref, label, x, y):
        tx = 25.0
        ty = 15.0
        res = [f"""Element["" "PAD1" "{ref}" "{label}" {x:.2f}mil {y:.2f}mil {tx:.2f}mil {ty:.2f}mil 0 60 ""]""", "("]
        res.append("""\tPin[0.0000 0.0000 80.00mil 15.00mil 86.00mil 35.00mil \"1\" \"1\" \"square\"]""")
        res.append(")")
        return "\n".join(res)

    def sip_scratchpad_v11(ref, n, x, y):
        # Scratchpad column with 90 mil pads and 35 mil drill, 100 mil pitch (10 mil gap between pads)
        tx = 24.0
        ty = 60.0
        scale = 60
        res = [f"""Element["" "SIP{n}_90PAD" "{ref}" "unknown" {x:.2f}mil {y:.2f}mil {tx:.2f}mil {ty:.2f}mil 3 {scale} ""]""", "("]
        for i in range(1, n + 1):
            py = (i - 1) * 100.0
            res.append(f"""\tPin[0.0000 {py:.2f}mil 90.00mil 10.00mil 96.00mil 35.00mil "{i}" "{i}" ""]""")
        res.append(")")
        return "\n".join(res)

    def sip_v11(ref, n, x, y):
        # Vertical strip:
        # For 20-pin rails (CONN101..116): TDir = 3 (vertical down along rail), TScale = 80
        # For 4-pin bottom strips (CONN231..239, 331..339): TDir = 3, TScale = 70
        if n == 20:
            tx = 24.0
            ty = 200.0
            scale = 80
        elif n == 3:
            tx = 24.0
            ty = 50.0
            scale = 70
        else:
            tx = 24.0
            ty = 60.0
            scale = 70
        res = [f"""Element["" "SIP{n}N" "{ref}" "unknown" {x:.2f}mil {y:.2f}mil {tx:.2f}mil {ty:.2f}mil 3 {scale} ""]""", "("]
        for i in range(1, n + 1):
            py = (i - 1) * 100.0
            flag = "square" if i == 1 else ""
            res.append(f"""\tPin[0.0000 {py:.2f}mil 80.00mil 10.00mil 86.00mil 35.00mil "{i}" "{i}" "{flag}"]""")
        end_y = (n - 1) * 100.0
        res.append(f"\tElementLine [-30.00mil 0.0000 -30.00mil {end_y:.2f}mil 8.00mil]")
        res.append(f"\tElementLine [ 30.00mil 0.0000  30.00mil {end_y:.2f}mil 8.00mil]")
        res.append(f"\tElementArc [0.0000 0.0000 30.00mil 30.00mil 180 180 8.00mil]")
        res.append(f"\tElementArc [0.0000 {end_y:.2f}mil 30.00mil 30.00mil 0 180 8.00mil]")
        res.append(")")
        return "\n".join(res)

    def sip_h11(ref, n, x, y):
        # Horizontal 9-pin strip: width 800 mil, centered at X = 400 mil, Y = 0 mil
        tx = 320.0
        ty = -24.0
        res = [f"""Element["" "SIP{n}N" "{ref}" "unknown" {x:.2f}mil {y:.2f}mil {tx:.2f}mil {ty:.2f}mil 0 80 ""]""", "("]
        for i in range(1, n + 1):
            px = (i - 1) * 100.0
            flag = "square" if i == 1 else ""
            res.append(f"""\tPin[{px:.2f}mil 0.0000 80.00mil 10.00mil 86.00mil 35.00mil "{i}" "{i}" "{flag}"]""")
        end_x = (n - 1) * 100.0
        res.append(f"\tElementLine [0.0000 -30.00mil {end_x:.2f}mil -30.00mil 8.00mil]")
        res.append(f"\tElementLine [0.0000  30.00mil {end_x:.2f}mil  30.00mil 8.00mil]")
        res.append(f"\tElementArc [0.0000 0.0000 30.00mil 30.00mil 90 180 8.00mil]")
        res.append(f"\tElementArc [{end_x:.2f}mil 0.0000 30.00mil 30.00mil 270 180 8.00mil]")
        res.append(")")
        return "\n".join(res)

    def header18_11(ref, x, y):
        # 2x9 header: centered horizontally at X = 400 mil, vertically at Y = 50 mil
        tx = 350.0
        ty = 26.0
        res = [f"""Element["" "HEADER18" "{ref}" "unknown" {x:.2f}mil {y:.2f}mil {tx:.2f}mil {ty:.2f}mil 0 80 ""]""", "("]
        for c in range(9):
            px = c * 100.0
            p1 = 2 * c + 1
            p2 = 2 * c + 2
            res.append(f"""\tPin[{px:.2f}mil 0.0000 80.00mil 10.00mil 86.00mil 35.00mil "{p1}" "{p1}" ""]""")
            res.append(f"""\tPin[{px:.2f}mil 100.00mil 80.00mil 10.00mil 86.00mil 35.00mil "{p2}" "{p2}" ""]""")
        end_x = 8 * 100.0
        res.append(f"\tElementLine [-30.00mil -30.00mil {end_x+30:.2f}mil -30.00mil 8.00mil]")
        res.append(f"\tElementLine [-30.00mil 130.00mil {end_x+30:.2f}mil 130.00mil 8.00mil]")
        res.append(f"\tElementLine [-30.00mil -30.00mil -30.00mil 130.00mil 8.00mil]")
        res.append(f"\tElementLine [{end_x+30:.2f}mil -30.00mil {end_x+30:.2f}mil 130.00mil 8.00mil]")
        res.append(")")
        return "\n".join(res)

    def pwrjack11(ref, x, y):
        # Power jack: centered at X = 100 mil, clear bottom region at Y = 300 mil
        tx = 25.0
        ty = 276.0
        return f"""Element["" "PWRJACK" "{ref}" "unknown" {x:.2f}mil {y:.2f}mil {tx:.2f}mil {ty:.2f}mil 0 80 ""]
(
\tPin[0.0000 0.0000 80.00mil 25.00mil 90.00mil 45.00mil "1" "1" "square"]
\tPin[180.00mil 90.00mil 80.00mil 25.00mil 90.00mil 45.00mil "2" "2" ""]
\tPin[0.0000 180.00mil 80.00mil 25.00mil 90.00mil 45.00mil "3" "3" ""]
\tElementLine [-80.00mil -60.00mil -80.00mil 380.00mil 10.00mil]
\tElementLine [ 280.00mil -60.00mil  280.00mil 380.00mil 10.00mil]
\tElementLine [-80.00mil -60.00mil  280.00mil -60.00mil 10.00mil]
\tElementLine [-80.00mil  380.00mil  280.00mil  380.00mil 10.00mil]
)"""

    def edge_finger(ref, x, has_finger=True):
        # Element placed at (x, 4920 mil)
        # Single-sided edge fingers on solder side (bottom layer)
        res = [f"""Element["" "EDGE_FINGER" "{ref}" "unknown" {x:.2f}mil 4920.00mil 0 0 0 0 ""]""", "("]
        if has_finger:
            # Solder Jumper: two pads on solder side ONLY (onsolder)
            # Pad 1 (top): center Y = 4750 mil -> relative Y = -170 mil. dx=50, dy=30. th=30, x1=-10, x2=+10
            res.append("\tPad[-10.00mil -170.00mil 10.00mil -170.00mil 30.00mil 15.00mil 40.00mil \"1\" \"1\" \"square,onsolder\"]")
            # Pad 2 (bottom): center Y = 4793 mil -> relative Y = -127 mil. dx=50, dy=30. th=30, x1=-10, x2=+10
            res.append("\tPad[-10.00mil -127.00mil 10.00mil -127.00mil 30.00mil 15.00mil 40.00mil \"2\" \"2\" \"square,onsolder\"]")
            # Silk outline around solder jumper
            res.append("\tElementLine [-28.00mil -190.00mil 28.00mil -190.00mil 6.00mil]")
            res.append("\tElementLine [-28.00mil -107.00mil 28.00mil -107.00mil 6.00mil]")
            res.append("\tElementLine [-28.00mil -190.00mil -28.00mil -107.00mil 6.00mil]")
            res.append("\tElementLine [28.00mil -190.00mil 28.00mil -107.00mil 6.00mil]")

            # Edge Finger: centered at Y = 4925 mil -> relative Y = +5 mil. Length = 230 mil (Y = 4810 to 5040 mil).
            # Width dx = 65 mil, Length dy = 230 mil. SINGLE-SIDED (onsolder ONLY).
            res.append("\tPad[0.0000 -77.50mil 0.0000 87.50mil 65.00mil 20.00mil 75.00mil \"F\" \"F\" \"square,onsolder\"]")
        res.append(")")
        return "\n".join(res)

    def mthole11(ref, x, y, ty_offset):
        tx = -60.0
        return f"""Element["" "Mounting Hole" "{ref}" "M3" {x:.2f}mil {y:.2f}mil {tx:.2f}mil {ty_offset:.2f}mil 0 80 ""]
(
\tPin[0.0000 0.0000 240.00mil 40.00mil 250.00mil 126.00mil "1" "1" ""]
\tElementArc [0.0000 0.0000 150.00mil 150.00mil 0 360 10.00mil]
)"""

    def vr101_outline(ref, cx, cy):
        # Narrow 200 mil wide outline for upright module (length 1720 mil = 43.6 mm, no details needed)
        # cx = 300 mil, cy = 1500 mil -> X spans 200 to 400 mil (width 200 mil), Y spans 640 to 2360 mil
        tx = -90.0
        ty = -890.0
        return f"""Element["" "LM2596_UPRIGHT" "{ref}" "unknown" {cx:.2f}mil {cy:.2f}mil {tx:.2f}mil {ty:.2f}mil 0 80 ""]
(
\tElementLine [-100.00mil -860.00mil  100.00mil -860.00mil 10.00mil]
\tElementLine [ 100.00mil -860.00mil  100.00mil  860.00mil 10.00mil]
\tElementLine [ 100.00mil  860.00mil -100.00mil  860.00mil 10.00mil]
\tElementLine [-100.00mil  860.00mil -100.00mil -860.00mil 10.00mil]
)"""

    # 1. 8 Rails of 40 pins (2x SIP20N each)
    rails_x = [500.0, 600.0, 700.0, 1700.0, 1800.0, 2800.0, 2900.0, 3000.0]
    for idx, rx in enumerate(rails_x):
        ref1 = f"CONN1{2*idx+1:02d}"
        ref2 = f"CONN1{2*idx+2:02d}"
        elems11.append(sip_v11(ref1, 20, rx, 800.0))
        elems11.append(sip_v11(ref2, 20, rx, 2800.0))

    # 2. Power Jacks & Breakout Connectors (spaced apart towards edges)
    # Jack 1 placed at X = 800 mil, breakout CONN119..121 to the left at X = 500, 600, 700 mil
    elems11.append(pwrjack11("CONN117", 800.0, 200.0))
    elems11.append(sip_v11("CONN119", 3, 500.0, 200.0))
    elems11.append(sip_v11("CONN120", 3, 600.0, 200.0))
    elems11.append(sip_v11("CONN121", 3, 700.0, 200.0))

    # Jack 2 placed at X = 2400 mil, breakout CONN122..124 to the right at X = 2800, 2900, 3000 mil
    elems11.append(pwrjack11("CONN118", 2400.0, 200.0))
    elems11.append(sip_v11("CONN122", 3, 2800.0, 200.0))
    elems11.append(sip_v11("CONN123", 3, 2900.0, 200.0))
    elems11.append(sip_v11("CONN124", 3, 3000.0, 200.0))

    # 2b. Two LM317 Regulator Circuits inserted between the Power Jacks (Through-Hole Default)
    # Circuit 1: X = 1400..1600 mil (U101, C101, C102, R101, R102, J101, J102, J103)
    elems11.append(lm317_to220("U101", 1400.0, 300.0))
    elems11.append(single_pad("J101", "VIN1", 1400.0, 200.0))
    elems11.append(single_pad("J102", "VOUT1", 1500.0, 200.0))
    elems11.append(single_pad("J103", "GND", 1400.0, 700.0))
    elems11.append(cap_2pin_v("C101", "0.1uF", 1400.0, 400.0, 600.0))
    elems11.append(cap_2pin_v("C102", "1uF", 1500.0, 400.0, 600.0))
    elems11.append(res_2pin_h("R101", "240", 1500.0, 1600.0, 500.0))
    elems11.append(res_2pin_v("R102", "R2", 1600.0, 400.0, 600.0))

    # Circuit 2: X = 1900..2100 mil (U102, C103, C104, R103, R104, J104, J105, J106)
    elems11.append(lm317_to220("U102", 1900.0, 300.0))
    elems11.append(single_pad("J104", "VIN2", 1900.0, 200.0))
    elems11.append(single_pad("J105", "VOUT2", 2000.0, 200.0))
    elems11.append(single_pad("J106", "GND", 1900.0, 700.0))
    elems11.append(cap_2pin_v("C103", "0.1uF", 1900.0, 400.0, 600.0))
    elems11.append(cap_2pin_v("C104", "1uF", 2000.0, 400.0, 600.0))
    elems11.append(res_2pin_h("R103", "240", 2000.0, 2100.0, 500.0))
    elems11.append(res_2pin_v("R104", "R2", 2100.0, 400.0, 600.0))

    # 3. 6x M3 Mounting Holes (in dedicated side margin columns at X = 200 mil and X = 3300 mil)
    # MH103 and MH104 centered at Y = 2400 mil to provide equal 2200 mil spans (200..2400 and 2400..4600)
    elems11.append(mthole11("MH101", 200.0, 200.0, 160.0))
    elems11.append(mthole11("MH102", 3300.0, 200.0, 160.0))
    elems11.append(mthole11("MH103", 200.0, 2400.0, 160.0))
    elems11.append(mthole11("MH104", 3300.0, 2700.0, 160.0))
    elems11.append(mthole11("MH105", 200.0, 4600.0, -180.0))
    elems11.append(mthole11("MH106", 3300.0, 4600.0, -180.0))

    # Stripboard Module 1 connectors VIN1+, VIN1-, OUT1+, OUT1- (4x7 points centered between MH101 and MH103)
    # Left row (X = 100 mil): VIN1+ (top, Y=600..1200) and OUT1+ (bottom, Y=1400..2000)
    # Right row (X = 300 mil): VIN1- (top, Y=600..1200) and OUT1- (bottom, Y=1400..2000)
    elems11.append(sip_v11("CONN125", 7, 100.0, 600.0))
    elems11.append(sip_v11("CONN126", 7, 300.0, 600.0))
    elems11.append(sip_v11("CONN127", 7, 100.0, 1400.0))
    elems11.append(sip_v11("CONN128", 7, 300.0, 1400.0))
    elems11.append(vr101_outline("VR101", 200.0, 1300.0))

    # Stripboard Module 2 connectors VIN2+, VIN2-, OUT2+, OUT2- (4x7 points centered between MH103 and MH105)
    # Left row (X = 100 mil): VIN2+ (top, Y=2800..3400) and OUT2+ (bottom, Y=3600..4200)
    # Right row (X = 300 mil): VIN2- (top, Y=2800..3400) and OUT2- (bottom, Y=3600..4200)
    elems11.append(sip_v11("CONN129", 7, 100.0, 2800.0))
    elems11.append(sip_v11("CONN130", 7, 300.0, 2800.0))
    elems11.append(sip_v11("CONN131", 7, 100.0, 3600.0))
    elems11.append(sip_v11("CONN132", 7, 300.0, 3600.0))
    elems11.append(vr101_outline("VR102", 200.0, 3500.0))

    # KRE 10-way 5.08mm Terminal Block + 3 Pass-thru columns (between MH102 and MH104)
    elems11.append(kre10_v11("TB101", 3400.0, 600.0))
    elems11.append(sip10_200mil("CONN137", 3300.0, 600.0))
    elems11.append(sip10_200mil("CONN138", 3200.0, 600.0))
    elems11.append(sip10_200mil("CONN139", 3100.0, 600.0))

    # Scratch-pad proto area (4 columns x 14 rows = 56 pads, 90 mil pad, 35 mil drill, 100 mil pitch)
    # Positioned between MH104 (Y=2850) and MH106 (Y=4600)
    sp_cols = [3100.0, 3200.0, 3300.0, 3400.0]
    for c_idx, cx in enumerate(sp_cols):
        ref = f"CONN13{3+c_idx}"
        elems11.append(sip_scratchpad_v11(ref, 14, cx, 3000.0))

    # 4. Left Bank: Cols 4..12 (X = 800.0 to 1600.0)
    # Rows 1..29 (CONN201..CONN229 at Y = 800 to 3600 mil)
    for r in range(29):
        ref = f"CONN2{r+1:02d}"
        y = 800.0 + r * 100.0
        elems11.append(sip_h11(ref, 9, 800.0, y))
    # Interconnect 1: Horizontal sandwich (HEADER18 in center, CONN240 above, CONN230 below)
    elems11.append(sip_h11("CONN240", 9, 800.0, 3800.0))
    elems11.append(header18_11("J201", 800.0, 3900.0))
    elems11.append(sip_h11("CONN230", 9, 800.0, 4100.0))
    for c in range(9):
        ref = f"CONN2{31+c:02d}"
        x = 800.0 + c * 100.0
        elems11.append(sip_v11(ref, 4, x, 4400.0))
    # 6. Card Edge Connector Fingers & Open Solder Jumpers (26 positions at Y = 4750..5000 mil)
    # Keyed with missing finger at column 8 from left to right (seen from top, X = 1200 mil)
    finger_cols = (
        [500.0, 600.0, 700.0] +
        [800.0 + c * 100.0 for c in range(9)] +
        [1700.0, 1800.0] +
        [1900.0 + c * 100.0 for c in range(9)] +
        [2800.0, 2900.0, 3000.0]
    )
    for idx, fx in enumerate(finger_cols):
        k = idx + 1
        if k != 8:
            elems11.append(edge_finger(f"EF{k}", fx, has_finger=True))


    # 5. Right Bank: Cols 15..23 (X = 1900.0 to 2700.0)
    # Rows 1..29 (CONN301..CONN329 at Y = 800 to 3600 mil)
    for r in range(29):
        ref = f"CONN3{r+1:02d}"
        y = 800.0 + r * 100.0
        elems11.append(sip_h11(ref, 9, 1900.0, y))
    # Interconnect 2: Horizontal sandwich (HEADER18 in center, CONN340 above, CONN330 below)
    elems11.append(sip_h11("CONN340", 9, 1900.0, 3800.0))
    elems11.append(header18_11("J301", 1900.0, 3900.0))
    elems11.append(sip_h11("CONN330", 9, 1900.0, 4100.0))
    for c in range(9):
        ref = f"CONN3{31+c:02d}"
        x = 1900.0 + c * 100.0
        elems11.append(sip_v11(ref, 4, x, 4400.0))

    # Copper tracks on bottom layer (connecting strip pins)
    bottom_lines11 = []
    # Power Jack 1 and Breakout SIP3 Traces (40 mil)
    # Pin 1 (+V): from Jack pin 1 (800, 200) to CONN119 pin 1 (500, 200)
    bottom_lines11.append('\tLine[500.00mil 200.00mil 800.00mil 200.00mil 40.00mil 20.00mil ""]')
    # Pin 2 (Middle): from Jack pin 2 (980, 290) to (800, 300) to CONN119 pin 2 (500, 300)
    bottom_lines11.append('\tLine[800.00mil 300.00mil 980.00mil 290.00mil 40.00mil 20.00mil ""]')
    bottom_lines11.append('\tLine[500.00mil 300.00mil 800.00mil 300.00mil 40.00mil 20.00mil ""]')
    # Pin 3 (Bottom): from Jack pin 3 (800, 380) to (800, 400) to CONN119 pin 3 (500, 400)
    bottom_lines11.append('\tLine[800.00mil 380.00mil 800.00mil 400.00mil 40.00mil 20.00mil ""]')
    bottom_lines11.append('\tLine[500.00mil 400.00mil 800.00mil 400.00mil 40.00mil 20.00mil ""]')

    # Power Jack 2 and Breakout SIP3 Traces (40 mil)
    # Pin 1 (+V): from Jack pin 1 (2400, 200) to CONN124 pin 1 (3000, 200)
    bottom_lines11.append('\tLine[2400.00mil 200.00mil 3000.00mil 200.00mil 40.00mil 20.00mil ""]')
    # Pin 2 (Middle): from Jack pin 2 (2580, 290) to (2700, 300) to CONN124 pin 2 (3000, 300)
    bottom_lines11.append('\tLine[2580.00mil 290.00mil 2700.00mil 300.00mil 40.00mil 20.00mil ""]')
    bottom_lines11.append('\tLine[2700.00mil 300.00mil 3000.00mil 300.00mil 40.00mil 20.00mil ""]')
    # Pin 3 (Bottom): from Jack pin 3 (2400, 380) to (2600, 400) to CONN124 pin 3 (3000, 400)
    bottom_lines11.append('\tLine[2400.00mil 380.00mil 2600.00mil 400.00mil 40.00mil 20.00mil ""]')
    bottom_lines11.append('\tLine[2600.00mil 400.00mil 3000.00mil 400.00mil 40.00mil 20.00mil ""]')

    # LM317 Circuit 1 traces (40 mil power/gnd, 20 mil adj)
    bottom_lines11.append('\tLine[1400.00mil 200.00mil 1400.00mil 400.00mil 40.00mil 20.00mil ""]')  # VIN1
    bottom_lines11.append('\tLine[1500.00mil 200.00mil 1500.00mil 500.00mil 40.00mil 20.00mil ""]')  # VOUT1
    bottom_lines11.append('\tLine[1600.00mil 300.00mil 1600.00mil 500.00mil 20.00mil 20.00mil ""]')  # ADJ1
    bottom_lines11.append('\tLine[1400.00mil 600.00mil 1600.00mil 600.00mil 40.00mil 20.00mil ""]')  # GND1 rail
    bottom_lines11.append('\tLine[1400.00mil 600.00mil 1400.00mil 700.00mil 40.00mil 20.00mil ""]')  # PAD_GND1

    # LM317 Circuit 2 traces (40 mil power/gnd, 20 mil adj)
    bottom_lines11.append('\tLine[1900.00mil 200.00mil 1900.00mil 400.00mil 40.00mil 20.00mil ""]')  # VIN2
    bottom_lines11.append('\tLine[2000.00mil 200.00mil 2000.00mil 500.00mil 40.00mil 20.00mil ""]')  # VOUT2
    bottom_lines11.append('\tLine[2100.00mil 300.00mil 2100.00mil 500.00mil 20.00mil 20.00mil ""]')  # ADJ2
    bottom_lines11.append('\tLine[1900.00mil 600.00mil 2100.00mil 600.00mil 40.00mil 20.00mil ""]')  # GND2 rail
    bottom_lines11.append('\tLine[1900.00mil 600.00mil 1900.00mil 700.00mil 40.00mil 20.00mil ""]')  # PAD_GND2

    # Common Ground bridge connecting both LM317 circuits (40 mil)
    bottom_lines11.append('\tLine[1600.00mil 600.00mil 1900.00mil 600.00mil 40.00mil 20.00mil ""]')

    # Stripboard 4x7 Power Connector Rails Module 1 (40 mil copper traces)
    bottom_lines11.append("\tLine[100.00mil 600.00mil 100.00mil 1200.00mil 40.00mil 20.00mil \"\"]")  # VIN1+
    bottom_lines11.append("\tLine[300.00mil 600.00mil 300.00mil 1200.00mil 40.00mil 20.00mil \"\"]")  # VIN1-
    bottom_lines11.append("\tLine[100.00mil 1400.00mil 100.00mil 2000.00mil 40.00mil 20.00mil \"\"]")  # OUT1+
    bottom_lines11.append("\tLine[300.00mil 1400.00mil 300.00mil 2000.00mil 40.00mil 20.00mil \"\"]")  # OUT1-

    # Stripboard 4x7 Power Connector Rails Module 2 (40 mil copper traces)
    bottom_lines11.append("\tLine[100.00mil 2800.00mil 100.00mil 3400.00mil 40.00mil 20.00mil \"\"]")  # VIN2+
    bottom_lines11.append("\tLine[300.00mil 2800.00mil 300.00mil 3400.00mil 40.00mil 20.00mil \"\"]")  # VIN2-
    bottom_lines11.append("\tLine[100.00mil 3600.00mil 100.00mil 4200.00mil 40.00mil 20.00mil \"\"]")  # OUT2+
    bottom_lines11.append("\tLine[300.00mil 3600.00mil 300.00mil 4200.00mil 40.00mil 20.00mil \"\"]")  # OUT2-

    # KRE 10-way horizontal pass-thru connections (30 mil copper traces, 10 distinct nets)
    for i in range(10):
        yi = 600.0 + i * 200.0
        bottom_lines11.append(f"\tLine[3100.00mil {yi:.2f}mil 3400.00mil {yi:.2f}mil 30.00mil 20.00mil \"\"]")

    # Scratch-pad 3 mil interconnections on bottom layer (net SCRATCHPAD)
    # Vertical lines along each of the 4 columns (13 segments each)
    for cx in sp_cols:
        for r in range(13):
            y1 = 3000.0 + r * 100.0
            y2 = y1 + 100.0
            bottom_lines11.append(f"\tLine[{cx:.2f}mil {y1:.2f}mil {cx:.2f}mil {y2:.2f}mil 3.00mil 10.00mil \"\"]")
    # Horizontal lines across each of the 14 rows (3 segments each)
    for r in range(14):
        y = 3000.0 + r * 100.0
        for c in range(3):
            x1 = sp_cols[c]
            x2 = sp_cols[c+1]
            bottom_lines11.append(f"\tLine[{x1:.2f}mil {y:.2f}mil {x2:.2f}mil {y:.2f}mil 3.00mil 10.00mil \"\"]")

    # 1. 8 Rails of 40 pins (from Y = 800.00 to 4700.00 mil) - 40 mil
    for rx in rails_x:
        bottom_lines11.append(f"\tLine[{rx:.2f}mil 800.00mil {rx:.2f}mil 4700.00mil 40.00mil 20.00mil \"\"]")
    # 2. Left Bank Horizontal Strips (Rows 1..29 at Y=800..3600) - 10 mil
    for r in range(29):
        y = 800.0 + r * 100.0
        bottom_lines11.append(f"\tLine[800.00mil {y:.2f}mil 1600.00mil {y:.2f}mil 10.00mil 20.00mil \"\"]")
    # Interconnect 1 vertical 100 mil bridges (CONN240 -> J201 row 1, and J201 row 2 -> CONN230) - 30 mil
    for c in range(9):
        x = 800.0 + c * 100.0
        bottom_lines11.append(f"\tLine[{x:.2f}mil 3800.00mil {x:.2f}mil 3900.00mil 30.00mil 20.00mil \"\"]")
        bottom_lines11.append(f"\tLine[{x:.2f}mil 4000.00mil {x:.2f}mil 4100.00mil 30.00mil 20.00mil \"\"]")
    # 3. Left Bank Bottom Vertical Strips (Cols 4..12, 4 pins from Y=4400 to 4700) - 40 mil
    for c in range(9):
        x = 800.0 + c * 100.0
        bottom_lines11.append(f"\tLine[{x:.2f}mil 4400.00mil {x:.2f}mil 4700.00mil 40.00mil 20.00mil \"\"]")
    # 4. Right Bank Horizontal Strips (Rows 1..29 at Y=800..3600) - 10 mil
    for r in range(29):
        y = 800.0 + r * 100.0
        bottom_lines11.append(f"\tLine[1900.00mil {y:.2f}mil 2700.00mil {y:.2f}mil 10.00mil 20.00mil \"\"]")
    # Interconnect 2 vertical 100 mil bridges (CONN340 -> J301 row 1, and J301 row 2 -> CONN330) - 30 mil
    for c in range(9):
        x = 1900.0 + c * 100.0
        bottom_lines11.append(f"\tLine[{x:.2f}mil 3800.00mil {x:.2f}mil 3900.00mil 30.00mil 20.00mil \"\"]")
        bottom_lines11.append(f"\tLine[{x:.2f}mil 4000.00mil {x:.2f}mil 4100.00mil 30.00mil 20.00mil \"\"]")
    # 5. Right Bank Bottom Vertical Strips (Cols 15..23, 4 pins from Y=4400 to 4700) - 40 mil
    for c in range(9):
        x = 1900.0 + c * 100.0
        bottom_lines11.append(f"\tLine[{x:.2f}mil 4400.00mil {x:.2f}mil 4700.00mil 40.00mil 20.00mil \"\"]")
    # 6. Open Solder Jumpers and Edge Finger Connections (30 mil)
    # Traces from pin (Y=4700) to Jumper Pad 1 (Y=4767.5), and Jumper Pad 2 (Y=4817.5) to Finger (Y=4855)
    # Column 8 (k=8 at X=1200 mil) is omitted (keyed missing finger)
    for idx, fx in enumerate(finger_cols):
        k = idx + 1
        if k != 8:
            bottom_lines11.append(f"\tLine[{fx:.2f}mil 4700.00mil {fx:.2f}mil 4750.00mil 30.00mil 20.00mil \"\"]")
            bottom_lines11.append(f"\tLine[{fx:.2f}mil 4793.00mil {fx:.2f}mil 4815.00mil 30.00mil 20.00mil \"\"]")

    rev11_pcb = f"""# release: pcb 4.2.2
FileVersion[20091103]
PCB["Custom Stripboard Rev 1.1" {w11:.2f}mil {h11:.2f}mil]
Grid[100.00mil 0.0000 0.0000 0]
PolyArea[200000000.000000]
Thermal[0.500000]
DRC[10.00mil 10.00mil 3.00mil 10.00mil 15.00mil 10.00mil]
Flags("nameonpcb,uniquename,clearnew,snappin")
Groups("1,c:2:3:4:5:6,s:7:8")
Styles["Signal,10.00mil,30.00mil,16.00mil,10.00mil:Power,20.00mil,45.00mil,25.00mil,10.00mil:Fat,30.00mil,50.00mil,25.00mil,10.00mil:Skinny,3.00mil,20.00mil,10.00mil,3.00mil"]
{symbols11}
{chr(10).join(elems11)}
Layer(1 "top") ()
Layer(2 "ground") ()
Layer(3 "signal2") ()
Layer(4 "signal3") ()
Layer(5 "power") ()
Layer(6 "bottom")
(
{chr(10).join(bottom_lines11)}
)
Layer(7 "outline")
(
\tLine[0.0000 0.0000 {w11:.2f}mil 0.0000 10.00mil 10.00mil ""]
\tLine[{w11:.2f}mil 0.0000 {w11:.2f}mil 4740.00mil 10.00mil 10.00mil ""]
\tLine[{w11:.2f}mil 4740.00mil 3100.00mil 4740.00mil 10.00mil 10.00mil ""]
\tLine[3100.00mil 4740.00mil 3100.00mil 5010.00mil 10.00mil 10.00mil ""]
\tLine[3100.00mil 5010.00mil 3060.00mil 5050.00mil 10.00mil 10.00mil ""]
\tLine[3060.00mil 5050.00mil 440.00mil 5050.00mil 10.00mil 10.00mil ""]
\tLine[440.00mil 5050.00mil 400.00mil 5010.00mil 10.00mil 10.00mil ""]
\tLine[400.00mil 5010.00mil 400.00mil 4740.00mil 10.00mil 10.00mil ""]
\tLine[400.00mil 4740.00mil 0.0000 4740.00mil 10.00mil 10.00mil ""]
\tLine[0.0000 4740.00mil 0.0000 0.0000 10.00mil 10.00mil ""]
)
Layer(8 "silk")
(
\tText[3410.00mil 800.00mil 3 120 "CUSTOM STRIPBOARD REV 1.1" ""]
\tText[1160.00mil 4725.00mil 0 60 "KEY" ""]
\tText[500.00mil 4735.00mil 0 60 "1" ""]
\tText[1100.00mil 4735.00mil 0 60 "7" ""]
\tText[1300.00mil 4735.00mil 0 60 "9" ""]
\tText[2980.00mil 4735.00mil 0 60 "26" ""]
\tText[1400.00mil 4715.00mil 0 70 "CARD EDGE - SINGLE SIDED (BOTTOM)" ""]
\tText[450.00mil 720.00mil 0 100 "RAILS (GND/+5V/+12V)" ""]
\tText[2750.00mil 720.00mil 0 100 "RAILS (GND/+5V/+12V)" ""]
\tText[1650.00mil 720.00mil 0 100 "CENTER" ""]
\tText[430.00mil 1600.00mil 3 70 "VR101: LM2596 #1" ""]
\tText[50.00mil 540.00mil 0 60 "VIN1+" ""]
\tText[250.00mil 540.00mil 0 60 "VIN1-" ""]
\tText[160.00mil 1320.00mil 0 50 "VR101" ""]
\tText[50.00mil 2060.00mil 0 60 "OUT1+" ""]
\tText[250.00mil 2060.00mil 0 60 "OUT1-" ""]
\tText[430.00mil 3800.00mil 3 70 "VR102: LM2596 #2" ""]
\tText[50.00mil 2740.00mil 0 60 "VIN2+" ""]
\tText[250.00mil 2740.00mil 0 60 "VIN2-" ""]
\tText[160.00mil 3520.00mil 0 50 "VR102" ""]
\tText[50.00mil 4260.00mil 0 60 "OUT2+" ""]
\tText[250.00mil 4260.00mil 0 60 "OUT2-" ""]
\tText[3050.00mil 520.00mil 0 50 "BORNE KRE 10P 5.08MM" ""]
\tText[3050.00mil 2520.00mil 0 50 "PASS-THRU (3 PINS/NET)" ""]
\tText[1350.00mil 130.00mil 0 50 "LM317 #1" ""]
\tText[1650.00mil 130.00mil 0 50 "LM317 #2" ""]
\tText[1330.00mil 210.00mil 0 45 "VIN1" ""]
\tText[1525.00mil 210.00mil 0 45 "VOUT1" ""]
\tText[1630.00mil 210.00mil 0 45 "VIN2" ""]
\tText[1825.00mil 210.00mil 0 45 "VOUT2" ""]
\tText[1340.00mil 710.00mil 0 45 "GND" ""]
\tText[1640.00mil 710.00mil 0 45 "GND" ""]
\tText[3050.00mil 2930.00mil 0 50 "SCRATCHPAD 56-PAD" ""]
\tText[3050.00mil 4370.00mil 0 50 "3MIL TRACE CUT" ""]
\tLine[3040.00mil 2950.00mil 3460.00mil 2950.00mil 10.00mil 10.00mil ""]
\tLine[3460.00mil 2950.00mil 3460.00mil 4350.00mil 10.00mil 10.00mil ""]
\tLine[3460.00mil 4350.00mil 3040.00mil 4350.00mil 10.00mil 10.00mil ""]
\tLine[3040.00mil 4350.00mil 3040.00mil 2950.00mil 10.00mil 10.00mil ""]
\tText[950.00mil 600.00mil 0 120 "PWR JACK 1" ""]
\tText[2050.00mil 600.00mil 0 120 "PWR JACK 2" ""]
\tText[1350.00mil 130.00mil 0 80 "J1 PWR OUT" ""]
\tText[2450.00mil 130.00mil 0 80 "J2 PWR OUT" ""]
)
"""
    with open(p11_file, "w") as f:
        f.write(rev11_pcb)

    # ------------------ REV 1.1a ------------------
    # Sub-revision 1.1a:
    # 1. Sandwiched connectors J201 / J301 with CONN240/CONN230 and CONN340/CONN330 shifted 2 rows down (to Y = 4000..4300 mil).
    # 2. Opened rows (Y = 3700, 3800, 3900 mil) filled with 9-pin connectors as the others (CONN241..243 and CONN341..343).
    w11a = 3500.0
    h11a = 5050.0

    p11a_file = os.path.join(base_dir, "rev1.1a/stripboard_rev1.1a.pcb")

    elems11a = []

    # 1. 8 Rails of 40 pins (2x SIP20N each)
    for idx, rx in enumerate(rails_x):
        ref1 = f"CONN1{2*idx+1:02d}"
        ref2 = f"CONN1{2*idx+2:02d}"
        elems11a.append(sip_v11(ref1, 20, rx, 800.0))
        elems11a.append(sip_v11(ref2, 20, rx, 2800.0))

    # 2. Power Jacks & Breakout Connectors (spaced apart towards edges)
    # Jack 1 placed at X = 800 mil, breakout CONN119..121 to the left at X = 500, 600, 700 mil
    elems11a.append(pwrjack11("CONN117", 800.0, 200.0))
    elems11a.append(sip_v11("CONN119", 3, 500.0, 200.0))
    elems11a.append(sip_v11("CONN120", 3, 600.0, 200.0))
    elems11a.append(sip_v11("CONN121", 3, 700.0, 200.0))

    # Jack 2 placed at X = 2400 mil, breakout CONN122..124 to the right at X = 2800, 2900, 3000 mil
    elems11a.append(pwrjack11("CONN118", 2400.0, 200.0))
    elems11a.append(sip_v11("CONN122", 3, 2800.0, 200.0))
    elems11a.append(sip_v11("CONN123", 3, 2900.0, 200.0))
    elems11a.append(sip_v11("CONN124", 3, 3000.0, 200.0))

    # 2b. Two LM317 Regulator Circuits inserted between the Power Jacks (Through-Hole Default)
    # Circuit 1: X = 1400..1600 mil (U101, C101, C102, R101, R102, J101, J102, J103)
    elems11a.append(lm317_to220("U101", 1400.0, 300.0))
    elems11a.append(single_pad("J101", "VIN1", 1400.0, 200.0))
    elems11a.append(single_pad("J102", "VOUT1", 1500.0, 200.0))
    elems11a.append(single_pad("J103", "GND", 1400.0, 700.0))
    elems11a.append(cap_2pin_v("C101", "0.1uF", 1400.0, 400.0, 600.0))
    elems11a.append(cap_2pin_v("C102", "1uF", 1500.0, 400.0, 600.0))
    elems11a.append(res_2pin_h("R101", "240", 1500.0, 1600.0, 500.0))
    elems11a.append(res_2pin_v("R102", "R2", 1600.0, 400.0, 600.0))

    # Circuit 2: X = 1900..2100 mil (U102, C103, C104, R103, R104, J104, J105, J106)
    elems11a.append(lm317_to220("U102", 1900.0, 300.0))
    elems11a.append(single_pad("J104", "VIN2", 1900.0, 200.0))
    elems11a.append(single_pad("J105", "VOUT2", 2000.0, 200.0))
    elems11a.append(single_pad("J106", "GND", 1900.0, 700.0))
    elems11a.append(cap_2pin_v("C103", "0.1uF", 1900.0, 400.0, 600.0))
    elems11a.append(cap_2pin_v("C104", "1uF", 2000.0, 400.0, 600.0))
    elems11a.append(res_2pin_h("R103", "240", 2000.0, 2100.0, 500.0))
    elems11a.append(res_2pin_v("R104", "R2", 2100.0, 400.0, 600.0))

    # 3. 6x M3 Mounting Holes (margins at X = 200 mil and X = 3300 mil)
    # MH103 and MH104 centered at Y = 2400 mil to provide equal 2200 mil spans (200..2400 and 2400..4600)
    elems11a.append(mthole11("MH101", 200.0, 200.0, 160.0))
    elems11a.append(mthole11("MH102", 3300.0, 200.0, 160.0))
    elems11a.append(mthole11("MH103", 200.0, 2400.0, 160.0))
    elems11a.append(mthole11("MH104", 3300.0, 2700.0, 160.0))
    elems11a.append(mthole11("MH105", 200.0, 4600.0, -180.0))
    elems11a.append(mthole11("MH106", 3300.0, 4600.0, -180.0))

    # Stripboard Module 1 connectors VIN1+, VIN1-, OUT1+, OUT1- (4x7 points centered between MH101 and MH103)
    # Left row (X = 100 mil): VIN1+ (top, Y=600..1200) and OUT1+ (bottom, Y=1400..2000)
    # Right row (X = 300 mil): VIN1- (top, Y=600..1200) and OUT1- (bottom, Y=1400..2000)
    elems11a.append(sip_v11("CONN125", 7, 100.0, 600.0))
    elems11a.append(sip_v11("CONN126", 7, 300.0, 600.0))
    elems11a.append(sip_v11("CONN127", 7, 100.0, 1400.0))
    elems11a.append(sip_v11("CONN128", 7, 300.0, 1400.0))
    elems11a.append(vr101_outline("VR101", 200.0, 1300.0))

    # Stripboard Module 2 connectors VIN2+, VIN2-, OUT2+, OUT2- (4x7 points centered between MH103 and MH105)
    # Left row (X = 100 mil): VIN2+ (top, Y=2800..3400) and OUT2+ (bottom, Y=3600..4200)
    # Right row (X = 300 mil): VIN2- (top, Y=2800..3400) and OUT2- (bottom, Y=3600..4200)
    elems11a.append(sip_v11("CONN129", 7, 100.0, 2800.0))
    elems11a.append(sip_v11("CONN130", 7, 300.0, 2800.0))
    elems11a.append(sip_v11("CONN131", 7, 100.0, 3600.0))
    elems11a.append(sip_v11("CONN132", 7, 300.0, 3600.0))
    elems11a.append(vr101_outline("VR102", 200.0, 3500.0))

    # KRE 10-way 5.08mm Terminal Block + 3 Pass-thru columns (between MH102 and MH104)
    elems11a.append(kre10_v11("TB101", 3400.0, 600.0))
    elems11a.append(sip10_200mil("CONN137", 3300.0, 600.0))
    elems11a.append(sip10_200mil("CONN138", 3200.0, 600.0))
    elems11a.append(sip10_200mil("CONN139", 3100.0, 600.0))

    # Scratch-pad proto area (4 columns x 14 rows = 56 pads, 90 mil pad, 35 mil drill, 100 mil pitch)
    # Positioned between MH104 (Y=2850) and MH106 (Y=4600)
    for c_idx, cx in enumerate(sp_cols):
        ref = f"CONN13{3+c_idx}"
        elems11a.append(sip_scratchpad_v11(ref, 14, cx, 3000.0))

    # 4. Left Bank: Cols 4..12 (X = 800.0 to 1600.0)
    # Rows 1..29 (CONN201..CONN229 at Y = 800 to 3600 mil)
    for r in range(29):
        ref = f"CONN2{r+1:02d}"
        y = 800.0 + r * 100.0
        elems11a.append(sip_h11(ref, 9, 800.0, y))
    # Rows 30..32 (CONN241..CONN243 at Y = 3700 to 3900 mil) filling opened rows
    elems11a.append(sip_h11("CONN241", 9, 800.0, 3700.0))
    elems11a.append(sip_h11("CONN242", 9, 800.0, 3800.0))
    elems11a.append(sip_h11("CONN243", 9, 800.0, 3900.0))

    # Interconnect 1: Shifted 2 rows down (CONN240 at 4000, J201 at 4100, CONN230 at 4300)
    elems11a.append(sip_h11("CONN240", 9, 800.0, 4000.0))
    elems11a.append(header18_11("J201", 800.0, 4100.0))
    elems11a.append(sip_h11("CONN230", 9, 800.0, 4300.0))

    # Bottom vertical strips (Cols 4..12, 4 pins from Y = 4400 to 4700 mil)
    for c in range(9):
        ref = f"CONN2{31+c:02d}"
        x = 800.0 + c * 100.0
        elems11a.append(sip_v11(ref, 4, x, 4400.0))

    # 5. Right Bank: Cols 15..23 (X = 1900.0 to 2700.0)
    # Rows 1..29 (CONN301..CONN329 at Y = 800 to 3600 mil)
    for r in range(29):
        ref = f"CONN3{r+1:02d}"
        y = 800.0 + r * 100.0
        elems11a.append(sip_h11(ref, 9, 1900.0, y))
    # Rows 30..32 (CONN341..CONN343 at Y = 3700 to 3900 mil) filling opened rows
    elems11a.append(sip_h11("CONN341", 9, 1900.0, 3700.0))
    elems11a.append(sip_h11("CONN342", 9, 1900.0, 3800.0))
    elems11a.append(sip_h11("CONN343", 9, 1900.0, 3900.0))

    # Interconnect 2: Shifted 2 rows down (CONN340 at 4000, J301 at 4100, CONN330 at 4300)
    elems11a.append(sip_h11("CONN340", 9, 1900.0, 4000.0))
    elems11a.append(header18_11("J301", 1900.0, 4100.0))
    elems11a.append(sip_h11("CONN330", 9, 1900.0, 4300.0))

    # Bottom vertical strips (Cols 15..23, 4 pins from Y = 4400 to 4700 mil)
    for c in range(9):
        ref = f"CONN3{31+c:02d}"
        x = 1900.0 + c * 100.0
        elems11a.append(sip_v11(ref, 4, x, 4400.0))

    # 6. Card Edge Connector Fingers & Open Solder Jumpers (26 positions)
    for idx, fx in enumerate(finger_cols):
        k = idx + 1
        if k != 8:
            elems11a.append(edge_finger(f"EF{k}", fx, has_finger=True))

    # Copper tracks on bottom layer for Rev 1.1a
    bottom_lines11a = []
    # Power Jack 1 and Breakout SIP3 Traces (40 mil)
    # Pin 1 (+V): from Jack pin 1 (800, 200) to CONN119 pin 1 (500, 200)
    bottom_lines11a.append('\tLine[500.00mil 200.00mil 800.00mil 200.00mil 40.00mil 20.00mil ""]')
    # Pin 2 (Middle): from Jack pin 2 (980, 290) to (800, 300) to CONN119 pin 2 (500, 300)
    bottom_lines11a.append('\tLine[800.00mil 300.00mil 980.00mil 290.00mil 40.00mil 20.00mil ""]')
    bottom_lines11a.append('\tLine[500.00mil 300.00mil 800.00mil 300.00mil 40.00mil 20.00mil ""]')
    # Pin 3 (Bottom): from Jack pin 3 (800, 380) to (800, 400) to CONN119 pin 3 (500, 400)
    bottom_lines11a.append('\tLine[800.00mil 380.00mil 800.00mil 400.00mil 40.00mil 20.00mil ""]')
    bottom_lines11a.append('\tLine[500.00mil 400.00mil 800.00mil 400.00mil 40.00mil 20.00mil ""]')

    # Power Jack 2 and Breakout SIP3 Traces (40 mil)
    # Pin 1 (+V): from Jack pin 1 (2400, 200) to CONN124 pin 1 (3000, 200)
    bottom_lines11a.append('\tLine[2400.00mil 200.00mil 3000.00mil 200.00mil 40.00mil 20.00mil ""]')
    # Pin 2 (Middle): from Jack pin 2 (2580, 290) to (2700, 300) to CONN124 pin 2 (3000, 300)
    bottom_lines11a.append('\tLine[2580.00mil 290.00mil 2700.00mil 300.00mil 40.00mil 20.00mil ""]')
    bottom_lines11a.append('\tLine[2700.00mil 300.00mil 3000.00mil 300.00mil 40.00mil 20.00mil ""]')
    # Pin 3 (Bottom): from Jack pin 3 (2400, 380) to (2600, 400) to CONN124 pin 3 (3000, 400)
    bottom_lines11a.append('\tLine[2400.00mil 380.00mil 2600.00mil 400.00mil 40.00mil 20.00mil ""]')
    bottom_lines11a.append('\tLine[2600.00mil 400.00mil 3000.00mil 400.00mil 40.00mil 20.00mil ""]')

    # LM317 Circuit 1 traces (40 mil power/gnd, 20 mil adj)
    bottom_lines11a.append('\tLine[1400.00mil 200.00mil 1400.00mil 400.00mil 40.00mil 20.00mil ""]')  # VIN1
    bottom_lines11a.append('\tLine[1500.00mil 200.00mil 1500.00mil 500.00mil 40.00mil 20.00mil ""]')  # VOUT1
    bottom_lines11a.append('\tLine[1600.00mil 300.00mil 1600.00mil 500.00mil 20.00mil 20.00mil ""]')  # ADJ1
    bottom_lines11a.append('\tLine[1400.00mil 600.00mil 1600.00mil 600.00mil 40.00mil 20.00mil ""]')  # GND1 rail
    bottom_lines11a.append('\tLine[1400.00mil 600.00mil 1400.00mil 700.00mil 40.00mil 20.00mil ""]')  # PAD_GND1

    # LM317 Circuit 2 traces (40 mil power/gnd, 20 mil adj)
    bottom_lines11a.append('\tLine[1900.00mil 200.00mil 1900.00mil 400.00mil 40.00mil 20.00mil ""]')  # VIN2
    bottom_lines11a.append('\tLine[2000.00mil 200.00mil 2000.00mil 500.00mil 40.00mil 20.00mil ""]')  # VOUT2
    bottom_lines11a.append('\tLine[2100.00mil 300.00mil 2100.00mil 500.00mil 20.00mil 20.00mil ""]')  # ADJ2
    bottom_lines11a.append('\tLine[1900.00mil 600.00mil 2100.00mil 600.00mil 40.00mil 20.00mil ""]')  # GND2 rail
    bottom_lines11a.append('\tLine[1900.00mil 600.00mil 1900.00mil 700.00mil 40.00mil 20.00mil ""]')  # PAD_GND2

    # Common Ground bridge connecting both LM317 circuits (40 mil)
    bottom_lines11a.append('\tLine[1600.00mil 600.00mil 1900.00mil 600.00mil 40.00mil 20.00mil ""]')

    # Stripboard 4x7 Power Connector Rails Module 1 (40 mil copper traces)
    bottom_lines11a.append("\tLine[100.00mil 600.00mil 100.00mil 1200.00mil 40.00mil 20.00mil \"\"]")  # VIN1+
    bottom_lines11a.append("\tLine[300.00mil 600.00mil 300.00mil 1200.00mil 40.00mil 20.00mil \"\"]")  # VIN1-
    bottom_lines11a.append("\tLine[100.00mil 1400.00mil 100.00mil 2000.00mil 40.00mil 20.00mil \"\"]")  # OUT1+
    bottom_lines11a.append("\tLine[300.00mil 1400.00mil 300.00mil 2000.00mil 40.00mil 20.00mil \"\"]")  # OUT1-

    # Stripboard 4x7 Power Connector Rails Module 2 (40 mil copper traces)
    bottom_lines11a.append("\tLine[100.00mil 2800.00mil 100.00mil 3400.00mil 40.00mil 20.00mil \"\"]")  # VIN2+
    bottom_lines11a.append("\tLine[300.00mil 2800.00mil 300.00mil 3400.00mil 40.00mil 20.00mil \"\"]")  # VIN2-
    bottom_lines11a.append("\tLine[100.00mil 3600.00mil 100.00mil 4200.00mil 40.00mil 20.00mil \"\"]")  # OUT2+
    bottom_lines11a.append("\tLine[300.00mil 3600.00mil 300.00mil 4200.00mil 40.00mil 20.00mil \"\"]")  # OUT2-

    # KRE 10-way horizontal pass-thru connections (30 mil copper traces, 10 distinct nets)
    for i in range(10):
        yi = 600.0 + i * 200.0
        bottom_lines11a.append(f"\tLine[3100.00mil {yi:.2f}mil 3400.00mil {yi:.2f}mil 30.00mil 20.00mil \"\"]")

    # Scratch-pad 3 mil interconnections on bottom layer (net SCRATCHPAD)
    # Vertical lines along each of the 4 columns (13 segments each)
    for cx in sp_cols:
        for r in range(13):
            y1 = 3000.0 + r * 100.0
            y2 = y1 + 100.0
            bottom_lines11a.append(f"\tLine[{cx:.2f}mil {y1:.2f}mil {cx:.2f}mil {y2:.2f}mil 3.00mil 10.00mil \"\"]")
    # Horizontal lines across each of the 14 rows (3 segments each)
    for r in range(14):
        y = 3000.0 + r * 100.0
        for c in range(3):
            x1 = sp_cols[c]
            x2 = sp_cols[c+1]
            bottom_lines11a.append(f"\tLine[{x1:.2f}mil {y:.2f}mil {x2:.2f}mil {y:.2f}mil 3.00mil 10.00mil \"\"]")

    # 1. 8 Rails of 40 pins (from Y = 800.00 to 4700.00 mil) - 40 mil
    for rx in rails_x:
        bottom_lines11a.append(f"\tLine[{rx:.2f}mil 800.00mil {rx:.2f}mil 4700.00mil 40.00mil 20.00mil \"\"]")

    # 2. Left Bank Horizontal Strips (Rows 1..32 at Y = 800..3900 mil) - 10 mil
    for r in range(32):
        y = 800.0 + r * 100.0
        bottom_lines11a.append(f"\tLine[800.00mil {y:.2f}mil 1600.00mil {y:.2f}mil 10.00mil 20.00mil \"\"]")

    # Interconnect 1 vertical 100 mil bridges (CONN240 -> J201 row 1, and J201 row 2 -> CONN230) - 30 mil
    for c in range(9):
        x = 800.0 + c * 100.0
        bottom_lines11a.append(f"\tLine[{x:.2f}mil 4000.00mil {x:.2f}mil 4100.00mil 30.00mil 20.00mil \"\"]")
        bottom_lines11a.append(f"\tLine[{x:.2f}mil 4200.00mil {x:.2f}mil 4300.00mil 30.00mil 20.00mil \"\"]")

    # 3. Left Bank Bottom Vertical Strips (Cols 4..12, 4 pins from Y = 4400 to 4700 mil) - 40 mil
    for c in range(9):
        x = 800.0 + c * 100.0
        bottom_lines11a.append(f"\tLine[{x:.2f}mil 4400.00mil {x:.2f}mil 4700.00mil 40.00mil 20.00mil \"\"]")

    # 4. Right Bank Horizontal Strips (Rows 1..32 at Y = 800..3900 mil) - 10 mil
    for r in range(32):
        y = 800.0 + r * 100.0
        bottom_lines11a.append(f"\tLine[1900.00mil {y:.2f}mil 2700.00mil {y:.2f}mil 10.00mil 20.00mil \"\"]")

    # Interconnect 2 vertical 100 mil bridges (CONN340 -> J301 row 1, and J301 row 2 -> CONN330) - 30 mil
    for c in range(9):
        x = 1900.0 + c * 100.0
        bottom_lines11a.append(f"\tLine[{x:.2f}mil 4000.00mil {x:.2f}mil 4100.00mil 30.00mil 20.00mil \"\"]")
        bottom_lines11a.append(f"\tLine[{x:.2f}mil 4200.00mil {x:.2f}mil 4300.00mil 30.00mil 20.00mil \"\"]")

    # 5. Right Bank Bottom Vertical Strips (Cols 15..23, 4 pins from Y = 4400 to 4700 mil) - 40 mil
    for c in range(9):
        x = 1900.0 + c * 100.0
        bottom_lines11a.append(f"\tLine[{x:.2f}mil 4400.00mil {x:.2f}mil 4700.00mil 40.00mil 20.00mil \"\"]")

    # 6. Open Solder Jumpers and Edge Finger Connections (30 mil)
    for idx, fx in enumerate(finger_cols):
        k = idx + 1
        if k != 8:
            bottom_lines11a.append(f"\tLine[{fx:.2f}mil 4700.00mil {fx:.2f}mil 4750.00mil 30.00mil 20.00mil \"\"]")
            bottom_lines11a.append(f"\tLine[{fx:.2f}mil 4793.00mil {fx:.2f}mil 4815.00mil 30.00mil 20.00mil \"\"]")

    rev11a_pcb = f"""# release: pcb 4.2.2
FileVersion[20091103]
PCB["Custom Stripboard Rev 1.1a" {w11a:.2f}mil {h11a:.2f}mil]
Grid[100.00mil 0.0000 0.0000 0]
PolyArea[200000000.000000]
Thermal[0.500000]
DRC[10.00mil 10.00mil 3.00mil 10.00mil 15.00mil 10.00mil]
Flags("nameonpcb,uniquename,clearnew,snappin")
Groups("1,c:2:3:4:5:6,s:7:8")
Styles["Signal,10.00mil,30.00mil,16.00mil,10.00mil:Power,20.00mil,45.00mil,25.00mil,10.00mil:Fat,30.00mil,50.00mil,25.00mil,10.00mil:Skinny,3.00mil,20.00mil,10.00mil,3.00mil"]
{symbols11}
{chr(10).join(elems11a)}
Layer(1 "top") ()
Layer(2 "ground") ()
Layer(3 "signal2") ()
Layer(4 "signal3") ()
Layer(5 "power") ()
Layer(6 "bottom")
(
{chr(10).join(bottom_lines11a)}
)
Layer(7 "outline")
(
\tLine[0.0000 0.0000 {w11a:.2f}mil 0.0000 10.00mil 10.00mil ""]
\tLine[{w11a:.2f}mil 0.0000 {w11a:.2f}mil 4740.00mil 10.00mil 10.00mil ""]
\tLine[{w11a:.2f}mil 4740.00mil 3100.00mil 4740.00mil 10.00mil 10.00mil ""]
\tLine[3100.00mil 4740.00mil 3100.00mil 5010.00mil 10.00mil 10.00mil ""]
\tLine[3100.00mil 5010.00mil 3060.00mil 5050.00mil 10.00mil 10.00mil ""]
\tLine[3060.00mil 5050.00mil 440.00mil 5050.00mil 10.00mil 10.00mil ""]
\tLine[440.00mil 5050.00mil 400.00mil 5010.00mil 10.00mil 10.00mil ""]
\tLine[400.00mil 5010.00mil 400.00mil 4740.00mil 10.00mil 10.00mil ""]
\tLine[400.00mil 4740.00mil 0.0000 4740.00mil 10.00mil 10.00mil ""]
\tLine[0.0000 4740.00mil 0.0000 0.0000 10.00mil 10.00mil ""]
)
Layer(8 "silk")
(
\tText[3410.00mil 800.00mil 3 120 "CUSTOM STRIPBOARD REV 1.1a" ""]
\tText[1160.00mil 4725.00mil 0 60 "KEY" ""]
\tText[500.00mil 4735.00mil 0 60 "1" ""]
\tText[1100.00mil 4735.00mil 0 60 "7" ""]
\tText[1300.00mil 4735.00mil 0 60 "9" ""]
\tText[2980.00mil 4735.00mil 0 60 "26" ""]
\tText[1400.00mil 4715.00mil 0 70 "CARD EDGE - SINGLE SIDED (BOTTOM)" ""]
\tText[450.00mil 720.00mil 0 100 "RAILS (GND/+5V/+12V)" ""]
\tText[2750.00mil 720.00mil 0 100 "RAILS (GND/+5V/+12V)" ""]
\tText[1650.00mil 720.00mil 0 100 "CENTER" ""]
\tText[430.00mil 1600.00mil 3 70 "VR101: LM2596 #1" ""]
\tText[50.00mil 540.00mil 0 60 "VIN1+" ""]
\tText[250.00mil 540.00mil 0 60 "VIN1-" ""]
\tText[160.00mil 1320.00mil 0 50 "VR101" ""]
\tText[50.00mil 2060.00mil 0 60 "OUT1+" ""]
\tText[250.00mil 2060.00mil 0 60 "OUT1-" ""]
\tText[430.00mil 3800.00mil 3 70 "VR102: LM2596 #2" ""]
\tText[50.00mil 2740.00mil 0 60 "VIN2+" ""]
\tText[250.00mil 2740.00mil 0 60 "VIN2-" ""]
\tText[160.00mil 3520.00mil 0 50 "VR102" ""]
\tText[50.00mil 4260.00mil 0 60 "OUT2+" ""]
\tText[250.00mil 4260.00mil 0 60 "OUT2-" ""]
\tText[3050.00mil 520.00mil 0 50 "BORNE KRE 10P 5.08MM" ""]
\tText[3050.00mil 2520.00mil 0 50 "PASS-THRU (3 PINS/NET)" ""]
\tText[1350.00mil 130.00mil 0 50 "LM317 #1" ""]
\tText[1650.00mil 130.00mil 0 50 "LM317 #2" ""]
\tText[1330.00mil 210.00mil 0 45 "VIN1" ""]
\tText[1525.00mil 210.00mil 0 45 "VOUT1" ""]
\tText[1630.00mil 210.00mil 0 45 "VIN2" ""]
\tText[1825.00mil 210.00mil 0 45 "VOUT2" ""]
\tText[1340.00mil 710.00mil 0 45 "GND" ""]
\tText[1640.00mil 710.00mil 0 45 "GND" ""]
\tText[3050.00mil 2930.00mil 0 50 "SCRATCHPAD 56-PAD" ""]
\tText[3050.00mil 4370.00mil 0 50 "3MIL TRACE CUT" ""]
\tLine[3040.00mil 2950.00mil 3460.00mil 2950.00mil 10.00mil 10.00mil ""]
\tLine[3460.00mil 2950.00mil 3460.00mil 4350.00mil 10.00mil 10.00mil ""]
\tLine[3460.00mil 4350.00mil 3040.00mil 4350.00mil 10.00mil 10.00mil ""]
\tLine[3040.00mil 4350.00mil 3040.00mil 2950.00mil 10.00mil 10.00mil ""]
\tText[950.00mil 600.00mil 0 120 "PWR JACK 1" ""]
\tText[2050.00mil 600.00mil 0 120 "PWR JACK 2" ""]
\tText[1350.00mil 130.00mil 0 80 "J1 PWR OUT" ""]
\tText[2450.00mil 130.00mil 0 80 "J2 PWR OUT" ""]
)
"""
    with open(p11a_file, "w") as f:
        f.write(rev11a_pcb)

    # ------------------ REV 1.0 ------------------
    # Board dimensions: Width = 1300.00 mil (33.02 mm), Height = 2840.00 mil (72.14 mm)
    w10 = 1300.0
    h10 = 2840.0

    p10_file = os.path.join(base_dir, "rev1.0/stripboard_rev1.0.pcb")
    with open(p10_file) as f:
        text10 = f.read()

    symbols_block10 = text10.split("PCB[")[1].split("Element[")[0]
    sym_idx10 = symbols_block10.find("Symbol[")
    symbols10 = symbols_block10[sym_idx10:]

    elems10 = []

    def sip12_h10(ref, x, y):
        tx = 450.0
        ty = -24.0
        res = [f"""Element["" "SIP12N" "{ref}" "unknown" {x:.2f}mil {y:.2f}mil {tx:.2f}mil {ty:.2f}mil 0 80 ""]""", "("]
        for i in range(1, 13):
            px = (i - 1) * 100.0
            flag = "square" if i == 1 else ""
            res.append(f"""\tPin[{px:.2f}mil 0.0000 80.00mil 10.00mil 86.00mil 35.00mil "{i}" "{i}" "{flag}"]""")
        end_x = 11 * 100.0
        res.append(f"\tElementLine [0.0000 -35.00mil {end_x:.2f}mil -35.00mil 10.00mil]")
        res.append(f"\tElementLine [0.0000  35.00mil {end_x:.2f}mil  35.00mil 10.00mil]")
        res.append(f"\tElementArc [0.0000 0.0000 35.00mil 35.00mil 90 180 10.00mil]")
        res.append(f"\tElementArc [{end_x:.2f}mil 0.0000 35.00mil 35.00mil 270 180 10.00mil]")
        res.append(")")
        return "\n".join(res)

    def sip27_v10(ref, x, y):
        tx = 24.0
        ty = 200.0
        res = [f"""Element["" "SIP27N" "{ref}" "unknown" {x:.2f}mil {y:.2f}mil {tx:.2f}mil {ty:.2f}mil 3 80 ""]""", "("]
        for i in range(1, 28):
            py = (i - 1) * 100.0
            flag = "square" if i == 1 else ""
            res.append(f"""\tPin[0.0000 {py:.2f}mil 80.00mil 10.00mil 86.00mil 35.00mil "{i}" "{i}" "{flag}"]""")
        end_y = 26 * 100.0
        res.append(f"\tElementLine [-35.00mil 0.0000 -35.00mil {end_y:.2f}mil 10.00mil]")
        res.append(f"\tElementLine [ 35.00mil 0.0000  35.00mil {end_y:.2f}mil 10.00mil]")
        res.append(f"\tElementArc [0.0000 0.0000 35.00mil 35.00mil 180 180 10.00mil]")
        res.append(f"\tElementArc [0.0000 {end_y:.2f}mil 35.00mil 35.00mil 0 180 10.00mil]")
        res.append(")")
        return "\n".join(res)

    def sip4_h10(ref, x, y):
        tx = 60.0
        ty = -24.0
        res = [f"""Element["" "SIP4N" "{ref}" "unknown" {x:.2f}mil {y:.2f}mil {tx:.2f}mil {ty:.2f}mil 0 80 ""]""", "("]
        for i in range(1, 5):
            px = (i - 1) * 100.0
            flag = "square" if i == 1 else ""
            res.append(f"""\tPin[{px:.2f}mil 0.0000 80.00mil 10.00mil 86.00mil 35.00mil "{i}" "{i}" "{flag}"]""")
        end_x = 3 * 100.0
        res.append(f"\tElementLine [0.0000 -35.00mil {end_x:.2f}mil -35.00mil 10.00mil]")
        res.append(f"\tElementLine [0.0000  35.00mil {end_x:.2f}mil  35.00mil 10.00mil]")
        res.append(f"\tElementArc [0.0000 0.0000 35.00mil 35.00mil 90 180 10.00mil]")
        res.append(f"\tElementArc [{end_x:.2f}mil 0.0000 35.00mil 35.00mil 270 180 10.00mil]")
        res.append(")")
        return "\n".join(res)

    # CONN101: Top rail
    elems10.append(sip12_h10("CONN101", 100.0, 70.0))
    # CONN102, 103, 104, 105: 4 vertical rails
    elems10.append(sip27_v10("CONN102", 100.0, 170.0))
    elems10.append(sip27_v10("CONN103", 600.0, 170.0))
    elems10.append(sip27_v10("CONN104", 700.0, 170.0))
    elems10.append(sip27_v10("CONN105", 1200.0, 170.0))
    # Left bank 27 rows of SIP4N (CONN201..CONN227)
    for r in range(27):
        ref = f"CONN2{r+1:02d}"
        y = 170.0 + r * 100.0
        elems10.append(sip4_h10(ref, 200.0, y))
    # Right bank 27 rows of SIP4N (CONN301..CONN327)
    for r in range(27):
        ref = f"CONN3{r+1:02d}"
        y = 170.0 + r * 100.0
        elems10.append(sip4_h10(ref, 800.0, y))

    # Copper tracks on bottom layer for Rev 1.0
    bottom_lines10 = []
    # 1. Top horizontal rail (CONN101, 12 pins) from X = 100 to 1200 mil at Y = 70 mil
    bottom_lines10.append(f"\tLine[100.00mil 70.00mil 1200.00mil 70.00mil 40.00mil 20.00mil \"\"]")
    # 2. 4 vertical rails (CONN102..105, 27 pins) at X = 100, 600, 700, 1200 mil from Y = 170 to 2770 mil
    for rx in [100.0, 600.0, 700.0, 1200.0]:
        bottom_lines10.append(f"\tLine[{rx:.2f}mil 170.00mil {rx:.2f}mil 2770.00mil 40.00mil 20.00mil \"\"]")
    # 3. Left bank 27 horizontal rows (CONN201..227, 4 pins) from X = 200 to 500 mil
    for r in range(27):
        y = 170.0 + r * 100.0
        bottom_lines10.append(f"\tLine[200.00mil {y:.2f}mil 500.00mil {y:.2f}mil 40.00mil 20.00mil \"\"]")
    # 4. Right bank 27 horizontal rows (CONN301..327, 4 pins) from X = 800 to 1100 mil
    for r in range(27):
        y = 170.0 + r * 100.0
        bottom_lines10.append(f"\tLine[800.00mil {y:.2f}mil 1100.00mil {y:.2f}mil 40.00mil 20.00mil \"\"]")

    rev10_pcb = f"""# release: pcb 4.2.2
FileVersion[20091103]
PCB["Custom Stripboard Rev 1.0 (33x72mm)" {w10:.2f}mil {h10:.2f}mil]
Grid[100.00mil 0.0000 0.0000 0]
PolyArea[200000000.000000]
Thermal[0.500000]
DRC[10.00mil 10.00mil 3.00mil 10.00mil 15.00mil 10.00mil]
Flags("nameonpcb,uniquename,clearnew,snappin")
Groups("1,c:2:3:4:5:6,s:7:8")
Styles["Signal,10.00mil,36.00mil,20.00mil,10.00mil:Power,25.00mil,60.00mil,35.00mil,10.00mil:Fat,40.00mil,60.00mil,35.00mil,10.00mil:Skinny,6.00mil,24.02mil,11.81mil,6.00mil"]
{symbols10}
{chr(10).join(elems10)}
Layer(1 "top") ()
Layer(2 "ground") ()
Layer(3 "signal2") ()
Layer(4 "signal3") ()
Layer(5 "power") ()
Layer(6 "bottom")
(
{chr(10).join(bottom_lines10)}
)
Layer(7 "outline")
(
\tLine[0.0000 0.0000 {w10:.2f}mil 0.0000 10.00mil 10.00mil ""]
\tLine[{w10:.2f}mil 0.0000 {w10:.2f}mil {h10:.2f}mil 10.00mil 10.00mil ""]
\tLine[{w10:.2f}mil {h10:.2f}mil 0.0000 {h10:.2f}mil 10.00mil 10.00mil ""]
\tLine[0.0000 {h10:.2f}mil 0.0000 0.0000 10.00mil 10.00mil ""]
)
Layer(8 "silk")
(
\tText[300.00mil 2800.00mil 0 100 "STRIPBOARD REV 1.0 (33x72mm)" ""]
)
"""
    with open(p10_file, "w") as f:
        f.write(rev10_pcb)

    # Render PNGs using pcb-rnd or pcb
    pcb_cmd = shutil.which("pcb-rnd") or shutil.which("pcb")
    if pcb_cmd:
        subprocess.run([pcb_cmd, "-x", "png", "--dpi", "300", "--photo-mode", "--outfile", os.path.join(base_dir, "rev1.1/stripboard_rev1.1_preview_300dpi.png"), p11_file], check=True)
        subprocess.run([pcb_cmd, "-x", "png", "--dpi", "300", "--photo-mode", "--photo-flip-x", "--outfile", os.path.join(base_dir, "rev1.1/stripboard_rev1.1_bottom_preview_300dpi.png"), p11_file], check=True)
        subprocess.run([pcb_cmd, "-x", "png", "--photo-mode", "--outfile", os.path.join(base_dir, "rev1.1/stripboard_rev1.1_preview.png"), p11_file], check=True)
        subprocess.run([pcb_cmd, "-x", "png", "--dpi", "300", "--photo-mode", "--outfile", os.path.join(base_dir, "rev1.1a/stripboard_rev1.1a_preview_300dpi.png"), p11a_file], check=True)
        subprocess.run([pcb_cmd, "-x", "png", "--dpi", "300", "--photo-mode", "--photo-flip-x", "--outfile", os.path.join(base_dir, "rev1.1a/stripboard_rev1.1a_bottom_preview_300dpi.png"), p11a_file], check=True)
        subprocess.run([pcb_cmd, "-x", "png", "--photo-mode", "--outfile", os.path.join(base_dir, "rev1.1a/stripboard_rev1.1a_preview.png"), p11a_file], check=True)
        subprocess.run([pcb_cmd, "-x", "png", "--dpi", "300", "--photo-mode", "--outfile", os.path.join(base_dir, "rev1.0/stripboard_rev1.0_preview_300dpi.png"), p10_file], check=True)
        subprocess.run([pcb_cmd, "-x", "png", "--dpi", "300", "--photo-mode", "--photo-flip-x", "--outfile", os.path.join(base_dir, "rev1.0/stripboard_rev1.0_bottom_preview_300dpi.png"), p10_file], check=True)
        subprocess.run([pcb_cmd, "-x", "png", "--photo-mode", "--outfile", os.path.join(base_dir, "rev1.0/stripboard_rev1.0_preview.png"), p10_file], check=True)
        print(f"Rendered previews using {pcb_cmd}!")
    else:
        print("Warning: Neither pcb-rnd nor pcb found in PATH, skipping PNG preview generation.")

    print("Rev 1.1a, Rev 1.1 and Rev 1.0 layouts updated!")

if __name__ == "__main__":
    main()
