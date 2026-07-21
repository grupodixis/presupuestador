# Skills de presupuestación

Esta carpeta es el punto de entrada del agente para presupuestar. La organización separa tres capas:

1. **Skills base**: procedimiento general, revisión, complejidad, montaje, tratamientos, oferta/demanda y proveedores.
2. **Áreas de negocio**: aluminio, carpintería metálica, instalaciones eléctricas, fontanería, clima y futuras industrias.
3. **Aprendizaje**: criterios observados en presupuestos reales y correcciones realizadas por usuarios.

## Mapa operativo

| Área | Estado | Entrada principal | Sectores incluidos |
|---|---|---|---|
| Aluminio | Activa | `areas/aluminio/README.md` | ventanas, puertas, cerramientos, mallorquinas, pergolas/parasoles, vidrio asociado |
| Carpintería metálica | Activa | `areas/carpinteria_metalica/README.md` | barandillas, rejas, puertas, cancelas, escaleras, estructuras, herrería, marquesinas |
| Instalaciones eléctricas | Preparada | `areas/instalaciones_electricas/README.md` | cuadros, líneas, mecanismos, iluminación, fotovoltaica auxiliar, legalización |
| Fontanería | Preparada | `areas/fontaneria/README.md` | agua fría/caliente, saneamiento, ACS, sanitarios, pruebas |
| Clima | Preparada | `areas/clima/README.md` | splits, conductos, ventilación, extracción, RITE, puesta en marcha |
| Otras industrias | Abierta | `areas/otras_industrias/README.md` | sectores nuevos que se quieran atacar |

## Skills existentes

| Archivo | Tipo | Uso |
|---|---|---|
| `skill_presupuestacion_general.md` | base | Cargar siempre primero. Define flujo, partidas y prudencia comercial. |
| `skill_revision_presupuesto.md` | base | Cargar antes de guardar o imprimir. Detecta omisiones y riesgos. |
| `skill_complejidad.md` | base | Ajusta horas, riesgo y margen por dificultad. |
| `skill_montaje_en_obra.md` | proceso | Montaje, acceso, medios auxiliares, sellados y remates. |
| `skill_tratamientos_superficiales.md` | proceso | Pintura, galvanizado, imprimación, lacado, anodizado y ambiente marino. |
| `skill_oferta_demanda.md` | comercial | Ajustes por urgencia, carga de trabajo y oportunidad. |
| `skill_solicitud_presupuestos_proveedores.md` | proveedores | Pedir precios claros a proveedores. |
| `skill_investigacion_proveedores.md` | proveedores | Buscar y cualificar proveedores. |
| `skill_carpinteria_aluminio.md` | área/producto | Aluminio y cerramientos. Complementar con `areas/aluminio/README.md`. |
| `skill_barandillas.md` | producto | Barandillas metálicas. Complementar con carpintería metálica. |
| `skill_rejas.md` | producto | Rejas y protecciones. |
| `skill_puertas_metalicas.md` | producto | Puertas metálicas. |
| `skill_portones_cancelas.md` | producto | Portones y cancelas. |
| `skill_escaleras.md` | producto | Escaleras metálicas. |
| `skill_estructuras_metalicas.md` | producto | Estructuras metálicas. |
| `skill_herreria.md` | producto | Herrería funcional/decorativa. |
| `skill_marquesinas_pergolas.md` | producto | Marquesinas, pérgolas y toldos. |
| `skill_productos_compuestos.md` | transversal | Trabajos con varios oficios, materiales o interfaces. |
| `skill_instalaciones.md` | área genérica | Instalaciones eléctricas, fontanería y clima hasta que se creen skills específicas completas. |

## Orden de carga recomendado

1. `skill_presupuestacion_general.md`.
2. Área correspondiente en `skills/areas/.../README.md`.
3. Skill específica del producto o proceso.
4. Composición YAML en `productos/composiciones/`.
5. Costes y proveedores en `presupuestacion/costes/` y `proveedores/`.
6. Aprendizaje relevante en `skills/aprendizaje/`.
7. `skill_revision_presupuesto.md` antes de guardar.

## Cómo debe crecer esta base

- Una corrección puntual del usuario se guarda primero en `skills/aprendizaje/aprendizaje_<area>.md`.
- Si el criterio se repite o es estable, se consolida en la skill del área o del producto.
- Si aparecen costes fiables, se pasan a `presupuestacion/costes/` o a fichas de proveedor.
- Si aparece un nuevo tipo de trabajo, se registra en `areas/otras_industrias/` hasta tener suficiente material para crear su área propia.