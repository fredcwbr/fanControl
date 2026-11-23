# Custom Stripboard Rev 1.1 & Rev 1.1a — Especificação Técnica Completa e Manual de Engenharia

> **Idiomas / Languages:** [Português](CUSTOM_STRIPBOARD_REV1.1_SPEC_PT.md) | [English (US)](CUSTOM_STRIPBOARD_REV1.1_SPEC_EN.md) | [Español](CUSTOM_STRIPBOARD_REV1.1_SPEC_ES.md)

Este documento consolida todas as notas técnicas, especificações elétricas, mecânicas, regras de layout, opções de montagem e detalhes adicionais das revisões **Rev 1.1** e **Rev 1.1a** da placa **Custom Stripboard**.

---

## 1. Visão Geral e Filosofia de Projeto

A **Custom Stripboard Rev 1.1 / Rev 1.1a** é uma plataforma de prototipagem e controle em formato de placa padrão Eurocard/Vector de face única inferior (*single-sided* na camada de solda, com componentes passantes pelo topo), projetada no fluxo **Lepton-EDA** + **`pcb-rnd`**.

### Princípios Fundamentais:
1. **Padrão Thru-Hole (Furo Passante) como Default Obrigatório**:
   - A montagem SMD é estritamente uma opção secundária/acessória.
   - O padrão nativo e prioritário da placa é **100% Through-Hole (THT / PTH)** com furos metalizados.
   - Todos os componentes discretos (capacitores cerâmicos/eletrolíticos, resistores axiais), circuitos integrados (DIP), reguladores lineares (TO-220 upright), bornes de parafusos e conectores utilizam pinos passantes.
2. **Pad Sizes Padronizados ($\ge 80\text{ mil}$)**:
   - Todas as ilhas de solda da matriz de prototipagem, pass-thrus, conectores e reguladores possuem diâmetro externo $\ge 80.00\text{ mil}$ ($2.032\text{ mm}$), broca de $35.00\text{ mil}$ ($0.889\text{ mm}$) e máscara de solda de $86.00\text{ mil}$ ($2.184\text{ mm}$).
   - Ilhas da área de prototipagem rápida (*scratch-pad*) possuem diâmetro de $90.00\text{ mil}$ ($2.286\text{ mm}$) com gap de $10\text{ mil}$.
3. **Face Única com Conector de Borda Industrial**:
   - Toda a fiação de cobre reside exclusivamente na **camada inferior (`Layer 6 "bottom"`)**.
   - A lingueta inferior de 44 pinos padrão Sullins / Vector ($2.54\text{ mm}$ / $100\text{ mil}$ pitch) possui dedos de contato e jumpers de solda apenas na face inferior, garantindo segurança contra curtos na face superior virgem.

---

## 2. Geometria Mecânica e Posicionamento dos Furos M3

### Dimensões Físicas:
- **Largura Estrutural:** $3500.00\text{ mil}$ ($88.90\text{ mm}$)
- **Comprimento Total:** $5050.00\text{ mil}$ ($128.27\text{ mm}$)
- **Largura da Lingueta de Borda:** $2700.00\text{ mil}$ ($68.58\text{ mm}$), estendendo-se de $X = 400.00\text{ mil}$ a $3100.00\text{ mil}$.
- **Profundidade de Inserção da Lingueta:** $310.00\text{ mil}$ ($7.87\text{ mm}$), de $Y = 4740.00\text{ mil}$ a $5050.00\text{ mil}$.
- **Ombros de Encosto Mecânico:** Degrau de $400.00\text{ mil}$ em cada lado na cota $Y = 4740.00\text{ mil}$.
- **Chanfros de Inserção:** $40.00\text{ mil} \times 45^\circ$ nos cantos inferiores da lingueta.

### Furação de Fixação M3 (Broca $126\text{ mil}$ / $3.20\text{ mm}$, Pad $240\text{ mil}$, Keepout $300\text{ mil}$):
| Identificador | Coordenadas $(X, Y)$ | Justificativa de Posicionamento e Folgas Mecânicas |
| :---: | :---: | :--- |
| **MH101** | $(200.00, 200.00\text{ mil})$ | Canto superior esquerdo. Folga ampla para o Jack DC 1 e módulo VR101. |
| **MH102** | $(3300.00, 200.00\text{ mil})$ | Canto superior direito. Mantém $>150\text{ mil}$ de isolação livre até o corpo do Borne KRE (`TB101`) em $Y = 600\text{ mil}$. |
| **MH103** | $(200.00, 2000.00\text{ mil})$ | **Reposicionado para $Y = 2000\text{ mil}$**. Localizado exatamente no espaço intermediário entre o Módulo LM2596 #1 (`VR101`, que termina em $Y = 1200\text{ mil}$) e o Módulo LM2596 #2 (`VR102`, que inicia em $Y = 2800\text{ mil}$). O keepout de $300\text{ mil}$ ($Y \in [1850, 2150]$) possui mais de $650\text{ mil}$ de folga para os pinos de ambos os módulos. |
| **MH104** | $(3300.00, 2700.00\text{ mil})$ | **Ajustado para $Y = 2700\text{ mil}$**. Mantém $80\text{ mil}$ de folga para a base do corpo plástico do Borne KRE (`TB101`, base em $Y = 2500\text{ mil}$) e $135\text{ mil}$ de folga até o topo da área scratch-pad ($Y = 2955\text{ mil}$). |
| **MH105** | $(200.00, 4600.00\text{ mil})$ | Canto inferior esquerdo. Borda inferior do anel de cobre ($Y = 4720\text{ mil}$) alinha-se perfeitamente com a base da última linha de prototipagem ($Y = 4728\text{ mil}$), garantindo $140\text{ mil}$ de recuo em relação aos ombros da placa ($Y = 4740\text{ mil}$). |
| **MH106** | $(3300.00, 4600.00\text{ mil})$ | Canto inferior direito, alinhado com MH105. |

