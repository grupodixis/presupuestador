# Catalogo Factusol - Precios y Referencias de Materiales (2026)

Fuente base: Maestro de articulos Factusol procesado (`articulos factusol actual.xlsx`, exportado y estructurado en `C:\Users\grupo\outputs\catalogo-20260917\prepared.json`).

Este documento sirve como guia rapida de costes de adquisicion y precios de venta (PVP) historicos para el razonamiento de presupuestos tecnicos e industriales en Menorca.

---

## 1. Volumen y Distribucion del Catalogo

- **Total articulos en catalogo:** 16.820
- **Materiales fisicos clasificados:** 8.366 articulos
- **Servicios y mano de obra:** 651 partidas
- **Familias clave:**
  - `MET` Metales, perfiles, tubos y chapas: 4.144 articulos
  - `TOR` Tornilleria, fijaciones y anclajes: 1.662 articulos
  - `PIN` Pinturas, quimicos y adhesivos: 953 articulos
  - `HER` Herramientas y recambios: 876 articulos
  - `ELE` Electricidad e iluminacion: 850 articulos
  - `CON` Construccion y materiales: 534 articulos
  - `CER` Cerrajeria y cerramientos: 495 articulos
  - `FON` Fontaneria y conducciones: 421 articulos
  - `EPI` Proteccion laboral: 304 articulos
  - `ABR` Abrasivos y discos: 300 articulos
  - `SOL` Soldadura y consumibles: 154 articulos

---

## 2. Herramienta de Consulta Rapida

Para consultar cualquier articulo, coste o disponibilidad desde la terminal:

```powershell
# Busqueda general por texto
python herramientas/buscar_catalogo.py "tubo 40x40"

# Busqueda filtrando por familia
python herramientas/buscar_catalogo.py "din 933" --familia TOR --con-precio

# Busqueda con stock disponible
python herramientas/buscar_catalogo.py "oxiron" --familia PIN

# Salida estructurada JSON para procesamiento automatico
python herramientas/buscar_catalogo.py "pletina 50x5" --json
```

---

## 3. Tarifas de Referencia de Materiales Frecuentes

### 3.1. Tubos Estructurales y Comerciales (€/ml)

| Articulo / Tipo | Material / Acabado | Coste Compra (€/ml) | PVP Ref. (€/ml) | Aplicacion / Entorno Menorca |
|---|---|---:|---:|---|
| Tubo cuadrado 40x40x1.5 | S-235 Laminado negro | 1,73 € | 3,14 € | Estructuras ligeras / interior |
| Tubo cuadrado 40x40x2 | S-235 Laminado negro | 2,26 € | 5,47 € | Cerrajería general / interior |
| Tubo cuadrado 40x40x1.5 | Galvanizado | 3,54 € | 6,43 € | Exterior C3 / protegido |
| Tubo cuadrado 40x40x2 | S-235 Galvanizado | 2,21 € | 4,01 € | Cerrajería exterior / bastidores |
| Tubo cuadrado 40x40x2 | Acero Corten | 2,90 € | 5,26 € | Estética óxido controlada |
| Tubo cuadrado 40x40x2 | Inox AISI 304 SPA | 6,75 € | 13,98 € | Interior / exterior no marino |
| Tubo cuadrado 40x40x2 | Inox AISI 304 2B | 9,23 € | 16,76 € | Carpintería inox estándar |
| Tubo cuadrado 40x40x2 | Inox AISI 316 2B | 14,80 € | 26,86 € | **Costa / marino severo C5-M** |
| Tubo rectangular 60x40x2 | S-235 Negro | ~ 3,20 € | ~ 6,50 € | Bastidores y cancelas |
| Tubo rectangular 80x40x2 | S-235 Galvanizado | ~ 5,10 € | ~ 9,80 € | Portones y marcos |
| Tubo redondo D.43 / D.50 | Inox AISI 316 pulido | 12,50 - 18,00 € | 22,00 - 32,00 € | Barandillas marinas |

### 3.2. Tornilleria y Fijaciones (€/ud)

> [!IMPORTANT]
> En exteriores de Menorca o ambientes salinos, **priorizar siempre calidad A4 (AISI 316)**. En ambientes interiores o no agresivos puede admitirse zincado o A2 (AISI 304).

