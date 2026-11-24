# Tabela Mestra de Posicionamento e Coordenadas Físicas — Custom Stripboard Rev 1.1a
## Implementação com Par Sziklai High-Side (BC549 NPN + BC328 PNP)

> **Origem dos Eixos:** Canto superior esquerdo $(X=0, Y=0)$. Passo padrão: $100\,\text{mil}$ ($2.54\,\text{mm}$).
> **Alinhamento dos Furos:** Broca de $35\,\text{mil}$ ($0.889\,\text{mm}$), Pad de $80\,\text{mil}$ ($2.032\,\text{mm}$).

---

## 1. Mapeamento Completo de Componentes e Terminais

| Ref | Componente | Encapsulamento | Pino | Função / Nome do Pino | Banco / Trilha | Linha | X (mil) | Y (mil) | X (mm) | Y (mm) | Rede Elétrica (Net) |
| :--- | :--- | :--- | :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **U1** | ATmega328P-PU | DIP-28 (300 mil) | 1 | /RESET | Left | 1 | 1600.0 | 800.0 | 40.64 | 20.32 | `NET_RESET` |
| **U1** | ATmega328P-PU | DIP-28 (300 mil) | 2 | PD0 (RXD) | Left | 2 | 1600.0 | 900.0 | 40.64 | 22.86 | `NET_UART_RX` |
| **U1** | ATmega328P-PU | DIP-28 (300 mil) | 3 | PD1 (TXD) | Left | 3 | 1600.0 | 1000.0 | 40.64 | 25.40 | `NET_UART_TX` |
| **U1** | ATmega328P-PU | DIP-28 (300 mil) | 4 | PD2 (INT0 / Tach 1) | Left | 4 | 1600.0 | 1100.0 | 40.64 | 27.94 | `NET_TACH1` |
| **U1** | ATmega328P-PU | DIP-28 (300 mil) | 5 | PD3 (OC2B / PWM 4) | Left | 5 | 1600.0 | 1200.0 | 40.64 | 30.48 | `NET_PWM4` |
| **U1** | ATmega328P-PU | DIP-28 (300 mil) | 6 | PD4 (PCINT20 / Tach 2) | Left | 6 | 1600.0 | 1300.0 | 40.64 | 33.02 | `NET_TACH2` |
| **U1** | ATmega328P-PU | DIP-28 (300 mil) | 7 | VCC (+5V) | Left | 7 | 1600.0 | 1400.0 | 40.64 | 35.56 | `NET_5V` |
| **U1** | ATmega328P-PU | DIP-28 (300 mil) | 8 | GND (0V) | Left | 8 | 1600.0 | 1500.0 | 40.64 | 38.10 | `NET_GND` |
| **U1** | ATmega328P-PU | DIP-28 (300 mil) | 9 | PB6 (XTAL1) | Left | 9 | 1600.0 | 1600.0 | 40.64 | 40.64 | `NET_XTAL1` |
| **U1** | ATmega328P-PU | DIP-28 (300 mil) | 10 | PB7 (XTAL2) | Left | 10 | 1600.0 | 1700.0 | 40.64 | 43.18 | `NET_XTAL2` |
| **U1** | ATmega328P-PU | DIP-28 (300 mil) | 11 | PD5 (PCINT21 / Tach 3) | Left | 11 | 1600.0 | 1800.0 | 40.64 | 45.72 | `NET_TACH3` |
| **U1** | ATmega328P-PU | DIP-28 (300 mil) | 12 | PD6 (PCINT22 / Tach 4) | Left | 12 | 1600.0 | 1900.0 | 40.64 | 48.26 | `NET_TACH4` |
| **U1** | ATmega328P-PU | DIP-28 (300 mil) | 13 | PD7 | Left | 13 | 1600.0 | 2000.0 | 40.64 | 50.80 | `NC` |
| **U1** | ATmega328P-PU | DIP-28 (300 mil) | 14 | PB0 | Left | 14 | 1600.0 | 2100.0 | 40.64 | 53.34 | `NC` |
| **U1** | ATmega328P-PU | DIP-28 (300 mil) | 15 | PB1 (OC1A / PWM 1) | Right | 14 | 1900.0 | 2100.0 | 48.26 | 53.34 | `NET_PWM1` |
| **U1** | ATmega328P-PU | DIP-28 (300 mil) | 16 | PB2 (OC1B / PWM 2) | Right | 13 | 1900.0 | 2000.0 | 48.26 | 50.80 | `NET_PWM2` |
| **U1** | ATmega328P-PU | DIP-28 (300 mil) | 17 | PB3 (OC2A / PWM 3) | Right | 12 | 1900.0 | 1900.0 | 48.26 | 48.26 | `NET_PWM3` |
| **U1** | ATmega328P-PU | DIP-28 (300 mil) | 18 | PB4 (MISO) | Right | 11 | 1900.0 | 1800.0 | 48.26 | 45.72 | `NC` |
| **U1** | ATmega328P-PU | DIP-28 (300 mil) | 19 | PB5 (SCK) | Right | 10 | 1900.0 | 1700.0 | 48.26 | 43.18 | `NC` |
| **U1** | ATmega328P-PU | DIP-28 (300 mil) | 20 | AVCC (+5V) | Right | 9 | 1900.0 | 1600.0 | 48.26 | 40.64 | `NET_5V` |
| **U1** | ATmega328P-PU | DIP-28 (300 mil) | 21 | AREF (100nF to GND) | Right | 8 | 1900.0 | 1500.0 | 48.26 | 38.10 | `NET_AREF` |
| **U1** | ATmega328P-PU | DIP-28 (300 mil) | 22 | GND (0V) | Right | 7 | 1900.0 | 1400.0 | 48.26 | 35.56 | `NET_GND` |
| **U1** | ATmega328P-PU | DIP-28 (300 mil) | 23 | PC0 | Right | 6 | 1900.0 | 1300.0 | 48.26 | 33.02 | `NC` |
| **U1** | ATmega328P-PU | DIP-28 (300 mil) | 24 | PC1 | Right | 5 | 1900.0 | 1200.0 | 48.26 | 30.48 | `NC` |
| **U1** | ATmega328P-PU | DIP-28 (300 mil) | 25 | PC2 | Right | 4 | 1900.0 | 1100.0 | 48.26 | 27.94 | `NC` |
| **U1** | ATmega328P-PU | DIP-28 (300 mil) | 26 | PC3 | Right | 3 | 1900.0 | 1000.0 | 48.26 | 25.40 | `NC` |
| **U1** | ATmega328P-PU | DIP-28 (300 mil) | 27 | PC4 (SDA) | Right | 2 | 1900.0 | 900.0 | 48.26 | 22.86 | `NC` |
| **U1** | ATmega328P-PU | DIP-28 (300 mil) | 28 | PC5 (SCL) | Right | 1 | 1900.0 | 800.0 | 48.26 | 20.32 | `NC` |
| **Y1** | 16.000 MHz Crystal | HC-49/S THT | 1 | XTAL1 | Left | 9 | 1300.0 | 1600.0 | 33.02 | 40.64 | `NET_XTAL1` |
| **Y1** | 16.000 MHz Crystal | HC-49/S THT | 2 | XTAL2 | Left | 10 | 1300.0 | 1700.0 | 33.02 | 43.18 | `NET_XTAL2` |
| **C3** | 22pF Ceramic | Disc 2.54mm | 1 | 1 | Left | 9 | 1200.0 | 1600.0 | 30.48 | 40.64 | `NET_XTAL1` |
| **C3** | 22pF Ceramic | Disc 2.54mm | 2 | 2 | Rail 4 | 9 | 1700.0 | 1600.0 | 43.18 | 40.64 | `NET_GND` |
| **C4** | 22pF Ceramic | Disc 2.54mm | 1 | 1 | Left | 10 | 1200.0 | 1700.0 | 30.48 | 43.18 | `NET_XTAL2` |
| **C4** | 22pF Ceramic | Disc 2.54mm | 2 | 2 | Rail 4 | 10 | 1700.0 | 1700.0 | 43.18 | 43.18 | `NET_GND` |
| **R4** | 10kΩ 1/4W | Axial 300mil | 1 | Tach1 | Left | 4 | 1500.0 | 1100.0 | 38.10 | 27.94 | `NET_TACH1` |
| **R4** | 10kΩ 1/4W | Axial 300mil | 2 | +5V | Rail 5 | 4 | 1800.0 | 1100.0 | 45.72 | 27.94 | `NET_5V` |
| **R5** | 10kΩ 1/4W | Axial 300mil | 1 | Tach2 | Left | 6 | 1500.0 | 1300.0 | 38.10 | 33.02 | `NET_TACH2` |
| **R5** | 10kΩ 1/4W | Axial 300mil | 2 | +5V | Rail 5 | 6 | 1800.0 | 1300.0 | 45.72 | 33.02 | `NET_5V` |
| **R6** | 10kΩ 1/4W | Axial 300mil | 1 | Tach3 | Left | 11 | 1500.0 | 1800.0 | 38.10 | 45.72 | `NET_TACH3` |
| **R6** | 10kΩ 1/4W | Axial 300mil | 2 | +5V | Rail 5 | 11 | 1800.0 | 1800.0 | 45.72 | 45.72 | `NET_5V` |
| **R7** | 10kΩ 1/4W | Axial 300mil | 1 | Tach4 | Left | 12 | 1500.0 | 1900.0 | 38.10 | 48.26 | `NET_TACH4` |
| **R7** | 10kΩ 1/4W | Axial 300mil | 2 | +5V | Rail 5 | 12 | 1800.0 | 1900.0 | 45.72 | 48.26 | `NET_5V` |
| **CONN1** | CH340 Header 1x6 | SIP6 Female 2.54mm | 1 | DTR | Left | 27 | 1000.0 | 3400.0 | 25.40 | 86.36 | `NET_CH340_DTR` |
| **CONN1** | CH340 Header 1x6 | SIP6 Female 2.54mm | 2 | RXD | Left | 28 | 1000.0 | 3500.0 | 25.40 | 88.90 | `NET_UART_TX` |
| **CONN1** | CH340 Header 1x6 | SIP6 Female 2.54mm | 3 | TXD | Left | 29 | 1000.0 | 3600.0 | 25.40 | 91.44 | `NET_UART_RX` |
| **CONN1** | CH340 Header 1x6 | SIP6 Female 2.54mm | 4 | VCC | Left | 30 | 1000.0 | 3700.0 | 25.40 | 93.98 | `NET_5V` |
| **CONN1** | CH340 Header 1x6 | SIP6 Female 2.54mm | 5 | CTS | Left | 31 | 1000.0 | 3800.0 | 25.40 | 96.52 | `NC` |
| **CONN1** | CH340 Header 1x6 | SIP6 Female 2.54mm | 6 | GND | Left | 32 | 1000.0 | 3900.0 | 25.40 | 99.06 | `NET_GND` |
| **CONN_MOLEX** | Conector MOLEX ATX 4-Pin | Molex 8981 / KRE 4-Pin (Passo 5.08mm) | 1 | +12V (Amarelo) | Rail 6 | 30 | 2800.0 | 3700.0 | 71.12 | 93.98 | `NET_12V` |
| **CONN_MOLEX** | Conector MOLEX ATX 4-Pin | Molex 8981 / KRE 4-Pin (Passo 5.08mm) | 2 | GND (Preto) | Rail 8 | 30 | 3000.0 | 3700.0 | 76.20 | 93.98 | `NET_GND` |
| **CONN_MOLEX** | Conector MOLEX ATX 4-Pin | Molex 8981 / KRE 4-Pin (Passo 5.08mm) | 3 | GND (Preto) | Rail 4 | 30 | 1700.0 | 3700.0 | 43.18 | 93.98 | `NET_GND` |
| **CONN_MOLEX** | Conector MOLEX ATX 4-Pin | Molex 8981 / KRE 4-Pin (Passo 5.08mm) | 4 | +5V (Vermelho) | Rail 5 | 30 | 1800.0 | 3700.0 | 45.72 | 93.98 | `NET_5V` |
| **C_DTR** | 100nF Ceramic | Disc 2.54mm | 1 | DTR | Left | 27 | 1100.0 | 3400.0 | 27.94 | 86.36 | `NET_CH340_DTR` |
| **C_DTR** | 100nF Ceramic | Disc 2.54mm | 2 | /RESET | Left | 27 | 1300.0 | 3400.0 | 33.02 | 86.36 | `NET_RESET` |
| **R_RST** | 10kΩ 1/4W | Axial 300mil | 1 | /RESET | Left | 1 | 1500.0 | 800.0 | 38.10 | 20.32 | `NET_RESET` |
| **R_RST** | 10kΩ 1/4W | Axial 300mil | 2 | +5V | Rail 5 | 1 | 1800.0 | 800.0 | 45.72 | 20.32 | `NET_5V` |
| **R1_1** | 1.5kΩ 1/4W | Axial 300mil | 1 | PWM | Right | 17 | 2000.0 | 2400.0 | 50.80 | 60.96 | `NET_PWM1` |
| **R1_1** | 1.5kΩ 1/4W | Axial 300mil | 2 | B_NPN | Right | 17 | 2300.0 | 2400.0 | 58.42 | 60.96 | `NET_B_NPN_1` |
| **Q1_1** | BC549 | TO-92 (C-B-E) | 1 | C | Right | 18 | 2400.0 | 2500.0 | 60.96 | 63.50 | `NET_MID_1` |
| **Q1_1** | BC549 | TO-92 (C-B-E) | 2 | B | Right | 17 | 2400.0 | 2400.0 | 60.96 | 60.96 | `NET_B_NPN_1` |
| **Q1_1** | BC549 | TO-92 (C-B-E) | 3 | E | Rail 4 | 17 | 1700.0 | 2400.0 | 43.18 | 60.96 | `NET_GND` |
| **R2_1** | 4.7kΩ 1/4W | Axial 300mil | 1 | +12V | Rail 6 | 18 | 2800.0 | 2500.0 | 71.12 | 63.50 | `NET_12V` |
| **R2_1** | 4.7kΩ 1/4W | Axial 300mil | 2 | B_PNP | Right | 18 | 2500.0 | 2500.0 | 63.50 | 63.50 | `NET_MID_1` |
| **R3_1** | 680Ω 1/4W | Axial 200mil | 1 | IN | Right | 18 | 2300.0 | 2500.0 | 58.42 | 63.50 | `NET_MID_1` |
| **R3_1** | 680Ω 1/4W | Axial 200mil | 2 | B_Q2 | Right | 19 | 2300.0 | 2600.0 | 58.42 | 66.04 | `NET_B_PNP_1` |
| **Q2_1** | BC328 | TO-92 (C-B-E) | 1 | C | Right | 19 | 2500.0 | 2600.0 | 63.50 | 66.04 | `FAN1_12V` |
| **Q2_1** | BC328 | TO-92 (C-B-E) | 2 | B | Right | 19 | 2400.0 | 2600.0 | 60.96 | 66.04 | `NET_B_PNP_1` |
| **Q2_1** | BC328 | TO-92 (C-B-E) | 3 | E | Rail 6 | 19 | 2800.0 | 2600.0 | 71.12 | 66.04 | `NET_12V` |
| **D1_1** | 1N4007 | DO-41 Axial | 1 | K (Cathode) | Right | 19 | 2600.0 | 2600.0 | 66.04 | 66.04 | `FAN1_12V` |
| **D1_1** | 1N4007 | DO-41 Axial | 2 | A (Anode) | Rail 8 | 19 | 3000.0 | 2600.0 | 76.20 | 66.04 | `NET_GND` |
| **R1_2** | 1.5kΩ 1/4W | Axial 300mil | 1 | PWM | Right | 20 | 2000.0 | 2700.0 | 50.80 | 68.58 | `NET_PWM2` |
| **R1_2** | 1.5kΩ 1/4W | Axial 300mil | 2 | B_NPN | Right | 20 | 2300.0 | 2700.0 | 58.42 | 68.58 | `NET_B_NPN_2` |
| **Q1_2** | BC549 | TO-92 (C-B-E) | 1 | C | Right | 21 | 2400.0 | 2800.0 | 60.96 | 71.12 | `NET_MID_2` |
| **Q1_2** | BC549 | TO-92 (C-B-E) | 2 | B | Right | 20 | 2400.0 | 2700.0 | 60.96 | 68.58 | `NET_B_NPN_2` |
| **Q1_2** | BC549 | TO-92 (C-B-E) | 3 | E | Rail 4 | 20 | 1700.0 | 2700.0 | 43.18 | 68.58 | `NET_GND` |
| **R2_2** | 4.7kΩ 1/4W | Axial 300mil | 1 | +12V | Rail 6 | 21 | 2800.0 | 2800.0 | 71.12 | 71.12 | `NET_12V` |
| **R2_2** | 4.7kΩ 1/4W | Axial 300mil | 2 | B_PNP | Right | 21 | 2500.0 | 2800.0 | 63.50 | 71.12 | `NET_MID_2` |
| **R3_2** | 680Ω 1/4W | Axial 200mil | 1 | IN | Right | 21 | 2300.0 | 2800.0 | 58.42 | 71.12 | `NET_MID_2` |
| **R3_2** | 680Ω 1/4W | Axial 200mil | 2 | B_Q2 | Right | 22 | 2300.0 | 2900.0 | 58.42 | 73.66 | `NET_B_PNP_2` |
| **Q2_2** | BC328 | TO-92 (C-B-E) | 1 | C | Right | 22 | 2500.0 | 2900.0 | 63.50 | 73.66 | `FAN2_12V` |
| **Q2_2** | BC328 | TO-92 (C-B-E) | 2 | B | Right | 22 | 2400.0 | 2900.0 | 60.96 | 73.66 | `NET_B_PNP_2` |
| **Q2_2** | BC328 | TO-92 (C-B-E) | 3 | E | Rail 6 | 22 | 2800.0 | 2900.0 | 71.12 | 73.66 | `NET_12V` |
| **D1_2** | 1N4007 | DO-41 Axial | 1 | K (Cathode) | Right | 22 | 2600.0 | 2900.0 | 66.04 | 73.66 | `FAN2_12V` |
| **D1_2** | 1N4007 | DO-41 Axial | 2 | A (Anode) | Rail 8 | 22 | 3000.0 | 2900.0 | 76.20 | 73.66 | `NET_GND` |
| **R1_3** | 1.5kΩ 1/4W | Axial 300mil | 1 | PWM | Right | 23 | 2000.0 | 3000.0 | 50.80 | 76.20 | `NET_PWM3` |
| **R1_3** | 1.5kΩ 1/4W | Axial 300mil | 2 | B_NPN | Right | 23 | 2300.0 | 3000.0 | 58.42 | 76.20 | `NET_B_NPN_3` |
| **Q1_3** | BC549 | TO-92 (C-B-E) | 1 | C | Right | 24 | 2400.0 | 3100.0 | 60.96 | 78.74 | `NET_MID_3` |
| **Q1_3** | BC549 | TO-92 (C-B-E) | 2 | B | Right | 23 | 2400.0 | 3000.0 | 60.96 | 76.20 | `NET_B_NPN_3` |
| **Q1_3** | BC549 | TO-92 (C-B-E) | 3 | E | Rail 4 | 23 | 1700.0 | 3000.0 | 43.18 | 76.20 | `NET_GND` |
| **R2_3** | 4.7kΩ 1/4W | Axial 300mil | 1 | +12V | Rail 6 | 24 | 2800.0 | 3100.0 | 71.12 | 78.74 | `NET_12V` |
| **R2_3** | 4.7kΩ 1/4W | Axial 300mil | 2 | B_PNP | Right | 24 | 2500.0 | 3100.0 | 63.50 | 78.74 | `NET_MID_3` |
| **R3_3** | 680Ω 1/4W | Axial 200mil | 1 | IN | Right | 24 | 2300.0 | 3100.0 | 58.42 | 78.74 | `NET_MID_3` |
| **R3_3** | 680Ω 1/4W | Axial 200mil | 2 | B_Q2 | Right | 25 | 2300.0 | 3200.0 | 58.42 | 81.28 | `NET_B_PNP_3` |
| **Q2_3** | BC328 | TO-92 (C-B-E) | 1 | C | Right | 25 | 2500.0 | 3200.0 | 63.50 | 81.28 | `FAN3_12V` |
| **Q2_3** | BC328 | TO-92 (C-B-E) | 2 | B | Right | 25 | 2400.0 | 3200.0 | 60.96 | 81.28 | `NET_B_PNP_3` |
| **Q2_3** | BC328 | TO-92 (C-B-E) | 3 | E | Rail 6 | 25 | 2800.0 | 3200.0 | 71.12 | 81.28 | `NET_12V` |
| **D1_3** | 1N4007 | DO-41 Axial | 1 | K (Cathode) | Right | 25 | 2600.0 | 3200.0 | 66.04 | 81.28 | `FAN3_12V` |
| **D1_3** | 1N4007 | DO-41 Axial | 2 | A (Anode) | Rail 8 | 25 | 3000.0 | 3200.0 | 76.20 | 81.28 | `NET_GND` |
| **R1_4** | 1.5kΩ 1/4W | Axial 300mil | 1 | PWM | Right | 26 | 2000.0 | 3300.0 | 50.80 | 83.82 | `NET_PWM4` |
| **R1_4** | 1.5kΩ 1/4W | Axial 300mil | 2 | B_NPN | Right | 26 | 2300.0 | 3300.0 | 58.42 | 83.82 | `NET_B_NPN_4` |
| **Q1_4** | BC549 | TO-92 (C-B-E) | 1 | C | Right | 27 | 2400.0 | 3400.0 | 60.96 | 86.36 | `NET_MID_4` |
| **Q1_4** | BC549 | TO-92 (C-B-E) | 2 | B | Right | 26 | 2400.0 | 3300.0 | 60.96 | 83.82 | `NET_B_NPN_4` |
| **Q1_4** | BC549 | TO-92 (C-B-E) | 3 | E | Rail 4 | 26 | 1700.0 | 3300.0 | 43.18 | 83.82 | `NET_GND` |
| **R2_4** | 4.7kΩ 1/4W | Axial 300mil | 1 | +12V | Rail 6 | 27 | 2800.0 | 3400.0 | 71.12 | 86.36 | `NET_12V` |
| **R2_4** | 4.7kΩ 1/4W | Axial 300mil | 2 | B_PNP | Right | 27 | 2500.0 | 3400.0 | 63.50 | 86.36 | `NET_MID_4` |
| **R3_4** | 680Ω 1/4W | Axial 200mil | 1 | IN | Right | 27 | 2300.0 | 3400.0 | 58.42 | 86.36 | `NET_MID_4` |
| **R3_4** | 680Ω 1/4W | Axial 200mil | 2 | B_Q2 | Right | 28 | 2300.0 | 3500.0 | 58.42 | 88.90 | `NET_B_PNP_4` |
| **Q2_4** | BC328 | TO-92 (C-B-E) | 1 | C | Right | 28 | 2500.0 | 3500.0 | 63.50 | 88.90 | `FAN4_12V` |
| **Q2_4** | BC328 | TO-92 (C-B-E) | 2 | B | Right | 28 | 2400.0 | 3500.0 | 60.96 | 88.90 | `NET_B_PNP_4` |
| **Q2_4** | BC328 | TO-92 (C-B-E) | 3 | E | Rail 6 | 28 | 2800.0 | 3500.0 | 71.12 | 88.90 | `NET_12V` |
| **D1_4** | 1N4007 | DO-41 Axial | 1 | K (Cathode) | Right | 28 | 2600.0 | 3500.0 | 66.04 | 88.90 | `FAN4_12V` |
| **D1_4** | 1N4007 | DO-41 Axial | 2 | A (Anode) | Rail 8 | 28 | 3000.0 | 3500.0 | 76.20 | 88.90 | `NET_GND` |
| **FAN1** | Header 3 Pinos (PC Fan) | Molex KK 254 3-Pin | 1 | GND | Margem Direita | - | 3400.0 | 600.0 | 86.36 | 15.24 | `NET_GND` |
| **FAN1** | Header 3 Pinos (PC Fan) | Molex KK 254 3-Pin | 2 | PWR (+12V PWM) | Margem Direita | - | 3400.0 | 700.0 | 86.36 | 17.78 | `FAN1_12V` |
| **FAN1** | Header 3 Pinos (PC Fan) | Molex KK 254 3-Pin | 3 | TACH | Margem Direita | - | 3400.0 | 800.0 | 86.36 | 20.32 | `NET_TACH1` |
| **FAN2** | Header 3 Pinos (PC Fan) | Molex KK 254 3-Pin | 1 | GND | Margem Direita | - | 3400.0 | 1000.0 | 86.36 | 25.40 | `NET_GND` |
| **FAN2** | Header 3 Pinos (PC Fan) | Molex KK 254 3-Pin | 2 | PWR (+12V PWM) | Margem Direita | - | 3400.0 | 1100.0 | 86.36 | 27.94 | `FAN2_12V` |
| **FAN2** | Header 3 Pinos (PC Fan) | Molex KK 254 3-Pin | 3 | TACH | Margem Direita | - | 3400.0 | 1200.0 | 86.36 | 30.48 | `NET_TACH2` |
| **FAN3** | Header 3 Pinos (PC Fan) | Molex KK 254 3-Pin | 1 | GND | Margem Direita | - | 3400.0 | 1400.0 | 86.36 | 35.56 | `NET_GND` |
| **FAN3** | Header 3 Pinos (PC Fan) | Molex KK 254 3-Pin | 2 | PWR (+12V PWM) | Margem Direita | - | 3400.0 | 1500.0 | 86.36 | 38.10 | `FAN3_12V` |
| **FAN3** | Header 3 Pinos (PC Fan) | Molex KK 254 3-Pin | 3 | TACH | Margem Direita | - | 3400.0 | 1600.0 | 86.36 | 40.64 | `NET_TACH3` |
| **FAN4** | Header 3 Pinos (PC Fan) | Molex KK 254 3-Pin | 1 | GND | Margem Direita | - | 3400.0 | 1800.0 | 86.36 | 45.72 | `NET_GND` |
| **FAN4** | Header 3 Pinos (PC Fan) | Molex KK 254 3-Pin | 2 | PWR (+12V PWM) | Margem Direita | - | 3400.0 | 1900.0 | 86.36 | 48.26 | `FAN4_12V` |
| **FAN4** | Header 3 Pinos (PC Fan) | Molex KK 254 3-Pin | 3 | TACH | Margem Direita | - | 3400.0 | 2000.0 | 86.36 | 50.80 | `NET_TACH4` |