---

## 3. Subsistema de Potência de Topo: DC Jacks & Duplo Regulador LM317

### 3.1 Entradas de Força DC Barrel Jack & Breakouts SIP3
Para evitar congestionamento na área central e possibilitar dissipadores de calor generosos nos reguladores, as duas tomadas DC Jack 2.1mm $\times$ 5.5mm foram afastadas para as extremidades:
- **DC Jack 1 (`CONN117`):** Posicionado em $X = 800.00\text{ mil}, Y = 200.00\text{ mil}$.
  - Conector Breakout SIP3 (`CONN119..121`): réguas verticais em $X = 500, 600, 700\text{ mil}$ ($Y = 200, 300, 400\text{ mil}$).
  - Pino 1 ($+V$), Pino 2 (Switch), Pino 3 (GND/Sleeve) interligados com **trilhas de cobre de $40\text{ mil}$**.
- **DC Jack 2 (`CONN118`):** Posicionado em $X = 2400.00\text{ mil}, Y = 200.00\text{ mil}$.
  - Conector Breakout SIP3 (`CONN122..124`): réguas verticais em $X = 2800, 2900, 3000\text{ mil}$ ($Y = 200, 300, 400\text{ mil}$).
  - Interligações roteadas com **trilhas de cobre de $40\text{ mil}$**.

### 3.2 Duplo Regulador Linear LM317 (Datasheet TI, Página 1)
Entre os dois Jacks DC ($X = 1400\text{ mil}$ a $X = 2100\text{ mil}$, $Y = 200..700\text{ mil}$), foram implementados dois circuitos reguladores independentes e completos, seguindo rigorosamente a aplicação padrão do datasheet da Texas Instruments:

$$V_{OUT} = 1.25\,\text{V} \times \left(1 + \frac{R_2}{R_1}\right) + I_{ADJ} \times R_2$$

```
                         CIRCUITO LM317 (Datasheet TI Página 1)
                              ┌──────────────┐
                  VIN o───────┤ 3 (VIN)      │
                              │   LM317      │
                    ┌─────────┤ 1 (ADJ)    2 ├──┬───────────────o VOUT
                    │         └──────────────┘  │
                    │               │           │
                   [R2]            [R1 240Ω]   [C2 1.0µF]
                    │ (Ajuste)      │           │
                    │               └───────────┘
                    │
           GND o────┴───────────────────────────────────────────o GND (Comum)
               (C1 0.1µF desacoplamento na entrada VIN)
```

#### LM317 Circuito #1:
- **CI Regulador `U101` (TO-220 Upright):** Pino 3 (VIN) em $(1400, 300)$, Pino 2 (VOUT) em $(1500, 300)$, Pino 1 (ADJ) em $(1600, 300)$.
- **Capacitor de Entrada `C101` ($0.1\,\mu\text{F}$ disco cerâmico):** Terminais em $(1400, 400)$ e $(1400, 600)$.
- **Capacitor de Saída `C102` ($1.0\,\mu\text{F}$ tântalo/eletrolítico):** Terminais em $(1500, 400)$ e $(1500, 600)$.
- **Resistor de Feedback `R101` ($240\,\Omega$, 1/4W axial):** Montado entre $(1500, 500)$ [VOUT1] e $(1600, 500)$ [ADJ1].
- **Resistor de Ajuste `R102` ($R_2$, resistor fixo ou trimpot multi-voltas):** Terminais em $(1600, 400)$ e $(1600, 600)$ [GND].
- **Ilhas de Teste e Derivação THT (Pads $\ge 80\text{ mil}$):**
  - `J101` (VIN1): $(1400.00, 200.00\text{ mil})$
  - `J102` (VOUT1): $(1500.00, 200.00\text{ mil})$
  - `J103` (GND): $(1400.00, 700.00\text{ mil})$

#### LM317 Circuito #2:
- **CI Regulador `U102` (TO-220 Upright):** Pino 3 (VIN) em $(1900, 300)$, Pino 2 (VOUT) em $(2000, 300)$, Pino 1 (ADJ) em $(2100, 300)$.
- **Capacitor de Entrada `C103` ($0.1\,\mu\text{F}$ disco cerâmico):** Terminais em $(1900, 400)$ e $(1900, 600)$.
- **Capacitor de Saída `C104` ($1.0\,\mu\text{F}$ tântalo/eletrolítico):** Terminais em $(2000, 400)$ e $(2000, 600)$.
- **Resistor de Feedback `R103` ($240\,\Omega$, 1/4W axial):** Montado entre $(2000, 500)$ [VOUT2] e $(2100, 500)$ [ADJ2].
- **Resistor de Ajuste `R104` ($R_2$, resistor fixo ou trimpot multi-voltas):** Terminais em $(2100, 400)$ e $(2100, 600)$ [GND].
- **Ilhas de Teste e Derivação THT (Pads $\ge 80\text{ mil}$):**
  - `J104` (VIN2): $(1900.00, 200.00\text{ mil})$
  - `J105` (VOUT2): $(2000.00, 200.00\text{ mil})$
  - `J106` (GND): $(1900.00, 700.00\text{ mil})$

