# Extracciones de correos para costes y catalogos - 2026-08-18

## Alcance

- Revisado: `grupodixis@gmail.com`.
- Pendiente: `pablo@dixis.es` y `administracion@dixis.es`, ambos Microsoft 365.
- Criterio: estos datos son candidatos. No deben marcarse como `confirmado` sin validacion humana o contraste con tarifa vigente.
- Las extracciones de carpinteria de aluminio se archivaron en `archivo-carpinteria-aluminio/`.

## Candidatos para lista de precios

### Carpinteria metalica / estructura y cerramientos

Fuente: Gmail `grupodixis@gmail.com`, remitente Patec / Joan Mestres, asunto `ES CASTELL (Illes Balears) .... Pablo Sanchez.`, PDF `Presupuesto.pdf`, fecha del documento `04/08/2026`.

| categoria | area | nombre | unidad | precio candidato | confianza | notas |
| --- | --- | --- | --- | ---: | --- | --- |
| producto | carpinteria_metalica | Nave deportiva: estructura metalica laminada soldada, cerramientos, cubierta y puerta corredera | m2_planta | 263.89 | pendiente | Total 66500 EUR para 252 m2 de planta. Incluye estructura, chapa cubierta 0.6 mm, cerramientos, remates, puerta corredera, calculo, pintura y montaje. Excluir IVA y revisar transporte/alcance antes de usar. |

## Candidatos de catalogo pendientes de lectura

- ZaraCLIMA: `PRESUPUESTO VENTILADORES DE GRAN CAUDAL VENTIGRAN VGX y PLENUM ASPIRACION`, PDF `fra PROFORMA GA 192007v3.pdf`, posible base para futura area de clima/ventilacion. No cargar en presupuestos de herreria salvo que sea un elemento auxiliar del trabajo metalico.

## Reglas para importar

- Usar `confidence: antiguo` cuando el documento sea historico.
- Usar `confidence: pendiente` en precios derivados por m2/ml o cuando el alcance combine materiales, fabricacion y montaje.
- No sustituir precios confirmados actuales sin revisar fecha, proveedor, transporte, descuentos, IVA y unidad real.
- Guardar siempre `supplier`, `source`, fecha del documento y nombre del PDF en notas para trazabilidad.
