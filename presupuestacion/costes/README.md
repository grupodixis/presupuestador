# Costes

Tablas, factores y criterios para calcular el coste técnico base de un producto o partida.

## Componentes del coste

| Componente | Descripción |
|---|---|
| Materiales principales | Acero, aluminio, inoxidable, vidrio, etc. |
| Materiales auxiliares | Tornillería, anclajes, consumibles |
| Mano de obra de taller | Horas de fabricación |
| Mano de obra de montaje | Horas de instalación en obra |
| Maquinaria | Uso de equipos: corte, soldadura, plegado |
| Tratamientos externos | Pintura, galvanizado, anodizado, chorreado |
| Transporte | Portes a obra |
| Diseño técnico | Horas de oficina técnica |
| Medición y replanteo | Visita a obra, topografía |
| Controles de calidad | Ensayos, certificados |
| Mermas | Porcentaje sobre materiales |

## Archivos de costes

Se pueden crear archivos específicos para:

- `costes-materiales.md` — precios, medidas estándar y cálculo de mermas (documento principal).
- `costes-materiales.json` — precios en formato estructurado.
- `costes-mo.json` — tarifas de mano de obra por categoría.
- `costes-maquinaria.json` — coste horario de maquinaria.
- `costes-tratamientos.json` — precios de tratamientos externos.
- `costes-transporte.json` — tarifas de transporte.
- `proveedores.md` — flujo de petición de precios a proveedores (Notion + email).
- `proveedores-conocidos.md` — catálogo de proveedores habituales (Ferros Puig Sallent, corte láser, etc.).
- `historico-ferros-puig.md` — precios reales extraidos de presupuestos/pedidos de Ferros Puig.

## Criterios generales

- Los precios de materiales deben actualizarse periódicamente.
- La mano de obra incluye cargas sociales y Seguridad Social.
- El coste de maquinaria incluye amortización, mantenimiento y energía.
- Los tratamientos externos deben pedirse como coste real de proveedor.
- Las mermas estándar son del 5-10% según el producto.
- El **transporte peninsular** debe calcularse según el peso real o volumétrico.
- La **ruta Barcelona → Menorca** tiene un coste de referencia de **0.20 €/kg** (ver `costes-transporte.json`).
