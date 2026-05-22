# Skill: Presupuestación General

## Cuándo usar esta skill

Siempre. Es la skill base que se aplica a cualquier presupuesto. Debe cargarse primero y ejecutarse secuencialmente antes de pasar a skills específicas de producto.

## Disparadores por Palabra Clave (Cuestionarios Rápidos)

Cuando el usuario introduzca una palabra clave en solitario o solicitando presupuestar un producto específico, el agente IA debe activar inmediatamente la skill correspondiente y formular un cuestionario estructurado con los requisitos y preguntas clave del producto antes de calcular costes.

| Palabra Clave | Skill Asociada | Cuestionario a Lanzar |
|---|---|---|
| **Barandilla** / **Barandillas** | `skill_barandillas.md` | Requisitos de barandillas (ml, altura, material, anclaje, tramos, ubicación, acabado). |
| **Puerta** / **Puertas** / **Portón** / **Cancela** | `skill_puertas_metalicas.md` / `skill_portones_cancelas.md` | Requisitos de puertas (medidas, tipo apertura, cerradura, chapa/barrotes, motorización). |
| **Estructura** / **Estructuras** / **Viga** / **Pilares** | `skill_estructuras_metalicas.md` | Requisitos de estructura (peso, perfiles, planos, soldadura, altura, montaje, grúa). |
| **Ventana** / **Cerramiento** / **Aluminio** / **PVC** | `skill_carpinteria_aluminio.md` | Requisitos de carpintería (hueco, serie, tipo de vidrio, persiana, premarco, herrajes). |
| **Escalera** / **Escaleras** / **Peldaños** | `skill_escaleras.md` | Requisitos de escalera (altura total, desarrollo, anchura, huella/contrahuella, material peldaños, barandilla). |
| **Reja** / **Rejas** | `skill_rejas.md` | Requisitos de reja (medidas luz, tipo de barrote, fijación, pintura, cerradura, fija/abrible). |
| **Pérgola** / **Marquesina** / **Toldo** | `skill_marquesinas_pergolas.md` | Requisitos de pérgola (dimensiones, pilares, correas, tipo de cubierta/toldo, anclaje suelo/pared, acabado). |
| **Herrería** / **Forja** | `skill_herreria.md` | Requisitos de herrería (estilo, material, grado de adorno, acabado, transporte). |

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
- Todo presupuesto solicitado por el usuario debe entregarse en dos versiones: una interna técnica con supuestos, mediciones, costes y riesgos; y una versión cliente limpia, comercial y sin márgenes internos.
- Las mediciones deben ser verificables y basadas en planos o visita.
- Los precios unitarios deben ser coherentes con el mercado local.
- Por defecto, los presupuestos se consideran para Menorca: isla con ambiente salino, oxidante y corrosivo. Aplicar `presupuestacion/criterios-ambientales-menorca.md` salvo ubicacion distinta indicada por el usuario.
- En productos exteriores de acero, no presupuestar pintura simple sin galvanizado o sistema anticorrosivo C4/C5 salvo aceptacion expresa.

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
- Requerimiento de resistencia a ambiente marino en Menorca (AISI 316, galvanizado en caliente, sistemas C4/C5, tornilleria inox A4).
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

Cada presupuesto debe incluir dos bloques diferenciados:

1. **Version interna tecnica**: datos de entrada, supuestos, mediciones, materiales, procesos, horas, costes estimados, riesgos, recomendaciones tecnicas, exclusiones y precio recomendado.
2. **Version cliente**: descripcion clara del alcance, partidas comerciales agrupadas, incluidos, no incluidos, plazo, validez, condiciones y precio final. No mostrar costes internos, margen, horas internas ni dudas del agente.

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
