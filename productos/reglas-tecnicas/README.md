# Reglas Técnicas

Conocimiento normativo, dimensional y de diseño aplicable a cada tipo de producto.

## Propósito

Establecer las reglas técnicas que el agente debe verificar antes de validar un presupuesto:

- Normativa aplicable (CTE, Eurocódigos, RITE, REBT, etc.).
- Tolerancias de fabricación.
- Alturas mínimas/máximas.
- Separaciones reglamentarias.
- Cargas de uso.
- Resistencia al fuego.
- Protección anticorrosión según ambiente.
- Especificaciones de soldadura.
- Tratamientos superficiales exigibles.

## Estructura sugerida por producto

```
producto: Nombre
normativa_aplicable:
  - Norma 1
  - Norma 2
tolerancias:
  corte: ± mm
  soldadura: clase
  montaje: ± mm
especificaciones_tecnicas:
  - parámetro: valor
controles_obligatorios:
  - Control 1
  - Control 2
```

## Uso

El agente debe consultar las reglas técnicas del producto identificado para:

1. Verificar que el diseño cumple normativa.
2. Aplicar tolerancias correctas en la estimación.
3. Detectar requisitos especiales (sellado, aislamiento, etc.).
4. Incluir controles de calidad obligatorios en el coste.
