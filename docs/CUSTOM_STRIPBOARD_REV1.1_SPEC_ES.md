# Custom Stripboard Rev 1.1 y Rev 1.1a — Especificación Técnica Completa y Manual de Ingeniería

> **Idiomas / Languages:** [Español](CUSTOM_STRIPBOARD_REV1.1_SPEC_ES.md) | [English (US)](CUSTOM_STRIPBOARD_REV1.1_SPEC_EN.md) | [Português](CUSTOM_STRIPBOARD_REV1.1_SPEC_PT.md)

Este documento consolida todas las notas técnicas, especificaciones eléctricas, mecánicas, reglas de diseño (layout), opciones de ensamblaje, pautas de fabricación y modelos de costos de producción para la placa **Custom Stripboard Rev 1.1** y **Rev 1.1a**.

---

## 1. Visión General y Filosofía de Diseño

La **Custom Stripboard Rev 1.1 / Rev 1.1a** es una plataforma modular de prototipado y control de ventiladores en formato estándar Eurocard/Vector, diseñada con el conjunto de herramientas de código abierto **Lepton-EDA** y **`pcb-rnd`**.

### Principios Fundamentales de Ingeniería:
1. **Tecnología Through-Hole (Agujero Pasante - THT) como Estándar Obligatorio**:
   - El montaje superficial (SMD) es estrictamente una opción accesoria y secundaria.
   - El estándar nativo y predeterminado de la placa es **100% Through-Hole (THT / PTH)** con orificios metalizados.
   - Todos los componentes discretos (condensadores cerámicos y electrolíticos, resistencias axiales de 1/4W), circuitos integrados (DIP), reguladores lineales (TO-220 vertical/upright), bloques de terminales de tornillo y conectores emplean pines pasantes.
2. **Dimensiones de Pads Estandarizadas de Alta Confiabilidad ($\ge 80\text{ mil}$)**:
   - Todas las islas de soldadura de la matriz de prototipado, conectores pass-thru, zócalos de CI y reguladores poseen un diámetro exterior de cobre $\ge 80.00\text{ mil}$ ($2.032\text{ mm}$), broca de taladrado de $35.00\text{ mil}$ ($0.889\text{ mm}$) y apertura de máscara de soldadura de $86.00\text{ mil}$ ($2.184\text{ mm}$).
   - Las islas del área de prototipado rápido (*scratch-pad*) presentan un diámetro de pad de $90.00\text{ mil}$ ($2.286\text{ mm}$) con una separación de cobre (*gap*) de exactamente $10.00\text{ mil}$ ($0.254\text{ mm}$).
3. **Cobre de Cara Única Inferior con Conector de Borde Industrial**:
   - Todo el ruteo de pistas de cobre reside exclusivamente en la **capa inferior de soldadura (`Layer 6 "bottom"` / `onsolder`)**.
   - La lengüeta inferior de 44 contactos ($2.54\text{ mm}$ / $100\text{ mil}$ pitch, estándar industrial Sullins / Vector) dispone de dedos de contacto y puentes de soldadura (*jumpers*) únicamente en la cara inferior, manteniendo la cara superior en laminado FR4 virgen para eliminar riesgos de cortocircuito en racks y bastidores.

---

## 2. Geometría Mecánica y Posicionamiento de Orificios M3

### Dimensiones Físicas:
- **Ancho del Cuerpo de la Placa:** $3500.00\text{ mil}$ ($88.90\text{ mm}$)
- **Longitud Total:** $5050.00\text{ mil}$ ($128.27\text{ mm}$)
- **Ancho de la Lengüeta de Borde:** $2700.00\text{ mil}$ ($68.58\text{ mm}$), desde $X = 400.00\text{ mil}$ hasta $3100.00\text{ mil}$.
- **Profundidad de Inserción de la Lengüeta:** $310.00\text{ mil}$ ($7.87\text{ mm}$), de $Y = 4740.00\text{ mil}$ a $5050.00\text{ mil}$.
- **Hombros de Apoyo Mecánico:** Escalón lateral de $400.00\text{ mil}$ ($10.16\text{ mm}$) en la cota $Y = 4740.00\text{ mil}$.
- **Chaflanes de Entrada (Lead-in):** Biseles a $40.00\text{ mil} \times 45^\circ$ en las esquinas inferiores de la lengüeta para una inserción suave en el zócalo.

