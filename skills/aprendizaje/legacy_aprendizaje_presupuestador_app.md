# Skill: Aprendizaje del Presupuestador App

Criterios aceptados desde la interfaz local de presupuestacion.

## 2026-07-17 - Aprendizaje desde presupuesto P-2026-0018

- Presupuesto: Estructura de Soporte Fotovoltaico y Obra Civil - Ciutadella (Menorca)
- Cliente/obra: Es Cardo 
- Total final guardado: 18875.00 EUR + IVA
- Origen: cambios reales realizados durante edicion y guardado del presupuesto.

### Cambios observados
- manual: linea eliminada Fabricacion / Obra civil: Excavación y cimentación de hormigón, cant. 12, precio 375, importe 4500.
- ia-linea: Transporte / Transporte marítimo y distribución local en Ciutadella (Incluido en Galvanizado): IA aplicada con prompt "inlcuirlo en la linea del galvanizado". Antes: cant. 1, precio 850, importe 850. Despues: cant. 0, precio 0, importe 0.
- manual: linea eliminada Riesgo / Margen de riesgo por dureza del terreno y viento, cant. 1, precio 800, importe 800.
- manual: linea eliminada Transporte / Transporte marítimo y distribución local en Ciutadella (Incluido en Galvanizado), cant. 0, precio 0, importe 0.
- ia-linea: Materiales / Perfiles de acero laminado S275JR: IA aplicada con prompt "este precio a 3.1 el Kg". Antes: cant. 2500, precio 2.5, importe 6250. Despues: cant. 2500, precio 3.1, importe 7750.

### Criterio de uso futuro
- Al presupuestar trabajos similares, revisar estas correcciones antes de cerrar cantidades, precios unitarios, capitulos y partidas omitidas.