---

## 2. Mapa dos 4 Canais Sziklai nas Réguas Horizontais do Banco Direito

```text
         X=1900    X=2000    X=2100    X=2200    X=2300    X=2400    X=2500    X=2600    X=2700      Rail 6 (+12V)  Rail 8 (GND)
        (Right1)  (Right2)  (Right3)  (Right4)  (Right5)  (Right6)  (Right7)  (Right8)  (Right9)     (X=2800 mil)   (X=3000 mil)
CANAL 1 (FAN1 Pin 2):
 Row 17:   [      ]  [R1_1 PWM] [      ]  [      ]  [R1_2 B_NPN][Q1 Base] [      ]   [      ]  [      ]  ──► (Q1 Emitter to Rail 4 GND)
 Row 18:   [      ]  [      ]   [      ]  [      ]  [R3 In ]  [Q1 Col ] [R2 B_PNP][      ]  [      ]  ◄── [R2 Pull-up leg to Rail 6 +12V]
 Row 19:   [      ]  [      ]   [      ]  [      ]  [R3 B_Q2] [Q2 Base] [Q2 Col ] [D1 Cath][Jumper] ──► To FAN1 Pin 2 | (Q2 E to +12V, D1 A to GND)
-----------------------------------------------------------------------------------------------------------------------------
CANAL 2 (FAN2 Pin 2):
 Row 20:   [      ]  [R1_1 PWM] [      ]  [      ]  [R1_2 B_NPN][Q1 Base] [      ]   [      ]  [      ]  ──► (Q1 Emitter to Rail 4 GND)
 Row 21:   [      ]  [      ]   [      ]  [      ]  [R3 In ]  [Q1 Col ] [R2 B_PNP][      ]  [      ]  ◄── [R2 Pull-up leg to Rail 6 +12V]
 Row 22:   [      ]  [      ]   [      ]  [      ]  [R3 B_Q2] [Q2 Base] [Q2 Col ] [D1 Cath][Jumper] ──► To FAN2 Pin 2 | (Q2 E to +12V, D1 A to GND)
-----------------------------------------------------------------------------------------------------------------------------
CANAL 3 (FAN3 Pin 2):
 Row 23:   [      ]  [R1_1 PWM] [      ]  [      ]  [R1_2 B_NPN][Q1 Base] [      ]   [      ]  [      ]  ──► (Q1 Emitter to Rail 4 GND)
 Row 24:   [      ]  [      ]   [      ]  [      ]  [R3 In ]  [Q1 Col ] [R2 B_PNP][      ]  [      ]  ◄── [R2 Pull-up leg to Rail 6 +12V]
 Row 25:   [      ]  [      ]   [      ]  [      ]  [R3 B_Q2] [Q2 Base] [Q2 Col ] [D1 Cath][Jumper] ──► To FAN3 Pin 2 | (Q2 E to +12V, D1 A to GND)
-----------------------------------------------------------------------------------------------------------------------------
CANAL 4 (FAN4 Pin 2):
 Row 26:   [      ]  [R1_1 PWM] [      ]  [      ]  [R1_2 B_NPN][Q1 Base] [      ]   [      ]  [      ]  ──► (Q1 Emitter to Rail 4 GND)
 Row 27:   [      ]  [      ]   [      ]  [      ]  [R3 In ]  [Q1 Col ] [R2 B_PNP][      ]  [      ]  ◄── [R2 Pull-up leg to Rail 6 +12V]
 Row 28:   [      ]  [      ]   [      ]  [      ]  [R3 B_Q2] [Q2 Base] [Q2 Col ] [D1 Cath][Jumper] ──► To FAN4 Pin 2 | (Q2 E to +12V, D1 A to GND)
-----------------------------------------------------------------------------------------------------------------------------
```
