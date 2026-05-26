# Unidades y Criterios de Medicion

## Unidades base

| Unidad | Significado | Cuándo usarla |
|---|---|---|
| ud | Unidad fisica | Equipos, sensores, mecanismos, llaves, luminarias |
| punto | Punto funcional | Tomas, salidas de luz, puntos de agua, desagues, alimentaciones |
| ml | Metro lineal | Cable, tubo, canaleta, bandeja, tuberia, saneamiento |
| canal | Canal de control | Actuadores domoticos con varias salidas |
| circuito | Circuito electrico o hidraulico | Lineas dedicadas, sectores, zonas |
| conjunto | Partida global | Configuracion, puesta en marcha, pruebas, legalizacion |
| estancia | Agrupacion espacial | Baño, cocina, salon, dormitorio, sala tecnica |

## Criterios generales

- Usar `punto` cuando el elemento representa una funcion final para el usuario.
- Usar `ud` cuando se cuenta un objeto fisico concreto.
- Usar `ml` solo con plano escalado, cotas o medicion fiable.
- Usar `conjunto` para trabajos no divisibles facilmente en unidades repetibles.
- Usar `canal` en domotica cuando un modulo controla varias salidas.

## Jerarquia recomendada

1. Disciplina.
2. Zona o estancia.
3. Tipo de elemento.
4. Unidad.
5. Cantidad.
6. Criterio o supuesto.

## Control de duplicidades

- Si se cuenta un punto completo, definir si incluye cable/tubo o solo terminal.
- Si se mide cable/tubo aparte, indicarlo en criterio de conteo.
- Si una caja contiene varios mecanismos, contar mecanismos utiles, no solo cajas.
- Si una estancia se repite, multiplicar con una linea separada y explicar la planta tipo.
