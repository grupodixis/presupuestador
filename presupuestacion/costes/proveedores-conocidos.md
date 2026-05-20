# Proveedores Conocidos

Catalogo de proveedores habituales y talleres subcontratados. Esta lista es la semilla para la base de datos de Notion. Cada vez que se trabaje con un proveedor nuevo, anadirlo aqui y en Notion.

## Regla general: estimar sin pedir presupuesto

Siempre que sea posible, el agente debe **estimar el coste del subcontratista** usando los precios de referencia historicos. Solo se pide presupuesto real cuando:

1. El importe estimado supera los 6.000 € para trabajos repetitivos o 3.000 € para trabajos con geometria nueva.
2. La pieza tiene complejidad especial no contemplada en los precios de referencia.
3. Es la primera vez que se trabaja con ese proveedor o material.
4. El cliente exige precio cerrado garantizado (licitacion publica).

Para trabajos tipicos (soportes, placas, pequenas estructuras, vigas cortadas y taladradas), usar los precios de referencia directamente y ajustar con IPC o variacion del acero si es necesario.

---

## Talleres subcontratados (fabricacion)

### Ferros Puig Sallent

| Campo | Valor |
|---|---|
| Especialidad | Estructuras metalicas grandes, cerrajeria de acero negro, piezas para galvanizar en caliente |
| Materiales | Acero al carbono (S235, S275, S355), perfiles laminados, chapa gruesa, tubo |
| Procesos | Corte, soldadura, montaje en taller, preparacion para galvanizado |
| Contacto | Tomas Tejero / Josep Bramon / Tecnicsallent |
| Email | ttejero@ferrospuig.com / jbramon@ferrospuig.com / tecnicsallent@ferrospuig.com |
| Telefono | 936 33 37 93 / Tomas 661 909 920 |
| Ubicacion | Sallent (Barcelona) |
| Plazo habitual | 2-4 semanas segun carga |
| Valoracion | 5/5 |
| Notas | Usar especialmente cuando la estructura ira a galvanizar en caliente. Tambien hacen montaje en obra si se les pide. |

#### Pricing de referencia (para estimar sin pedir presupuesto)

Este bloque se ha extraido de presupuestos/pedidos reales de abril-mayo 2026. Usar para estimar sin pedir presupuesto salvo trabajos especiales.

| Concepto | Precio referencia | Observaciones |
|---|---|---|
| Perfil laminado IPN/IPE/HEB S275 cortado | 1.40 €/kg | Referencia real: IPN 280 a 1.397 €/kg. No incluye cortes/perforaciones/escotes. |
| Redondo liso / plano acero negro | 0.87 €/kg | Referencia real: redondo 12 mm y plano 50x12 a 866 €/Tn. |
| Tubo laminado cuadrado S235 50x50x4 | 5.80 €/ml | Referencia real: 579.88 €/Hm. Equivale aprox. a 1.02 €/kg en ese pedido. |
| Corte recto en perfil | 15.00 €/corte | Referencia real: 15.0645 €/corte recto. |
| Taladro / perforacion | 2.50-3.00 €/ud | 2.50 €/perf en IPN; 3.00 €/taladro en otro pedido. Usar 3.00 €/ud por prudencia. |
| Escote en perfil | 40.00 €/ud | Referencia real: escotes en IPN 280. |
| G+I rojo | 0.10 €/kg | Referencia real: 0.0991 €/kg. Confirmar si significa granallado + imprimacion rojo, no galvanizado. |
| Placa S275 10 mm cortada a medida pequeña | 2.20-5.00 €/ud | Referencia real: frontal 100x172+4T a 2.20 €/ud; PL200x172+8T a 5.00 €/ud. |
| Montaje en obra pequeño | 400 €/servicio | Referencia real: montaje asociado a vigas IPN 280. |
| Montaje en obra grande | 4.000 €/servicio | Referencia real: pedido con redondo/plano/tubo y 160 taladros. |
| Transporte Ferros Puig a Sant Lluis | 32-57 € | Referencias reales: 32 € para 63 kg; 57.04 € para 1.426 kg. Si no hay tarifa real, usar minimo 60 €. |
| Pedido minimo practico | 150-200 € | Referencias reales con envio: base 154.20 € para 63 kg. |

**Regla para el agente:** Para perfiles, placas, taladros, cortes, escotes y montajes tipicos, estimar con esta tabla. Pedir presupuesto real solo si hay geometria especial, soldaduras complejas, galvanizado real no tabulado, tolerancias criticas o importe alto.

#### Formula rapida Ferros Puig

```
Coste estimado =
  material_kg * precio_kg
  + cortes * 15
  + taladros * 3
  + escotes * 40
  + tratamiento_kg * 0.10 (si G+I rojo)
  + montaje_estimado
  + transporte
```

Para presupuesto rapido al cliente, aplicar por defecto un **10% de margen de gestion** sobre subcontratacion conocida. Si ademas se disena, mide, replantea o supervisa de forma relevante, subir a 10-15%.

### Taller de corte laser inoxidable

| Campo | Valor |
|---|---|
| Especialidad | Corte laser de precision en acero inoxidable (AISI 304 y 316) |
| Materiales | Chapa inoxidable hasta 20 mm, pletina, cortes con diseno |
| Procesos | Corte laser CNC, mecanizado, desbarbado |
| Contacto | (pendiente) |
| Email | (pendiente) |
| Telefono | (pendiente) |
| Ubicacion | Barcelona / Cataluna |
| Plazo habitual | 3-7 dias |
| Valoracion | (pendiente) |
| Notas | El corte laser en inoxidable evita deformaciones del corte termico. Ideal para pletinas de anclaje y piezas vistas. |

---

## Tratamientos externos

### Galvanizado en caliente

| Campo | Valor |
|---|---|
| Proveedores habituales | Consultar en Notion (Galvanizadoras de Barcelona y su area) |
| Proceso | Galvanizado en caliente segun UNE EN ISO 1461 |
| Precio referencia | (consultar) |
| Plazo habitual | 1-2 semanas |
| Notas | Las piezas deben tener agujeros de ventilacion y vaciado. Coordinar con el taller de fabricacion (Ferros Puig Sallent) para que las preparen correctamente. El espesor minimo de acero es 3 mm (riesgo de deformacion en piezas finas). |

---

## Transporte

| Proveedor | Ruta | Contacto |
|---|---|---|
| (pendiente) | Barcelona - Menorca | (pendiente) |
| (pendiente) | Peninsula - Menorca | (pendiente) |

---

## Materiales (suministro)

(Consultar base de datos de Notion para lista actualizada de proveedores de acero, inoxidable, aluminio, vidrio, tornilleria, etc.)

---

## Flujo de uso por el agente

1. Identificar si el trabajo requiere subcontratacion (estructura grande, galvanizado, corte laser).
2. Consultar este catalogo para comprobar si el proveedor es conocido.
3. Si el proveedor tiene ficha completa (email, telefono), preparar email de solicitud de presupuesto.
4. Si faltan datos, indicar al usuario que faltan los datos de contacto.
5. Incorporar el coste del subcontratista al coste tecnico base con margen rapido de gestion del 10%, salvo indicacion contraria.

### Regla de margen sobre subcontratacion

- Coste del subcontratista en presupuesto rapido: aplicar margen de gestion del 10%.
- Justificacion: el riesgo de calidad y plazo es del subcontratista, no nuestro.
- Opcional: si hacemos coordinacion, diseno y supervision, aplicar margen del 10-15%.