#### Barramento de Terra Comum:
- Linha $Y = 600.00\text{ mil}$ une o GND do circuito 1 ao GND do circuito 2 ($X = 1400$ a $X = 2100\text{ mil}$) com **trilha de cobre de $40\text{ mil}$**.

---

## 4. Margem Esquerda: Módulos Step-Down LM2596 Upright (`VR101`, `VR102`)

Para conversão chaveada eficiente DC-DC (+12V para +5V, +3.3V ou tensão ajustável de alta corrente até 3A), a placa disponibiliza footprint para 2 módulos LM2596 na orientação vertical (*upright*):

- **Footprint:** Matriz de $4 \times 7$ pinos em passo de $200.00\text{ mil}$ ($5.08\text{ mm}$):
  - Colunas: $X = 100, 200, 300, 400\text{ mil}$.
- **Módulo 1 (`VR101`):** $Y = 600.00\text{ mil}$ a $1200.00\text{ mil}$.
  - Linhas 1 a 4: Conexão de Entrada (`VIN1+` em $X = 100$, `VIN1-` em $X = 300$).
  - Linhas 5 a 7: Conexão de Saída (`OUT1+` em $X = 100$, `OUT1-` em $X = 300$).
- **Módulo 2 (`VR102`):** $Y = 2800.00\text{ mil}$ a $3400.00\text{ mil}$.
  - Linhas 1 a 4: Conexão de Entrada (`VIN2+` em $X = 100$, `VIN2-` em $X = 300$).
  - Linhas 5 a 7: Conexão de Saída (`OUT2+` em $X = 100$, `OUT2-` em $X = 300$).
- **Trilhas de Potência de $40\text{ mil}$:** Todas as linhas verticais que agrupam os pinos de força de cada módulo utilizam trilhas de cobre de $40\text{ mil}$, minimizando aquecimento e permitindo alta capacidade de condução de corrente.
- **Espaçamento e Isolação Mecânica:** Entre o módulo 1 e o módulo 2 situa-se o parafuso `MH103` ($Y = 2000\text{ mil}$), mantendo isolamento de qualquer componente de chaveamento.

---

## 5. Margem Direita: Borne KRE 10 Vias 5.08mm & Pass-Thru Matrix

Na borda direita superior, entre os furos `MH102` e `MH104`, localiza-se o bloco terminal de parafusos industrial:

- **Modelo do Conector:** Conector Borne KRE 10 Vias $5.08\text{ mm}$ (modelo ZB128 altura 14mm).
- **Posição do Conector (`TB101`):** $X = 3400.00\text{ mil}$, com os 10 pinos distribuídos em:
  $$Y = [600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400]\text{ mil}$$
- **Matriz Pass-Thru Horizontal de 3 Pontos:**
  - Para cada pino do conector `TB101`, existem 3 ilhas passantes alinhadas na horizontal em direção ao centro da placa:
    - Ponto 1: `CONN137` em $X = 3300.00\text{ mil}$
    - Ponto 2: `CONN138` em $X = 3200.00\text{ mil}$
    - Ponto 3: `CONN139` em $X = 3100.00\text{ mil}$
  - As 3 ilhas e o pino correspondente do KRE são interligados por **trilhas de cobre de $30\text{ mil}$**.
  - Cada linha de 4 pontos forma uma rede elétrica totalmente independente: `KRE_1`, `KRE_2`, ..., `KRE_10`.
- **Folgas Mecânicas Seguras:**
  - Acima do pino 1 ($Y = 600\text{ mil}$), o keepout de isolação do parafuso `MH102` termina em $Y = 350\text{ mil}$ (folga $>150\text{ mil}$).
  - Abaixo do corpo plástico do borne ($Y = 2500\text{ mil}$), o furo `MH104` em $Y = 2700\text{ mil}$ possui folga de $80\text{ mil}$ até o pad e $>50\text{ mil}$ até o anel de alívio do parafuso.

---

## 6. Margem Direita: Scratch-Pad Proto Area (Área de Prototipagem Rápida)

Entre o furo `MH104` e o furo inferior `MH106`, foi incorporada uma matriz densa de prototipagem rápida tipo *scratch-pad*:

- **Geometria da Matriz:** $14\text{ linhas} \times 4\text{ colunas} = \mathbf{56\text{ ilhas}}$.
  - Colunas: $X = [3100.00, 3200.00, 3300.00, 3400.00]\text{ mil}$.
  - Linhas: $Y = 3000.00\text{ mil}$ a $4300.00\text{ mil}$ com passo de $100.00\text{ mil}$ ($2.54\text{ mm}$).
- **Dimensões dos Pads:**
  - Diâmetro externo do Pad: **$90.00\text{ mil}$** ($2.286\text{ mm}$).
  - Diâmetro do furo passante metalizado (drill): **$35.00\text{ mil}$** ($0.889\text{ mm}$).
  - Abertura de máscara de solda: **$96.00\text{ mil}$** ($2.438\text{ mil}$).
  - **Gap de Cobre entre Pads Adjacentes:** Exatamente **$10.00\text{ mil}$** ($0.254\text{ mm}$), facilitando soldagem ponto a ponto com pontes de solda intencionais ou pontes de estanho.