### Orificios Metalizados de Montaje M3 (Broca: $126.00\text{ mil}$ / $3.20\text{ mm}$, Pad: $240.00\text{ mil}$, Aislamiento: $300.00\text{ mil}$):
| Identificador | Coordenadas $(X, Y)$ | Justificación de Posicionamiento y Espacios Libres |
| :---: | :---: | :--- |
| **MH101** | $(200.00, 200.00\text{ mil})$ | Esquina superior izquierda. Espacio amplio para el conector Jack DC 1 y el módulo VR101. |
| **MH102** | $(3300.00, 200.00\text{ mil})$ | Esquina superior derecha. Mantiene $>150\text{ mil}$ de aislamiento hacia la bornera TB101 ($Y = 600\text{ mil}$). |
| **MH103** | $(200.00, 2000.00\text{ mil})$ | **Reubicado en $Y = 2000\text{ mil}$**. Situado exactamente en el punto medio entre el Módulo LM2596 #1 (`VR101`, finaliza en $Y = 1200\text{ mil}$) y el Módulo #2 (`VR102`, inicia en $Y = 2800\text{ mil}$). El espacio de aislamiento de $300\text{ mil}$ ($Y \in [1850, 2150]$) ofrece $>650\text{ mil}$ de margen respecto a ambos módulos. |
| **MH104** | $(3300.00, 2700.00\text{ mil})$ | **Ajustado en $Y = 2700\text{ mil}$**. Proporciona $80\text{ mil}$ de margen hasta el cuerpo plástico de la bornera TB101 ($Y = 2500\text{ mil}$) y $135\text{ mil}$ de aislamiento en cobre hacia el área scratch-pad ($Y = 2955\text{ mil}$). |
| **MH105** | $(200.00, 4600.00\text{ mil})$ | Esquina inferior izquierda. El borde inferior del anillo de cobre ($Y = 4720\text{ mil}$) se alinea con la base de la última fila de prototipado ($Y = 4728\text{ mil}$), asegurando $140\text{ mil}$ de margen libre hacia los hombros de la lengüeta ($Y = 4740\text{ mil}$). |
| **MH106** | $(3300.00, 4600.00\text{ mil})$ | Esquina inferior derecha, simétricamente alineado con MH105. |

---

## 3. Subsistema de Potencia Superior: Conectores Jack DC y Regulador Doble LM317

### 3.1 Conectores Jack DC Tipo Barril y Cabezales Breakout SIP3
Para facilitar la disipación térmica y despejar el centro de la placa, los dos conectores hembra Jack DC 2.1mm $\times$ 5.5mm se desplazaron hacia los extremos laterales:
- **Jack DC 1 (`CONN117`):** Ubicado en $(X = 800.00\text{ mil}, Y = 200.00\text{ mil})$.
  - Cabezal de derivación SIP3 (`CONN119..121`) en $X = 500, 600, 700\text{ mil}$ ($Y = 200..400\text{ mil}$).
  - Conexiones de terminal central ($+V$), interruptor central y masa ruteadas exclusivamente con **pistas de cobre de $40\text{ mil}$ (`Layer 6 "bottom"`)** para corrientes de hasta 5A continuo.
- **Jack DC 2 (`CONN118`):** Ubicado en $(X = 2400.00\text{ mil}, Y = 200.00\text{ mil})$.
  - Cabezal de derivación SIP3 (`CONN122..124`) en $X = 2800, 2900, 3000\text{ mil}$ ($Y = 200..400\text{ mil}$).
  - Ruteado íntegramente con **pistas de cobre de $40\text{ mil}$**.

