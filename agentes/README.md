# Agentes de presupuestación

Este módulo define la arquitectura objetivo para convertir la documentación del repositorio en un agente operativo de presupuestación.

## Visión

El objetivo no es solo generar documentos estáticos, sino construir un agente dockerizado capaz de:

1. Presupuestar trabajos técnicos y comerciales.
2. Detectar datos faltantes o costes no fiables.
3. Investigar proveedores existentes o nuevos.
4. Redactar emails y WhatsApps para solicitar precios.
5. Incorporar respuestas de proveedores a los costes.
6. Aprender de cada presupuesto y proponer mejoras a la documentación.
7. Mantener una metodología viva, versionada y auditable en Git.

## Agente objetivo

El agente podrá implementarse con OpenClaw, Hermes u otra base compatible, siempre que cumpla estas condiciones:

- Ejecutarse en Docker.
- Tener acceso controlado al repositorio de documentación.
- Poder leer costes, skills, plantillas, proveedores y ejemplos.
- Poder generar presupuestos HTML/PDF y previews internos.
- Poder preparar comunicaciones a proveedores.
- Poder proponer cambios documentales mediante Git.
- No enviar correos, WhatsApps ni modificar datos críticos sin aprobación humana.

## Principios

- La documentación del repositorio es la fuente de verdad metodológica.
- El agente debe justificar presupuestos con criterios trazables.
- Los precios reales de proveedor deben registrar fecha, condiciones, IVA y transporte.
- Los datos personales de clientes no deben subirse a Git salvo autorización expresa.
- Los cambios en metodología deben ser revisables mediante diff y commit.

## Módulos relacionados

| Módulo | Uso por el agente |
|---|---|
| `skills/` | Procedimientos de actuación por tarea o producto |
| `productos/` | Composición técnica de productos |
| `presupuestacion/` | Costes, márgenes, complejidad y criterios comerciales |
| `proveedores/` | I+D, fichas, búsquedas y cualificación de proveedores |
| `plantillas/` | Salidas de presupuesto, email y WhatsApp |
| `ejemplos/` | Casos de prueba y presupuestos de referencia |

## Estados del sistema

| Estado | Descripción |
|---|---|
| Documental | El agente usa Markdown/YAML/JSON como base de conocimiento |
| Semiautomático | El agente genera presupuestos y comunicaciones, humano aprueba envío |
| Integrado | El agente consulta proveedores, actualiza fichas y genera propuestas de cambio |
| Autónomo supervisado | El agente ejecuta flujos completos con permisos y auditoría |

## Siguiente paso técnico

Crear una imagen Docker con:

- Runtime del agente elegido.
- Montaje del repositorio como volumen.
- Configuración de permisos.
- Variables de entorno para credenciales externas.
- Comandos para presupuestar, investigar proveedores y actualizar documentación.
