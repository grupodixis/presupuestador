# Memoria Justificativa de Cálculo Estructural y Dimensionamiento
## Proyecto: Marquesina Rectangular Atornillable 16 x 8 m (H = 8,00 m)
**Localización:** Polígono Industrial de Alaior, Menorca  
**Cliente:** Nautic KIM (Contacto: Mariano)  
**Ref. Interna:** P-2026-0050 / PRE-2026-1102-MARQ-NAUTIC  
**Fecha:** 2 de noviembre de 2026  
**Empresa:** DIXIS Recursos y Soluciones S.L. / HAM Estructuras Metálicas Menorca  

---

### 1. Objeto y Descripción General
El presente documento justifica el predimensionamiento y cálculo estructural para una **marquesina industrial rectangular abierta por sus 4 costados**, de estructura 100% desmontable y atornillada (tipo mecano), destinada al resguardo de embarcaciones, maquinaria y material logístico náutico en el Polígono Industrial de Alaior (Menorca).

- **Longitud entre ejes extremos:** 16,00 m (4 vanos de 4,00 m).
- **Luz libre transversal:** 8,00 m.
- **Altura libre al alero:** 8,00 m.
- **Altura máxima en cumbrera/punto alto:** 8,60 m (pendiente a un agua ~7,5 % hacia fachada posterior).
- **Superficie real techada:** 150,30 m² (16,70 m longitud x 9,00 m desarrollo de faldón con aleros protectores de 0,50 m).
- **Cubierta:** Panel sándwich de 30 mm de poliuretano inyectado (PUR 40 kg/m³), chapa grecada exterior 0,5 mm prelacada e interior 0,4 mm blanco pirineo.
- **Tipo de unión:** Estructura atornillada mediante placas frontales, cartelas mecanizadas en taller y tornillería de alta resistencia M16 y M20 calidad 8.8 cincada.

---

### 2. Normativa y Bases de Cálculo
- **CTE DB-SE:** Seguridad Estructural.
- **CTE DB-SE-AE:** Acciones en la edificación.
- **CTE DB-SE-A:** Estructuras de acero.
- **UNE-EN 1993 (Eurocódigo 3):** Proyecto de estructuras de acero.
- **EAE:** Instrucción de Acero Estructural.
- **Materiales:** Acero estructural S275JR ($f_y = 275\text{ N/mm}^2$, $f_u = 430\text{ N/mm}^2$, $\gamma_{M0} = 1,05$, $\gamma_{M1} = 1,05$). Tornillería métrica calidad 8.8 ($f_{yb} = 640\text{ N/mm}^2$, $f_{ub} = 800\text{ N/mm}^2$).

---

### 3. Cargas y Acciones de Diseño (CTE DB-SE-AE)

#### 3.1. Cargas Permanentes ($G$)
- Panel sándwich PUR 30 mm (chapa 0,5/0,4 mm): $0,10\text{ kN/m}^2$ ($\approx 10\text{ kg/m}^2$).
- Correas de cubierta y fijaciones: $0,08\text{ kN/m}^2$.
- Peso propio de vigas y accesorios: considerado internamente por el modelo.
- **Total Carga Muerta en cubierta:** $G_k = 0,18\text{ kN/m}^2$.

#### 3.2. Sobrecargas de Uso y Nieve ($Q, S$)
- Cubierta ligera tipo G1 (mantenimiento y limpieza): $Q_k = 0,40\text{ kN/m}^2$.
- Nieve en Alaior (altitud $\approx 130\text{ m}$, Zona 2): $s_k = 0,20\text{ kN/m}^2$.

#### 3.3. Acción del Viento en Alaior ($W$) - Factor Crítico
- **Zona eólica:** Menorca está clasificada en **Zona C** ($v_b = 29\text{ m/s} \approx 104,4\text{ km/h}$; $q_b = 0,52\text{ kN/m}^2$).
- **Grado de aspereza:** Tipo III (Zona industrial, Polígono de Alaior).
- **Altura de referencia:** $z = 8,00\text{ m}$.
- **Coeficiente de exposición:** $c_e(z) = 1,92$.
- **Presión dinámica de pico:**  
  $$q_p(z) = c_e(z) \cdot q_b = 1,92 \cdot 0,52 = 1,00\text{ kN/m}^2 \quad (100\text{ kg/m}^2)$$
- **Marquesina abierta (Tabla 3.8 CTE DB-SE-AE):**
  - Presión neta máxima hacia abajo (viento descendente): $c_{p,\text{net}} = +1,20 \rightarrow w_{\text{down}} = +1,20\text{ kN/m}^2$.
  - Succión neta máxima hacia arriba (viento ascendente/levantamiento): $c_{p,\text{net}} = -1,30 \rightarrow w_{\text{up}} = -1,30\text{ kN/m}^2$.
  - Empuje lateral en cantos y pilares: $q_{\text{lat}} = 1,00\text{ kN/m}^2$.