### 3.2 Circuito Doble Regulador Lineal LM317 (Datasheet TI, Página 1)
En el vano central superior ($X = 1400\text{ mil}$ a $X = 2100\text{ mil}$, $Y = 200..700\text{ mil}$), se implementaron dos circuitos reguladores lineales LM317 independientes siguiendo el esquema del fabricante:

$$V_{OUT} = 1.25\,\text{V} \times \left(1 + \frac{R_2}{R_1}\right) + I_{ADJ} \times R_2$$

```
                         CIRCUITO REGULADOR LM317 (Datasheet TI Página 1)
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
           GND o────┴───────────────────────────────────────────o GND (Común)
               (C1 0.1µF desacoplamiento en la entrada VIN)
```

#### LM317 Circuito #1:
- **CI Regulador `U101` (TO-220 Vertical):** Pin 3 (VIN) en $(1400, 300)$, Pin 2 (VOUT) en $(1500, 300)$, Pin 1 (ADJ) en $(1600, 300)$.
- **Condensadores THT:** $C_{101}$ ($0.1\,\mu\text{F}$ cerámico de disco) en $(1400, 400..600)$; $C_{102}$ ($1.0\,\mu\text{F}$ tántalo/electrolítico) en $(1500, 400..600)$.
- **Resistencias Axiales:** $R_{101}$ ($240\,\Omega$, 1/4W) en $(1500..1600, 500)$; $R_{102}$ ($R_2$, fija o trimpot multivuelta) en $(1600, 400..600)$.
- **Puntos de Prueba THT (Pads $\ge 80\text{ mil}$):** `J101` (VIN1 en $1400, 200$), `J102` (VOUT1 en $1500, 200$), `J103` (GND en $1400, 700$).

#### LM317 Circuito #2:
- **CI Regulador `U102` (TO-220 Vertical):** Pin 3 (VIN) en $(1900, 300)$, Pin 2 (VOUT) en $(2000, 300)$, Pin 1 (ADJ) en $(2100, 300)$.
- **Condensadores THT:** $C_{103}$ ($0.1\,\mu\text{F}$) en $(1900, 400..600)$; $C_{104}$ ($1.0\,\mu\text{F}$) en $(2000, 400..600)$.
- **Resistencias Axiales:** $R_{103}$ ($240\,\Omega$) en $(2000..2100, 500)$; $R_{104}$ ($R_2$) en $(2100, 400..600)$.
- **Puntos de Prueba THT (Pads $\ge 80\text{ mil}$):** `J104` (VIN2 en $1900, 200$), `J105` (VOUT2 en $2000, 200$), `J106` (GND en $1900, 700$).
- **Bus de Tierra Común:** Pista de cobre de $40\text{ mil}$ en $Y = 600.00\text{ mil}$ que une las tierras de ambos reguladores ($X = 1400$ a $X = 2100\text{ mil}$).

---

## 4. Margen Izquierda: Módulos Step-Down LM2596 Verticales (`VR101`, `VR102`)

Para conversión conmutada DC-DC de alta eficiencia (+12V a +5V o +3.3V con corrientes de hasta 3A):
- **Huella (Footprint):** Matriz de $4 \times 7$ pines con paso de $200.00\text{ mil}$ ($5.08\text{ mm}$), columnas $X = 100, 200, 300, 400\text{ mil}$.
- **Módulo 1 (`VR101`):** $Y = 600.00\text{ mil}$ a $1200.00\text{ mil}$. Filas 1–4 para `VIN1+` ($X = 100$) y `VIN1-` ($X = 300$); Filas 5–7 para `OUT1+` ($X = 100$) y `OUT1-` ($X = 300$).
- **Módulo 2 (`VR102`):** $Y = 2800.00\text{ mil}$ a $3400.00\text{ mil}$. Filas 1–4 para `VIN2+` y `VIN2-`; Filas 5–7 para `OUT2+` y `OUT2-`.
- **Pistas de Potencia de $40\text{ mil}$:** Barras verticales continuas de $40\text{ mil}$ agrupan los pines en cada función de alimentación.
- **Tornillo `MH103`:** Situado en $(X = 200\text{ mil}, Y = 2000\text{ mil})$, con más de $650\text{ mil}$ de aislamiento respecto a los dos módulos.

