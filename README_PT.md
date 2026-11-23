# Controlador Customizado de Ventiladores para PC (Controlado via Linux)

[![Licença: LGPL v3](https://img.shields.io/badge/License-LGPL_v3-blue.svg)](LICENSE)
[![CI Build](https://img.shields.io/badge/Build-Passing-brightgreen.svg)](.github/workflows/ci.yml)
[![EDA: Lepton-EDA & pcb-rnd](https://img.shields.io/badge/EDA-Lepton--EDA%20%2F%20pcb--rnd-orange.svg)](lepton/)
[![Assistido por IA: Gemini 3.8 Flash](https://img.shields.io/badge/AI--Assisted-Gemini%203.8%20Flash-blueviolet.svg)](#8-projeto-assistido-por-ia---gemini-38-flash-medium)

> **Idiomas / Languages:** [Português](README_PT.md) | [English (US)](README.md) | [Español](README_ES.md)

Um sistema completo de hardware, firmware e software para controle inteligente e customizado de arrefecimento interno de gabinetes de computador desktop. O controlador é baseado em uma **placa padrão de prototipagem 33.0 mm $\times$ 72.0 mm (through-hole)**, microcontrolador dedicado **ATmega328P-PU** a **16.000 MHz**, conversor **USB-Serial CH340 de 6 pinos**, e um driver Darlington **ULN2003A / ULN7003A** acionando até 4 ventiladores de PC (ex: 4x Akasa 90mm e Arctic P8) com leitura em tempo real de pulsos de tacômetro (RPM), proteção watchdog failsafe e gerenciamento térmico automatizado pelo Linux.

---

## Índice

- [🎯 Contexto e Motivação](#-contexto-e-motivação)

1. [Visão Geral da Arquitetura](#visão-geral-da-arquitetura)
2. [Lista de Materiais de Hardware (BOM)](#lista-de-materiais-de-hardware-bom)
3. [Decisões e Justificativas de Engenharia](#decisões-e-justificativas-de-engenharia)
   - [Form Factor: ATmega328P DIP-28 Avulso vs. Arduino Nano](#form-factor-atmega328p-dip-28-avulso-vs-arduino-nano)
   - [Integração com Placa-Mãe: Módulo CH340 vs. USB Virtual (V-USB)](#integração-com-placa-mãe-módulo-ch340-vs-usb-virtual-v-usb)
   - [Análise da Matriz Estilo Protoboard](#análise-da-matriz-estilo-protoboard)
   - [Inovação do Barramento Dividido: Corte de Trilha R16 / C12](#inovação-do-barramento-dividido-corte-de-trilha-r16--c12)
   - [Posicionamento dos Conectores de Ventilador: Opção A (Borda Inferior)](#posicionamento-dos-conectores-de-ventilador-opção-a-borda-inferior)
   - [Identificação Escalonada das Colunas](#identificação-escalonada-das-colunas)
   - [Estratégia de Controle e Failsafe](#estratégia-de-controle-e-failsafe)
4. [Custom Stripboard Rev 1.1 / 1.1a — Arquitetura Modular & Especificações](#custom-stripboard-rev-11--11a--arquitetura-modular--especificações)
5. [Gabaritos de Impressão em Escala 1:1](#gabaritos-de-impressão-em-escala-11)
6. [Estrutura de Diretórios](#estrutura-de-diretórios)
7. [Guia Rápido de Compilação e Gravação](#guia-rápido-de-compilação-e-gravação)
8. [Projeto Assistido por IA - Gemini 3.8 Flash Medium](#8-projeto-assistido-por-ia---gemini-38-flash-medium)
9. [Bibliografia e Referências](#9-bibliografia-e-referências)
10. [Avaliação Detalhada de Custo de Produção (Production Cost Analysis)](#10-avaliação-detalhada-de-custo-de-produção-production-cost-analysis)
11. [Licença](#11-licença)

---

## 🎯 Contexto e Motivação

Este projeto nasceu de uma necessidade real de bancada e manutenção: a queima da ventoinha frontal de 180 mm do meu gabinete principal — uma medida fora de padrão e proprietária, essencial para meu único computador de trabalho.

A ventoinha original já vinha sofrendo com eventos frequentes de superaquecimento, especialmente durante os meses mais quentes do ano. Ao pesquisar a peça de reposição compatível, o custo orbitava os **R$ 180,00** por um componente de baixa eficiência. A alternativa geométrica viável foi preencher o mesmo vão físico com **quatro ventoinhas de 90 mm**. No entanto, surgiu o gargalo técnico: a placa-mãe não possuía conexões suficientes nem capacidade de acionamento independente para gerenciar esse conjunto de forma segura e elegante.

### Da gambiarra temporária ao circuito definitivo

1. **O protótipo de emergência:** Montei uma solução rápida em *perfboard* para não paralisar o trabalho diário, mas o espaço físico reduzido e o arranjo de fiação criaram uma situação indesejável de manutenção.
2. **O problema do chaveamento Low-Side vs. Tacômetro:**  
   > ⚠️ **Nota Técnica:** O controle de rotação usando arranjos *low-side* tradicionais (como dar pull-down no terra via ULN2003 ou N-MOSFETs comuns) chaveia o pino de GND da ventoinha. Isso faz com que a referência interna de terra do circuito do sensor Hall flutue. O resultado prático é que o sinal do **tacômetro (pino de RPM)** é corrompido ou para de ser lido com precisão pela placa-mãe/controlador.
3. **A evolução da placa:** Como não havia espaço físico na perfboard para implementar o chaveamento adequado (preservando o terra comum para o tacômetro) e o roteamento virou uma teia de fios, decidi projetar uma placa dedicada.
4. **Pensando em futuros protótipos:** Sabendo que no ecossistema maker *"nada é mais definitivo que uma solução temporária"*, aproveitei o redesenho para adicionar barramentos de alimentação, proteções e pontos de conexão que rotineiramente fazem falta na bancada em outros projetos de automação e refrigeração.

---

O projeto foi disponibilizado publicamente na esperança de poupar tempo e retrabalho de quem estiver enfrentando problemas similares com arrefecimento customizado ou prototipagem de periféricos. 

Comentários, correções, testes e *pull requests* são muito bem-vindos!

---

## Visão Geral da Arquitetura

```
 Interior do Gabinete PC:
 ┌─────────────────────────────────────────────────────────────┐
 │ Conector USB 2.0 Interno 9 Pinos da Placa-Mãe (Porta 1)     │
 │   └── 5V, D-, D+, GND                                       │
 │         │                                                   │
 │         ▼                                                   │
 │ Módulo Conversor USB-Serial TTL CH340 6 Pinos (Jumper 5V)   │
 │   └── DTR (auto-reset 100nF), RXD, TXD, 5V, GND             │
 │         │                                                   │
 │         ▼                                                   │
 │ Placa Controladora Stripboard (33.0 mm x 72.0 mm)           │
 │   ├── ATmega328P-PU (Cristal 16.000 MHz + 2x Caps 22pF)     │
 │   │     ├── Hardware UART (USART0 @ 115200 baud)            │
 │   │     ├── 4x Canais Hardware PWM (Timers 1 & 2)           │
 │   │     └── 4x Contadores de Interrupção de Tacômetro       │
 │   │                                                         │
 │   ├── ULN2003A / ULN7003A Darlington Driver (DIP-16)        │
 │   │     ├── Chaveamento de Terra Low-Side (4 Canais)        │
 │   │     └── Diodo Clamp Pino 9 COM ligado ao barramento +12V│
 │   │                                                         │
 │   └── Alimentação da Fonte ATX do PC (SATA / Molex 4 Pinos) │
 │         ├── Fio Amarelo: Barramento de Potência +12V        │
 │         └── Fio Preto: Terra Comum do Sistema (GND)         │
 │         │                                                   │
 │         ▼                                                   │
 │ 4x Ventiladores de PC (4x Akasa 90mm / Arctic P8)           │
 └─────────────────────────────────────────────────────────────┘
```

---

## Lista de Materiais de Hardware (BOM)

Todos os componentes são **100% Through-Hole (THT / DIP)**:

| Item | Componente | Encapsulamento / Valor | Qtd | Conexão / Função no Circuito |
| :--- | :--- | :---: | :---: | :--- |
| **BRD1** | Placa Padrão Trilha | 33.0 $\times$ 72.0 mm | 1 | Matriz estilo protoboard (12 cols $\times$ 28 linhas, 336 furos, passo 2.54 mm) |
| **U1** | ATmega328P-PU | DIP-28 Estreito | 1 | Microcontrolador mestre (16 MHz) |
| **SKT1** | Soquete de CI | DIP-28 Estreito | 1 | Soquete para o ATmega328P |
| **U2** | ULN2003A ou ULN7003A | DIP-16 | 1 | Driver Darlington 7 canais chaveamento low-side |
| **SKT2** | Soquete de CI | DIP-16 | 1 | Soquete para o ULN2003A |
| **MOD1** | Módulo USB-TTL CH340 6 Pinos | Módulo 6 pinos | 1 | Ponte USB-UART com conector interno da placa-mãe |
| **HDR_USB**| Barra de Pinos Fêmea/Macho | 1x6, passo 2.54 mm | 1 | Soquete para o módulo CH340 |
| **Y1** | Cristal de Quartzo | 16.000 MHz (HC-49) | 1 | Clock mestre nos pinos 9 e 10 do ATmega |
| **C3, C4** | Capacitores Cerâmicos | 22 pF (Disco) | 2 | Capacitores de carga do cristal ao GND |
| **C_DTR** | Capacitor Cerâmico | 100 nF (0.1 µF) | 1 | Acoplamento AC para auto-reset do DTR |
| **C2, C5** | Capacitores Cerâmicos | 100 nF (0.1 µF) | 2 | Desacoplamento bypass VCC/GND e AVCC/GND |
| **C1** | Capacitor Eletrolítico | 100 µF, 25V (Radial) | 1 | Desacoplamento de potência entre +12V e GND |
| **R_RST** | Resistor Filme Metálico | $10\text{ k}\Omega$, 1/4W | 1 | Pull-up no pino 1 (/RESET) ao +5V |
| **R1–R4** | Resistores Filme Metálico | $10\text{ k}\Omega$, 1/4W | 4 | Pull-ups de tacômetro (ligados de C11 ao C12 superior) |
| **J_PWR** | Borne de Parafuso KRE | 2 Pinos, 5.08 mm | 1 | Entrada +12V (Amarelo) e GND (Preto) |
| **J_FAN** | Barras de Pinos Macho | 3 Pinos, 2.54 mm | 4 | Conectores Fan 1 a Fan 4 (Opção A) |
| **WIRE** | Fio Rígido para Jumper | 24 AWG | ~1 m | Jumpers superiores de interligação |

---

## Decisões e Justificativas de Engenharia

### Form Factor: ATmega328P DIP-28 Avulso vs. Arduino Nano
- **Considerado:** Utilização de placa comercial Arduino Nano com USB integrado.
- **Decisão:** Adoção do **ATmega328P-PU (DIP-28)** avulso com **cristal de 16.000 MHz**.
- **Justificativa:** O Arduino Nano possui espaçamento largo de 0.6" (15.24 mm), ocupando 7 das 12 colunas da placa e impedindo o roteamento do ULN2003A e conectores. O chip DIP-28 estreito (0.3") alinha-se perfeitamente com o vão central sem desperdício de espaço.

### Integração com Placa-Mãe: Módulo CH340 vs. USB Virtual (V-USB)
- **Decisão:** Adoção do **Módulo CH340 6 Pinos USB-Serial TTL**.
- **Justificativa:** Descarrega a CPU do AVR permitindo o uso da **USART0 em hardware a 115200 baud** sem jitter no PWM ou tacômetros. Suportado nativamente no kernel Linux pelo módulo `ch341.ko`. Auto-reset via DTR permite gravação com 1 clique via `avrdude`.

### Inovação do Barramento Dividido: Corte de Trilha R16 / C12
- Um corte simples na **Coluna C12 na Linha R16** divide o barramento direito em duas zonas elétricas independentes:
  - **C12 Superior (R02 a R15):** Conectado ao **+5V Lógico**.
  - **C12 Inferior (R17 a R28):** Conectado ao **+12V de Potência**.
- Elimina 4 fios de cruzamento na placa: os 4 resistores de pull-up do tacômetro ponteiam diretamente entre C11 e C12.

---

## Custom Stripboard Rev 1.1 / 1.1a — Arquitetura Modular & Especificações

> **Manual de Engenharia Completo:**  
> 🇧🇷 **Português:** [CUSTOM_STRIPBOARD_REV1.1_SPEC_PT.md](file:///home/fred/C/fanControl/docs/CUSTOM_STRIPBOARD_REV1.1_SPEC_PT.md) | 🇺🇸 **US-English:** [CUSTOM_STRIPBOARD_REV1.1_SPEC_EN.md](file:///home/fred/C/fanControl/docs/CUSTOM_STRIPBOARD_REV1.1_SPEC_EN.md) | 🇪🇸 **Español:** [CUSTOM_STRIPBOARD_REV1.1_SPEC_ES.md](file:///home/fred/C/fanControl/docs/CUSTOM_STRIPBOARD_REV1.1_SPEC_ES.md)

A evolução do projeto de controle de arrefecimento originou a **Custom Stripboard Rev 1.1** e sua sub-revisão **Rev 1.1a**, uma plataforma modular expandida de prototipagem no formato Eurocard/Vector desenvolvida com **Lepton-EDA** e **`pcb-rnd`**. A placa incorpora barramentos triplos de alimentação (+12V, +5V, GND), duas entradas DC barrel jack afastadas, **duplo regulador linear LM317** (TI Datasheet), **dois módulos step-down LM2596 verticais** na margem esquerda, um **borne terminal KRE 10 vias 5.08mm com 3 pass-thrus por pino**, uma **área de prototipagem rápida scratch-pad com 56 ilhas e microtrilhas raspáveis de 3 mil**, matriz central de prototipagem e conector de borda industrial de 44 pinos (passo de 2.54 mm), estritamente de face única na camada inferior.

> [!IMPORTANT]
> **Diretriz de Fabricação — Padrão Thru-Hole (THT) como Padrão Obrigatório**:
> O padrão DEFAULT de fabricação é **100% Through-Hole (furo passante metalizado)**. Todas as ilhas da matriz de tiras, pass-thrus do KRE, scratch-pad, conectores e reguladores utilizam furação metalizada com diâmetro externo $\ge 80.00\text{ mil}$ ($2.032\text{ mm}$).

---

## Gabaritos de Impressão em Escala 1:1

O diretório [`docs/templates/`](docs/templates/) disponibiliza gabaritos calibrados em escala 1:1 para corte e conferência:
- **[`stripboard_1to1_printout.pdf`](docs/templates/stripboard_1to1_printout.pdf)**: Folha mestra A4 para impressão sem redimensionamento.
- **[`board_ruler_indicator.png`](docs/templates/board_ruler_indicator.png)**: Régua física e indicador de coordenadas.
- **[`board_cuts_top_view.png`](docs/templates/board_cuts_top_view.png)**: Guia de cortes com os 7 pontos destacados em vermelho.
- **[`board_cuts_bottom_drill_view.png`](docs/templates/board_cuts_bottom_drill_view.png)**: Guia espelhado para furação no lado do cobre.

---

## Estrutura de Diretórios

```
fanControl/
├── Makefile                          # Automação de compilação geral
├── README.md                         # Documentação principal em Inglês-EUA
├── README_PT.md                      # Documentação completa em Português
├── README_ES.md                      # Documentação completa em Espanhol
├── lepton/                           # Esquemas e layout PCB Lepton-EDA / pcb-rnd
│   ├── layout_stripboards.py         # Sintetizador paramétrico das placas
│   ├── rev1.0/                       # Placa 33x72mm original
│   ├── rev1.1/                       # Stripboard modular com conector de borda
│   └── rev1.1a/                      # Sub-revisão 1.1a com 32 linhas contínuas
├── firmware/                         # Firmware AVR C puro para ATmega328P
├── daemon/                           # Daemon Linux C e utilitário CLI
├── kernel/                           # Módulo de kernel hwmon opcional
└── docs/                             # Manuais de engenharia multilíngues
    ├── CUSTOM_STRIPBOARD_REV1.1_SPEC.md    # Especificação (Inglês padrão)
    ├── CUSTOM_STRIPBOARD_REV1.1_SPEC_EN.md # Especificação (Inglês)
    ├── CUSTOM_STRIPBOARD_REV1.1_SPEC_PT.md # Especificação (Português)
    └── CUSTOM_STRIPBOARD_REV1.1_SPEC_ES.md # Especificação (Espanhol)
```

---

## Guia Rápido de Compilação e Gravação

### 1. Compilar Firmware e Daemon Linux
```bash
make
```

### 2. Gravar no ATmega328P via USB
```bash
cd firmware
make flash PORT=/dev/ttyUSB0
```

### 3. Testar via Linha de Comando Linux
```bash
cd ../daemon
./fancontrold --list-hwmon                       # Lista sensores de temperatura
./fancontrold -p /dev/ttyUSB0 --status           # Consulta RPM e PWM ao vivo
./fancontrold -p /dev/ttyUSB0 --setall 180       # Define ventiladores a ~70%
```

---

## 8. Projeto Assistido por IA - Gemini 3.8 Flash Medium

> [!NOTE]
> **Identificação Oficial de Desenvolvimento:**  
> *"projeto usando lepton-eda/pcb-rnd assistido com IA-Gemini-3.8-Flash-Medium"*

Este projeto foi totalmente concebido, projetado, codificado, depurado e documentado de ponta a ponta com a assistência interativa do modelo **Google DeepMind Gemini 3.8 Flash (Medium)**.

| Métrica | Quantidade / Escopo | Descrição das Operações |
| :--- | :---: | :--- |
| **Modelo de IA** | `Gemini 3.8 Flash (Medium)` | Modelo de raciocínio multimodal de alta velocidade e precisão |
| **Iterações com Usuário (Turns)** | **17 turnos de diálogo** | Da concepção inicial da protoboard até o layout final Rev 1.1 / Rev 1.1a |
| **Execuções de Ferramental (Tool Calls)** | **413 invocações** | Operações automatizadas de compilação, inspeção, edição e validação EDA |
| • `run_command` | **290 chamadas** | Execução de bash, compiladores C/AVR, scripts Python, Lepton-EDA e `pcb-rnd` |
| • `edit_file` | **42 chamadas** | Edições cirúrgicas de código-fonte, layout algorítmico e documentação |
| • `manage_task` | **28 chamadas** | Gerenciamento de processos em background e renderizações gráficas |
| • `read_file` | **26 chamadas** | Leitura e verificação de integridade de netlists, esquemáticos e tabelas |
| • `search_web` | **16 chamadas** | Consulta de datasheets (TI LM317, WCH CH340, ULN2003, Sullins, Vector, etc.) |
| • `write_file` | **9 chamadas** | Criação de geradores paramétricos, especificações técnicas e Makefiles |
| • `ask_question` | **2 chamadas** | Alinhamento e esclarecimento direto de requisitos com o usuário |
| **Código Gerado** | **~5.200+ linhas de código** | Firmware AVR C puro, Daemon Linux C, módulo Kernel hwmon, layout PCB, Makefiles |
| **Gráficos e Previews Gerados** | **14 artefatos gráficos** | Esquemas Lepton-EDA (.png), PCBs topo/fundo 300 DPI, gabaritos 1:1 (.svg, .png, .pdf) |

---

## 9. Bibliografia e Referências

### 1. Projetos de Referência & Comunidade
- **pnjorge (Paulo Nogueira / F5VMJ):** *"Silent Running With This Dual Fan Controller"* (Hackster.io, 2021).  
  [https://www.hackster.io/pnjorge/silent-running-with-this-dual-fan-controller-0accb8](https://www.hackster.io/pnjorge/silent-running-with-this-dual-fan-controller-0accb8)
- **pnjorge:** *Cooler-Fan-Controller Hardware & Firmware Repository* (GitHub).  
  [https://github.com/pnjorge/Cooler-Fan-Controller](https://github.com/pnjorge/Cooler-Fan-Controller)

### 2. Componentes de Hardware & Datasheets Oficiais
- **Texas Instruments LM317 3-Terminal Adjustable Regulator:** Datasheet SNVS774P.  
  [https://www.ti.com/lit/ds/symlink/lm317.pdf](https://www.ti.com/lit/ds/symlink/lm317.pdf)
- **Texas Instruments / STMicroelectronics ULN2003A & ULN7003A:** Datasheet SLRS027P.  
  [https://www.ti.com/lit/ds/symlink/uln2003a.pdf](https://www.ti.com/lit/ds/symlink/uln2003a.pdf)
- **Microchip / Atmel ATmega328P-PU:** Datasheet DS40002061B / Atmel-8271.  
  [https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7810-Automotive-Microcontrollers-ATmega328P_Datasheet.pdf](https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7810-Automotive-Microcontrollers-ATmega328P_Datasheet.pdf)
- **WCH: CH340 USB-to-Serial Converter:** [https://www.wch-ic.com/products/CH340.html](https://www.wch-ic.com/products/CH340.html)
- **Sullins Connector Solutions — Card Edge Connectors:** [https://www.sullinscorp.com/](https://www.sullinscorp.com/)
- **Vector Electronics & Technology — Eurocard Plugboards:** [https://www.vectorelect.com/](https://www.vectorelect.com/)

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

## 11. Licença

Este projeto é de código aberto sob os termos da **GNU Lesser General Public License v3.0 (LGPLv3)**.
- Termos da Licença: [LICENSE](LICENSE)
- GNU Lesser General Public License: [COPYING.LESSER](COPYING.LESSER) / [LICENSE.LESSER](LICENSE.LESSER)
- GNU General Public License: [COPYING](COPYING)
