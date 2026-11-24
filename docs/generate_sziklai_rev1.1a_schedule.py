#!/usr/bin/env python3
"""
generate_sziklai_rev1.1a_schedule.py
Computes and verifies exact physical coordinates for all components of the
Fan Controller on Custom Stripboard Rev 1.1a using High-Side Sziklai Drivers (BC549 + BC328).
"""

import os

def main():
    rows = []
    
    # Board parameters
    # Left bank: X in [800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600]
    # Right bank: X in [1900, 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700]
    # Center rails: Rail 4 (X=1700, GND), Rail 5 (X=1800, +5V)
    # Right rails: Rail 6 (X=2800, +12V), Rail 7 (X=2900, +12V), Rail 8 (X=3000, GND)
    # Rows 1..32: Y = 800 + (r-1)*100
    
    components = []
    
    def add_comp(ref, part, footprint, desc, pins):
        # Ensure x_mm and y_mm exist for all pins
        for p in pins:
            if "x_mm" not in p:
                p["x_mm"] = p["x_mil"] * 0.0254
            if "y_mm" not in p:
                p["y_mm"] = p["y_mil"] * 0.0254
        components.append({
            "ref": ref,
            "part": part,
            "footprint": footprint,
            "desc": desc,
            "pins": pins
        })

    # 1. ATmega328P-PU (DIP-28) on Rows 1 to 14
    # Pins 1..14 on Left Bank at X=1600 mil
    # Pins 15..28 on Right Bank at X=1900 mil
    atmega_pins = []
    atmega_pin_names = [
        # Left side: Pins 1 to 14 (Row 1 to 14)
        (1, 1, "Left", 1600.0, "/RESET", "NET_RESET"),
        (2, 2, "Left", 1600.0, "PD0 (RXD)", "NET_UART_RX"),
        (3, 3, "Left", 1600.0, "PD1 (TXD)", "NET_UART_TX"),
        (4, 4, "Left", 1600.0, "PD2 (INT0 / Tach 1)", "NET_TACH1"),
        (5, 5, "Left", 1600.0, "PD3 (OC2B / PWM 4)", "NET_PWM4"),
        (6, 6, "Left", 1600.0, "PD4 (PCINT20 / Tach 2)", "NET_TACH2"),
        (7, 7, "Left", 1600.0, "VCC (+5V)", "NET_5V"),
        (8, 8, "Left", 1600.0, "GND (0V)", "NET_GND"),
        (9, 9, "Left", 1600.0, "PB6 (XTAL1)", "NET_XTAL1"),
        (10, 10, "Left", 1600.0, "PB7 (XTAL2)", "NET_XTAL2"),
        (11, 11, "Left", 1600.0, "PD5 (PCINT21 / Tach 3)", "NET_TACH3"),
        (12, 12, "Left", 1600.0, "PD6 (PCINT22 / Tach 4)", "NET_TACH4"),
        (13, 13, "Left", 1600.0, "PD7", "NC"),
        (14, 14, "Left", 1600.0, "PB0", "NC"),
        # Right side: Pins 15 to 28 (Row 14 down to 1)
        (15, 14, "Right", 1900.0, "PB1 (OC1A / PWM 1)", "NET_PWM1"),
        (16, 13, "Right", 1900.0, "PB2 (OC1B / PWM 2)", "NET_PWM2"),
        (17, 12, "Right", 1900.0, "PB3 (OC2A / PWM 3)", "NET_PWM3"),
        (18, 11, "Right", 1900.0, "PB4 (MISO)", "NC"),
        (19, 10, "Right", 1900.0, "PB5 (SCK)", "NC"),
        (20, 9, "Right", 1900.0, "AVCC (+5V)", "NET_5V"),
        (21, 8, "Right", 1900.0, "AREF (100nF to GND)", "NET_AREF"),
        (22, 7, "Right", 1900.0, "GND (0V)", "NET_GND"),
        (23, 6, "Right", 1900.0, "PC0", "NC"),
        (24, 5, "Right", 1900.0, "PC1", "NC"),
        (25, 4, "Right", 1900.0, "PC2", "NC"),
        (26, 3, "Right", 1900.0, "PC3", "NC"),
        (27, 2, "Right", 1900.0, "PC4 (SDA)", "NC"),
        (28, 1, "Right", 1900.0, "PC5 (SCL)", "NC"),
    ]
    for pin_num, row_num, bank, x, name, net in atmega_pin_names:
        y = 800.0 + (row_num - 1) * 100.0
        atmega_pins.append({
            "pin": pin_num,
            "name": name,
            "bank": bank,
            "row": row_num,
            "x_mil": x,
            "y_mil": y,
            "x_mm": x * 0.0254,
            "y_mm": y * 0.0254,
            "net": net
        })
    add_comp("U1", "ATmega328P-PU", "DIP-28 (300 mil)", "Microcontrolador Principal 16MHz", atmega_pins)

    # 2. Clock: Crystal 16MHz + 2x 22pF Capacitors
    # Rows 9 and 10 on Left Bank
    add_comp("Y1", "16.000 MHz Crystal", "HC-49/S THT", "Cristal de Quartzo Fundamental", [
        {"pin": 1, "name": "XTAL1", "bank": "Left", "row": 9, "x_mil": 1300.0, "y_mil": 1600.0, "net": "NET_XTAL1"},
        {"pin": 2, "name": "XTAL2", "bank": "Left", "row": 10, "x_mil": 1300.0, "y_mil": 1700.0, "net": "NET_XTAL2"}
    ])
    add_comp("C3", "22pF Ceramic", "Disc 2.54mm", "Capacitor de Carga XTAL1", [
        {"pin": 1, "name": "1", "bank": "Left", "row": 9, "x_mil": 1200.0, "y_mil": 1600.0, "net": "NET_XTAL1"},
        {"pin": 2, "name": "2", "bank": "Rail 4", "row": 9, "x_mil": 1700.0, "y_mil": 1600.0, "net": "NET_GND"}
    ])
    add_comp("C4", "22pF Ceramic", "Disc 2.54mm", "Capacitor de Carga XTAL2", [
        {"pin": 1, "name": "1", "bank": "Left", "row": 10, "x_mil": 1200.0, "y_mil": 1700.0, "net": "NET_XTAL2"},
        {"pin": 2, "name": "2", "bank": "Rail 4", "row": 10, "x_mil": 1700.0, "y_mil": 1700.0, "net": "NET_GND"}
    ])

    # 3. Pull-ups para Tacômetro (R4, R5, R6, R7 = 10kΩ)
    # Fan 1 Tach (PD2) is Row 4 Left Bank (Y=1100). Pull-up to Rail 5 (+5V at X=1800)
    # Fan 2 Tach (PD4) is Row 6 Left Bank (Y=1300). Pull-up to Rail 5 (+5V at X=1800)
    # Fan 3 Tach (PD5) is Row 11 Left Bank (Y=1800). Pull-up to Rail 5 (+5V at X=1800)
    # Fan 4 Tach (PD6) is Row 12 Left Bank (Y=1900). Pull-up to Rail 5 (+5V at X=1800)
    add_comp("R4", "10kΩ 1/4W", "Axial 300mil", "Pull-up Fan 1 Tach (PD2)", [
        {"pin": 1, "name": "Tach1", "bank": "Left", "row": 4, "x_mil": 1500.0, "y_mil": 1100.0, "net": "NET_TACH1"},
        {"pin": 2, "name": "+5V", "bank": "Rail 5", "row": 4, "x_mil": 1800.0, "y_mil": 1100.0, "net": "NET_5V"}
    ])
    add_comp("R5", "10kΩ 1/4W", "Axial 300mil", "Pull-up Fan 2 Tach (PD4)", [
        {"pin": 1, "name": "Tach2", "bank": "Left", "row": 6, "x_mil": 1500.0, "y_mil": 1300.0, "net": "NET_TACH2"},
        {"pin": 2, "name": "+5V", "bank": "Rail 5", "row": 6, "x_mil": 1800.0, "y_mil": 1300.0, "net": "NET_5V"}
    ])
    add_comp("R6", "10kΩ 1/4W", "Axial 300mil", "Pull-up Fan 3 Tach (PD5)", [
        {"pin": 1, "name": "Tach3", "bank": "Left", "row": 11, "x_mil": 1500.0, "y_mil": 1800.0, "net": "NET_TACH3"},
        {"pin": 2, "name": "+5V", "bank": "Rail 5", "row": 11, "x_mil": 1800.0, "y_mil": 1800.0, "net": "NET_5V"}
    ])
    add_comp("R7", "10kΩ 1/4W", "Axial 300mil", "Pull-up Fan 4 Tach (PD6)", [
        {"pin": 1, "name": "Tach4", "bank": "Left", "row": 12, "x_mil": 1500.0, "y_mil": 1900.0, "net": "NET_TACH4"},
        {"pin": 2, "name": "+5V", "bank": "Rail 5", "row": 12, "x_mil": 1800.0, "y_mil": 1900.0, "net": "NET_5V"}
    ])

    # 4. CH340 6-Pin Socket Header & Decoupling (Rows 29..32 Left Bank)
    # Pins: 1:DTR, 2:RXD, 3:TXD, 4:VCC, 5:CTS, 6:GND
    ch340_pins = [
        {"pin": 1, "name": "DTR", "bank": "Left", "row": 27, "x_mil": 1000.0, "y_mil": 3400.0, "net": "NET_CH340_DTR"},
        {"pin": 2, "name": "RXD", "bank": "Left", "row": 28, "x_mil": 1000.0, "y_mil": 3500.0, "net": "NET_UART_TX"}, # CH340 RX connects to MCU TX
        {"pin": 3, "name": "TXD", "bank": "Left", "row": 29, "x_mil": 1000.0, "y_mil": 3600.0, "net": "NET_UART_RX"}, # CH340 TX connects to MCU RX
        {"pin": 4, "name": "VCC", "bank": "Left", "row": 30, "x_mil": 1000.0, "y_mil": 3700.0, "net": "NET_5V"},
        {"pin": 5, "name": "CTS", "bank": "Left", "row": 31, "x_mil": 1000.0, "y_mil": 3800.0, "net": "NC"},
        {"pin": 6, "name": "GND", "bank": "Left", "row": 32, "x_mil": 1000.0, "y_mil": 3900.0, "net": "NET_GND"}
    ]
    add_comp("CONN1", "CH340 Header 1x6", "SIP6 Female 2.54mm", "Barra Fêmea para Módulo CH340 USB", ch340_pins)
    # 4b. Conector MOLEX ATX de Entrada de Força (4 Pinos, Passo 5.08mm / 200 mil)
    # Pino 1 (Amarelo): +12V
    # Pino 2 (Preto): GND
    # Pino 3 (Preto): GND
    # Pino 4 (Vermelho): +5V
    add_comp("CONN_MOLEX", "Conector MOLEX ATX 4-Pin", "Molex 8981 / KRE 4-Pin (Passo 5.08mm)", "Entrada de Alimentação Autônoma da Fonte ATX", [
        {"pin": 1, "name": "+12V (Amarelo)", "bank": "Rail 6", "row": 30, "x_mil": 2800.0, "y_mil": 3700.0, "net": "NET_12V"},
        {"pin": 2, "name": "GND (Preto)", "bank": "Rail 8", "row": 30, "x_mil": 3000.0, "y_mil": 3700.0, "net": "NET_GND"},
        {"pin": 3, "name": "GND (Preto)", "bank": "Rail 4", "row": 30, "x_mil": 1700.0, "y_mil": 3700.0, "net": "NET_GND"},
        {"pin": 4, "name": "+5V (Vermelho)", "bank": "Rail 5", "row": 30, "x_mil": 1800.0, "y_mil": 3700.0, "net": "NET_5V"}
    ])
    add_comp("C_DTR", "100nF Ceramic", "Disc 2.54mm", "Capacitor AC Auto-Reset", [
        {"pin": 1, "name": "DTR", "bank": "Left", "row": 27, "x_mil": 1100.0, "y_mil": 3400.0, "net": "NET_CH340_DTR"},
        {"pin": 2, "name": "/RESET", "bank": "Left", "row": 27, "x_mil": 1300.0, "y_mil": 3400.0, "net": "NET_RESET"}
    ])
    add_comp("R_RST", "10kΩ 1/4W", "Axial 300mil", "Pull-up ATmega /RESET", [
        {"pin": 1, "name": "/RESET", "bank": "Left", "row": 1, "x_mil": 1500.0, "y_mil": 800.0, "net": "NET_RESET"},
        {"pin": 2, "name": "+5V", "bank": "Rail 5", "row": 1, "x_mil": 1800.0, "y_mil": 800.0, "net": "NET_5V"}
    ])

    # 5. OS 4 CANAIS HIGH-SIDE SZIKLAI (Right Bank Rows 17 to 28)
    # Channel 1 (Fan 1): Rows 17, 18, 19
    # Channel 2 (Fan 2): Rows 20, 21, 22
    # Channel 3 (Fan 3): Rows 23, 24, 25
    # Channel 4 (Fan 4): Rows 26, 27, 28
    channels = [
        (1, 17, "NET_PWM1", "FAN1_12V", "FAN1 Pin 2", "FAN1 Pin 3"),
        (2, 20, "NET_PWM2", "FAN2_12V", "FAN2 Pin 2", "FAN2 Pin 3"),
        (3, 23, "NET_PWM3", "FAN3_12V", "FAN3 Pin 2", "FAN3 Pin 3"),
        (4, 26, "NET_PWM4", "FAN4_12V", "FAN4 Pin 2", "FAN4 Pin 3"),
    ]

    for ch, base_row, pwm_net, out_net, kre_12v, kre_tach in channels:
        r_npn = base_row      # Row A of channel
        r_mid = base_row + 1  # Row B of channel
        r_pnp = base_row + 2  # Row C of channel

        y_npn = 800.0 + (r_npn - 1) * 100.0
        y_mid = 800.0 + (r_mid - 1) * 100.0
        y_pnp = 800.0 + (r_pnp - 1) * 100.0

        # R1: 1.5k Base resistor from PWM net to Q1 Base
        add_comp(f"R1_{ch}", "1.5kΩ 1/4W", "Axial 300mil", f"Resistor de Base NPN Ch{ch}", [
            {"pin": 1, "name": "PWM", "bank": "Right", "row": r_npn, "x_mil": 2000.0, "y_mil": y_npn, "net": pwm_net},
            {"pin": 2, "name": "B_NPN", "bank": "Right", "row": r_npn, "x_mil": 2300.0, "y_mil": y_npn, "net": f"NET_B_NPN_{ch}"}
        ])

        # Q1: BC549 (NPN, TO-92 C-B-E)
        # Pins: 1:Collector (Row r_mid), 2:Base (Row r_npn), 3:Emitter (Row r_npn to GND)
        add_comp(f"Q1_{ch}", "BC549", "TO-92 (C-B-E)", f"NPN Driver Sziklai Ch{ch}", [
            {"pin": 1, "name": "C", "bank": "Right", "row": r_mid, "x_mil": 2400.0, "y_mil": y_mid, "net": f"NET_MID_{ch}"},
            {"pin": 2, "name": "B", "bank": "Right", "row": r_npn, "x_mil": 2400.0, "y_mil": y_npn, "net": f"NET_B_NPN_{ch}"},
            {"pin": 3, "name": "E", "bank": "Rail 4", "row": r_npn, "x_mil": 1700.0, "y_mil": y_npn, "net": "NET_GND"}
        ])

        # R2: 4.7k Pull-up resistor between +12V (Rail 6 at X=2800) and Q2 Base / Q1 Collector (Row r_mid)
        add_comp(f"R2_{ch}", "4.7kΩ 1/4W", "Axial 300mil", f"Pull-up +12V Base PNP Ch{ch}", [
            {"pin": 1, "name": "+12V", "bank": "Rail 6", "row": r_mid, "x_mil": 2800.0, "y_mil": y_mid, "net": "NET_12V"},
            {"pin": 2, "name": "B_PNP", "bank": "Right", "row": r_mid, "x_mil": 2500.0, "y_mil": y_mid, "net": f"NET_MID_{ch}"}
        ])

        # R3: 680Ω series base drive resistor between Row r_mid and Q2 Base
        add_comp(f"R3_{ch}", "680Ω 1/4W", "Axial 200mil", f"Resistor de Drive Base PNP Ch{ch}", [
            {"pin": 1, "name": "IN", "bank": "Right", "row": r_mid, "x_mil": 2300.0, "y_mil": y_mid, "net": f"NET_MID_{ch}"},
            {"pin": 2, "name": "B_Q2", "bank": "Right", "row": r_pnp, "x_mil": 2300.0, "y_mil": y_pnp, "net": f"NET_B_PNP_{ch}"}
        ])

        # Q2: BC328 (PNP, TO-92 C-B-E, 800mA)
        # Pins: 1:Collector (Switched Output), 2:Base, 3:Emitter (to +12V Rail 6)
        add_comp(f"Q2_{ch}", "BC328", "TO-92 (C-B-E)", f"PNP Pass de Potência Sziklai Ch{ch}", [
            {"pin": 1, "name": "C", "bank": "Right", "row": r_pnp, "x_mil": 2500.0, "y_mil": y_pnp, "net": out_net},
            {"pin": 2, "name": "B", "bank": "Right", "row": r_pnp, "x_mil": 2400.0, "y_mil": y_pnp, "net": f"NET_B_PNP_{ch}"},
            {"pin": 3, "name": "E", "bank": "Rail 6", "row": r_pnp, "x_mil": 2800.0, "y_mil": y_pnp, "net": "NET_12V"}
        ])

        # D1: 1N4007 Flyback Diode across Load (Cathode to Output in Row r_pnp, Anode to GND Rail 8)
        add_comp(f"D1_{ch}", "1N4007", "DO-41 Axial", f"Diodo de Roda-Livre Flyback Ch{ch}", [
            {"pin": 1, "name": "K (Cathode)", "bank": "Right", "row": r_pnp, "x_mil": 2600.0, "y_mil": y_pnp, "net": out_net},
            {"pin": 2, "name": "A (Anode)", "bank": "Rail 8", "row": r_pnp, "x_mil": 3000.0, "y_mil": y_pnp, "net": "NET_GND"}
        ])

    # 6. Conectores de 3 Pinos para Ventoinhas (FAN1..FAN4, Molex KK 254 / Barra 3P 2.54mm)
    fan_conns = [
        ("FAN1", 600.0, "FAN1_12V", "NET_TACH1"),
        ("FAN2", 1000.0, "FAN2_12V", "NET_TACH2"),
        ("FAN3", 1400.0, "FAN3_12V", "NET_TACH3"),
        ("FAN4", 1800.0, "FAN4_12V", "NET_TACH4"),
    ]
    for fan_ref, y_base, pwr_net, tach_net in fan_conns:
        add_comp(fan_ref, "Header 3 Pinos (PC Fan)", "Molex KK 254 3-Pin", f"Conector Direto da Ventoinha {fan_ref}", [
            {"pin": 1, "name": "GND", "bank": "Margem Direita", "row": "-", "x_mil": 3400.0, "y_mil": y_base, "net": "NET_GND"},
            {"pin": 2, "name": "PWR (+12V PWM)", "bank": "Margem Direita", "row": "-", "x_mil": 3400.0, "y_mil": y_base + 100.0, "net": pwr_net},
            {"pin": 3, "name": "TACH", "bank": "Margem Direita", "row": "-", "x_mil": 3400.0, "y_mil": y_base + 200.0, "net": tach_net}
        ])

    print(f"Total Components Registered: {len(components)}")
    
    # Generate Output Schedule in Markdown format
    md_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "SZIKLAI_REV1.1A_COORDINATE_SCHEDULE.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Tabela Mestra de Posicionamento e Coordenadas Físicas — Custom Stripboard Rev 1.1a\n")
        f.write("## Implementação com Par Sziklai High-Side (BC549 NPN + BC328 PNP)\n\n")
        f.write("> **Origem dos Eixos:** Canto superior esquerdo $(X=0, Y=0)$. Passo padrão: $100\\,\\text{mil}$ ($2.54\\,\\text{mm}$).\n")
        f.write("> **Alinhamento dos Furos:** Broca de $35\\,\\text{mil}$ ($0.889\\,\\text{mm}$), Pad de $80\\,\\text{mil}$ ($2.032\\,\\text{mm}$).\n\n")
        f.write("---\n\n")
        f.write("## 1. Mapeamento Completo de Componentes e Terminais\n\n")
        f.write("| Ref | Componente | Encapsulamento | Pino | Função / Nome do Pino | Banco / Trilha | Linha | X (mil) | Y (mil) | X (mm) | Y (mm) | Rede Elétrica (Net) |\n")
        f.write("| :--- | :--- | :--- | :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |\n")
        for c in components:
            for p in c["pins"]:
                row_str = str(p.get("row", "-"))
                f.write(f"| **{c['ref']}** | {c['part']} | {c['footprint']} | {p['pin']} | {p['name']} | {p['bank']} | {row_str} | {p['x_mil']:.1f} | {p['y_mil']:.1f} | {p['x_mm']:.2f} | {p['y_mm']:.2f} | `{p['net']}` |\n")
        f.write("\n---\n\n")
        f.write("## 2. Mapa dos 4 Canais Sziklai nas Réguas Horizontais do Banco Direito\n\n")
        f.write("```text\n")
        f.write("         X=1900    X=2000    X=2100    X=2200    X=2300    X=2400    X=2500    X=2600    X=2700      Rail 6 (+12V)  Rail 8 (GND)\n")
        f.write("        (Right1)  (Right2)  (Right3)  (Right4)  (Right5)  (Right6)  (Right7)  (Right8)  (Right9)     (X=2800 mil)   (X=3000 mil)\n")
        for ch, base_row, pwm_net, out_net, kre_12v, kre_tach in channels:
            r_npn = base_row
            r_mid = base_row + 1
            r_pnp = base_row + 2
            f.write(f"CANAL {ch} ({kre_12v}):\n")
            f.write(f" Row {r_npn:02d}:   [      ]  [R1_1 PWM] [      ]  [      ]  [R1_2 B_NPN][Q1 Base] [      ]   [      ]  [      ]  ──► (Q1 Emitter to Rail 4 GND)\n")
            f.write(f" Row {r_mid:02d}:   [      ]  [      ]   [      ]  [      ]  [R3 In ]  [Q1 Col ] [R2 B_PNP][      ]  [      ]  ◄── [R2 Pull-up leg to Rail 6 +12V]\n")
            f.write(f" Row {r_pnp:02d}:   [      ]  [      ]   [      ]  [      ]  [R3 B_Q2] [Q2 Base] [Q2 Col ] [D1 Cath][Jumper] ──► To {kre_12v} | (Q2 E to +12V, D1 A to GND)\n")
            f.write("-----------------------------------------------------------------------------------------------------------------------------\n")
        f.write("```\n")

    print(f"Schedule written to: {md_path}")

if __name__ == "__main__":
    main()
