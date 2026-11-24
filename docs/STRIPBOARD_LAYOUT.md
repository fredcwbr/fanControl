# Stripboard Physical Matrix & Coordinate System
## Plataforma Principal: Custom Stripboard Rev 1.1a (Eurocard 88.90 x 128.27 mm)
### Arquitetura: Controle High-Side por Par Sziklai (BC549 + BC328) & Alimentação Autônoma MOLEX ATX (+12V / +5V)

---

## 1. Decisões Arquiteturais Consolidadas

1. **Placa Padrão Eurocard Industrial (Custom Stripboard Rev 1.1a):**
   - Dimensões: $3500.00\,\text{mil} \times 5050.00\,\text{mil}$ ($88.90\,\text{mm} \times 128.27\,\text{mm}$).
   - Padrão **100% Through-Hole (THT / PTH)** com pads $\ge 80\,\text{mil}$ ($2.032\,\text{mm}$) e broca de $35\,\text{mil}$ ($0.889\,\text{mm}$).
   - 64 réguas horizontais de prototipagem de 9 pinos cada (32 linhas no Banco Esquerdo e 32 linhas no Banco Direito).
   - 8 Barramentos Verticais de Força com trilhas pesadas de $40\,\text{mil}$ (+12V, +5V, GND).
   - Conectores diretos de 3 pinos para ventoinhas (`FAN1`..`FAN4`, passo $2.54\,\text{mm}$ / padrão PC fan Molex KK 254), eliminando o borne KRE (`TB101`), reduzindo custo e economizando espaço.

2. **Controle High-Side por Par Sziklai (Complementary Feedback Pair — CFP):**
   - **$Q_1$ (NPN Driver / Level-Shifter):** **BC549** (ou BC548 / BC337) em encapsulamento TO-92 (C-B-E).
   - **$Q_2$ (PNP Pass / Saída de Alta Corrente):** **BC328** (ou BC327) em encapsulamento TO-92 (C-B-E, $800\,\text{mA}$ contínuo).
   - **Queda de Tensão Mínima ($V_{CE(sat)} \le 0.15\,\text{V}$):** A ventoinha recebe mais de $11.85\,\text{V}$ a 100% de PWM, garantindo rotação plena sem perdas térmicas (contra a queda de $1.2\text{--}1.5\,\text{V}$ do Darlington).
   - **Terra Sólido e Contínuo (0V):** O pino 1 (GND) dos 4 fans é permanentemente conectado ao terra comum da fonte do PC. A leitura do tacômetro (Pino 3) é 100% imune a ruídos e jitter de PWM.

3. **Alimentação Autônoma Onboard via Conector MOLEX ATX Padrão:**
   - Utilização direta das tensões de $+12\,\text{V}$ e $+5\,\text{V}$ do conector de periféricos MOLEX ATX de 4 vias (Molex 8981, passo $5.08\,\text{mm}$):
     - **Pino 1 (Fio Amarelo):** $+12\,\text{V}$ $\to$ Barramento de Potência (Rail 6 em $X = 2800\,\text{mil}$) e Emissores dos PNP BC328.
     - **Pino 2 (Fio Preto):** GND $\to$ Ponto Estrela de Terra (Rail 8 em $X = 3000\,\text{mil}$).
     - **Pino 3 (Fio Preto):** GND $\to$ Ponto Estrela de Terra (Rail 4 em $X = 1700\,\text{mil}$).
     - **Pino 4 (Fio Vermelho):** $+5\,\text{V}$ $\to$ Barramento Lógico (Rail 5 em $X = 1800\,\text{mil}$) para ATmega328P, CH340 e pull-ups.
   - **Zero Dissipação Térmica:** Elimina a necessidade de reguladores lineares ou conversores buck adicionais.

4. **Conexão Direta Onboard via Conectores PC Fan de 3 Pinos (`FAN1`..`FAN4`):**
   - Conectores macho padrão Molex KK 254 com rampa de travamento (passo $2.54\,\text{mm}$):
     - **FAN1:** Pino 1 (GND), Pino 2 (+12V Chaveado High-Side `FAN1_12V`), Pino 3 (Tacômetro RPM $\to$ PD2 / INT0)
     - **FAN2:** Pino 1 (GND), Pino 2 (+12V Chaveado High-Side `FAN2_12V`), Pino 3 (Tacômetro RPM $\to$ PD4 / PCINT20)
     - **FAN3:** Pino 1 (GND), Pino 2 (+12V Chaveado High-Side `FAN3_12V`), Pino 3 (Tacômetro RPM $\to$ PD5 / PCINT21)
     - **FAN4:** Pino 1 (GND), Pino 2 (+12V Chaveado High-Side `FAN4_12V`), Pino 3 (Tacômetro RPM $\to$ PD6 / PCINT22)
   - Elimina o borne KRE (`TB101`), permitindo o encaixe direto dos chicotes das ventoinhas do gabinete sem emendas ou custo de blocos terminais.

---

## 2. Mapa Geral de Coordenadas da Placa Custom Stripboard Rev 1.1a

