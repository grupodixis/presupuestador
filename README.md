# Entorno de Presupuestación Técnica y Comercial

Repositorio de conocimiento, reglas y procedimientos para que un agente IA genere presupuestos técnicos de artículos industriales fabricados a medida.

## Visión evolutiva

Este repositorio está pensado como la base documental de un futuro agente dockerizado de presupuestación, capaz de presupuestar, investigar proveedores, solicitar precios y actualizar su metodología de forma versionada y auditable.

Ver `/agentes/` para la arquitectura objetivo del agente.

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
├── agentes/                  # Arquitectura del agente dockerizado de presupuestación
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
├── proveedores/              # I+D, fichas y búsqueda de proveedores
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
6. Detectar materiales o servicios sin precio fiable.
7. Si faltan precios, consultar o investigar proveedores en `/proveedores/`.
8. Estimar mano de obra.
9. Evaluar complejidad.
10. Evaluar riesgos.
11. Evaluar montaje.
12. Evaluar tratamientos externos.
13. Calcular coste técnico base.
14. Aplicar margen industrial.
15. Ajustar precio según oferta/demanda.
16. Generar una explicación clara del presupuesto.
17. Indicar dudas o datos faltantes.

## Convenciones del repositorio

- Los archivos Markdown contienen conocimiento estructurado para el agente.
- Los archivos YAML contienen datos estructurados (composiciones, costes, etc.).
- Los archivos JSON se usan para tablas de datos o configuraciones.
- Cada carpeta tiene un README.md explicando su finalidad.
- Las skills en `/skills/` son el punto de entrada del agente para cada tipo de trabajo.
