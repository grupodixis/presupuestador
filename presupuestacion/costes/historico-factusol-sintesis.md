# Sintesis historica FACTUSOL

Fuente: backups locales FACTUSOL `0012015.accdb` a `0012026.accdb` y `0022022.accdb` a `0022023.accdb`.

Esta sintesis es memoria anonima para presupuestacion. No contiene nombres de clientes, obras ni numeros de factura. Los datos completos quedan en `datos-privados/factusol/` y no deben subirse a GitHub.

## Volumen analizado

- Bases Access analizadas: 14.
- Lineas de factura extraidas: 7.497.
- Lineas con fiabilidad alta para reglas: 4.783.
- Lineas con fiabilidad media: 1.001.
- Lineas con fiabilidad baja: 906.
- Lineas excluidas: 795.
- Partidas agrupadas por texto: 4.961.

## Criterio de fiabilidad

| Fiabilidad | Uso |
|---|---|
| Alta | Linea con descripcion, cantidad, precio unitario e importe. Puede usarse como referencia directa si el contexto encaja. |
| Media | Linea con importe y descripcion, pero unidad o alcance poco claro. Usar como referencia comercial o revisar manualmente. |
| Baja | Certificacion global, anticipo, importe sin desglose o linea con datos incompletos. No usar para precio unitario. |
| Excluir | Actividad no industrial para este sistema o ruido contable/fiscal. |

## Familias detectadas

Importe total y mediana son importes de linea historicos, no coste tecnico ni precio recomendado automatico.

| Familia | Lineas | Directas | Importe total | Mediana linea | Unidades frecuentes |
|---|---:|---:|---:|---:|---|
| Electricidad / telecomunicaciones | 1.351 | 1.155 | 1.064.117 EUR | 212 EUR | h, cantidad FACTUSOL, ud/lote, ud, m2 |
| Equipamiento aeroportuario / electronico | 617 | 569 | 950.931 EUR | 177 EUR | ud/lote, h, cantidad FACTUSOL, ud, ml |
| Estructuras metalicas | 418 | 385 | 1.146.059 EUR | 511 EUR | cantidad FACTUSOL, kg, ud/lote, ml, h |
| Mantenimiento / reparacion | 365 | 271 | 62.401 EUR | 65 EUR | ud/lote, h, lote, cantidad FACTUSOL |
| Puertas / portones / cancelas | 286 | 261 | 406.886 EUR | 475 EUR | ud/lote, cantidad FACTUSOL, h, ud |
| Acero inoxidable | 277 | 250 | 169.720 EUR | 96 EUR | cantidad FACTUSOL, ud/lote, ud, h, ml |
| Pasarelas / plataformas | 241 | 202 | 674.266 EUR | 212 EUR | ud/lote, cantidad FACTUSOL, h, ml, m2 |
| Montaje / instalacion | 228 | 198 | 196.195 EUR | 135 EUR | ud/lote, h, cantidad FACTUSOL, ud |
| Transporte / desplazamientos | 211 | 173 | 38.653 EUR | 40 EUR | ud/lote, kg, cantidad FACTUSOL, lote, h |
| Materiales genericos | 194 | 173 | 160.578 EUR | 48 EUR | cantidad FACTUSOL, ud/lote, ml, kg, ud |
| Cerrajeria / herreria general | 180 | 172 | 58.797 EUR | 71 EUR | h, ud/lote, ud |
| Galvanizado / pintura / acabados | 165 | 152 | 184.423 EUR | 220 EUR | cantidad FACTUSOL, ud/lote, ml, h, ud |
| Climatizacion / ventilacion | 162 | 150 | 430.346 EUR | 200 EUR | h, ud/lote, cantidad FACTUSOL, ud, ml |
| Barandillas / pasamanos | 167 | 135 | 358.678 EUR | 1.080 EUR | cantidad FACTUSOL, ud/lote, ml, h, ud |
| Chapa / plegado / corte | 140 | 131 | 169.447 EUR | 140 EUR | cantidad FACTUSOL, ud/lote, ud, m2, ml |
| Rejas / protecciones | 102 | 95 | 223.248 EUR | 302 EUR | ud/lote, cantidad FACTUSOL, h, ud, m2 |
| Mano de obra herreria | 104 | 90 | 25.337 EUR | 82 EUR | h, ud/lote |
| Aluminio / carpinteria aluminio | 91 | 86 | 154.130 EUR | 489 EUR | ud/lote, cantidad FACTUSOL, ud, kg, h |
| Pergolas / marquesinas / cubiertas | 114 | 79 | 1.058.885 EUR | 2.000 EUR | ud/lote, cantidad FACTUSOL, ud, m2, lote |
| Escaleras / peldaños | 49 | 47 | 72.756 EUR | 313 EUR | ud/lote, h, cantidad FACTUSOL, ml, ud |
| Certificaciones globales sin detalle | 53 | 9 | 532.366 EUR | 7.575 EUR | ud/lote, lote, cantidad FACTUSOL, ud |
| Otros / pendiente clasificar | 1.225 | 0 | 488.628 EUR | 30 EUR | cantidad FACTUSOL, ud/lote, ud, h, lote |
| Web / dominios / hosting | 745 | 0 | 28.862 EUR | 35 EUR | ud/lote, cantidad FACTUSOL, h, lote |

