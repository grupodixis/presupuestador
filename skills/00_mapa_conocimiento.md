# Mapa de conocimiento del presupuestador

## Objetivo

Mantener una base de conocimiento modular, auditable y evolutiva para que el agente presupueste herrería y carpintería metálica sin mezclar criterios de otras industrias.

## Capas de conocimiento

| Capa | Carpeta | Qué contiene | Quién la actualiza |
|---|---|---|---|
| Procedimiento | `skills/skill_*.md` | Cómo razona el agente y qué debe comprobar | Usuario/admin, con IA si procede |
| Áreas | `skills/areas/` | Mapa por industria, sectores, estado y faltantes | Usuario/admin |
| Composiciones | `productos/composiciones/` | Partidas tipo, materiales y procesos recurrentes | Usuario/admin |
| Costes | `presupuestacion/costes/` | Precios, históricos y rangos de referencia | Usuario/admin tras validación |
| Proveedores | `proveedores/` | Fichas, contactos y criterios de compra | Usuario/admin |
| Aprendizaje | `skills/aprendizaje/` | Correcciones reales y criterios observados en uso | App + usuario/admin |

## Estado actual resumido

### Cubierto razonablemente

- Presupuestación general.
- Carpintería metálica: barandillas, rejas, puertas, cancelas, escaleras, estructuras, herrería, marquesinas y pérgolas.
- Procesos transversales: montaje, tratamientos superficiales, complejidad, revisión y oferta/demanda.

### Falta profundizar

- Márgenes por industria y tipo de cliente.
- Proveedores homologados por área y rangos de precio actualizados.

### Archivado para otra app

- Carpintería de aluminio, ALUFAC, CORTIZO, mallorquinas, ventanas, cerramientos y precios asociados viven en `archivo-carpinteria-aluminio/`.
- Esta app no debe cargar ni aplicar ese conocimiento en presupuestos nuevos.

## Regla de evolución

Toda mejora debe clasificarse con estas etiquetas mínimas:

- Área: carpinteria_metalica, general u otra.
- Sector: producto o familia concreta.
- Tipo de conocimiento: coste, composición, criterio técnico, riesgo, pregunta, proveedor, margen o condición comercial.
- Estado: observado, validado, consolidado o descartado.
- Origen: usuario, presupuesto, proveedor, factura, catálogo o norma.

Cuando algo esté validado y se repita, debe dejar de vivir solo en aprendizaje y pasar a la skill o composición correspondiente.