---

## 5. Margen Derecha: Bornera de Tornillo KRE 10 Vías (5.08mm) y Matriz Pass-Thru

Ubicada en el borde superior derecho entre `MH102` y `MH104`:
- **Modelo de Conector (`TB101`):** Bornera KRE 10 Vías, paso $5.08\text{ mm}$ ($0.2''$), serie ZB128 (altura 14mm).
- **Pines:** $X = 3400.00\text{ mil}$, $Y = [600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400]\text{ mil}$.
- **Matriz Pass-Thru Horizontal de 3 Puntos:** Por cada tornillo terminal, se extienden 3 orificios pasantes hacia el centro:
  - Punto 1: `CONN137` en $X = 3300.00\text{ mil}$
  - Punto 2: `CONN138` en $X = 3200.00\text{ mil}$
  - Punto 3: `CONN139` en $X = 3100.00\text{ mil}$
- **Pistas de Cobre de $30\text{ mil}$:** Cada fila de 4 orificios está unida por pistas de $30\text{ mil}$, constituyendo 10 redes independientes (`KRE_1` a `KRE_10`).
- **Espacios Mecánicos:** $>150\text{ mil}$ de aislamiento respecto al tornillo `MH102` superior, y $80\text{ mil}$ respecto al tornillo `MH104` inferior.

---

## 6. Margen Derecha: Área de Prototipado Rápido Scratch-Pad (56 Pads, Pistas Cortables de 3 mil)

Ubicada entre los orificios `MH104` y `MH106`:
- **Geometría de la Matriz:** 14 filas $\times$ 4 columnas = **56 islas** ($X = 3100..3400\text{ mil}$, $Y = 3000..4300\text{ mil}$).
- **Dimensiones de Pad:** Diámetro de **$90.00\text{ mil}$**, broca de **$35.00\text{ mil}$**, apertura de máscara de **$96.00\text{ mil}$**.
- **Separación de $10\text{ mil}$:** Distancia de cobre entre pads adyacentes de **$10.00\text{ mil}$ ($0.254\text{ mm}$)**.
- **Pistas Seccionables de $3\text{ mil}$ (Knife-Scratchable):**
  - Inicialmente, los 56 pads pertenecen a la red común `SCRATCHPAD`.
  - La unión física se realiza mediante micropistas de cobre de **$3.00\text{ mil}$ ($0.0762\text{ mm}$)** en la capa inferior.
  - El usuario puede seccionar cualquier pista con bisturí o cuchilla para aislar pads o armar buses a medida.
- **Serigrafía:** Contorno rectangular delimitado con el texto `"SCRATCH PAD"`.

---

## 7. Jerarquía Estandarizada de Anchos de Pista de Cobre

| Ancho de Pista | Aislamiento | Capa | Señales y Circuitos Asignados |
| :---: | :---: | :---: | :--- |
| **$40.00\text{ mil}$** ($1.016\text{ mm}$) | $20.00\text{ mil}$ | Bottom | 8 Barras de alimentación (+12V, +5V, GND); Pistas de Jacks DC; Pistas de potencia LM2596; Alimentación y tierra LM317; Tiras verticales inferiores (`SIP4N`). |
| **$30.00\text{ mil}$** ($0.762\text{ mm}$) | $20.00\text{ mil}$ | Bottom | Puentes verticales de 100 mil en el sándwich `HEADER18`; Puentes de soldadura; Pistas de la bornera KRE a la matriz pass-thru. |
| **$20.00\text{ mil}$** ($0.508\text{ mm}$) | $20.00\text{ mil}$ | Bottom | Pistas de ajuste (Pin 1 ADJ) del LM317 a resistencias $R_1$ y $R_2$. |
| **$10.00\text{ mil}$** ($0.254\text{ mm}$) | $20.00\text{ mil}$ | Bottom | Pistas horizontales de prototipado (58 líneas en Rev 1.1, 64 líneas en Rev 1.1a). |
| **$3.00\text{ mil}$** ($0.076\text{ mm}$) | $10.00\text{ mil}$ | Bottom | Micropistas seccionables del área de prototipado rápido *scratch-pad*. |

