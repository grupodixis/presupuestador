# Skills de Presupuestación

Cada archivo Markdown en esta carpeta define una habilidad (skill) que el agente IA debe activar según el tipo de producto o situación.

## Lista de skills

| Archivo | Propósito |
|---|---|
| `skill_presupuestacion_general.md` | Procedimiento base para cualquier presupuesto |
| `skill_barandillas.md` | Presupuestación de barandillas metálicas |
| `skill_puertas_metalicas.md` | Presupuestación de puertas metálicas |
| `skill_estructuras_metalicas.md` | Presupuestación de estructuras metálicas |
| `skill_carpinteria_aluminio.md` | Presupuestación de carpintería de aluminio |
| `skill_instalaciones.md` | Presupuestación de instalaciones (elec, font, clima) |
| `skill_montaje_en_obra.md` | Evaluación y coste del montaje en obra |
| `skill_tratamientos_superficiales.md` | Tratamientos: pintura, galvanizado, chorreado, etc. |
| `skill_oferta_demanda.md` | Ajuste de precio por oferta y demanda |
| `skill_complejidad.md` | Evaluación de complejidad de fabricación |
| `skill_revision_presupuesto.md` | Revisión final del presupuesto antes de enviar |
| `skill_escaleras.md` | Presupuestación de escaleras metálicas |
| `skill_herreria.md` | Herrería artística y funcional (forja, decoración) |
| `skill_rejas.md` | Rejas de protección (ventanas, puertas, locales) |
| `skill_portones_cancelas.md` | Portones y cancelas metálicas (vehiculares, peatonales) |
| `skill_marquesinas_pergolas.md` | Marquesinas, pérgolas y toldos |
| `skill_productos_compuestos.md` | Productos que combinan múltiples materiales y oficios |
| `skill_solicitud_presupuestos_proveedores.md` | Redacción de emails y WhatsApps para pedir precios a proveedores |

## Estructura de cada skill

Cada skill sigue esta plantilla:

- **Cuándo usar esta skill**
- **Datos mínimos necesarios**
- **Datos recomendados**
- **Criterios técnicos**
- **Composición habitual del producto**
- **Procesos habituales**
- **Factores que aumentan el coste**
- **Factores que aumentan la complejidad**
- **Factores de riesgo**
- **Errores frecuentes a evitar**
- **Preguntas que el agente debe hacerse**
- **Checklist final**
- **Formato de salida recomendado**

## Uso

Cuando el agente recibe una descripción de trabajo, debe:

1. Identificar el tipo de producto.
2. Cargar la skill correspondiente.
3. Si aplican varias skills (ej. barandilla + montaje en obra), cargarlas secuencialmente.
4. Seguir el procedimiento de la skill paso a paso.
