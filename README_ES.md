# Controlador Personalizado de Ventiladores para PC (Controlado vía Linux)

[![Licencia: LGPL v3](https://img.shields.io/badge/License-LGPL_v3-blue.svg)](LICENSE)
[![CI Build](https://img.shields.io/badge/Build-Passing-brightgreen.svg)](.github/workflows/ci.yml)
[![EDA: Lepton-EDA & pcb-rnd](https://img.shields.io/badge/EDA-Lepton--EDA%20%2F%20pcb--rnd-orange.svg)](lepton/)
[![Asistido por IA: Gemini 3.8 Flash](https://img.shields.io/badge/AI--Assisted-Gemini%203.8%20Flash-blueviolet.svg)](#8-proyecto-asistido-por-ia---gemini-38-flash-medium)

> **Idiomas / Languages:** [Español](README_ES.md) | [English (US)](README.md) | [Português](README_PT.md)

Un sistema completo de hardware, firmware y software para el control térmico inteligente de ventiladores dentro de un gabinete de PC. El controlador está construido sobre una **placa de prototipado estándar de 33.0 mm $\times$ 72.0 mm (through-hole)**, microcontrolador autónomo **ATmega328P-PU** a **16.000 MHz**, conversor **USB-Serial CH340 de 6 pines**, y un arreglo Darlington **ULN2003A / ULN7003A** que comanda hasta 4 ventiladores de PC (ej: 4x Akasa 90mm y Arctic P8) con lectura de pulsos de tacómetro (RPM) en tiempo real, protección watchdog failsafe y gestión térmica automatizada desde Linux.

---

## Tabla de Contenidos

- [🎯 Contexto y Motivación](#-contexto-y-motivación)

1. [Visión General de la Arquitectura](#visión-general-de-la-arquitectura)
2. [Lista de Materiales de Hardware (BOM)](#lista-de-materiales-de-hardware-bom)
3. [Decisiones y Justificaciones de Ingeniería](#decisiones-y-justificaciones-de-ingeniería)
4. [Custom Stripboard Rev 1.1 / 1.1a — Arquitectura Modular y Especificaciones](#custom-stripboard-rev-11--11a--arquitectura-modular-y-especificaciones)
5. [Plantillas Imprimibles en Escala 1:1](#plantillas-imprimibles-en-escala-11)
6. [Estructura de Directorios](#estructura-de-directorios)
7. [Guía Rápida de Compilación y Grabación](#guía-rápida-de-compilación-y-grabación)
8. [Proyecto Asistido por IA - Gemini 3.8 Flash Medium](#8-proyecto-asistido-por-ia---gemini-38-flash-medium)
9. [Bibliografía y Referencias](#9-bibliografía-y-referencias)
10. [Evaluación Detallada de Costos de Producción (Production Cost Analysis)](#10-evaluación-detallada-de-costos-de-producción-production-cost-analysis)
11. [Licencia](#11-licencia)

---

## 🎯 Contexto y Motivación

Este proyecto nació de una necesidad real de banco de trabajo y mantenimiento: la falla del ventilador frontal de 180 mm de mi gabinete principal — una medida propietaria y fuera de estándar, indispensable para mantener operativa mi única computadora de trabajo.

El ventilador original ya venía sufriendo frecuentes episodios de sobrecalentamiento, especialmente durante los meses más calurosos del año. Al buscar el repuesto compatible, el costo rondaba los **R$ 180,00 (~$31 USD)** por un componente de baja eficiencia. La alternativa geométrica viable consistió en ocupar el mismo espacio físico con **cuatro ventiladores de 90 mm**. Sin embargo, surgió de inmediato el obstáculo técnico: la placa base no disponía de suficientes conectores ni de la capacidad de control independiente para gestionar este conjunto de forma segura y prolija.

### De la solución improvisada al circuito definitivo

1. **El prototipo de emergencia:** Armé una solución rápida en placa perforada (*perfboard*) para no interrumpir el trabajo diario, pero el espacio reducido y el cableado aéreo crearon una situación indeseable para el mantenimiento.
2. **El dilema de la conmutación Low-Side vs. Tacómetro:**  
   > ⚠️ **Nota Técnica:** El control de velocidad mediante configuraciones *low-side* tradicionales (conmutando la masa a través de un ULN2003 o transistores N-MOSFET) corta el pin GND del ventilador. Esto hace que la referencia interna de masa del sensor Hall del ventilador quede flotante. Como resultado práctico, la señal del **tacómetro (pin de RPM)** se corrompe o deja de leerse con precisión en el microcontrolador o placa madre.
3. **Evolución a una placa dedicada:** Dado que no había espacio físico en la perfboard para implementar el filtrado adecuado (preservando una masa común sólida para el tacómetro) y el ruteo se convirtió en una maraña de cables, decidí diseñar una placa de circuito impreso dedicada.
4. **Pensando en futuros prototipos:** Sabiendo que en la cultura maker *"no hay nada más definitivo que una solución temporal"*, aproveché el rediseño para integrar rieles de alimentación, diodos de protección y puntos de prueba que habitualmente se echan en falta en el banco de trabajo para otros proyectos de automatización y refrigeración.

---

El proyecto se publica de forma abierta con la esperanza de ahorrar tiempo y esfuerzo a quienes enfrenten desafíos similares en refrigeración personalizada o prototipado de periféricos.

¡Comentarios, correcciones, pruebas y *pull requests* son muy bienvenidos!

---

## Visión General de la Arquitectura

```
 Interior del Gabinete PC:
 ┌─────────────────────────────────────────────────────────────┐
 │ Conector USB 2.0 Interno de 9 Pines de Placa Base (Puerto 1)│
 │   └── 5V, D-, D+, GND                                       │
 │         │                                                   │
 │         ▼                                                   │
 │ Módulo Conversor USB-Serial TTL CH340 de 6 Pines            │
 │   └── DTR (auto-reset 100nF), RXD, TXD, 5V, GND             │
 │         │                                                   │
 │         ▼                                                   │
 │ Placa Controladora Stripboard (33.0 mm x 72.0 mm)           │
 │   ├── ATmega328P-PU (Cristal 16.000 MHz + 2x Caps 22pF)     │
 │   │     ├── Hardware UART (USART0 @ 115200 baud)            │
 │   │     ├── 4x Canales Hardware PWM (Timers 1 & 2)          │
 │   │     └── 4x Contadores de Interrupción de Tacómetro      │
 │   │                                                         │
 │   ├── ULN2003A / ULN7003A Darlington Driver (DIP-16)        │
 │   │     ├── Conmutación Low-Side de Tierra (4 Canales)      │
 │   │     └── Diodo Clamp Pin 9 COM conectado al riel +12V   │
 │   │                                                         │
 │   └── Alimentación de la Fuente ATX del PC (SATA / Molex)   │
 │         ├── Cable Amarillo: Riel de Potencia +12V           │
 │         └── Cable Negro: Tierra Común del Sistema (GND)     │
 │         │                                                   │
 │         ▼                                                   │
 │ 4x Ventiladores de PC (4x Akasa 90mm / Arctic P8)           │
 └─────────────────────────────────────────────────────────────┘
```

---

## Lista de Materiales de Hardware (BOM)

Todos los componentes son **100% Through-Hole (THT / DIP)**:

| Item | Componente | Encapsulado / Valor | Cant | Conexión / Función en el Circuito |
| :--- | :--- | :---: | :---: | :--- |
| **BRD1** | Placa Estándar Stripboard | 33.0 $\times$ 72.0 mm | 1 | Matriz estilo protoboard (12 cols $\times$ 28 filas, 336 agujeros, paso 2.54 mm) |
| **U1** | ATmega328P-PU | DIP-28 Estrecho | 1 | Microcontrolador principal (16 MHz) |
| **SKT1** | Zócalo para CI | DIP-28 Estrecho | 1 | Zócalo para ATmega328P |
| **U2** | ULN2003A o ULN7003A | DIP-16 | 1 | Driver Darlington 7 canales conmutación low-side |
| **SKT2** | Zócalo para CI | DIP-16 | 1 | Zócalo para ULN2003A |
| **MOD1** | Módulo USB-TTL CH340 | Módulo 6 pines | 1 | Puente USB-UART con conector interno de la placa base |
| **Y1** | Cristal de Cuarzo | 16.000 MHz (HC-49) | 1 | Reloj maestro en pines 9 y 10 del ATmega |
| **C3, C4** | Condensadores Cerámicos | 22 pF (Disco) | 2 | Condensadores de carga del cristal a GND |
| **C_DTR** | Condensador Cerámico | 100 nF (0.1 µF) | 1 | Acoplamiento AC para auto-reset de DTR |
| **C2, C5** | Condensadores Cerámicos | 100 nF (0.1 µF) | 2 | Desacoplamiento bypass VCC/GND y AVCC/GND |
| **C1** | Condensador Electrolítico | 100 µF, 25V (Radial) | 1 | Desacoplamiento de potencia entre +12V y GND |
| **R_RST** | Resistencia Película Metálica | $10\text{ k}\Omega$, 1/4W | 1 | Pull-up en pin 1 (/RESET) a +5V |
| **R1–R4** | Resistencias Película Metálica | $10\text{ k}\Omega$, 1/4W | 4 | Pull-ups de tacómetro (conectados de C11 a C12 superior) |
| **J_PWR** | Bloque Terminal Tornillo | 2 Pines, 5.08 mm | 1 | Entrada +12V (Amarillo) y GND (Negro) |
| **J_FAN** | Tiras de Pines Macho | 3 Pines, 2.54 mm | 4 | Conectores Fan 1 a Fan 4 (Opción A) |

---

## Custom Stripboard Rev 1.1 / 1.1a — Arquitectura Modular y Especificaciones

> **Manual de Ingeniería Completo:**  
> 🇪🇸 **Español:** [CUSTOM_STRIPBOARD_REV1.1_SPEC_ES.md](file:///home/fred/C/fanControl/docs/CUSTOM_STRIPBOARD_REV1.1_SPEC_ES.md) | 🇺🇸 **US-English:** [CUSTOM_STRIPBOARD_REV1.1_SPEC_EN.md](file:///home/fred/C/fanControl/docs/CUSTOM_STRIPBOARD_REV1.1_SPEC_EN.md) | 🇧🇷 **Português:** [CUSTOM_STRIPBOARD_REV1.1_SPEC_PT.md](file:///home/fred/C/fanControl/docs/CUSTOM_STRIPBOARD_REV1.1_SPEC_PT.md)

La **Custom Stripboard Rev 1.1** y sub-revisión **Rev 1.1a** es una plataforma modular de prototipado en formato Eurocard/Vector diseñada con **Lepton-EDA** y **`pcb-rnd`**. Dispone de rieles triples de alimentación (+12V, +5V, GND), dos entradas jack DC, **doble regulador lineal LM317** (TI Datasheet), **dos módulos step-down LM2596 verticales**, **bloque de terminales KRE de 10 vías con matriz pass-thru**, **área scratch-pad con 56 pads y microtrazas raspables de 3 mil**, y conector de borde de 44 pines estrictamente en la cara inferior.

> [!IMPORTANT]
> **Directriz de Fabricación — Estándar Through-Hole (THT) Obligatorio**:
> El estándar DEFAULT de fabricación es **100% Through-Hole (orificio pasante metalizado)**. Todos los pads utilizan orificios metalizados con diámetro externo $\ge 80.00\text{ mil}$ ($2.032\text{ mm}$).

---

## Guía Rápida de Compilación y Grabación

```bash
# Compilar firmware y daemon Linux:
make

# Grabar firmware en el ATmega328P vía USB:
cd firmware && make flash PORT=/dev/ttyUSB0

# Consultar estado de ventiladores en Linux:
cd ../daemon && ./fancontrold -p /dev/ttyUSB0 --status
```

---

## 8. Proyecto Asistido por IA - Gemini 3.8 Flash Medium

> [!NOTE]
> **Identificación Oficial de Desarrollo:**  
> *"projeto usando lepton-eda/pcb-rnd assistido com IA-Gemini-3.8-Flash-Medium"*

Este proyecto fue concebido, diseñado, codificado, depurado y documentado de extremo a extremo con la asistencia interactiva y autónoma del modelo **Google DeepMind Gemini 3.8 Flash (Medium)**.

| Métrica | Cantidad / Alcance | Descripción de Operaciones |
| :--- | :---: | :--- |
| **Modelo de IA** | `Gemini 3.8 Flash (Medium)` | Modelo de razonamiento multimodal de alta velocidad y precisión |
| **Iteraciones con Usuario (Turns)** | **17 turnos de diálogo** | Desde el concepto inicial hasta el layout final Rev 1.1 / Rev 1.1a |
| **Ejecuciones de Herramientas (Tool Calls)** | **413 invocaciones** | Operaciones automatizadas de compilación, inspección, edición y validación EDA |
| • `run_command` | **290 llamadas** | Ejecución de bash, compiladores C/AVR, scripts Python, Lepton-EDA y `pcb-rnd` |
| • `edit_file` | **42 llamadas** | Ediciones quirúrgicas de código, layout algorítmico y documentación |
| • `manage_task` | **28 chamadas** | Gestión de procesos en segundo plano y renderizado gráfico pesado |
| • `read_file` | **26 llamadas** | Lectura y verificación de integridad de netlists, esquemáticos y tablas |
| • `search_web` | **16 llamadas** | Consulta de datasheets (TI LM317, WCH CH340, ULN2003, Sullins, Vector, etc.) |
| • `write_file` | **9 llamadas** | Creación de generadores paramétricos, especificaciones técnicas y Makefiles |
| • `ask_question` | **2 llamadas** | Aclaración directa de requisitos con el usuario |
| **Código Generado** | **~5.200+ líneas de código** | Firmware AVR C puro, Daemon Linux C, módulo Kernel hwmon, layout PCB, Makefiles |
| **Gráficos y Previews Generados** | **14 artefactos gráficos** | Esquemas Lepton-EDA (.png), PCBs superior/inferior 300 DPI, plantillas 1:1 (.svg, .png, .pdf) |

---

## 9. Bibliografía y Referencias

- **Texas Instruments LM317 3-Terminal Adjustable Regulator:** [https://www.ti.com/lit/ds/symlink/lm317.pdf](https://www.ti.com/lit/ds/symlink/lm317.pdf)
- **Texas Instruments / STMicroelectronics ULN2003A & ULN7003A:** [https://www.ti.com/lit/ds/symlink/uln2003a.pdf](https://www.ti.com/lit/ds/symlink/uln2003a.pdf)
- **Microchip / Atmel ATmega328P-PU:** [https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7810-Automotive-Microcontrollers-ATmega328P_Datasheet.pdf](https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7810-Automotive-Microcontrollers-ATmega328P_Datasheet.pdf)
- **pnjorge:** *Cooler-Fan-Controller Hardware & Firmware:* [https://github.com/pnjorge/Cooler-Fan-Controller](https://github.com/pnjorge/Cooler-Fan-Controller)

---

## 10. Evaluación Detallada de Costos de Producción (Production Cost Analysis)

> [!WARNING]
> **Aviso de Vigencia Temporal de Precios (Noviembre/Diciembre de 2026):**  
> Todas las cotizaciones, precios de componentes (BOM), mano de obra y tasas de cambio reflejan las condiciones de mercado vigentes en **Noviembre/Diciembre de 2026** (tipo de cambio de referencia: US$ 1.00 = R$ 5.80). Los costos de materias primas (cobre, laminado FR4), inflación, políticas arancelarias de importación, disponibilidad de componentes y variaciones cambiarias modificarán estas cifras con el tiempo. Quienes consulten esta documentación en el futuro deben solicitar cotizaciones actualizadas directamente a los fabricantes y distribuidores antes de planificar la producción.


Presentamos el análisis cuantitativo y cualitativo integral de costos para la fabricación de la **Custom Stripboard Rev 1.1 / Rev 1.1a**, incorporando cotizaciones de referencia de los principales **fabricantes nacionales brasileños de circuitos impresos (TEC-CI, PCB Brasil, Micro-Circuitos, Griffus PCB, Micropress y Circuibras)**, lista completa de materiales (BOM), mano de obra de ensamblaje y soldadura through-hole, grabación de firmware, pruebas funcionales de calidad y escenarios de escalabilidad por volumen.

---

### 10.1 Costos de Fabricación del PCB — Benchmark de la Industria Brasileña vs. Importación

#### Parámetros Técnicos de Fabricación de la Placa:
- **Dimensiones:** $88.90\text{ mm} \times 128.27\text{ mm}$ ($3.50'' \times 5.05''$, superficie $\approx 114\text{ cm}^2$).
- **Número de Capas:** 2 Capas (Doble cara FR4, ruteo de cobre de cara única en la capa inferior `Layer 6`).
- **Sustrato y Cobre:** FR-4 estándar ($T_g \ge 130\text{--}140^\circ\text{C}$), espesor $1.60\text{ mm}$, cobre 1 oz ($35\,\mu\text{m}$).
- **Especificación de Taladro Pasante:** Agujeros metalizados (PTH), estándar 100% Through-Hole default, diámetro externo de pad $\ge 80.00\text{ mil}$ ($2.032\text{ mm}$), broca $35.00\text{ mil}$ ($0.889\text{ mm}$).
- **Acabado Superficial:** HASL Lead-Free (estaño sin plomo estándar) o ENIG (Oro Químico, recomendado para durabilidad de los dedos de borde).
- **Conector de Borde:** Chaflán de inserción a $45^\circ$ en la lengüeta de 44 pines.

#### Benchmark de los Principales Fabricantes Nacionales (Brasil):

| Fabricante | Sede / Perfil | Prototipo Típico (5 placas) | Lote Pequeño (30 placas) | Lote de Producción (100+ placas) | Plazo Promedio de Entrega | Diferencial Competitivo Principal |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **TEC-CI Circuitos Impressos** | São Paulo - SP (Fund. 1984) | **R$ 39,00** / un<br>*(US$ 6.72)* | **R$ 24,00** / un<br>*(US$ 4.14)* | **R$ 13,50** / un<br>*(US$ 2.33)* | 7 a 10 días hábiles | Cotizador instantáneo online; precios de prototipo altamente competitivos; soporte técnico directo |
| **PCB Brasil** | Campinas - SP | **R$ 42,00** / un<br>*(US$ 7.24)* | **R$ 26,00** / un<br>*(US$ 4.48)* | **R$ 14,50** / un<br>*(US$ 2.50)* | 7 a 10 días hábiles | Configurador web ágil con programa de prototipos; amplia gama de colores de máscara; seguimiento confiable |
| **Micro-Circuitos** | Rio de Janeiro / SP | **R$ 45,00** / un<br>*(US$ 7.76)* | **R$ 27,00** / un<br>*(US$ 4.65)* | **R$ 15,00** / un<br>*(US$ 2.59)* | 8 a 12 días hábiles | Especialista en prototipos y series pequeñas; revisión técnica de ingeniería y verificación de layout |
| **Griffus PCB** | Cotia - SP | **R$ 48,00** / un<br>*(US$ 8.28)* | **R$ 28,00** / un<br>*(US$ 4.83)* | **R$ 14,00** / un<br>*(US$ 2.41)* | 8 a 10 días hábiles | Certificación ISO 9001; alta estabilidad dimensional para conectores de inserción industrial |
| **Micropress** | São Paulo - SP (Fund. 1986) | **R$ 72,00** / un<br>*(US$ 12.41)* | **R$ 42,00** / un<br>*(US$ 7.24)* | **R$ 24,00** / un<br>*(US$ 4.14)* | **24h a 48h express**<br>*(o 5–7d estándar)* | Referente nacional en prototipado rápido de alta precisión (quick-turn); estándar aeroespacial/médico |
| **Circuibras** | Curitiba - PR | **R$ 56,00** / un<br>*(US$ 9.65)* | **R$ 25,00** / un<br>*(US$ 4.31)* | **R$ 12,00** / un<br>*(US$ 2.07)* | 10 a 15 días hábiles | Planta fabril automatizada de alta capacidad; excelente economía de escala para series de 100+ unidades |

*(Tasa de cambio de referencia: US$ 1.00 = R$ 5,80)*

---

### 10.2 Lista Completa de Materiales (BOM) por Unidad

Todos los componentes cumplen con la directriz de fabricación **100% Through-Hole (THT / DIP)**:

| Item | Componente / Especificación | Encapsulado / Paso | Cant | Precio Unit. (USD) | Precio Unit. (BRL) | Costo Total (BRL) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **U1** | Microcontrolador ATmega328P-PU | DIP-28 Estrecho ($0.3''$) | 1 | US$ 2.20 | R$ 12,80 | R$ 12,80 |
| **SKT1** | Zócalo DIP-28 Estampado / Torneado | 28 Pines paso $2.54\text{ mm}$ | 1 | US$ 0.25 | R$ 1,50 | R$ 1,50 |
| **U2** | Driver Darlington ULN2003A o ULN7003A | DIP-16 | 1 | US$ 0.40 | R$ 2,30 | R$ 2,30 |
| **SKT2** | Zócalo DIP-16 | 16 Pines paso $2.54\text{ mm}$ | 1 | US$ 0.15 | R$ 0,90 | R$ 0,90 |
| **MOD1** | Módulo Conversor USB-TTL CH340 (6 pines) | 6 Pines paso $2.54\text{ mm}$ | 1 | US$ 1.20 | R$ 7,00 | R$ 7,00 |
| **Y1** | Cristal de Cuarzo 16.000 MHz | HC-49S THT | 1 | US$ 0.18 | R$ 1,00 | R$ 1,00 |
| **C3, C4** | Condensadores Cerámicos 22 pF | Disco cerámico | 2 | US$ 0.05 | R$ 0,30 | R$ 0,60 |
| **U101, U102** | CI Regulador LM317T (Datasheet TI) | TO-220 Vertical | 2 | US$ 0.40 | R$ 2,30 | R$ 4,60 |
| **VR101, VR102**| Módulos Step-Down LM2596 DC-DC | Vertical $4 \times 7$ pines | 2 | US$ 1.30 | R$ 7,50 | R$ 15,00 |
| **TB101** | Conector Borne KRE 10 Vías 5.08mm | ZB128 altura 14mm | 1 | US$ 1.10 | R$ 6,40 | R$ 6,40 |
| **CONN117, 118**| Conector Jack DC Hembra 2.1 $\times$ 5.5mm | THT Radial | 2 | US$ 0.25 | R$ 1,45 | R$ 2,90 |
| **HDR_SANDWICH**| Tiras de Pines 2.54mm (Macho + Hembra) | Tiras de 40 pines | 2 tiras | US$ 0.60 | R$ 3,50 | R$ 7,00 |
| **PASIVOS** | Condensadores 100nF, 1uF, 100uF + Resistencias 1/4W | Kit Axial/Radial | 1 kit | US$ 0.70 | R$ 4,00 | R$ 4,00 |
| **MECÁNICA** | Tornillos, tuercas y separadores M3 latón/nylon | Kit 6 orificios | 6 kits | US$ 0.80 | R$ 4,60 | R$ 4,60 |
| **TOTAL BOM** | **Suma de Componentes Electrónicos por Placa** | — | — | **US$ 9.58** | **R$ 55,85** | **R$ 70,60 (con margen)** |

---

### 10.3 Costos de Ensamblaje, Soldadura y Pruebas Funcionales

- **Tiempo Promedio de Ensamblaje Manual Through-Hole:** ~25 a 35 minutos por placa (inserción de componentes, doblado de terminales, soldadura manual, corte de terminales y limpieza de flux).
- **Grabación de Firmware y Control de Calidad:** ~5 a 7 minutos (grabación vía USB `make flash`, verificación de captura de pulsos de tacómetro, barrido de PWM en 4 canales y medición de voltaje de reguladores con multímetro).
- **Modelos de Costo de Mano de Obra:**
  - *DIY / Autoensamblaje:* R$ 0,00 (hobby/académico).
  - *Técnico de Banco Calificado (Brasil):* Estimado en R$ 25,00 a R$ 35,00 por placa ensamblada y probada.
  - *Montaje Automatizado Selectivo / Ola (Lotes de 100+):* ~US$ 3.50 a US$ 5.00 (R$ 20,00 a R$ 29,00) por unidad.

---

### 10.4 Resumen Consolidado de Costo Unitario en Tres Escenarios

*(Considerando el promedio de fabricación nacional brasileña TEC-CI / PCB Brasil / Micro-Circuitos)*

| Escenario de Producción | Costo PCB Unit. (BR) | Costo BOM Unit. | Mano de Obra y Prueba | **Costo Unitario Total (BRL)** | **Costo Unitario Total (USD)** |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **1. Prototipo Único / DIY (1 a 5 un)** | R$ 39,00 (TEC-CI) | R$ 70,60 | R$ 0,00 (Autoensamblado) | **R$ 109,60** | **US$ 18.90** |
| **2. Lote Pequeño Semiartesanal (30 un)** | R$ 24,00 (TEC-CI) | R$ 52,00 | R$ 25,00 (Técnico) | **R$ 101,00** | **US$ 17.40** |
| **3. Lote Industrial en Serie (100+ un)** | R$ 12,00 (Circuibras) | R$ 42,00 | R$ 20,00 (Selectiva) | **R$ 74,00** | **US$ 12.75** |

---

## 11. Licencia

Este proyecto es de código abierto bajo la licencia **GNU Lesser General Public License v3.0 (LGPLv3)**.
- Términos de la Licencia: [LICENSE](LICENSE)
- GNU Lesser General Public License: [COPYING.LESSER](COPYING.LESSER) / [LICENSE.LESSER](LICENSE.LESSER)
- GNU General Public License: [COPYING](COPYING)