---

## 8. Comparativa Detallada: Rev 1.1 vs. Rev 1.1a

| Característica / Parámetro | Custom Stripboard Rev 1.1 | Custom Stripboard Rev 1.1a |
| :--- | :--- | :--- |
| **Líneas Horizontales de Prototipado** | 29 filas por banco (Filas 1–29, total 58 tiras de 9 pines) | **32 filas por banco (Filas 1–32, total 64 tiras de 9 pines)** |
| **Ubicación de la Sección Sándwich** | $Y = 3800\text{ mil}$ (`SIP9N`), $Y = 3900..4000\text{ mil}$ (`HEADER18`), $Y = 4100\text{ mil}$ (`SIP9N`) | **Desplazada $+200\text{ mil}$ hacia abajo:** $Y = 4000\text{ mil}$ (`SIP9N`), $Y = 4100..4200\text{ mil}$ (`HEADER18`), $Y = 4300\text{ mil}$ (`SIP9N`) |
| **Aprovechamiento Filas $Y = 3700, 3800, 3900\text{ mil}$** | Hueco de transición sin uso | **100% Ocupadas:** Tiras de 9 pines `CONN241..243` y `CONN341..343` con pistas de $10\text{ mil}$ |
| **Margen hacia Salidas Verticales ($Y = 4400\text{ mil}$)** | Hueco de $300\text{ mil}$ desaprovechado | **Continuo:** Tira inferior en $Y = 4300\text{ mil}$, a exactamente $100\text{ mil}$ de las salidas |
| **Módulos LM2596 Verticales (`VR101`, `VR102`)** | Presentes en margen izquierdo ($4 \times 7$ pines) | Presentes en margen izquierdo ($4 \times 7$ pines) |
| **Regulador Doble LM317 (`U101`, `U102`)** | Presentes entre Jacks DC con puntos THT | Presentes entre Jacks DC con puntos THT |
| **Bornera KRE 10 Vías + Pass-Thru** | Presente en margen derecho (`TB101` + 30 pines) | Presente en margen derecho (`TB101` + 30 pines) |
| **Área Scratch-Pad ($3\text{ mil}$)** | Presente entre `MH104` y `MH106` | Presente entre `MH104` e `MH106` |
| **Texto de Serigrafía** | `"CUSTOM STRIPBOARD REV 1.1"` | `"CUSTOM STRIPBOARD REV 1.1a"` |

---

## 9. Conector de Borde y Puentes de Soldadura Abiertos

- **Arquitectura de Cara Única Estricta:** Los 26 dedos de contacto residen exclusivamente en la cara de soldadura (`Layer 6 "bottom"` / `onsolder`). La cara superior es laminado FR4 sin cobre.
- **Geometría de Contactos:** $65.00\text{ mil} \times 230.00\text{ mil}$ ($1.65\text{ mm} \times 5.84\text{ mm}$), centrados en $Y = 4925\text{ mil}$.
- **Chaveta de Polarización en Dedo 8:** El contacto 8 ($X = 1200\text{ mil}$) y su jumper fueron omitidos deliberadamente e identificados con serigrafía `"KEY"`.
- **Puentes de Soldadura Abiertos:** Separación abierta de **$13\text{ mil}$ ($0.33\text{ mm}$)**. Una gota de estaño conecta cualquier señal al conector de borde.

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

## 11. Registro de Desarrollo Asistido por IA

