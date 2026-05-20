# Historico Ferros Puig

Datos extraidos de presupuestos/pedidos reales de Ferros Puig para crear reglas de estimacion sin esperar nuevos presupuestos.

---

## Pedido 603562 - Obra Sarada - 14/05/2026

### Datos generales

| Campo | Valor |
|---|---|
| Proveedor | Ferros Puig Sallent |
| Comercial | Tomas Tejero |
| Email | ttejero@ferrospuig.com |
| Telefono | 661 909 920 |
| Fecha pedido | 14/05/2026 |
| Fecha entrega | 29/05/2026 |
| Total kg | 1.426 kg |
| Importe productos | 2.392,12 € |
| Importe conceptos | 566,70 € |
| Envio | 57,04 € |
| Base imponible | 3.015,86 € |

### Partidas y precios unitarios

| Concepto | Precio extraido | Regla usable |
|---|---:|---|
| IPN 280 S275 | 1.397 €/kg | Usar 1.40 €/kg para perfil laminado S275 cortado |
| Corte recto | 15,0645 €/corte | Usar 15 €/corte |
| Perforacion | 2,50 €/perforacion | Usar 2,50-3,00 €/perforacion |
| G+I rojo | 0,0991 €/kg | Usar 0,10 €/kg |
| Escote | 40,00 €/escote | Usar 40 €/escote |
| Montaje | 400,00 €/servicio | Usar 400 € para montaje sencillo asociado |
| Envio | 57,04 € / 1.426 kg = 0,04 €/kg | Usar minimo 60 € si no hay tarifa concreta |

### Observaciones

- Pedido util para vigas laminadas con cortes, perforaciones, escotes y tratamiento G+I rojo.
- Confirmar con Ferros Puig si G+I rojo significa granallado + imprimacion rojo o galvanizado + imprimacion.

---

## Pedido 602088 / Oferta 1024033 - Soporte de viga - 29-30/04/2026

### Datos generales

| Campo | Valor |
|---|---|
| Proveedor | Ferros Puig Sallent |
| Contacto | Tecnicsallent |
| Email | tecnicsallent@ferrospuig.com |
| Total kg | 63 kg |
| Importe productos | 122,20 € |
| Envio | 32,00 € |
| Base imponible | 154,20 € |
| Plazo indicado | 4/6 dias laborables aprox. |

### Partidas y precios unitarios

| Concepto | Precio extraido | Regla usable |
|---|---:|---|
| Frontal 100x172+4T S275 10 mm | 2,20 €/ud | Placa pequeña cortada a medida: desde 2,20 €/ud |
| PL200x172+8T S275 10 mm | 5,00 €/ud | Placa/soporte medio cortado a medida: desde 5,00 €/ud |
| Envio pedido pequeño | 32,00 € | Usar 32-60 € segun peso/volumen |
| Coste medio productos | 122,20 € / 63 kg = 1,94 €/kg | Usar 2,00 €/kg para placas pequeñas ya cortadas |

### Observaciones

- Caso bueno para placas y soportes pequeños cortados a medida.
- Pedido pequeno: el envio pesa mucho en el coste unitario.

---

## Pedido 600340 - 17/04/2026

### Datos generales

| Campo | Valor |
|---|---|
| Proveedor | Ferros Puig Sallent |
| Comercial | Josep Bramon |
| Email | jbramon@ferrospuig.com |
| Total kg | 1.848 kg |
| Importe productos | 6.133,86 € |
| Envio | 0,00 € (lo pasan a buscar) |
| Base imponible | 6.133,86 € |

### Partidas y precios unitarios

| Concepto | Precio extraido | Regla usable |
|---|---:|---|
| Redondo liso 12 mm | 866 €/Tn = 0,866 €/kg | Usar 0,87 €/kg |
| Plano 50x12 | 866 €/Tn = 0,866 €/kg | Usar 0,87 €/kg |
| Tubo laminado cuadrado S235 50x50x4 a 6 m | 579,88 €/Hm = 5,7988 €/ml | Usar 5,80 €/ml |
| Taladrar | 3,00 €/ud | Usar 3,00 €/taladro |
| Montaje | 4.000,00 €/servicio | Usar como referencia para montaje grande |

### Observaciones

- Caso util para material comercial de acero negro y mucho taladro.
- El montaje domina el coste total. Separar siempre material de montaje.

---

## Reglas derivadas para estimacion rapida

| Familia | Regla recomendada |
|---|---|
| Perfil laminado S275 cortado | 1,40 €/kg + cortes + taladros + escotes |
| Redondo/plano acero negro comercial | 0,87 €/kg |
| Tubo cuadrado S235 50x50x4 | 5,80 €/ml |
| Placa S275 10 mm cortada pequeña | 2,20-5,00 €/ud o 2,00 €/kg si no hay desglose |
| Corte recto | 15 €/corte |
| Taladro/perforacion | 3 €/ud |
| Escote | 40 €/ud |
| G+I rojo | 0,10 €/kg |
| Montaje sencillo | 400 €/servicio |
| Montaje grande | 4.000 €/servicio |
| Envio pequeño | 32-60 € minimo |
| Envio medio/grande | 0,04 €/kg observado, pero usar minimo 60 € por prudencia |

## Margen para presupuesto rapido

Para presupuestos rapidos basados en historico de Ferros Puig, aplicar por defecto **10% de margen de gestion** sobre el coste estimado del proveedor.

Formula:

```text
Precio rapido al cliente = coste estimado Ferros Puig x 1,10
```

Si el trabajo requiere medicion, diseno, replanteo o supervision relevante, aplicar 10-15% segun criterio.

## Cuando pedir presupuesto real a Ferros Puig

- Estructuras con soldaduras importantes no inferibles por kg.
- Galvanizado en caliente real si no se conoce la tarifa actual.
- Piezas con tolerancias criticas o clase de ejecucion especial.
- Montajes en obra complejos o con grua.
- Importe estimado superior a 6.000 €.
- Cliente exige precio cerrado contractual.
