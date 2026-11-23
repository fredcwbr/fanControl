# Custom Stripboard Rev 1.1 & Rev 1.1a — Especificação Técnica Completa e Manual de Engenharia

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

Apresentamos a análise quantitativa e qualitativa de custo para produção da **Custom Stripboard Rev 1.1 / Rev 1.1a**, abrangendo a fabricação de circuito impresso (PCB), lista completa de materiais (BOM), montagem, soldagem, controle de qualidade e três cenários de escala.

### 10.1 Custos de Fabricação do PCB (Placa Virgem FR4)

- **Parâmetros Técnicos do PCB:**
  - Dimensões: $88.90\text{ mm} \times 128.27\text{ mm}$ ($3.5'' \times 5.05''$).
  - Camadas: 2 Camadas (Top / Bottom, com roteamento single-sided na camada inferior).
  - Material: FR4 padrão (Tg 130–140°C), espessura $1.60\text{ mm}$, cobre 1 oz ($35\,\mu\text{m}$).
  - Acabamento de Superfície: HASL Lead-Free (ou ENIG / Ouro Químico recomendado para longevidade dos dedos de borda).
  - Borda / Lingueta: Chanfro de inserção a $45^\circ$ (*Gold Finger Chamfering / Beveling*).

| Lote / Quantidade | Custo Fabricações (Ex: JLCPCB / PCBWay) | Frete + Impostos (BR) | Custo Unitário do PCB (USD) | Custo Unitário do PCB (BRL R$) |
| :---: | :---: | :---: | :---: | :---: |
| **Protótipo (5 placas)** | US\$ 4.00 (base) + US\$ 6.00 (chanfro) | US\$ 14.00 | **US\$ 4.80** | **R\$ 28,00** |
| **Pequeno Lote (30 placas)** | US\$ 28.00 + US\$ 10.00 (chanfro) | US\$ 22.00 | **US\$ 2.00** | **R\$ 11,60** |
| **Lote Médio (100 placas)** | US\$ 75.00 + US\$ 15.00 (ENIG/chanfro) | US\$ 35.00 | **US\$ 1.25** | **R\$ 7,25** |

---

### 10.2 Lista Completa de Materiais (Bill of Materials - BOM) por Placa

Todos os componentes são **Through-Hole (THT / DIP)** conforme a diretriz de fabricação:

| Item | Componente / Especificação | Qtd | Preço Unit. (USD) | Preço Unit. (BRL R$) | Custo Total (BRL R$) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **U1** | ATmega328P-PU (DIP-28 Estreito) | 1 | US\$ 2.20 | R\$ 12,80 | R\$ 12,80 |
| **SKT1** | Soquete DIP-28 Estampado / Torneado | 1 | US\$ 0.25 | R\$ 1,50 | R\$ 1,50 |
| **U2** | ULN2003A ou ULN7003A (DIP-16) | 1 | US\$ 0.40 | R\$ 2,30 | R\$ 2,30 |
| **SKT2** | Soquete DIP-16 | 1 | US\$ 0.15 | R\$ 0,90 | R\$ 0,90 |
| **MOD1** | Módulo Conversor USB-Serial TTL CH340 (6 pinos) | 1 | US\$ 1.20 | R\$ 7,00 | R\$ 7,00 |
| **Y1** | Cristal de Quartzo 16.000 MHz HC-49S | 1 | US\$ 0.18 | R\$ 1,00 | R\$ 1,00 |
| **C3, C4** | Capacitores Cerâmicos 22 pF (disco) | 2 | US\$ 0.05 | R\$ 0,30 | R\$ 0,60 |
| **U101, U102** | CI Regulador LM317T (TO-220 Upright) | 2 | US\$ 0.40 | R\$ 2,30 | R\$ 4,60 |
| **VR101, VR102**| Módulos Step-Down LM2596 DC-DC (Upright) | 2 | US\$ 1.30 | R\$ 7,50 | R\$ 15,00 |
| **TB101** | Conector Borne KRE 10 Vias 5.08mm (ZB128 14mm) | 1 | US\$ 1.10 | R\$ 6,40 | R\$ 6,40 |
| **CONN117, 118**| Conector Jack DC Fêmea 2.1 $\times$ 5.5mm THT | 2 | US\$ 0.25 | R\$ 1,45 | R\$ 2,90 |
| **HDR_SANDWICH**| Conectores Barra de Pinos 2.54mm (Macho + Fêmea) | 2 barras | US\$ 0.60 | R\$ 3,50 | R\$ 7,00 |
| **PASSIVOS** | Caps 100nF, 1uF, 100uF + Resistores 1/4W (conjunto) | 1 kit | US\$ 0.70 | R\$ 4,00 | R\$ 4,00 |
| **MECÂNICA** | Parafusos, porcas e espaçadores M3 de nylon/latão | 6 kits | US\$ 0.80 | R\$ 4,60 | R\$ 4,60 |
| **TOTAL BOM** | **Soma dos Componentes Eletrônicos por Unidade** | — | **US\$ 9.58** | **R\$ 55,85** | **R\$ 70,60 (c/ margem)** |

---

### 10.3 Custos de Montagem, Soldagem e Testes Funcionais

- **Tempo Médio de Montagem Manual (Through-Hole):** ~25 a 35 minutos por placa.
- **Gravação de Firmware & Teste Funcional:** ~5 a 7 minutos (`make flash`, leitura de tacômetros, acionamento PWM nos 4 canais e conferência de tensões).
- **Custo de Mão de Obra Técnica:**
  - *DIY / Montagem Própria:* R\$ 0,00 (hobby/estudo).
  - *Técnico Especializado (Brasil):* R\$ 25,00 a R\$ 40,00 por placa montada e testada.
  - *Montagem Industrial em Lote (100+ un):* ~US\$ 5.00 a US\$ 8.00 (R\$ 29,00 a R\$ 46,00) por unidade.

---

### 10.4 Comparativo de Custo Total por Unidade nos Três Cenários

*(Taxa de câmbio referencial US\$ 1.00 = R\$ 5,80)*

| Cenário de Produção | Custo PCB Unit. | Custo BOM Unit. | Mão de Obra / Teste | **Custo Unitário Total (BRL)** | **Custo Unitário Total (USD)** |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **1. Protótipo Avulso / DIY (1 a 5 un)** | R\$ 28,00 | R\$ 70,60 | R\$ 0,00 (DIY) | **R\$ 98,60** | **US\$ 17.00** |
| **2. Pequeno Lote Semi-Artesanal (30 un)** | R\$ 11,60 | R\$ 52,00 | R\$ 25,00 (montagem) | **R\$ 88,60** | **US\$ 15.30** |
| **3. Lote Industrial (100+ un)** | R\$ 7,25 | R\$ 42,00 | R\$ 20,00 (lote) | **R\$ 69,25** | **US\$ 11.95** |

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

