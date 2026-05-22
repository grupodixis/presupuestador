# Permisos y gobernanza del agente

## Regla base

El agente puede proponer, redactar y preparar. Las acciones externas y cambios críticos requieren aprobación humana.

## Acciones permitidas sin aprobación

- Leer documentación del repositorio.
- Buscar en costes, skills, proveedores y plantillas.
- Generar borradores de presupuesto.
- Generar previews internos.
- Redactar emails o WhatsApps sin enviarlos.
- Crear propuestas documentales locales.

## Acciones que requieren aprobación

- Enviar email a proveedor.
- Enviar WhatsApp a proveedor.
- Registrar un proveedor como `preferente`.
- Actualizar tablas de precios base.
- Subir documentos con datos personales a Git.
- Hacer commit o push.
- Cambiar reglas comerciales por defecto.

## Datos personales

- Los presupuestos de clientes pueden generarse localmente.
- No deben subirse a Git si contienen DNI, dirección, teléfono o datos privados.
- Para ejemplos reutilizables, anonimizar cliente, dirección y referencias personales.

## Auditoría

Cada cambio metodológico debe indicar:

- Qué se aprendió.
- De qué presupuesto o situación viene.
- A qué productos afecta.
- Qué documento se modificó.

## Actualización de precios

Un precio solo debe pasar a tabla de costes si incluye:

- Fecha.
- Proveedor o fuente.
- Unidad.
- IVA incluido/excluido.
- Transporte incluido/excluido.
- Validez o condiciones.

## Criterio de calidad

Un agente útil no solo calcula importes: debe explicar incertidumbres, proteger margen, evitar omisiones y mejorar el sistema documental con cada ciclo.