## Reglas de uso para presupuestar

- Usar el historico FACTUSOL como referencia comercial de precios facturados, no como coste base directo.
- Comparar siempre contra coste tecnico calculado: materiales, mano de obra, tratamientos, transporte, montaje y margen.
- Para lineas con unidad `h`, se puede usar como referencia de tarifa historica de mano de obra.
- Para lineas con unidad `ml`, `m2`, `kg` o `ud`, usar solo si la descripcion incluye alcance comparable.
- Las medianas por familia son orientativas: mezclan trabajos pequenos, reparaciones, suministros y lotes.
- No usar certificaciones globales, anticipos ni trabajos sin desglose para extraer precios unitarios.
- `Web / dominios / hosting` queda excluido del sistema industrial salvo peticion expresa.

## Familias prioritarias para reglas del sistema

Alta prioridad porque encajan con el objetivo del presupuestador y tienen volumen suficiente:

- Estructuras metalicas.
- Puertas / portones / cancelas.
- Acero inoxidable.
- Barandillas / pasamanos.
- Galvanizado / pintura / acabados.
- Chapa / plegado / corte.
- Rejas / protecciones.
- Aluminio / carpinteria aluminio.
- Pergolas / marquesinas / cubiertas.
- Mano de obra herreria.
- Montaje / instalacion.
- Transporte / desplazamientos.

Prioridad media o uso contextual:

- Pasarelas / plataformas.
- Cerrajeria / herreria general.
- Mantenimiento / reparacion.
- Materiales genericos.
- Climatizacion / ventilacion.
- Equipamiento aeroportuario / electronico.
- Electricidad / telecomunicaciones.

## Metodo recomendado en una nueva presupuestacion

1. Detectar familia del trabajo por keyword.
2. Calcular coste tecnico base con reglas actuales.
3. Consultar historico FACTUSOL por familia y texto similar.
4. Separar lineas de alta fiabilidad de lineas globales o certificaciones.
5. Usar historico para validar el precio comercial, no para sustituir el calculo tecnico.
6. Si el precio tecnico se aleja mucho del historico, explicar el motivo: alcance, medidas, tratamiento, montaje, urgencia o riesgo.

## Archivos locales privados relacionados

No subir a GitHub:

- `datos-privados/factusol/historico-facturas-factusol.csv`
- `datos-privados/factusol/referencia-precios-partidas-factusol.csv`
- `datos-privados/factusol/tipos-trabajo-factusol.csv`
- `datos-privados/factusol/lineas-clasificadas-factusol.csv`
- `datos-privados/factusol/referencia-presupuestacion-limpia.csv`
- `datos-privados/factusol/resumen-presupuestacion-limpia.csv`
- `datos-privados/factusol/visor-factusol.html`
- `datos-privados/factusol/tipos-trabajo-factusol.html`
- `datos-privados/factusol/presupuestacion-limpia-factusol.html`
