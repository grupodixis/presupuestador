# Skill: Presupuestación General

## Cuándo usar esta skill

Siempre. Es la skill base que se aplica a cualquier presupuesto. Debe cargarse primero y ejecutarse secuencialmente antes de pasar a skills específicas de producto.

## Datos mínimos necesarios

- Descripción del trabajo o producto.
- Tipo de producto.
- Dimensiones o cantidades.
- Tipo de cliente.
- Fecha del presupuesto.

## Datos recomendados

- Planos o croquis.
- Ubicación de la obra.
- Plazo de entrega deseado.
- Presupuesto objetivo del cliente (si lo indica).
- Referencia de presupuesto anterior (si es repetición).
- Fotografías del emplazamiento.

## Criterios técnicos

- Todo presupuesto debe tener un coste técnico base desglosado.
- Todo presupuesto debe indicar qué incluye y qué no incluye.
- Todo presupuesto debe tener una validez temporal.
- Las mediciones deben ser verificables y basadas en planos o visita.
- Los precios unitarios deben ser coherentes con el mercado local.

## Condiciones comerciales por defecto

- Validez del presupuesto: 30 días desde la fecha de emisión.
- Forma de pago: 100% a la aceptación del presupuesto.
- Cualquier condición distinta debe indicarse expresamente en la solicitud o en el documento comercial.

## Composición habitual del producto

Ver `/productos/composiciones/` para la composición específica de cada producto.

## Procesos habituales

1. Recepción de la solicitud.
2. Identificación del producto.
3. Consulta de composición.
4. Estimación de materiales.
5. Estimación de mano de obra.
6. Identificación de procesos externos.
7. Evaluación de complejidad.
8. Evaluación de riesgos.
9. Cálculo de coste técnico base.
10. Aplicación de margen industrial.
11. Ajuste por oferta/demanda.
12. Ajuste por urgencia.
13. Generación del documento.
14. Revisión final.

## Factores que aumentan el coste

- Materiales especiales (inoxidable, aluminio lacado, vidrio seguridad).
- Plazos reducidos.
- Acceso difícil a obra.
- Necesidad de certificados o ensayos.
- Diseño y cálculo estructural.
- Cliente con exigencias técnicas elevadas.

## Factores que aumentan la complejidad

- Geometría no estándar.
- Tolerancias muy ajustadas.
- Materiales difíciles de mecanizar.
- Combinación de varios oficios.
- Falta de información técnica previa.

## Factores de riesgo

- Mediciones sin visita a obra.
- Cliente nuevo sin referencias.
- Plazos muy ajustados.
- Materiales con plazos de entrega largos.
- Subcontratación de procesos críticos.

## Errores frecuentes a evitar

- No incluir todos los materiales auxiliares.
- Olvidar tratamientos superficiales.
- Subestimar horas de montaje.
- No considerar accesos a obra.
- Olvidar transporte.
- No aplicar mermas.
- Basar el precio solo en el coste de material.
- No documentar supuestos y exclusiones.

## Preguntas que el agente debe hacerse

- ¿He identificado correctamente el producto?
- ¿Tengo todas las dimensiones necesarias?
- ¿He incluido todos los procesos de fabricación?
- ¿He considerado el montaje en obra?
- ¿He evaluado la complejidad?
- ¿He aplicado el margen correcto?
- ¿He ajustado por oferta/demanda?
- ¿He revisado el presupuesto completo?

## Checklist final

- [ ] Producto identificado.
- [ ] Skill específica cargada.
- [ ] Composición consultada.
- [ ] Materiales cuantificados.
- [ ] MO de taller estimada.
- [ ] MO de montaje estimada.
- [ ] Tratamientos incluidos.
- [ ] Transporte incluido.
- [ ] Mermas aplicadas.
- [ ] Complejidad evaluada.
- [ ] Riesgos evaluados.
- [ ] Margen aplicado.
- [ ] Oferta/demanda ajustada.
- [ ] Exclusiones documentadas.
- [ ] Validez indicada.

## Formato de salida recomendado

El presupuesto debe incluir:

- Número de referencia y fecha.
- Datos del cliente.
- Descripción detallada del trabajo.
- Desglose de partidas con mediciones y precios.
- Total parcial y total final.
- Plazo de entrega.
- Condiciones de pago.
- Validez del presupuesto.
- Notas y exclusiones.
- Firma o responsable.
