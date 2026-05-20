# Skill: Instalaciones (Electricidad, Fontanería, Climatización)

## Cuándo usar esta skill

Cuando el producto a presupuestar incluye trabajos de instalaciones técnicas: electricidad (cuadros, cableado, mecanismos, alumbrado), fontanería (tuberías, desagües, grifería, sanitarios), climatización (calefacción, aire acondicionado, ventilación, ACS).

## Datos mínimos necesarios

- Tipo de instalación (eléctrica, fontanería, climatización).
- Tipo de inmueble (vivienda, local, nave, oficina).
- Superficie aproximada (m²).
- Puntos de consumo o potencia prevista.
- Necesidad de proyecto técnico.

## Datos recomendados

- Planos de la instalación o planta del inmueble.
- Relación de puntos (tomas, enchufes, luminarias, radiadores, splits).
- Calidad de materiales (gama básica, estándar, alta).
- Tipo de caldera o bomba de calor si aplica.
- Necesidad de certificado de instalación.
- Acceso a conductos o falsos techos.
- Previsión de cargas eléctricas.

## Criterios técnicos

- Instalación eléctrica debe cumplir REBT (Reglamento Electrotécnico de Baja Tensión).
- Instalación de fontanería debe cumplir CTE DB HS Salubridad.
- Instalación de climatización debe cumplir RITE (Reglamento de Instalaciones Térmicas).
- Toda instalación debe ser ejecutada por instalador autorizado.
- Debe entregarse certificado de instalación al finalizar.
- Las canalizaciones deben ser accesibles para mantenimiento.

## Composición habitual del producto

Ver composiciones en `/productos/composiciones/`:
- `instalacion_electrica.yaml`
- `instalacion_fontaneria.yaml`
- `instalacion_clima.yaml`

## Procesos habituales

1. Visita a obra para replanteo.
2. Realización de proyecto técnico si procede.
3. Rozas, canalizaciones y tubos empotrados / bandejas vista.
4. Tendido de cables / tuberías.
5. Colocación de mecanismos / sanitarios / equipos.
6. Conexión a red general o equipo.
7. Pruebas de funcionamiento.
8. Puesta en marcha y reglaje.
9. Certificado de instalación (boletín / certificado).

## Factores que aumentan el coste

- Obra de reforma (rozas en pared existente, reposición de pavimento).
- Necesidad de cuadro eléctrico nuevo (ICP, diferenciales, PIAs).
- Domótica o automatización.
- Climatización por conductos (obra de falsos techos).
- Gama alta de sanitarios o grifería.
- Necesidad de proyecto visado por ingeniero.
- Equipos de climatización de gran potencia.
- Distancia larga entre equipos y unidades exteriores.

## Factores que aumentan la complejidad

- Reforma en vivienda ocupada (convivencia con cliente).
- Instalación en edificio protegido (sin rozas permitidas).
- Necesidad de canalizaciones vistas (decoración industrial).
- Integración de instalaciones (clima+electricidad+fontanería coordinadas).
- Fachada protegida (no se pueden ver unidades exteriores).
- Edificio con varias plantas (columnas de bajantes).

## Factores de riesgo

- Cliente que no ha decidido la ubicación de puntos.
- Obra sin terminar que impide replanteo definitivo.
- Conductos de ventilación no previstos en proyecto de arquitectura.
- Carga eléctrica insuficiente en el edificio (necesidad de aumento de potencia).
- Baja de equipos con plazos de entrega largos.

## Errores frecuentes a evitar

- No incluir el proyecto técnico o memoria técnica.
- Olvidar legalizaciones y tasas.
- No considerar las rozas y reposición de paredes en reformas.
- Subestimar la longitud de tuberías o cableado.
- No incluir pequeño material (bridas, conectores, cintas, pasta de soldar).
- Olvidar las pruebas de estanqueidad en fontanería.
- No considerar el drenaje de condensados en climatización.
- Confundir precio de equipo con precio de instalación completa.

## Preguntas que el agente debe hacerse

- ¿Es obra nueva o reforma?
- ¿Hay proyecto técnico o hay que realizarlo?
- ¿Se ha visitado la obra?
- ¿El cliente ha elegido los materiales (mecanismos, sanitarios, equipos)?
- ¿Hay falso techo para conductos?
- ¿Hay acceso a fachada para unidades exteriores?
- ¿Se necesita legalización?
- ¿El cliente está en la vivienda durante la obra?

## Checklist final

- [ ] Tipo de instalación definido.
- [ ] Proyecto técnico incluido si necesario.
- [ ] Materiales y gama definidos.
- [ ] Número de puntos / equipos definido.
- [ ] Rozas y reposiciones consideradas (reforma).
- [ ] Canalizaciones incluidas.
- [ ] Cableado / tuberías incluidas.
- [ ] Legalización y tasas incluidas.
- [ ] Pruebas y puesta en marcha incluidas.
- [ ] Transporte incluido.
- [ ] Mermas aplicadas (3-5% material eléctrico/fontanería).
- [ ] Garantía indicada.

## Formato de salida recomendado

Desglose en partidas:

1. Proyecto técnico / memoria.
2. Mano de obra (replanteo, rozas, tendido, montaje).
3. Materiales (cable, tubería, canalizaciones, mecanismos).
4. Equipos (caldera, split, cuadro eléctrico, calentador).
5. Sanitarios y grifería (si aplica).
6. Legalización y tasas.
7. Transporte.
8. Mermas.
9. Total parcial.
10. Margen.
11. Total final.
