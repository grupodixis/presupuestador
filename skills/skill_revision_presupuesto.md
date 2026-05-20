# Skill: Revisión de Presupuesto

## Cuándo usar esta skill

Siempre. Es la última skill que se ejecuta antes de entregar el presupuesto al cliente. Su propósito es detectar errores, omisiones e incoherencias.

## Datos mínimos necesarios

El presupuesto completo generado por el agente, incluyendo todas las partidas, cálculos y notas.

## Datos recomendados

- Checklist de la skill específica del producto.
- Historial de presupuestos similares (para comparar).
- Precios de mercado de referencia.

## Criterios técnicos

- Un presupuesto incorrecto es peor que no hacer presupuesto.
- Es mejor indicar una duda que asumir un dato incorrecto.
- El presupuesto debe ser defendible técnicamente.
- El presupuesto debe ser claro para el cliente.
- Las exclusiones deben estar explícitas.

## Proceso de revisión

### Paso 1: Revisión de identificación
- ¿El tipo de producto es correcto?
- ¿La skill aplicada es la adecuada?
- ¿Se han cargado skills complementarias necesarias?

### Paso 2: Revisión de datos de entrada
- ¿Se han usado todos los datos proporcionados por el cliente?
- ¿Hay datos del cliente sin usar?
- ¿Se han identificado datos faltantes?
- ¿Se han hecho preguntas al cliente sobre lo que falta?

### Paso 3: Revisión de composición
- ¿Se han incluido todos los materiales de la composición?
- ¿Se han incluido todos los procesos?
- ¿Se han considerado los materiales auxiliares?
- ¿Se han aplicado mermas?

### Paso 4: Revisión de costes
- ¿Los precios unitarios son coherentes?
- ¿Las cantidades son correctas?
- ¿La mano de obra está bien estimada?
- ¿Los tratamientos externos están incluidos?
- ¿El transporte está incluido?
- ¿El montaje está incluido?
- ¿Los costes indirectos están considerados?

### Paso 5: Revisión de complejidad y riesgo
- ¿Se ha evaluado la complejidad?
- ¿El factor es razonable?
- ¿Se han identificado riesgos?
- ¿Se ha aplicado factor de riesgo si procede?

### Paso 6: Revisión de márgenes
- ¿El margen aplicado es el correcto para este producto?
- ¿Se ha ajustado por volumen?
- ¿Se ha ajustado por cliente?

### Paso 7: Revisión de oferta/demanda
- ¿Se ha considerado la carga de trabajo actual?
- ¿Se ha considerado la urgencia?
- ¿Se ha considerado el tipo de cliente?

### Paso 8: Revisión de formato
- ¿El presupuesto tiene todos los campos obligatorios?
- ¿Las partidas están desglosadas?
- ¿Las exclusiones están claras?
- ¿La validez está indicada?
- ¿Los datos de contacto están incluidos?

## Errores frecuentes a evitar

- Pasar por alto una partida completa (ej. olvidar el montaje).
- Duplicar partidas (ej. material incluido dos veces).
- Error aritmético en sumas o multiplicaciones.
- Precio unitario fuera de rango (demasiado alto o bajo).
- Margen aplicado incorrectamente (sobre coste o sobre precio).
- Confundir precio final con base imponible (IVA no incluido).
- Plazo de entrega no realista.
- Confundir medidas (mm vs m, lineal vs m²).
- No verificar la coherencia global del presupuesto.

## Preguntas que el agente debe hacerse

- ¿Este presupuesto tiene sentido globalmente?
- ¿El precio final es coherente con el mercado?
- ¿Hay alguna partida que parezca fuera de rango?
- ¿He dejado alguna duda sin resolver?
- ¿El cliente va a entender el presupuesto?
- ¿Hay algo que pueda explicar mejor?
- ¿Este presupuesto es defendible si el cliente pregunta?
- ¿He revisado todas las checklists?

## Checklist final de revisión

### Datos del presupuesto
- [ ] Fecha correcta.
- [ ] Número de referencia único.
- [ ] Datos del cliente completos.
- [ ] Descripción del trabajo clara.

### Partidas
- [ ] Todas las partidas incluidas.
- [ ] Mediciones correctas.
- [ ] Precios unitarios coherentes.
- [ ] Subtotal correcto por partida.
- [ ] Mermas aplicadas.
- [ ] Complejidad aplicada.
- [ ] Riesgo aplicado.

### Precio final
- [ ] Margen aplicado correctamente.
- [ ] Ajuste de oferta/demanda aplicado.
- [ ] Subtotal correcto.
- [ ] IVA indicado.
- [ ] Total final correcto.

### Condiciones
- [ ] Plazo de entrega indicado.
- [ ] Condiciones de pago indicadas.
- [ ] Validez del presupuesto indicada.
- [ ] Exclusiones documentadas.
- [ ] Notas aclaratorias si procede.

### Presentación
- [ ] Formato claro y profesional.
- [ ] Sin errores ortográficos.
- [ ] Contacto incluido.
- [ ] Firma o responsable incluido.

## Formato de salida recomendado

Documentar la revisión en un informe breve interno:

```
Revisión de presupuesto #[número]
Producto: [nombre]
Cliente: [nombre]

Estado: APROBADO / CON OBSERVACIONES / RECHAZADO

Observaciones:
- [observación 1]
- [observación 2]

Correcciones aplicadas:
- [corrección 1]

Revisado por: [agente / responsable]
Fecha: [fecha]
```