```text
       X=500  X=600  X=700   X=800..1600       X=1700 X=1800   X=1900..2700      X=2800 X=2900 X=3000   X=3400
       Rail1  Rail2  Rail3   (BANCO ESQUERDO)  Rail4  Rail5    (BANCO DIREITO)   Rail6  Rail7  Rail8    [FAN1..4 3P CON]
                             (9 furos / linha) (GND)  (+5V)    (9 furos / linha) (+12V) (+12V) (GND)
Y=800:   │      │      │     [Row 01 Left ] ── [ ATmega328P ] ── [Row 01 Right]     │      │      │      [FAN1: Pin 1 GND]
Y=900:   │      │      │     [Row 02 Left ] ── [   DIP-28   ] ── [Row 02 Right]     │      │      │      [FAN1: Pin 2 12V]
Y=1000:  │      │      │     [Row 03 Left ] ── [  Rows 1-14 ] ── [Row 03 Right]     │      │      │      [FAN1: Pin 3 TACH]
Y=1100:  │      │      │     [Row 04 Left ] ── [            ] ── [Row 04 Right]     │      │      │      [FAN2: Pin 1 GND]
Y=1200:  │      │      │     [Row 05 Left ] ── [ Cristal    ] ── [Row 05 Right]     │      │      │      [FAN2: Pin 2 12V]
Y=1300:  │      │      │     [Row 06 Left ] ── [ 16MHz +    ] ── [Row 06 Right]     │      │      │      [FAN2: Pin 3 TACH]
Y=1400:  │      │      │     [Row 07 Left ] ── [ Pull-ups   ] ── [Row 07 Right]     │      │      │      [FAN3: Pin 1 GND]
Y=1500:  │      │      │     [Row 08 Left ] ── [ Tacômetro  ] ── [Row 08 Right]     │      │      │      [FAN3: Pin 2 12V]
Y=1600:  │      │      │     [Row 09 Left ] ── [            ] ── [Row 09 Right]     │      │      │      [FAN3: Pin 3 TACH]
Y=1700:  │      │      │     [Row 10 Left ] ── [            ] ── [Row 10 Right]     │      │      │      [FAN4: Pin 1 GND]
Y=1800:  │      │      │     [Row 11 Left ] ── [            ] ── [Row 11 Right]     │      │      │      [FAN4: Pin 2 12V]
Y=1900:  │      │      │     [Row 12 Left ] ── [            ] ── [Row 12 Right]     │      │      │      [FAN4: Pin 3 TACH]
Y=2000:  │      │      │     [Row 13 Left ] ── [            ] ── [Row 13 Right]     │      │      │
Y=2100:  │      │      │     [Row 14 Left ] ── [            ] ── [Row 14 Right]     │      │      │
         ─────────────────── [ ESPAÇADOR E DESACOPLAMENTO: ROWS 15-16 ] ───────────────────────────
Y=2400:  │      │      │     [Row 17 Left ]                      [CANAL 1 SZIKLAI (Row 17, 18, 19)] ──► FAN1 Pin 2
Y=2700:  │      │      │     [Row 20 Left ]                      [CANAL 2 SZIKLAI (Row 20, 21, 22)] ──► FAN2 Pin 2
Y=3000:  │      │      │     [Row 23 Left ]                      [CANAL 3 SZIKLAI (Row 23, 24, 25)] ──► FAN3 Pin 2
Y=3300:  │      │      │     [Row 26 Left ]                      [CANAL 4 SZIKLAI (Row 26, 27, 28)] ──► FAN4 Pin 2
Y=3400:  │      │      │     [Row 27: CH340 DTR-Cap]             │      │      │
Y=3500:  │      │      │     [Row 28: CH340 RXD]                 │      │      │
Y=3600:  │      │      │     [Row 29: CH340 TXD]                 │      │      │
Y=3700:  │      │      │     [Row 30: CH340 VCC] ── [CONN_MOLEX: +12V / GND / GND / +5V]
Y=3800:  │      │      │     [Row 31: CH340 CTS]                 │      │      │
Y=3900:  │      │      │     [Row 32: CH340 GND]                 │      │      │
```

---

## 3. Topologia e Mapa Físico dos 4 Canais Sziklai High-Side

Cada canal ocupa 3 linhas horizontais no Banco Direito ($X = 1900$ a $2700\,\text{mil}$), acoplando-se diretamente ao barramento de $+12\,\text{V}$ (Rail 6 em $X = 2800\,\text{mil}$) e ao barramento de GND (Rail 4 em $X = 1700\,\text{mil}$ e Rail 8 em $X = 3000\,\text{mil}$):