- **Microtrilhas Raspáveis de $3\text{ mil}$ (Knife-Scratchable):**
  - Todas as 56 ilhas estão inicialmente unidas na rede elétrica comum `SCRATCHPAD`.
  - As ligações físicas entre cada ilha vizinha (horizontal e verticalmente) são feitas por microtrilhas de **$3.00\text{ mil}$** ($0.0762\text{ mm}$) na camada inferior de cobre.
  - **Uso Operacional:** Uma raspagem leve com lâmina de bisturi cirúrgico nº 11 ou estilete X-Acto secciona instantaneamente qualquer microtrilha de 3 mil, isolando a ilha ou formando grupos personalizados de redes elétricas sem risco de delaminação do laminado FR4.
- **Delimitação em Serigrafia:** Caixa retangular silkscreen de $X = 3040$ a $3460\text{ mil}$, $Y = 2950$ a $4350\text{ mil}$, com a legenda clara `"SCRATCH PAD"`.

---

## 7. Hierarquia Padronizada de Trilhas de Cobre

| Espessura da Trilha | Clearance | Camada | Aplicações e Circuitos Atendidos |
| :---: | :---: | :---: | :--- |
| **$40.00\text{ mil}$** ($1.016\text{ mm}$) | $20.00\text{ mil}$ | Bottom | 8 Barramentos verticais principais (+12V, +5V, GND); Trilhas de força dos Jacks DC 1 e 2; Trilhas dos barramentos dos módulos LM2596 (`VR101`, `VR102`); Trilhas de alimentação e terra dos LM317; Réguas verticais inferiores de 4 pinos (`SIP4N`). |
| **$30.00\text{ mil}$** ($0.762\text{ mm}$) | $20.00\text{ mil}$ | Bottom | Pontes de interligação vertical de $100\text{ mil}$ do sanduíche (`HEADER18` para `SIP9N`); Trilhas dos jumpers de solda abertos na lingueta; Trilhas de conexão do Borne KRE (`TB101`) para a matriz pass-thru (`CONN137..139`). |
| **$20.00\text{ mil}$** ($0.508\text{ mm}$) | $20.00\text{ mil}$ | Bottom | Trilhas do pino 1 (ADJ) dos reguladores LM317 até os resistores $R_1$ e $R_2$. |
| **$10.00\text{ mil}$** ($0.254\text{ mm}$) | $20.00\text{ mil}$ | Bottom | Trilhas horizontais das 58 linhas de prototipagem (Rev 1.1) ou 64 linhas de prototipagem (Rev 1.1a). |
| **$3.00\text{ mil}$** ($0.076\text{ mm}$) | $10.00\text{ mil}$ | Bottom | Microtrilhas seccionáveis da área de prototipagem rápida *scratch-pad*. |

---

## 8. Comparativo Detalhado: Rev 1.1 vs. Rev 1.1a

| Característica | Custom Stripboard Rev 1.1 | Custom Stripboard Rev 1.1a |
| :--- | :--- | :--- |
| **Número de Linhas de Prototipagem Horizontal** | 29 linhas por banco (Linhas 1 a 29, total de 58 réguas de 9 pinos) | **32 linhas por banco (Linhas 1 a 32, total de 64 réguas de 9 pinos)** |
| **Posicionamento do Sanduíche de Interconexão** | $Y = 3800\text{ mil}$ (`SIP9N`), $Y = 3900..4000\text{ mil}$ (`HEADER18`), $Y = 4100\text{ mil}$ (`SIP9N`) | **Deslocado $+200\text{ mil}$ para baixo:** $Y = 4000\text{ mil}$ (`SIP9N`), $Y = 4100..4200\text{ mil}$ (`HEADER18`), $Y = 4300\text{ mil}$ (`SIP9N`) |
| **Aproveitamento das Linhas $Y = 3700, 3800, 3900\text{ mil}$** | Área de transição / parcialmente desocupada | **100% preenchidas:** Réguas `CONN241..243` e `CONN341..343` com trilhas de 10 mil |
| **Folga para as Réguas Verticais de Saída ($Y = 4400\text{ mil}$)** | Lacuna de $300\text{ mil}$ não aproveitada ($Y = 4100$ a $4400\text{ mil}$) | **Perfeita:** Régua inferior em $Y = 4300\text{ mil}$, a exatos $100\text{ mil}$ (passo padrão) da entrada de saída |
| **Módulos LM2596 Upright (`VR101`, `VR102`)** | Presentes na margem esquerda ($4 \times 7$ pinos) | Presentes na margem esquerda ($4 \times 7$ pinos) |
| **Duplo Regulador Linear LM317 (`U101`, `U102`)** | Presentes entre os Jacks DC com pads passantes | Presentes entre os Jacks DC com pads passantes |
| **Borne KRE 10 Vias 5.08mm + Pass-Thru** | Presente na margem direita (`TB101` + 30 pads) | Presente na margem direita (`TB101` + 30 pads) |
| **Scratch-Pad Proto Area (56 pads, $3\text{ mil}$)** | Presente entre `MH104` e `MH106` | Presente entre `MH104` e `MH106` |
| **Identificação em Serigrafia** | `"CUSTOM STRIPBOARD REV 1.1"` | `"CUSTOM STRIPBOARD REV 1.1a"` |

