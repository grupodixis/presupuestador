# Skill: Evaluación de Complejidad

## Cuándo usar esta skill

Después de identificar los procesos de fabricación y antes de calcular el coste técnico base. Se aplica para ajustar el coste estimado según la dificultad real del trabajo. Complementa a las skills específicas de producto.

## Datos mínimos necesarios

- Descripción detallada del producto o trabajo.
- Tipo de producto.
- Dimensiones y geometría.
- Materiales involucrados.
- Procesos de fabricación identificados.
- Condiciones de montaje.

## Datos recomendados

- Planos de taller.
- Especificaciones técnicas del cliente.
- Tolerancias requeridas.
- Número de unidades.
- Repetitividad de piezas.

## Criterios técnicos

- La complejidad es un multiplicador del coste técnico base.
- No confundir complejidad con dificultad de montaje (montaje tiene su propia evaluación).
- La complejidad puede ser geométrica, de materiales, de procesos o de montaje.
- Un producto simple repetido muchas veces tiene menor complejidad unitaria.
- Un producto único y complejo tiene mayor complejidad aunque sea pequeño.

## Dimensiones de complejidad

### 1. Complejidad geométrica

| Nivel | Descripción | Factor |
|---|---|---|
| Baja | Formas rectilíneas, cortes rectos, ángulos de 90° | 1.0 |
| Media | Formas con ángulos variables, cortes inglete, chaflanes | 1.1-1.2 |
| Alta | Formas curvas, radios, geometría orgánica | 1.3-1.5 |
| Muy alta | Formas 3D complejas, superficies alabeadas | 1.5-2.0 |

### 2. Complejidad de materiales

| Nivel | Descripción | Factor |
|---|---|---|
| Baja | Acero carbono estándar, perfiles comerciales | 1.0 |
| Media | Acero inoxidable, aluminio, acero galvanizado | 1.1-1.2 |
| Alta | Materiales compuestos, vidrio, combinación de materiales | 1.2-1.4 |
| Muy alta | Materiales con certificación, trazabilidad, importados | 1.4-1.6 |

### 3. Complejidad de procesos

| Nivel | Descripción | Factor |
|---|---|---|
| Baja | Corte + soldadura simple | 1.0 |
| Media | Corte + soldadura + plegado + taladrado | 1.1-1.3 |
| Alta | Mecanizado de precisión, soldadura TIG/TAC, tratamientos múltiples | 1.3-1.5 |
| Muy alta | Procesos especiales, controles no destructivos, certificación | 1.5-1.8 |

### 4. Complejidad de montaje

| Nivel | Descripción | Factor |
|---|---|---|
| Baja | Montaje en taller, piezas pequeñas | 1.0 |
| Media | Montaje en obra, altura normal, acceso sencillo | 1.1-1.2 |
| Alta | Montaje en altura, acceso difícil, medios especiales | 1.3-1.5 |
| Muy alta | Montaje en condiciones extremas, plazos imposibles | 1.5-2.0 |

## Evaluación combinada

1. Evaluar cada dimensión por separado.
2. La puntuación total es la suma de los niveles (Baja=1, Media=2, Alta=3, Muy Alta=4).
3. El factor de complejidad combinado se obtiene de la tabla:

| Puntuación total | Factor combinado |
|---|---|
| 4-6 | 1.0 (estándar) |
| 7-9 | 1.1-1.2 |
| 10-12 | 1.2-1.4 |
| 13-15 | 1.4-1.7 |
| 16-20 | 1.7-2.5 |

## Factores que aumentan la complejidad

- Falta de repetitividad (cada pieza es diferente).
- Tolerancias muy ajustadas (< 1mm en conjuntos grandes).
- Necesidad de utillajes especiales.
- Soldadura en posición difícil (vertical, sobrecabeza, tubular).
- Mecanizado de piezas de gran tamaño.
- Tratamiento térmico o superficial en condiciones controladas.
- Acabado estético (visible, sin defectos admisibles).
- Control de calidad externo obligatorio.

## Errores frecuentes a evitar

- Subestimar la complejidad de piezas aparentemente simples.
- No considerar la complejidad de utillajes y preparación.
- Pensar que el precio del material domina el coste total.
- Confundir piezas grandes con piezas complejas.
- Ignorar la complejidad de la geometría en el corte (anidado).

## Preguntas que el agente debe hacerse

- ¿La geometría es simple o compleja?
- ¿Hay tolerancias especiales?
- ¿El material es estándar?
- ¿Los procesos son habituales o especiales?
- ¿Es una pieza única o se repite?
- ¿El montaje es en taller o en obra?
- ¿Hay controles de calidad adicionales?
- ¿Se necesita utillaje específico?

## Checklist final

- [ ] Geometría evaluada.
- [ ] Material evaluado.
- [ ] Procesos evaluados.
- [ ] Montaje evaluado.
- [ ] Factor combinado calculado.
- [ ] Factor documentado en el presupuesto.
- [ ] Ajuste de coste aplicado.

## Formato de salida recomendado

Documentar la evaluación de complejidad en el expediente interno:

```
Evaluación de complejidad:
  Geométrica: [Baja/Media/Alta/Muy Alta] - Factor X.X
  Materiales: [Baja/Media/Alta/Muy Alta] - Factor X.X
  Procesos:   [Baja/Media/Alta/Muy Alta] - Factor X.X
  Montaje:    [Baja/Media/Alta/Muy Alta] - Factor X.X
  Combinado:  X.X
  Justificación: [breve explicación]
```
