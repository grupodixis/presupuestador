# Entorno de presupuestación técnica y comercial

Repositorio de conocimiento, reglas, costes, proveedores y procedimientos para que un agente IA genere presupuestos técnicos y comerciales de trabajos industriales, instalaciones y productos fabricados a medida.

## Visión

El repositorio debe funcionar como una base de conocimiento viva:

- El agente consulta skills, composiciones, costes y proveedores antes de presupuestar.
- El usuario corrige líneas, precios, cantidades, condiciones o criterios.
- La app guarda esas correcciones como aprendizaje por área.
- Los aprendizajes repetidos o validados se consolidan en skills, composiciones, costes o fichas de proveedor.

## Áreas objetivo

| Área | Estado | Carpeta |
|---|---|---|
| Aluminio | activa | `skills/areas/aluminio/` |
| Carpintería metálica | activa | `skills/areas/carpinteria_metalica/` |
| Instalaciones eléctricas | preparada | `skills/areas/instalaciones_electricas/` |
| Fontanería | preparada | `skills/areas/fontaneria/` |
| Clima | preparada | `skills/areas/clima/` |
| Otras industrias | incubadora | `skills/areas/otras_industrias/` |

## Estructura del repositorio

```text
/
├── README.md                         # Mapa general del repositorio
├── agentes/                          # Arquitectura, permisos y flujo del agente
├── skills/                           # Skills, áreas y aprendizaje del agente
│   ├── README.md                     # Índice operativo de skills
│   ├── 00_mapa_conocimiento.md       # Qué hay, qué falta y cómo evoluciona
│   ├── areas/                        # Organización por industria y sector
│   └── aprendizaje/                  # Memoria viva por área
├── productos/                        # Catálogo técnico de productos
│   ├── composiciones/                # Composición típica por producto
│   └── reglas-tecnicas/              # Reglas técnicas por familia
├── presupuestacion/                  # Criterios comerciales, costes y márgenes
│   ├── costes/                       # Costes, históricos y proveedores conocidos
│   ├── margenes/                     # Política de márgenes
│   ├── oferta-demanda/               # Ajustes por demanda/capacidad
│   └── checklists/                   # Listas de revisión
├── proveedores/                      # I+D, fichas y búsqueda de proveedores
├── plantillas/                       # Plantillas de salida y comunicación
├── presupuestos/                     # Presupuestos generados
├── ejemplos/                         # Ejemplos de presupuestos completos
└── glosario/                         # Términos técnicos y comerciales
```

## Flujo de trabajo del agente IA

1. Identificar área, sector y tipo de producto.
2. Cargar `skills/skill_presupuestacion_general.md`.
3. Cargar el README del área en `skills/areas/`.
4. Cargar la skill específica del producto o proceso.
5. Consultar composición YAML en `productos/composiciones/`.
6. Consultar costes, históricos y proveedores.
7. Generar líneas de presupuesto editables con cantidades, unidades, precios e importes.
8. Mostrar supuestos, riesgos, preguntas y sugerencias memorizables.
9. Registrar cambios reales del usuario en `skills/aprendizaje/`.
10. Revisar y consolidar aprendizajes validados en skills, composiciones o costes.

## Convenciones

- Markdown (`.md`) para conocimiento, criterios, instrucciones y aprendizaje.
- YAML (`.yaml`) para composiciones de productos.
- JSON (`.json`) para costes, configuración y datos estructurados.
- Los aprendizajes automáticos son observaciones, no verdades definitivas.
- Todo aprendizaje importante debe poder trazarse a un presupuesto, proveedor, factura, catálogo o decisión del usuario.