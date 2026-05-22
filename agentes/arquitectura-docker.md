# Arquitectura Docker del agente presupuestador

## Objetivo

Ejecutar un agente de IA en un contenedor Docker capaz de trabajar sobre este repositorio y operar como asistente técnico-comercial de presupuestación.

## Componentes

| Componente | Función |
|---|---|
| Agente IA | Interpreta solicitudes, ejecuta skills y genera salidas |
| Repositorio montado | Fuente de conocimiento y destino de documentación actualizada |
| Motor de búsqueda local | Busca en Markdown, YAML, JSON y fichas de proveedores |
| Generador HTML/PDF | Produce presupuestos comerciales y previews internos |
| Módulo proveedores | Investiga, cualifica y prepara solicitudes de precio |
| Git | Versiona cambios metodológicos y documentación |

## Volúmenes recomendados

| Volumen | Uso |
|---|---|
| `/workspace` | Repositorio `Presupuestador` |
| `/output` | Presupuestos generados, PDFs y previews temporales |
| `/secrets` | Credenciales montadas como solo lectura si aplica |

## Variables de entorno previstas

| Variable | Uso |
|---|---|
| `AGENT_MODEL` | Modelo principal del agente |
| `AGENT_MODE` | `preview`, `commercial`, `research`, `maintenance` |
| `GIT_AUTHOR_NAME` | Autor para commits documentales |
| `GIT_AUTHOR_EMAIL` | Email para commits documentales |
| `EMAIL_DRAFT_ONLY` | Si es `true`, solo redacta emails sin enviarlos |
| `WHATSAPP_DRAFT_ONLY` | Si es `true`, solo redacta WhatsApps sin enviarlos |

## Permisos por modo

| Modo | Puede leer | Puede escribir | Puede enviar externo | Puede hacer commit |
|---|---|---|---|---|
| `preview` | Sí | Solo `/output` | No | No |
| `commercial` | Sí | Presupuestos HTML/PDF | No | No |
| `research` | Sí | `proveedores/`, borradores | No | Opcional |
| `maintenance` | Sí | Documentación | No | Sí, con aprobación |

## Flujo de arranque

1. Iniciar contenedor con el repositorio montado.
2. Indexar documentación local.
3. Validar que existen carpetas clave: `skills/`, `presupuestacion/`, `productos/`, `proveedores/`, `plantillas/`.
4. Cargar reglas comerciales por defecto.
5. Esperar tarea: presupuesto, proveedor, revisión o actualización documental.

## Flujo de salida

1. Generar presupuesto preview interno si hay incertidumbre.
2. Generar presupuesto cliente si se puede cerrar alcance.
3. Si faltan costes, crear solicitudes a proveedores.
4. Si se aprende un criterio nuevo, proponer cambio documental.
5. Mostrar diff antes de commit.

## Seguridad

- No almacenar credenciales dentro del repositorio.
- No subir presupuestos con datos personales sin aprobación.
- No enviar emails o WhatsApps sin confirmación humana.
- No actualizar precios globales sin fecha y fuente.
- No sobrescribir documentación sin diff revisable.
