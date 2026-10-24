# P-2026-0017 - Cancela corredera + puerta peatonal CORTIZO (3 diseños x 3 colores)

Sustitución de la cancela corredera y la puerta peatonal de madera por aluminio CORTIZO Portales con motor nuevo.
Fotomontajes sobre la foto del cliente en `img/`.

| Dato | Valor |
|---|---|
| Fecha | 19/10/2026 |
| Cliente | Florerine Laurent · +44 7763 526090 |
| Obra | Calle Baixada a la mar, 6 · 07713 Son Ganxo, Sant Lluís (Menorca) |
| Hueco cancela | 3.435 x 1.800 mm (hoja 3.585 x 1.800) |
| Hueco peatonal | 985 x 1.800 mm |
| Colores | Blanco RAL 9016 · Gris antracita RAL 7016 · Verde carruaje (código pendiente) |

## Precios (base imponible, motor incluido) · tarifas presupuestos.alufac.es

| Diseño | Blanco | Gris antracita | Verde carruaje |
|---|---:|---:|---:|
| A · Portales lama ciega COR-2290 | 6.553,94 € | 6.980,30 € | 6.980,30 € |
| B · Portales + Mallorquina lamas fijas | 7.489,90 € | 7.927,47 € | 7.927,47 € |
| C · Portales + rejas 100x20 cada 100 | 5.982,82 € | 6.295,05 € | 6.295,05 € |

## Origen de datos
- Pesos y referencias: catálogos oficiales Cortizo Portales (05/2022) y Mallorquina (02/2024), en `alufac-presupuestos/data/documents/cortizo/`.
- Tarifas de presupuestos.alufac.es: aluminio 9 €/kg, taller 40 €/h, montaje 45 €/h, transporte 100 €/obra, GG 15 %, margen 20 % (venta = coste × 1,15 / 0,80 + transporte).
- Herrajes, cerrajería y material del motor: P-2026-0016.
- Recargo color RAL 7016 / verde carruaje +2 €/kg (confirmado por ALUFAC; la app no lo contempla).
- Bisagras peatonal (105 €) y accesorios Mallorquina (60 %): skill costes-aluminio-cortizo.

## Pendientes antes de enviar o fabricar
- Email del cliente (no facilitado).
- Código del verde carruaje en la carta Cortizo.
- Tubo 100x20: espesor y proveedor (peso teórico 1,253 kg/m con 2 mm).
- Diseño B: validar con TSAC Baleares la unión Portales + Mallorquina.
- Medición en obra.
- Horas de taller de B y C (estimadas).

Regenerar: `python fuentes/calc.py && python fuentes/render.py && python fuentes/render3d.py && python fuentes/gen_html.py <carpeta>` (ejecutar desde la carpeta con `foto.png`).