> [!NOTE]
> **Identificación Oficial de Desarrollo:**  
> *"projeto usando lepton-eda/pcb-rnd assistido com IA-Gemini-3.8-Flash-Medium"*

- **Modelo de IA Utilizado:** Google DeepMind Gemini 3.8 Flash (Medium).
- **Iteraciones de Diálogo:** **17 turnos interactivos**.
- **Ejecuciones de Herramientas:** **413 llamadas** (290 `run_command`, 42 `edit_file`, 28 `manage_task`, 26 `read_file`, 16 `search_web`, 9 `write_file`, 2 `ask_question`).
- **Cadena de Herramientas:** Lepton-EDA (`lepton-schematic`, `lepton-netlist`, `lepton-cli`), `pcb-rnd` (modo fotográfico 300 DPI), `gcc` 14.2.0, `avr-gcc` 14.2.0, `avrdude`, Python 3.12/3.13, `reportlab` 4.x, `inkscape`, y `pdftoppm`.

---

## 12. Referencias, Normas y Hojas de Datos Oficiales

1. **Texas Instruments LM317 3-Terminal Adjustable Regulator:**  
   Datasheet SNVS774P. Circuito de aplicación de la página 1 ($1.25\text{V} - 37\text{V}$, $1.5\text{A}$, $R_1 = 240\,\Omega$, $C_1 = 0.1\,\mu\text{F}$, $C_2 = 1.0\,\mu\text{F}$).  
   PDF Oficial: [https://www.ti.com/lit/ds/symlink/lm317.pdf](https://www.ti.com/lit/ds/symlink/lm317.pdf)
2. **Texas Instruments / STMicroelectronics ULN2003A & ULN7003A:**  
   Datasheet SLRS027P. Matriz de transistores Darlington con diodos supresores integrados.  
   PDF Oficial: [https://www.ti.com/lit/ds/symlink/uln2003a.pdf](https://www.ti.com/lit/ds/symlink/uln2003a.pdf)
3. **Microchip / Atmel ATmega328P-PU:**  
   Datasheet DS40002061B / Atmel-8271. Registros PWM, interrupciones de tacómetro, USART0.  
   PDF Oficial: [https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7810-Automotive-Microcontrollers-ATmega328P_Datasheet.pdf](https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7810-Automotive-Microcontrollers-ATmega328P_Datasheet.pdf)
4. **WCH: Conversor USB-Serie TTL CH340:**  
   Especificaciones oficiales del circuito integrado y módulo.  
   [https://www.wch-ic.com/products/CH340.html](https://www.wch-ic.com/products/CH340.html)
5. **pnjorge (Paulo Nogueira / F5VMJ):**  
   *"Silent Running With This Dual Fan Controller"* (Hackster.io, 2021).  
   [https://www.hackster.io/pnjorge/silent-running-with-this-dual-fan-controller-0accb8](https://www.hackster.io/pnjorge/silent-running-with-this-dual-fan-controller-0accb8)  
   Repositorio en GitHub: [https://github.com/pnjorge/Cooler-Fan-Controller](https://github.com/pnjorge/Cooler-Fan-Controller)
6. **Sullins Connector Solutions — Conectores Card Edge (0.100" Pitch, Serie ETM / EBM):**  
   Conectores hembra de 44 posiciones / 22 contactos unilaterales.  
   [https://www.sullinscorp.com/](https://www.sullinscorp.com/)
7. **Vector Electronics & Technology — Eurocard & Vectorbord Plugboards:**  
   Placas de conector de borde estándar de 44 pines (Serie 3662).  
   [https://www.vectorelect.com/](https://www.vectorelect.com/)
8. **Intel Corporation:** *4-Wire Pulse Width Modulation (PWM) Controlled Fans Specification*, Rev 1.3.
9. **The Linux Kernel Organization:** *Hardware Monitoring Subsystem (`hwmon`)*.  
   [https://docs.kernel.org/hwmon/](https://docs.kernel.org/hwmon/)