```text
                  +12V Rail 6 (X=2800 mil)
                       │
                       ├──────────────────────────┐
                       │                          │
                   [R2: 4.7kΩ]                 Emissor (E) [X=2800 mil]
                 (Pull-up corte)                  │
                       │                          │ Q2: BC328 (PNP, TO-92)
                       ├───[R3: 680Ω]─── Base (B)─┤   [Pad X=2400 mil]
                       │                          │
                 Coletor (C)                      │ Coletor (C) [Pad X=2500 mil]
                       │                          │
                       │ Q1: BC549 (NPN, TO-92)   ├───────────────► Saída +12V Chaveada (para Borne KRE)
                       │                          │                 (Pino 2 do Fan)
 PWM In ──[R1: 1.5kΩ]──┤ Base (B)                [D1] 1N4007
 (MCU)                 │                         (Flyback)
                  Emissor (E)                     │
                       │                          ▼
                  GND (0V Rail 4) ────────────────┴───────────────► GND Comum (Pino 1 do Fan)
```

### Detalhamento Físico de cada Bloco de 3 Linhas (Exemplo Canal 1):
- **Linha 17 (NPN Driver):**
  - $R_1$ ($1.5\,\text{k}\Omega$): terminal 1 em $X=2000\,\text{mil}$ (ligado a `NET_PWM1`), terminal 2 em $X=2300\,\text{mil}$.
  - $Q_1$ (BC549 NPN): Base em $X=2400\,\text{mil}$, Emissor ligado ao Rail 4 GND em $X=1700\,\text{mil}$, Coletor inserido na Linha 18 em $X=2400\,\text{mil}$.
- **Linha 18 (Nó Intermediário de Drive & Pull-up):**
  - Coletor de $Q_1$ em $X=2400\,\text{mil}$.
  - $R_2$ ($4.7\,\text{k}\Omega$ pull-up): montado entre $X=2500\,\text{mil}$ e Rail 6 (+12V em $X=2800\,\text{mil}$).
  - $R_3$ ($680\,\Omega$ drive): terminal 1 em $X=2300\,\text{mil}$, terminal 2 na Linha 19 em $X=2300\,\text{mil}$.
- **Linha 19 (PNP de Potência & Proteção Flyback):**
  - Base de $Q_2$ em $X=2400\,\text{mil}$ (recebe $R_3$).
  - Emissor de $Q_2$ (BC328 PNP): soldado no Rail 6 (+12V em $X=2800\,\text{mil}$).
  - Coletor de $Q_2$: em $X=2500\,\text{mil}$ (Gera `FAN1_12V`).
  - Diodo Flyback $D_1$ (1N4007): Cátodo em $X=2600\,\text{mil}$ (Linha 19), Ânodo no Rail 8 (GND em $X=3000\,\text{mil}$).
  - Jumper de Saída: De $X=2700\,\text{mil}$ diretamente para o Pino 2 do conector `FAN1`!

---

## 4. Arquivo de Coordenadas Completas

A tabela detalhada contendo as coordenadas $(X, Y)$ em mil e milímetros de todos os 37 componentes, furos e pinos está registrada em:
- [`SZIKLAI_REV1.1A_COORDINATE_SCHEDULE.md`](SZIKLAI_REV1.1A_COORDINATE_SCHEDULE.md)
- Script gerador oficial: [`generate_sziklai_rev1.1a_schedule.py`](generate_sziklai_rev1.1a_schedule.py)

---

## 5. Visualizações do Circuito e Gabaritos de Impressão 1:1 (Rev 1.1a)

Os diagramas de montagem e gabaritos em escala real 1:1 para a placa Rev 1.1a estão disponíveis no diretório [`templates/`](templates/):
- **Diagrama de Montagem do Circuito no PCB (Top View):**
  - Imagem 300 DPI: [`circuit_assembly_rev1.1a_top_view.png`](templates/circuit_assembly_rev1.1a_top_view.png)
  - Vetorial SVG: [`circuit_assembly_rev1.1a_top_view.svg`](templates/circuit_assembly_rev1.1a_top_view.svg)
- **Diagrama de Solda e Furação (Bottom View espelhado):**
  - Imagem 300 DPI: [`circuit_assembly_rev1.1a_bottom_view.png`](templates/circuit_assembly_rev1.1a_bottom_view.png)
  - Vetorial SVG: [`circuit_assembly_rev1.1a_bottom_view.svg`](templates/circuit_assembly_rev1.1a_bottom_view.svg)
- **Folha de Impressão A4 1:1 com Calibradores Milimétricos:**
  - PDF Vetorial 100% Escala: [`stripboard_rev1.1a_1to1_printout.pdf`](templates/stripboard_rev1.1a_1to1_printout.pdf)
  - Script Gerador Automatizado: [`generate_rev1.1a_templates.py`](templates/generate_rev1.1a_templates.py)

---

## Apêndice: Referência Histórica do Protótipo em Placa Padrão (custoStripBoard.ods)

> Esta seção preserva o projeto histórico desenvolvido para a placa genérica de $33\,\text{mm} \times 72\,\text{mm}$ (336 furos) documentada em `custoStripBoard.ods`, utilizando o corte de trilha R16/C12 e chaveamento Low-Side com ULN2003A:
> - Matriz: 28 Linhas $\times$ 12 Colunas.
> - Corte de Trilha: R16/C12 para separar +5V superior de +12V inferior.
> - Layout detalhado, esquemas de cortes e moldes 1:1 permanecem disponíveis no diretório [`docs/templates/`](templates/).
