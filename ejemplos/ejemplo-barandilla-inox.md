# Ejemplo: Barandilla de acero inoxidable en ambiente marino

## Solicitud del cliente

"Barandilla de acero inoxidable pintada, 12 metros lineales, anclaje lateral, barrotes verticales, montaje en obra, ambiente marino C5"

## Paso 1: Identificación del producto

- **Tipo:** Barandilla metálica.
- **Material:** Acero inoxidable.
- **Uso:** Exterior, ambiente marino C5.
- **Skill principal:** `skill_barandillas.md` + `skill_montaje_en_obra.md` + `skill_tratamientos_superficiales.md`.

## Paso 2: Datos detectados y faltantes

### Detectados
- 12 metros lineales.
- Ambiente marino C5.
- Anclaje lateral.
- Barrotes verticales.
- Montaje en obra.

### Faltantes / dudas
- Altura de la barandilla (se asume 100 cm estándar para balcones).
- Tipo de acero inoxidable (se recomienda AISI 316 para C5).
- ¿La barandilla va pintada? Cliente indica "pintada" pero sobre inoxidable. Se aclara que el inoxidable no se pinta si es AISI 316. Se pregunta al cliente si quiere acero al carbono pintado o inoxidable AISI 316 en bruto cepillado.
- Número de tramos (se asume continuo si no se indica).
- Tipo de pasamanos (se asume tubo redondo de 50 mm).
- Separación entre barrotes (estándar 10 cm).
- Acceso a obra.
- Plazo de entrega.

## Paso 3: Composición consultada

`/productos/composiciones/barandilla.yaml`

Material principal: tubo inoxidable AISI 316.
Materiales auxiliares: tornillería inoxidable A2-70, discos de corte para inox, hilo TIG, gas argón.

## Paso 4: Cálculo de materiales

### Pasamanos
- Tubo redondo inoxidable AISI 316 Ø50 mm.
- 12 ml + 5% merma = 12.6 ml.

### Barrotes verticales
- Cada 10 cm → 120 uds.
- Altura 100 cm → tubo inoxidable AISI 316 Ø20 mm.
- 120 uds x 1.05 m = 126 ml + 5% merma = 132.3 ml.
- Se redondea a 133 ml.

### Largueros (larguerillo superior e inferior)
- 2 uds x 12 ml = 24 ml + 5% merma = 25.2 ml.
- Perfil tubular inoxidable AISI 316 40x20 mm.

### Pletinas de anclaje
- Cada 1.5 m → 8 uds.
- Pletina inoxidable AISI 316 100x100x8 mm.

### Tornillería
- 8 uds tacos químicos inoxidable M12.
- 8 uds arandela + tuerca inoxidable A4.

### Consumibles
- Discos de corte inoxidable: 5 uds.
- Hilo TIG inoxidable 316L: 1 kg.
- Gas argón: 1 botella.
- Discos de desbaste y pulido: 3 uds.

## Paso 5: Procesos de fabricación

1. Medición y replanteo (visita a obra necesaria).
2. Corte de perfiles con sierra para inoxidable.
3. Preparación de bordes y chaflanes.
4. Soldadura TIG de barrotes a largueros.
5. Pulido de soldaduras (grado de cepillado).
6. Pulido final de toda la superficie (grano 240).
7. Montaje en obra (fijación con tacos químicos).
8. Retoques de pulido en obra.

## Paso 6: Mano de obra estimada

### Taller (fabricación)
- Corte y preparación: 0.5 h/ml = 6 h.
- Soldadura TIG: 2 h/ml = 24 h.
- Pulido y acabado: 1 h/ml = 12 h.
- Subtotal taller: 42 horas.

### Montaje en obra
- 2 operarios x 2 días = 32 horas.
- Desplazamiento: 2 h.
- Subtotal montaje: 34 horas.

## Paso 7: Complejidad

### Evaluación
- **Geométrica:** Media (recta, barrotes verticales, estándar). Factor: 1.1.
- **Materiales:** Alta (inoxidable AISI 316, soldadura TIG, pulido). Factor: 1.3.
- **Procesos:** Media-alta (corte, TIG, pulido, múltiples barrotes). Factor: 1.2.
- **Montaje:** Media (anclaje lateral, fachada con posible dificultad). Factor: 1.2.

**Puntuación:** 2+3+3+2 = 10 → Factor combinado: 1.3

## Paso 8: Riesgo

### Identificación
- Ambiente marino C5 → requiere AISI 316 validado.
- No se ha visitado obra → riesgo en anclajes.
- Plasma de entrega no especificado → se asume 2 semanas.

**Factor de riesgo:** 1.1 (bajo si se confirma material correcto).

## Paso 9: Coste técnico base

### Materiales
| Concepto | Importe |
|---|---|
| Tubo inoxidable AISI 316 Ø50 mm x 12.6 ml | 315 € |
| Tubo inoxidable AISI 316 Ø20 mm x 133 ml | 665 € |
| Perfil inoxidable AISI 316 40x20 x 25.2 ml | 252 € |
| Pletina inoxidable AISI 316 8 uds | 80 € |
| Tacos químicos inoxidable M12 x 8 | 48 € |
| Tornillería inoxidable A4 | 24 € |
| Consumibles (discos, hilo, gas) | 95 € |
| **Total materiales** | **1.479 €** |

### Mano de obra
| Concepto | Horas | Coste/hora | Importe |
|---|---|---|---|
| Taller | 42 | 35 € | 1.470 € |
| Montaje | 34 | 40 € | 1.360 € |
| **Total MO** | | | **2.830 €** |

### Resumen coste técnico base
| Concepto | Importe |
|---|---|
| Materiales | 1.479 € |
| Mano de obra | 2.830 € |
| Transporte | 120 € |
| **Coste técnico base** | **4.429 €** |
| Factor complejidad (1.3) | 5.758 € |
| Factor riesgo (1.1) | **6.334 €** |

## Paso 10: Margen

Tipo de producto: Barandilla especial (inoxidable, ambiente C5).

**Margen industrial:** 25%
**Margen comercial total:** 35%

Aplicado sobre coste técnico ajustado:
- Precio con margen: 6.334 € x 1.35 = **8.551 €**

## Paso 11: Ajuste oferta/demanda

Asumiendo taller al 70% de carga (estándar).
Sin urgencia expresada.
Cliente nuevo.

**Ajuste:** 0% (estándar).

## Paso 12: Presupuesto final

| Concepto | Importe |
|---|---|
| Coste técnico ajustado | 6.334 € |
| Margen comercial (35%) | 2.217 € |
| **Total base** | **8.551 €** |
| IVA (21%) | 1.796 € |
| **TOTAL PRESUPUESTO** | **10.347 €** |

## Paso 13: Dudas al cliente

1. ¿Confirma que desea **acero inoxidable AISI 316** en lugar de acero al carbono pintado? El inoxidable no se pinta, se deja en acabado cepillado natural.
2. **Altura exacta** de la barandilla (asumimos 100 cm).
3. **Número de tramos** (si es continua o tiene esquinas/interrupciones).
4. **Tipo de pasamanos** (asumimos tubo redondo Ø50 mm).
5. ¿Hay **visita a obra** para confirmar anclajes y accesos?

## Notas

- El ambiente marino C5 exige acero inoxidable AISI 316 o acero al carbono con galvanizado + pintura epoxi de alto rendimiento.
- El presupuesto asume que el soporte (forjado/fachada) está preparado para recibir los anclajes.
- No incluye reparación de soporte si está en mal estado.
- Garantía: 2 años en fabricación, 1 año en montaje (según condiciones generales).
