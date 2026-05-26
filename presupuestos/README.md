# Presupuestos

Carpeta central para presupuestos generados.

## Criterio de numeración

Cada presupuesto debe guardarse en una carpeta propia con este formato:

`P-AAAA-NNNN-slug-descriptivo`

Donde:

- `P` indica presupuesto.
- `AAAA` es el año de emisión.
- `NNNN` es un número correlativo de 4 dígitos dentro del año.
- `slug-descriptivo` resume el trabajo sin espacios ni caracteres especiales.

Ejemplo:

`P-2026-0007-tenedero-inox`

## Regla para nuevos presupuestos

Antes de crear un presupuesto nuevo:

1. Revisar las carpetas existentes en `presupuestos/`.
2. Buscar el número más alto del año actual.
3. Crear la siguiente carpeta correlativa.
4. Guardar dentro las versiones generadas.
5. Actualizar `presupuestos/index.html` con el nuevo registro.

Si el último presupuesto del año 2026 es `P-2026-0007-*`, el siguiente debe ser `P-2026-0008-*`.

## Archivos internos de cada carpeta

| Archivo | Uso |
|---|---|
| `README.md` | Resumen del presupuesto y notas internas |
| `presupuesto-interno-tecnico.html` | Versión técnica interna, no enviar al cliente |
| `presupuesto-cliente.html` | Versión comercial para cliente |
| `presupuesto-interno-tecnico.pdf` | PDF técnico si se exporta |
| `presupuesto-cliente.pdf` | PDF cliente si se exporta |
| `logo-ham.svg` | Logo local si el presupuesto lo necesita |

## Reglas de privacidad

- Los presupuestos pueden contener datos personales de clientes.
- No usar presupuestos reales como ejemplo público sin anonimizar.
- Para casos reutilizables, crear una versión anonimizada en `ejemplos/`.

## Índice

Abrir `index.html` para ver la lista funcional de presupuestos y acceder a cada HTML/PDF disponible.