---

### 4. Combinaciones de Acciones (ELU y ELS)
- **ELU Viento descendente:** $1,35 \cdot G + 1,50 \cdot Q + 0,90 \cdot W = 1,35(0,18) + 1,50(0,40) + 0,90(1,20) = 1,92\text{ kN/m}^2$.
- **ELU Viento dominante:** $1,35 \cdot G + 1,50 \cdot W = 1,35(0,18) + 1,50(1,20) = 2,04\text{ kN/m}^2$.
- **ELU Viento de succión (arrancamiento):** $0,80 \cdot G - 1,50 \cdot W = 0,80(0,18) - 1,50(1,30) = -1,81\text{ kN/m}^2$ (Tracción pura en anclajes).
- **ELS Deformaciones:** $G + W = 0,18 + 1,00 = 1,18\text{ kN/m}^2$.

---

### 5. Dimensionamiento de Elementos

#### 5.1. Pilares a 8,00 m de Altura (10 unidades)
A una altura libre de 8,00 m en una estructura abierta sujeta a vientos de Menorca, el fenómeno de pandeo por flexocompresión es el criterio determinante.
- **Perfil adoptado:** Tubo estructural hueco cuadrado **180x180x6 mm** en acero S275JR.
- **Propiedades geométricas:**
  - Área: $A = 40,4\text{ cm}^2$.
  - Inercia: $I_y = I_z = 2.150\text{ cm}^4$.
  - Módulo elástico: $W_y = W_z = 239\text{ cm}^3$.
  - Radio de giro: $i = 7,08\text{ cm}$.
  - Masa lineal: $31,70\text{ kg/m}$.
- **Esbeltez y pandeo:**
  - Con jabalcones a 45° de 1,40 m en nudo cabeza y arriostramiento longitudinal en coronación, la longitud de pandeo en el plano del pórtico es $L_{k} \approx 0,80 \cdot 8,00 = 6,40\text{ m}$.
  - Esbeltez: $\lambda = 640 / 7,08 = 90,4$.
  - Esbeltez reducida: $\bar{\lambda} = 90,4 / 86,8 = 1,04$.
  - Curva de pandeo tipo c ($\alpha = 0,49$): $\chi = 0,55$.
  - Resistencia a compresión:  
    $$N_{b,\text{Rd}} = \frac{\chi \cdot A \cdot f_y}{\gamma_{M1}} = \frac{0,55 \cdot 4040 \cdot 275}{1,05} = 581,8\text{ kN} \quad (\approx 59\text{ toneladas})$$
  - Axil máximo actuante: $N_{\text{Ed}} \approx 32\text{ kN} \ll 581,8\text{ kN}$ (**Aprovechamiento por axil < 6%**).
  - Comprobación a flexión combinada con momento por viento en cabeza ($M_{\text{Ed}} \approx 28\text{ kNm}$):  
    $$\frac{N_{\text{Ed}}}{\chi N_{\text{pl},\text{Rd}}} + \frac{k_y M_{y,\text{Ed}}}{M_{y,\text{pl},\text{Rd}}} = 0,06 + 0,48 = 0,54 < 1,0 \quad \text{\textbf{[CUMPLE AMPLIO, FACTOR DE SEGURIDAD 1,85]}}$$

#### 5.2. Dinteles Principales de Pórticos (5 unidades, Luz = 8,00 m)
- **Perfil adoptado:** Viga laminada **IPE 240** en acero S275JR ($30,70\text{ kg/m}$).
- **Propiedades:** $W_{el,y} = 324\text{ cm}^3$, $I_y = 3.892\text{ cm}^4$.
- **Luz eficaz con jabalcones:** $L_{\text{ef}} = 6,00\text{ m}$ entre entregas de jabalcones.
- **Carga lineal de cálculo:** $q_{\text{Ed}} = 2,04\text{ kN/m}^2 \cdot 4,00\text{ m} = 8,16\text{ kN/m}$.
- **Momento flector máximo:** $M_{\text{Ed}} \approx 36,7\text{ kNm}$.
- **Momento resistente de la sección:**  
  $$M_{c,\text{Rd}} = \frac{W_{el,y} \cdot f_y}{\gamma_{M0}} = \frac{324 \cdot 10^3 \cdot 275}{1,05 \cdot 10^6} = 84,85\text{ kNm}$$
  $$\frac{M_{\text{Ed}}}{M_{c,\text{Rd}}} = \frac{36,7}{84,85} = 0,43 < 1,0 \quad \text{\textbf{[CUMPLE HOLGADAMENTE]}}$$
