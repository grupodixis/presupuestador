# Entorno de Presupuestación Técnica y Comercial

Repositorio de conocimiento, reglas y procedimientos para que un agente IA genere presupuestos técnicos de artículos industriales fabricados a medida.

## Propósito

Este entorno permite presupuestar cualquier producto o partida considerando:

1. Composición técnica real del producto.
2. Materiales, mano de obra, maquinaria, tratamientos, transporte y montaje.
3. Complejidad de fabricación.
4. Riesgo técnico.
5. Capacidad productiva actual.
6. Oferta y demanda.
7. Margen objetivo.
8. Urgencia del cliente.
9. Tipo de cliente.
10. Histórico de criterios y reglas de presupuestación.

## Ámbito de la empresa

- Estructuras metálicas.
- Herrería.
- Barandillas.
- Puertas metálicas.
- Escaleras.
- Carpintería de aluminio.
- Cerramientos.
- Instalaciones de electricidad, fontanería y climatización.
- Productos compuestos fabricados a medida.

## Estructura del repositorio

```
/
├── README.md                 # Este archivo
├── skills/                   # Habilidades de presupuestación del agente
├── productos/                # Catálogo técnico de productos
│   ├── composiciones/        # Composición típica de cada producto
│   └── reglas-tecnicas/      # Reglas técnicas por tipo de producto
├── presupuestacion/          # Lógica y criterios de presupuestación
│   ├── costes/               # Costes de materiales, MO, maquinaria, etc.
│   ├── margenes/             # Política de márgenes
│   ├── oferta-demanda/       # Ajustes por oferta y demanda
│   ├── complejidad/          # Evaluación de complejidad
│   └── checklists/           # Listas de verificación
├── plantillas/               # Plantillas de salida
├── ejemplos/                 # Ejemplos de presupuestos completos
└── glosario/                 # Términos técnicos y comerciales
```

## Flujo de trabajo del agente IA

1. Identificar el tipo de producto.
2. Buscar la skill correspondiente en `/skills/`.
3. Consultar la composición típica en `/productos/composiciones/`.
4. Detectar materiales principales.
5. Detectar procesos necesarios.
6. Estimar mano de obra.
7. Evaluar complejidad.
8. Evaluar riesgos.
9. Evaluar montaje.
10. Evaluar tratamientos externos.
11. Calcular coste técnico base.
12. Aplicar margen industrial.
13. Ajustar precio según oferta/demanda.
14. Generar una explicación clara del presupuesto.
15. Indicar dudas o datos faltantes.

## Convenciones del repositorio

- Los archivos Markdown contienen conocimiento estructurado para el agente.
- Los archivos YAML contienen datos estructurados (composiciones, costes, etc.).
- Los archivos JSON se usan para tablas de datos o configuraciones.
- Cada carpeta tiene un README.md explicando su finalidad.
- Las skills en `/skills/` son el punto de entrada del agente para cada tipo de trabajo.
