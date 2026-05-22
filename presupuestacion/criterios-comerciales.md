# Criterios comerciales y de presentación

Este documento recoge reglas prácticas aprendidas durante la generación de presupuestos comerciales para HAM Estructuras Metálicas.

## Condiciones comerciales por defecto

- Validez del presupuesto: **30 días** desde la fecha de emisión.
- Forma de pago: **100% a la aceptación del presupuesto**.
- Estas condiciones se aplican por defecto salvo que el usuario indique expresamente otras.

## Mano de obra

- Precio hora de referencia indicado por el usuario: **30 €/h**.
- Usar esta tarifa en presupuestos comerciales cuando no se indique otra.
- Si se usa una tabla interna con otras tarifas, documentar la diferencia como criterio interno y no mostrarla en el presupuesto comercial.

## Presupuesto preview vs presupuesto cliente

- **Preview interno/comercial:** puede incluir hipótesis, horas, costes internos, factores de complejidad, riesgo y márgenes.
- **Presupuesto cliente:** debe ocultar horas, factores internos y márgenes; mostrar producto terminado, alcance, incluidos, no incluidos, condiciones y precio final.
- Para cliente, agrupar las partidas por concepto entendible: estructura, materiales visibles, instalación, transporte, acabado.
- Por defecto, cada presupuesto solicitado debe entregarse en dos versiones: `Version interna tecnica` y `Version cliente`.
- La version interna debe servir para decidir y defender el precio; la version cliente debe poder copiarse al documento comercial sin revelar calculos internos.
- Procedimiento por defecto: ante un presupuesto completo, generar siempre una versión técnica interna y una versión comercial para cliente, salvo instrucción contraria del usuario.
- Si se trabaja en HTML, ambas versiones deben estar preparadas para exportación PDF.

## Formato HTML/PDF

- Usar formato A4 con estilos `@media print` y `@page { size: A4; margin: 0; }`.
- Compactar márgenes, tamaños y espaciados en impresión para evitar cortes o segunda página innecesaria.
- Incluir cabecera corporativa de HAM con logo, contacto y datos públicos:
  - Web: `www.hamenorca.com`
  - Email: `info@hamenorca.com`
  - Teléfono: `+34 971 35 20 18`
  - WhatsApp: `+34 669 769 541`
  - Dirección: `Av. Circunvalacio, 11, Poligono de Sant Lluis, 07710 Sant Lluis, Menorca`
- El SVG `https://www.hamenorca.com/images/logo-hamenorca-dark.svg` contiene relleno blanco; sobre fondo blanco debe forzarse a negro/gris oscuro con CSS `filter: brightness(0) saturate(100%)`.

## Solicitud de precios a proveedores

- Si falta precio real de materiales o subcontratas, generar email o WhatsApp listo para enviar al proveedor.
- Pedir siempre precio unitario, precio total, IVA, transporte, disponibilidad, plazo de entrega y validez de oferta.
- No cerrar costes definitivos de materiales especiales sin indicar que están sujetos a confirmación de proveedor.

## Reglas de redondeo

- Redondear precios comerciales a importes limpios cuando sea razonable.
- Mantener el IVA calculado sobre la base imponible redondeada.
- Si el usuario pide aplicar un porcentaje adicional, distribuirlo en partidas comerciales y evitar mostrarlo como recargo explícito al cliente.
