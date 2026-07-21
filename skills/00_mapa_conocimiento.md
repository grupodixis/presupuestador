# Mapa de conocimiento del presupuestador

## Objetivo

Mantener una base de conocimiento modular, auditable y evolutiva para que el agente pueda presupuestar trabajos actuales y ampliar sectores sin mezclar criterios.

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
- Carpintería de aluminio: ventanas y cerramientos como base.
- Procesos transversales: montaje, tratamientos superficiales, complejidad, revisión y oferta/demanda.
- Instalaciones como skill genérica.

### Falta profundizar

- Aluminio por sectores: mallorquinas, correderas, practicables, cerramientos, mosquiteras, persianas, vidrios, RPT, series y marcas.
- Electricidad por sectores: vivienda, local, nave, fotovoltaica auxiliar, cuadros, boletines, alumbrado, domótica.
- Fontanería por sectores: baños, cocinas, saneamiento, ACS, bombeo, pruebas de presión.
- Clima por sectores: split, multisplit, conductos, ventilación/extracción, aerotermia, mantenimiento.
- Márgenes por industria y tipo de cliente.
- Proveedores homologados por área y rangos de precio actualizados.

## Regla de evolución

Toda mejora debe clasificarse con estas etiquetas mínimas:

- Área: aluminio, carpinteria_metalica, instalaciones_electricas, fontaneria, clima, general u otra.
- Sector: producto o familia concreta.
- Tipo de conocimiento: coste, composición, criterio técnico, riesgo, pregunta, proveedor, margen o condición comercial.
- Estado: observado, validado, consolidado o descartado.
- Origen: usuario, presupuesto, proveedor, factura, catálogo o norma.

Cuando algo esté validado y se repita, debe dejar de vivir solo en aprendizaje y pasar a la skill o composición correspondiente.