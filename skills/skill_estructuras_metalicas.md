# Skill: Estructuras Metálicas

## Cuándo usar esta skill

Cuando el producto a presupuestar es una estructura metálica: pórticos, cerchas, vigas, pilares, correas, naves industriales, entramados, marquesinas, soportes, escaleras estructurales, pasarelas peatonales.

## Datos mínimos necesarios

- Tipo de estructura (pórtico, cercha, viga, pilares, nave, marquesina).
- Dimensiones principales (luces, alturas, separación entre pórticos).
- Cargas a soportar (cubierta, viento, nieve, sobrecarga de uso).
- Tipo de perfil (IPE, HEB, UPN, tubular, chapa plegada).
- Ubicación geográfica (carga de nieve y viento según CTE).

## Datos recomendados

- Planos estructurales o esquema de cargas.
- Tipo de uniones (soldadas, atornilladas, mixtas).
- Tipo de cubierta y cerramiento.
- Cimentación prevista (dado, zapata, losa).
- Normativa aplicable (CTE DB SE-A, Eurocódigo 3).
- Plazo de ejecución.
- Acceso a obra y medios de elevación.
- Protección contra incendio requerida.
- Ambiente de exposición.

## Criterios técnicos

- Toda estructura debe cumplir CTE DB SE-A o Eurocódigo 3.
- Las uniones deben ser capaces de transmitir los esfuerzos calculados.
- La flecha máxima admisible en vigas es L/250 (L/300 en cubiertas).
- La protección anticorrosión debe ser acorde al ambiente (C1-C5).
- En Menorca, las estructuras exteriores deben tratarse como ambiente salino: C4 minimo practico y C5-M en costa, cubiertas, terrazas o exposicion directa.
- Evitar acero pintado simple en exterior; valorar galvanizado en caliente, galvanizado + pintura o sistema epoxi/poliuretano C4/C5.
- La protección contra incendio debe cumplir CTE DB SI.
- Los pernos de anclaje deben especificarse en planos.
- La estructura debe ser estable en todas las fases de montaje.

## Composición habitual del producto

Ver `/productos/composiciones/estructura_metalica.yaml`.

## Procesos habituales

1. Cálculo estructural por ingeniero.
2. Despiece y elaboración de planos de taller.
3. Corte de perfiles (sierra, oxicorte, plasma).
4. Preparación de bordes y chaflanes.
5. Soldadura (MAG, SAW, electrodo, según espesor).
6. Taladrado de agujeros para uniones atornilladas.
7. Control de calidad (líquidos penetrantes, ultrasonidos).
8. Tratamiento superficial (chorreado + imprimación + pintura).
9. Transporte a obra (camión góndola, pluma).
10. Montaje en obra (grúa, nivelación, aplomado).
11. Uniones (soldadura en obra, atornillado).
12. Revisión y retoques finales.

## Factores que aumentan el coste

- Grandes luces (perfiles de gran canto).
- Cargas elevadas (perfiles más pesados).
- Acero especial (S355, S460, inoxidable).
- Protección contra incendio (pintura intumescente, mortero).
- Proteccion anticorrosiva reforzada para ambiente marino de Menorca.
- Uniones atornilladas de alta resistencia.
- Cerchas complejas (muchos nudos, piezas secundarias).
- Altura elevada de montaje.
- Necesidad de certificación CE de soldadura.

## Factores que aumentan la complejidad

- Geometría irregular de la estructura.
- Uniones con múltiples piezas concurrentes (nudos complejos).
- Estructura espacial en 3D.
- Tolerancias muy ajustadas.
- Montaje en fábricas en funcionamiento.
- Edificio con geometría singular.

## Factores de riesgo

- Cálculo estructural no verificado por ingeniero colegiado.
- Plazo de fabricación comprimido (soldaduras sin control).
- Montaje en altura sin medios adecuados.
- Cimentación ejecutada con errores (pernos mal situados).
- Cliente que modifica cargas durante la fabricación.
- Subcontratación del montaje sin supervisión.

## Errores frecuentes a evitar

- No incluir el cálculo estructural en el coste.
- Olvidar la protección contra incendio.
- No considerar los medios de elevación en montaje.
- Subestimar las horas de soldadura.
- No incluir controles de calidad.
- Olvidar los casquillos, arandelas y tuercas en uniones atornilladas.
- No considerar el replanteo de pernos de anclaje.

## Preguntas que el agente debe hacerse

- ¿Hay planos estructurales?
- ¿Se ha hecho cálculo de cargas?
- ¿Qué normativa aplica?
- ¿Necesita protección contra incendio?
- ¿Qué ambiente de exposición tiene?
- ¿Cómo se transportan las piezas?
- ¿Hay grúa en obra o se necesita camión pluma?
- ¿El suelo de la nave soporta las cargas de montaje?

## Checklist final

- [ ] Cálculo estructural incluido.
- [ ] Perfiles y espesores definidos.
- [ ] Ambiente de exposición definido.
- [ ] Protección anticorrosión definida.
- [ ] Protección contra incendio definida si aplica.
- [ ] Uniones definidas (soldadas/atornilladas).
- [ ] Planos de taller y despiece incluidos.
- [ ] Controles de calidad incluidos.
- [ ] Transporte y medios de elevación incluidos.
- [ ] Montaje en obra incluido.
- [ ] Mermas aplicadas (5% acero laminado, 10% tubo).
- [ ] Plazo de ejecución estimado.

## Formato de salida recomendado

Desglose en partidas:

1. Cálculo estructural.
2. Acero (perfiles, chapa, tubular).
3. Tornillería y anclajes.
4. Mecanizados (corte, taladrado, preparación).
5. Soldadura.
6. Tratamiento superficial.
7. Protección contra incendio (si aplica).
8. Control de calidad.
9. Transporte.
10. Montaje en obra (MO, grúa, medios auxiliares).
11. Mermas.
12. Total parcial.
13. Margen.
14. Total final.