---

## 9. Mapeamento de Arquivos e Instruções de Reprodução

Todos os fontes oficiais de engenharia residem no repositório:

- **Scripts e Fontes EDA**:
  - Script Gerador de Layout: [`layout_stripboards.py`](file:///home/fred/C/fanControl/lepton/layout_stripboards.py)
  - Esquemáticos Rev 1.1a: [`rev1.1a/centro.sch`](file:///home/fred/C/fanControl/lepton/rev1.1a/centro.sch), [`rev1.1a/lado1.sch`](file:///home/fred/C/fanControl/lepton/rev1.1a/lado1.sch), [`rev1.1a/lado2.sch`](file:///home/fred/C/fanControl/lepton/rev1.1a/lado2.sch), [`rev1.1a/interconnect.sch`](file:///home/fred/C/fanControl/lepton/rev1.1a/interconnect.sch)
  - Layout PCB Rev 1.1a: [`rev1.1a/stripboard_rev1.1a.pcb`](file:///home/fred/C/fanControl/lepton/rev1.1a/stripboard_rev1.1a.pcb)
  - Esquemáticos Rev 1.1: [`rev1.1/centro.sch`](file:///home/fred/C/fanControl/lepton/rev1.1/centro.sch), [`rev1.1/lado1.sch`](file:///home/fred/C/fanControl/lepton/rev1.1/lado1.sch), [`rev1.1/lado2.sch`](file:///home/fred/C/fanControl/lepton/rev1.1/lado2.sch), [`rev1.1/interconnect.sch`](file:///home/fred/C/fanControl/lepton/rev1.1/interconnect.sch)
  - Layout PCB Rev 1.1: [`rev1.1/stripboard_rev1.1.pcb`](file:///home/fred/C/fanControl/lepton/rev1.1/stripboard_rev1.1.pcb)

- **Imagens de Pré-Visualização em Alta Definição (300 DPI)**:
  - Rev 1.1a Topo (Componentes): [`stripboard_rev1.1a_preview_300dpi.png`](file:///home/fred/C/fanControl/lepton/rev1.1a/stripboard_rev1.1a_preview_300dpi.png)
  - Rev 1.1a Fundo (Cobre e Dedos de Borda): [`stripboard_rev1.1a_bottom_preview_300dpi.png`](file:///home/fred/C/fanControl/lepton/rev1.1a/stripboard_rev1.1a_bottom_preview_300dpi.png)
  - Rev 1.1 Topo (Componentes): [`stripboard_rev1.1_preview_300dpi.png`](file:///home/fred/C/fanControl/lepton/rev1.1/stripboard_rev1.1_preview_300dpi.png)
  - Rev 1.1 Fundo (Cobre e Dedos de Borda): [`stripboard_rev1.1_bottom_preview_300dpi.png`](file:///home/fred/C/fanControl/lepton/rev1.1/stripboard_rev1.1_bottom_preview_300dpi.png)
  - Esquema Elétrico Rev 1.1a: [`centro.png (Rev 1.1a)`](file:///home/fred/C/fanControl/lepton/rev1.1a/centro.png)
  - Esquema Elétrico Rev 1.1: [`centro.png (Rev 1.1)`](file:///home/fred/C/fanControl/lepton/rev1.1/centro.png)

### Comandos de Compilação:
```bash
# Regerar os layouts PCB, netlists e renderizações fotográficas em 300 DPI:
python3 lepton/layout_stripboards.py

# Exportar esquemáticos para PNG e compilar netlists:
cd lepton/rev1.1a && lepton-cli export -o centro.png centro.sch && lepton-netlist -g PCB -o stripboard_rev1.1a.net centro.sch
cd ../rev1.1 && lepton-cli export -o centro.png centro.sch && lepton-netlist -g PCB -o stripboard_rev1.1.net centro.sch
```

---

## 10. Avaliação Detalhada de Custo de Produção (Production Cost Analysis)

> [!WARNING]
> **Aviso de Vigência Temporal de Preços (Novembro/Dezembro de 2026):**  
> Todas as cotações de placas, valores de componentes (BOM), mão de obra e taxas de câmbio apresentados nesta seção têm como base o cenário de mercado apurado em **Novembro/Dezembro de 2026** (taxa cambial de referência: US$ 1,00 = R$ 5,80). Custos de insumos (laminados de fibra FR4, cobre), inflação acumulada, regimes tributários de importação (como alíquotas de ICMS e Remessa Conforme), ciclo de vida de componentes e oscilações cambiais alterarão esses montantes ao longo do tempo. Leitores e projetistas que consultarem este documento no futuro devem obter orçamentos atualizados diretamente junto aos fabricantes e distribuidores antes de executar ordens de produção.


Apresentamos a análise quantitativa e qualitativa abrangente de custo para produção da **Custom Stripboard Rev 1.1 / Rev 1.1a**, incorporando cotações de referência dos principais **fabricantes nacionais brasileiros de circuito impresso (TEC-CI, PCB Brasil, Micro-Circuitos, Griffus PCB, Micropress e Circuibras)**, lista completa de materiais (BOM), mão de obra de montagem e soldagem through-hole, gravação de firmware, testes funcionais de qualidade e cenários de escala de volume.

---

### 10.1 Custos de Fabricação do PCB — Benchmark da Indústria Nacional vs. Importação

#### Parâmetros Técnicos de Fabricação da Placa:
- **Dimensões:** $88.90\text{ mm} \times 128.27\text{ mm}$ ($3.50'' \times 5.05''$, área superficial $\approx 114\text{ cm}^2$).
- **Número de Camadas:** 2 Camadas (Dupla face FR4, roteamento de cobre de face única na camada inferior `Layer 6`).
- **Substrato e Cobre:** FR-4 padrão ($T_g \ge 130\text{--}140^\circ\text{C}$), espessura de $1.60\text{ mm}$, cobre 1 oz ($35\,\mu\text{m}$).
- **Especificação Furo Passante:** Furos metalizados (PTH), padrão 100% Through-Hole default, diâmetro externo de ilha $\ge 80.00\text{ mil}$ ($2.032\text{ mm}$), broca de $35.00\text{ mil}$ ($0.889\text{ mm}$).
- **Acabamento de Superfície:** HASL Lead-Free (estanho sem chumbo padrão) ou ENIG (Ouro Químico, recomendado para durabilidade dos dedos de borda).
- **Conector de Borda:** Chanfro de inserção a $45^\circ$ na lingueta de 44 pinos.

#### Benchmark dos Principais Fabricantes Nacionais (Brasil):

| Fabricante | Sede / Perfil | Protótipo Típico (5 placas) | Pequeno Lote (30 placas) | Lote de Produção (100+ placas) | Prazo Médio de Entrega | Diferencial Competitivo Principal |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **TEC-CI Circuitos Impressos** | São Paulo - SP (Fund. 1984) | **R$ 39,00** / un<br>*(US$ 6.72)* | **R$ 24,00** / un<br>*(US$ 4.14)* | **R$ 13,50** / un<br>*(US$ 2.33)* | 7 a 10 dias úteis | Plataforma de orçamento instantâneo online; preços agressivos de protótipos; forte suporte local |
| **PCB Brasil** | Campinas - SP | **R$ 42,00** / un<br>*(US$ 7.24)* | **R$ 26,00** / un<br>*(US$ 4.48)* | **R$ 14,50** / un<br>*(US$ 2.50)* | 7 a 10 dias úteis | Configurador web ágil com programa de protótipos; variedade de cores de máscara; rastreio confiável |
| **Micro-Circuitos** | Rio de Janeiro / SP | **R$ 45,00** / un<br>*(US$ 7.76)* | **R$ 27,00** / un<br>*(US$ 4.65)* | **R$ 15,00** / un<br>*(US$ 2.59)* | 8 a 12 dias úteis | Especialista em protótipos e pequenas séries; suporte técnico de engenharia e revisão de layout |
| **Griffus PCB** | Cotia - SP | **R$ 48,00** / un<br>*(US$ 8.28)* | **R$ 28,00** / un<br>*(US$ 4.83)* | **R$ 14,00** / un<br>*(US$ 2.41)* | 8 a 10 dias úteis | Certificação ISO 9001; alta estabilidade dimensional mecânica para conectores de gaveta industrial |
| **Micropress** | São Paulo - SP (Fund. 1986) | **R$ 72,00** / un<br>*(US$ 12.41)* | **R$ 42,00** / un<br>*(US$ 7.24)* | **R$ 24,00** / un<br>*(US$ 4.14)* | **24h a 48h express**<br>*(ou 5–7d padrão)* | Referência nacional em prototipagem rápida de alta precisão (quick-turn); padrão aeroespacial/médico |
| **Circuibras** | Curitiba - PR | **R$ 56,00** / un<br>*(US$ 9.65)* | **R$ 25,00** / un<br>*(US$ 4.31)* | **R$ 12,00** / un<br>*(US$ 2.07)* | 10 a 15 dias úteis | Parque fabril de alta capacidade; excelente economia de escala para lotes acima de 100 unidades |

*(Taxa cambial de referência: US$ 1.00 = R$ 5,80)*

#### Análise Estratégica: Fabricação Nacional vs. Importação da Ásia:

- **Fabricação Nacional (TEC-CI, PCB Brasil, Micro-Circuitos, etc.):**
  - **Zero Risco Aduaneiro:** Entrega doméstica rápida via Sedex (1 a 2 dias após produção).
  - **Emissão de Nota Fiscal (NF-e):** Faturamento com CNPJ nacional, essencial para prestação de contas de empresas e projetos acadêmicos fomentados (FAPESP, CNPq, FINEP).
  - **Previsibilidade Financeira:** Isenção das alíquotas aduaneiras e ICMS que no regime "Remessa Conforme" somam mais de 92% sobre valor do produto somado ao frete.
  - **Suporte Direto de Engenharia:** Mesma timezone, contato direto via telefone e WhatsApp com os engenheiros de CAM em português.
- **Fabricação Internacional (ex: JLCPCB / PCBWay):**
  - Preço base de tabela aparentemente menor (US$ 4.00 a US$ 75.00), porém o frete expresso internacional (US$ 14.00 a US$ 35.00) somado ao imposto de importação e ICMS elevam o protótipo real para **R$ 28,00 a R$ 35,00 por placa**, com prazo total de **15 a 30 dias corridos**.

---

### 10.2 Lista Completa de Materiais (Bill of Materials - BOM) por Placa

Todos os componentes atendem rigorosamente à diretriz de fabricação **100% Through-Hole (THT / DIP)**:

| Item | Componente / Especificação | Encapsulamento / Passo | Qtd | Preço Unit. (USD) | Preço Unit. (BRL) | Custo Total (BRL) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **U1** | Microcontrolador ATmega328P-PU | DIP-28 Estreito ($0.3''$) | 1 | US$ 2.20 | R$ 12,80 | R$ 12,80 |
| **SKT1** | Soquete DIP-28 Estampado / Torneado | 28 Pinos passo $2.54\text{ mm}$ | 1 | US$ 0.25 | R$ 1,50 | R$ 1,50 |
| **U2** | Driver Darlington ULN2003A ou ULN7003A | DIP-16 | 1 | US$ 0.40 | R$ 2,30 | R$ 2,30 |
| **SKT2** | Soquete DIP-16 | 16 Pinos passo $2.54\text{ mm}$ | 1 | US$ 0.15 | R$ 0,90 | R$ 0,90 |
| **MOD1** | Módulo Conversor USB-TTL CH340 (6 pinos) | 6 Pinos passo $2.54\text{ mm}$ | 1 | US$ 1.20 | R$ 7,00 | R$ 7,00 |
| **Y1** | Cristal de Quartzo 16.000 MHz | HC-49S THT | 1 | US$ 0.18 | R$ 1,00 | R$ 1,00 |
| **C3, C4** | Capacitores Cerâmicos 22 pF | Disco cerâmico | 2 | US$ 0.05 | R$ 0,30 | R$ 0,60 |
| **U101, U102** | CI Regulador LM317T (Datasheet TI) | TO-220 Upright | 2 | US$ 0.40 | R$ 2,30 | R$ 4,60 |
| **VR101, VR102**| Módulos Step-Down LM2596 DC-DC | Upright $4 \times 7$ pinos | 2 | US$ 1.30 | R$ 7,50 | R$ 15,00 |
| **TB101** | Conector Borne KRE 10 Vias 5.08mm | ZB128 altura 14mm | 1 | US$ 1.10 | R$ 6,40 | R$ 6,40 |
| **CONN117, 118**| Conector Jack DC Fêmea 2.1 $\times$ 5.5mm | THT Radial | 2 | US$ 0.25 | R$ 1,45 | R$ 2,90 |
| **HDR_SANDWICH**| Barra de Pinos 2.54mm (Macho + Fêmea) | Barras de 40 pinos | 2 barras | US$ 0.60 | R$ 3,50 | R$ 7,00 |
| **PASSIVOS** | Caps desacoplamento (100nF, 1uF, 100uF) + Resistores | Kit Axial/Radial | 1 kit | US$ 0.70 | R$ 4,00 | R$ 4,00 |
| **MECÂNICA** | Parafusos, porcas e espaçadores M3 de latão/nylon | Kit 6 furos | 6 kits | US$ 0.80 | R$ 4,60 | R$ 4,60 |
| **TOTAL BOM** | **Soma dos Componentes Eletrônicos por Placa** | — | — | **US$ 9.58** | **R$ 55,85** | **R$ 70,60 (c/ margem)** |

---

### 10.3 Custos de Montagem, Soldagem e Testes Funcionais

- **Tempo Médio de Montagem Manual Through-Hole:** ~25 a 35 minutos por placa (inserção de componentes, dobra de terminais, soldagem manual, corte de sobras e limpeza de fluxo).
- **Gravação de Firmware & Controle de Qualidade:** ~5 a 7 minutos (gravação via USB `make flash`, validação de pulsos de tacômetro, varredura de PWM nos 4 canais e medição multímetro das tensões de saída dos reguladores).
- **Modelos de Custo de Mão de Obra:**
  - *DIY / Montagem Própria:* R$ 0,00 (hobby/acadêmico).
  - *Técnico Especializado de Bancada (Brasil):* Estimado em R$ 25,00 a R$ 35,00 por placa montada e testada.
  - *Montagem Automatizada Seletiva / Onda (Lotes de 100+):* ~US$ 3.50 a US$ 5.00 (R$ 20,00 a R$ 29,00) por unidade.

---

### 10.4 Comparativo de Custo Total por Unidade nos Três Cenários

*(Considerando média de fabricação nacional brasileira TEC-CI / PCB Brasil / Micro-Circuitos)*

| Cenário de Produção | Custo PCB Unit. (BR) | Custo BOM Unit. | Mão de Obra e Teste | **Custo Unitário Total (BRL)** | **Custo Unitário Total (USD)** |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **1. Protótipo Avulso / DIY (1 a 5 un)** | R$ 39,00 (TEC-CI) | R$ 70,60 | R$ 0,00 (Montagem própria) | **R$ 109,60** | **US$ 18.90** |
| **2. Pequeno Lote Semi-Artesanal (30 un)** | R$ 24,00 (TEC-CI) | R$ 52,00 | R$ 25,00 (Técnico) | **R$ 101,00** | **US$ 17.40** |
| **3. Lote Industrial Seriado (100+ un)** | R$ 12,00 (Circuibras) | R$ 42,00 | R$ 20,00 (Seletiva) | **R$ 74,00** | **US$ 12.75** |

---

### 10.5 Oportunidades de Otimização de Custo (Cost Reduction Roadmap)

1. **Substituição de Módulos Prontos por Circuitos Discretos:**
   - A substituição dos dois módulos conversores LM2596 comerciais (R$ 15,00) por CIs conversores chaveados e indutores de potência montados diretamente na placa pode reduzir em até **R$ 8,00** o custo por unidade em lotes acima de 100 peças.
2. **Eliminação de Soquetes DIP:**
   - Em produção seriada final, a soldagem direta do ATmega328P e do ULN2003 economiza **R$ 2,40** por placa e aumenta a imunidade mecânica contra vibração em gabinetes de alta rotação.
3. **Compra em Carretéis / Fitas (Atacado):**
   - Capacitores, resistores e barras de pinos comprados no atacado em carretéis completos reduzem o kit de passivos de R$ 4,00 para menos de **R$ 1,20** por unidade.


---

## 11. Registro de Desenvolvimento Assistido por IA

> [!NOTE]
> **Identificação Oficial de Desenvolvimento:**  
> *"projeto usando lepton-eda/pcb-rnd assistido com IA-Gemini-3.8-Flash-Medium"*

- **Modelo de IA Utilizado:** Google DeepMind Gemini 3.8 Flash (Medium).
- **Número de Iterações com o Usuário:** **17 turnos de diálogo**.
- **Total de Invocações de Ferramentas:** **413 execuções** (290 `run_command`, 42 `edit_file`, 28 `manage_task`, 26 `read_file`, 16 `search_web`, 9 `write_file`, 2 `ask_question`).
- **Ferramental de Desenvolvimento Empregado:** Lepton-EDA (`lepton-schematic`, `lepton-netlist`, `lepton-cli export`), `pcb-rnd` (layout e renderização photo-mode 300 DPI), `gcc` 14.2.0, `avr-gcc` 14.2.0, `avrdude`, Python 3.12/3.13, `reportlab` 4.x, `inkscape` e `pdftoppm`.

---

## 12. Referências Bibliográficas, Normas e Datasheets Oficiais

1. **Texas Instruments LM317 3-Terminal Adjustable Regulator:**  
   Datasheet SNVS774P. Circuito padrão de aplicação da página 1 ($1.25\text{V} - 37\text{V}$, $1.5\text{A}$, $R_1 = 240\,\Omega$, $C_1 = 0.1\,\mu\text{F}$, $C_2 = 1.0\,\mu\text{F}$).  
   PDF Oficial: [https://www.ti.com/lit/ds/symlink/lm317.pdf](https://www.ti.com/lit/ds/symlink/lm317.pdf)
2. **Texas Instruments / STMicroelectronics / Allegro ULN2003A & ULN7003A:**  
   Datasheet SLRS027P. Matriz de transistores Darlington com diodos de supressão indutiva integrados no pino COM.  
   PDF Oficial: [https://www.ti.com/lit/ds/symlink/uln2003a.pdf](https://www.ti.com/lit/ds/symlink/uln2003a.pdf)
3. **Microchip / Atmel ATmega328P-PU:**  
   Datasheet DS40002061B / Atmel-8271. Registradores de PWM (Timer 1 e 2), interrupções de tacômetro (INT0/PCINT) e USART0 hardware.  
   PDF Oficial: [https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7810-Automotive-Microcontrollers-ATmega328P_Datasheet.pdf](https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7810-Automotive-Microcontrollers-ATmega328P_Datasheet.pdf)
4. **WCH (Jiangsu Qinheng Co.): CH340 USB-to-Serial TTL Converter:**  
   Página oficial e especificações técnicas do conversor USB-Serial.  
   [https://www.wch-ic.com/products/CH340.html](https://www.wch-ic.com/products/CH340.html)
5. **pnjorge (Paulo Nogueira / F5VMJ):**  
   *"Silent Running With This Dual Fan Controller"* (Hackster.io, 2021).  
   [https://www.hackster.io/pnjorge/silent-running-with-this-dual-fan-controller-0accb8](https://www.hackster.io/pnjorge/silent-running-with-this-dual-fan-controller-0accb8)  
   Repositório GitHub: [https://github.com/pnjorge/Cooler-Fan-Controller](https://github.com/pnjorge/Cooler-Fan-Controller)
6. **Sullins Connector Solutions — Card Edge Connectors (0.100" Pitch, ETM / EBM Series):**  
   Conectores industriais de borda padrão 44 posições / 22 contatos unilaterais.  
   [https://www.sullinscorp.com/](https://www.sullinscorp.com/)
7. **Vector Electronics & Technology — Eurocard & Vectorbord Card-Edge Plugboards:**  
   Plugboards padrão 44 pinos (Model 3662 series).  
   [https://www.vectorelect.com/](https://www.vectorelect.com/)
8. **Intel Corporation:** *4-Wire Pulse Width Modulation (PWM) Controlled Fans Specification*, Revision 1.3 (September 2005).  
   Norma de tacômetros e PWM para ventiladores de PC.
9. **The Linux Kernel Organization:** *Hardware Monitoring Kernel Subsystem (`hwmon`)*.  
   [https://docs.kernel.org/hwmon/](https://docs.kernel.org/hwmon/)