| Articulo | Calidad / Acabado | Coste Unit. (€) | PVP Unit. (€) | Observaciones |
|---|---|---:|---:|---|
| Tornillo DIN 933 M8x30 | Inox A2 | 0,18 € | 0,33 € | Tornillo hex. rosca completa |
| Tornillo DIN 933 M8x50 | Inox A2 | 0,27 € | 0,48 € | Tornillo hex. estándar |
| Tornillo DIN 933 M10x50 | Inox A2 | 0,26 € | 0,46 € | Fijación de pletinas |
| Tornillo DIN 933 M10x60 | Inox A2 | 0,48 € | 0,88 € | Anclajes y uniones |
| Tornillo DIN 933 M12x40 | Acero zincado | 0,26 € | 0,47 € | Estructuras en taller / interior |
| Tornillo DIN 933 M12x60 | Inox A4 | 0,61 € | 1,10 € | **Exterior costa Menorca** |
| Varilla roscada M10 (1 metro) | Inox A2 | ~ 2,80 € | ~ 5,50 € | Anclaje químico |
| Varilla roscada M12 (1 metro) | Inox A4 | ~ 5,40 € | ~ 10,20 € | Anclaje marino |
| Taco nylon c/ tornillo 8x60 | Nylon / zincado | ~ 0,15 € | ~ 0,35 € | Fijaciones a muro |
| Anclaje metálico expansión M10 | Acero zincado / A2 | 0,60 - 1,20 € | 1,20 - 2,50 € | Fijación losas hormigón |

### 3.3. Pinturas, Tratamientos y Quimicos de Taller

| Articulo | Formato / Tipo | Coste (€) | PVP Ref. (€) | Uso habitual |
|---|---|---:|---:|---|
| Esmalte Oxiron Forja / Liso | Bote 750 ml | ~ 14,00 € | ~ 22,00 € | Acabado directo antioxidante |
| Imprimacion Epoxi 2C | Bote 1 kg / kit | ~ 18,00 € | ~ 28,00 € | Capa puente alta adherencia |
| Poliuretano 2C exterior C4/C5 | Bote 1 kg / kit | ~ 22,00 € | ~ 35,00 € | Capa acabado intemperie |
| Cartucho Silicona Neutra / MS | Cartucho 300 ml | 3,20 - 4,80 € | 6,00 - 8,50 € | Sellado de juntas y cerramientos |
| Cartucho Taco Quimico Epoxi/Vinilester | Cartucho 300/400 ml | 8,50 - 12,00 € | 15,00 - 22,00 € | Fijaciones estructurales |
| Disco corte inox 115x1.0 | Unidad | 0,80 - 1,20 € | 1,60 - 2,20 € | Consumible corte radial |
| Disco láminas desbaste 115 Zirconio | Unidad | 1,80 - 2,50 € | 3,50 - 4,80 € | Limpieza de soldaduras |
| Electrodo rutilo 2.5 mm | Paquete (aprox. 4 kg) | ~ 16,00 € | ~ 28,00 € | Soldadura taller S-235 |

---

## 4. Criterios de Aplicacion en la Presupuestacion

1. **Coste Tecnico vs. PVP:**
   - La columna `COSTE` en el catálogo refleja el precio de compra o fabricación interna histórica.
   - Si se presupuesta a partir de materiales de catálogo con `COSTE`, se debe aplicar el margen técnico y comercial correspondiente (según `presupuestacion/margenes/politica-margenes.md`).
   - La columna `PVP` sirve como control comercial del precio de venta habitual minorista/taller.

2. **Logistica y Portes a Menorca:**
   - Si un material no se encuentra en stock local o se encarga a distribuidor en península (Barcelona), añadir el coste logístico estándar marítimo:
     $$\text{Porte} = 0,20\ \text{€/kg}$$
   - Consultar `presupuestacion/costes/costes-transporte.json`.

3. **Mermas Comerciales:**
   - Recordar que los perfiles y tubos se suministran en barras comerciales estándar de **6 metros** (o 12 m en vigas pesadas).
   - Aplicar el porcentaje de merma correspondiente (habitualmente entre el 5% y el 15% según el aprovechamiento del despiece).
