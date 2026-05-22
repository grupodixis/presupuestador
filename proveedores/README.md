# Proveedores e I+D

Módulo para investigar, cualificar y mantener datos de proveedores útiles para la presupuestación.

## Propósito

Permitir que el agente IA pueda:

1. Detectar materiales o servicios sin precio fiable.
2. Buscar proveedores existentes o nuevos proveedores potenciales.
3. Completar fichas de proveedor con datos de contacto y capacidades.
4. Evaluar si un proveedor sirve para una partida concreta.
5. Preparar emails o WhatsApps para pedir precios reales.
6. Registrar respuestas para alimentar costes futuros.

## Estructura

| Carpeta / Archivo | Propósito |
|---|---|
| `fichas/` | Fichas individuales de proveedores validados o candidatos |
| `busquedas/` | Registro de búsquedas realizadas y proveedores encontrados |
| `categorias.md` | Categorías de materiales y servicios a investigar |
| `checklist-cualificacion.md` | Checklist para decidir si un proveedor es útil |
| `plantilla-ficha-proveedor.md` | Formato estándar para crear fichas de proveedor |

## Flujo de uso

1. El presupuesto detecta una partida con precio incierto.
2. Se consulta si ya existe proveedor en `fichas/`.
3. Si no existe o falta información, se realiza I+D de proveedores.
4. Se crea o actualiza una ficha de proveedor.
5. Se prepara contacto usando las plantillas de `plantillas/`.
6. Cuando el proveedor responde, se registran precios, plazos y condiciones.

## Estados de proveedor

| Estado | Significado |
|---|---|
| `candidato` | Encontrado, pendiente de contacto o validación |
| `contactado` | Ya se le ha escrito o llamado |
| `validado` | Responde, tiene producto/servicio útil y condiciones claras |
| `preferente` | Buen precio, plazo, calidad y respuesta |
| `descartado` | No sirve por precio, zona, producto, calidad o falta de respuesta |

## Reglas

- No usar precios de proveedor como definitivos sin fecha y condiciones.
- Registrar siempre si el precio incluye IVA y transporte.
- Registrar plazo de entrega y validez de oferta.
- Mantener separados proveedores validados y candidatos.
- Si el proveedor es crítico para una partida, buscar al menos 2 alternativas.
