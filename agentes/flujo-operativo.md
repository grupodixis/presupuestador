# Flujo operativo del agente

## 1. Presupuestar

Entrada típica:

- Descripción del trabajo.
- Medidas.
- Fotos o planos si existen.
- Cliente y condiciones comerciales.

Proceso:

1. Identificar producto y skills aplicables.
2. Consultar composición técnica.
3. Medir o estimar materiales.
4. Detectar costes conocidos y costes inciertos.
5. Si faltan precios, activar I+D de proveedores.
6. Calcular coste técnico base.
7. Aplicar complejidad, riesgo y margen.
8. Generar preview interno.
9. Generar presupuesto comercial si el usuario lo pide.

Salidas:

- Presupuesto técnico desglosado.
- Presupuesto comercial HTML/PDF.
- Dudas o datos pendientes.

## 2. Solicitar precios

Entrada típica:

- Material o servicio sin precio fiable.
- Cantidad y unidad.
- Especificación.

Proceso:

1. Buscar proveedor validado en `proveedores/fichas/`.
2. Si no existe, buscar candidatos.
3. Crear ficha o búsqueda.
4. Redactar email o WhatsApp.
5. Esperar aprobación humana.

Salidas:

- Mensaje listo para enviar.
- Ficha de proveedor actualizada.
- Lista de datos pendientes.

## 3. Actualizar metodología

Entrada típica:

- Nuevo criterio aprendido.
- Error detectado en presupuesto.
- Nueva regla comercial.
- Nuevo proveedor o precio confirmado.

Proceso:

1. Identificar documento afectado.
2. Añadir criterio sin duplicar contenido.
3. Separar datos puntuales de reglas generales.
4. Mostrar diff.
5. Crear commit si el usuario lo aprueba.

Salidas:

- Documentación actualizada.
- Commit Git trazable.

## 4. Mantenimiento periódico

Tareas recomendadas:

- Revisar precios de materiales mensualmente.
- Revisar proveedores preferentes trimestralmente.
- Archivar proveedores descartados.
- Convertir presupuestos repetidos en ejemplos anonimizados.
- Actualizar plantillas HTML/PDF según feedback comercial.
