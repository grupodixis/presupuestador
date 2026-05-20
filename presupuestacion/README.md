# Presupuestación

Lógica, criterios y datos para la generación de presupuestos técnicos.

## Subcarpetas

| Carpeta | Propósito |
|---|---|
| `costes/` | Costes de materiales, mano de obra, maquinaria, tratamientos, transporte |
| `margenes/` | Política de márgenes por tipo de producto, cliente y volumen |
| `oferta-demanda/` | Ajustes estacionales y de mercado sobre el precio final |
| `complejidad/` | Evaluación de la complejidad de fabricación y montaje |
| `checklists/` | Listas de verificación previas a enviar un presupuesto |

## Flujo de uso

El agente sigue este orden al calcular un presupuesto:

1. **Costes**: calcular coste técnico base (materiales + MO + maquinaria + tratamientos + transporte).
2. **Complejidad**: obtener factor de complejidad y ajustar coste si procede.
3. **Riesgo**: aplicar factor de riesgo técnico si aplica.
4. **Margen**: aplicar margen industrial según política.
5. **Oferta/demanda**: ajustar precio final según condiciones de mercado.
6. **Checklist**: revisar que no falta nada antes de emitir.

Cada subcarpeta tiene su propio README con tablas, factores y criterios detallados.
