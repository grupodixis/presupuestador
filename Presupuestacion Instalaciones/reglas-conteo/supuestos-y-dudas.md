# Supuestos y Dudas

## Regla principal

Cuando falte informacion, no ocultar la incertidumbre. Registrar el supuesto, su impacto y la confirmacion necesaria.

## Estados recomendados

| Estado | Uso |
|---|---|
| confirmado | Aparece claramente en plano, memoria o indicacion del cliente |
| supuesto | No aparece completo, pero se infiere razonablemente |
| pendiente | Falta dato necesario para contar con seguridad |
| excluido | No forma parte del alcance actual |

## Ejemplos

| Caso | Como anotarlo |
|---|---|
| Plano sin escala | `ml pendiente_de_medicion; conteo por puntos disponible` |
| Simbolo no identificado | `1 ud pendiente de confirmar segun leyenda` |
| Baño dibujado sin detalle | `supuesto: lavabo + inodoro + ducha; confirmar aparatos` |
| WiFi existente | `pendiente prueba de cobertura; no se asume suficiente` |
| Cuadro sin esquema unifilar | `protecciones pendientes de definir por instalador/proyecto` |

## Impacto

- `bajo`: no cambia mucho la medicion.
- `medio`: puede añadir partidas auxiliares.
- `alto`: puede cambiar cantidad principal, legalizacion o trazado.