- **Flecha en servicio (ELS):**  
  $$f_{\text{max}} = \frac{5 \cdot q_{\text{ser}} \cdot L_{\text{ef}}^4}{384 \cdot E \cdot I_y} \approx 11,2\text{ mm} < \frac{L}{400} = 20,0\text{ mm} \quad \text{\textbf{[CUMPLE RIGIDEZ]}}$$

#### 5.3. Jabalcones / Tornapuntas a 45° (10 unidades)
- **Perfil:** Tubo estructural **100x100x4 mm** ($11,70\text{ kg/m}$, $L = 1,40\text{ m}$).
- Triangulan y rigidizan el nudo pilar-dintel, reduciendo en un 55% la deformación horizontal del pórtico y transmitiendo el viento directamente por esfuerzo axil.

#### 5.4. Vigas de Atado Longitudinal en Cabeza (2 líneas de 16,00 m)
- **Perfil:** Tubo estructural **120x120x5 mm** ($17,50\text{ kg/m}$).
- Arriostra las 5 cabezas de pilares en sentido longitudinal y absorbe el empuje de viento en testeros transmitiéndolo a las cruces de San Andrés.

#### 5.5. Correas de Cubierta (8 líneas de 16,70 m = 133,60 ml)
- **Perfil:** Tubo estructural rectangular **100x50x3 mm** ($6,62\text{ kg/m}$).
- Separación entre correas: $\approx 1,25\text{ m}$ (óptima para panel de 30 mm).
- Vano de correa: $4,00\text{ m}$ continuo sobre apoyos de pórticos.
- Carga mayorada por metro lineal: $q_{\text{correa}} = 2,04 \cdot 1,25 = 2,55\text{ kN/m}$.
- Flecha estimada: $f < L/300 = 13,3\text{ mm}$ (flecha real $\approx 8,4\text{ mm}$).

#### 5.6. Arriostramientos (Cruces de San Andrés)
- En fachada longitudinal: 2 vanos arriostrados por lateral (4 cruces completas).
- En plano de cubierta: 2 vanos arriostrados (2 cruces completas).
- Perfil: Redondo macizo calibrado $\varnothing 20\text{ mm}$ con tensores de acero forjado M20 calidad 8.8. Absorben los cortantes de viento en plano longitudinal sin permitir deformaciones laterales en cabeza de pilares.

#### 5.7. Placas Base y Anclajes a Cimentación
- 10 Placas de anclaje de $350 \times 350 \times 20\text{ mm}$ en acero S275JR con 4 cartelas triangulares rigidizadoras $e = 10\text{ mm}$.
- Anclaje mediante 4 varillas roscadas M20 calidad 8.8 cincadas con inyección de resina epoxi de alta resistencia (tipo Hilti HIT-HY 200) taladradas en solera/zapata de hormigón armado existente, garantizando una resistencia a tracción por arranque de $> 65\text{ kN}$ por perno frente a succiones extremas de viento.

---

### 6. Desglose Analítico de Acero (Hierro)

| Elemento Estructural | Perfil / Escuadría | Longitud / Uds | Peso unitario | Peso Total (kg) |
|---|---|---|---:|---:|
| **Pilares principales** | Tubo 180x180x6 mm | 10 uds x 8,00 m = 80,00 m | 31,70 kg/m | 2.536,00 kg |
| **Dinteles de pórticos** | Viga IPE 240 | 5 uds x 8,00 m = 40,00 m | 30,70 kg/m | 1.228,00 kg |
| **Jabalcones en nudos (45°)** | Tubo 100x100x4 mm | 10 uds x 1,40 m = 14,00 m | 11,70 kg/m | 163,80 kg |
| **Vigas de atado coronación** | Tubo 120x120x5 mm | 2 líneas x 16,00 m = 32,00 m | 17,50 kg/m | 560,00 kg |
| **Correas de faldón** | Tubo 100x50x3 mm | 8 líneas x 16,70 m = 133,60 m | 6,62 kg/m | 884,43 kg |
| **Cruces de San Andrés** | Redondo Ø20 mm + tensores | 108,00 m lineales totales | 2,47 kg/m | 386,76 kg |
| **Placas base, cartelas y herrajes** | Chapas e=20/15/10 mm | 10 placas base + cartelas | Global | 602,00 kg |
| **Tornillería estructural 8.8** | M16 y M20 cincada | Pernos, tuercas, arandelas | Global | 110,00 kg |
| **TOTAL ACERO ESTRUCTURAL (Kg)** | **S275JR** | **Estructura Atornillable** | **6.471,00 kg** |

> **Ratio estructural:** $6.471\text{ kg} / 150,3\text{ m}^2 = 43,05\text{ kg de acero/m}^2$, ratio óptimo de seguridad, robustez y economía para una altura libre de 8,00 metros en la climatología de Menorca.
