# Proveedores y Petición de Precios

Flujo de trabajo para consultar precios a proveedores usando la base de datos de Notion y generación de correos electrónicos.

---

## Visión general del proceso (Fase 5)

```
1. Detectar materiales/tratamientos/servicios externos necesarios
2. Consultar proveedores-conocidos.md (proveedores habituales locales)
3. Consultar Notion → lista completa de proveedores por tipo
4. Seleccionar proveedores candidatos (2-3 por material/servicio)
5. Generar borradores de email con solicitud de precio
6. → USUARIO: revisa y confirma los emails ←
7. Enviar emails (desde casilla de correo designada)
8. Recibir y registrar presupuestos de proveedores
9. Seleccionar mejor relación calidad-precio
10. Incorporar al coste técnico base
```

## Proveedores habituales conocidos

Antes de consultar Notion, revisar `proveedores-conocidos.md` para subcontrataciones tipicas:

| Situacion | Proveedor habitual | Cuando usarlo |
|---|---|---|
| Estructura grande + galvanizado | Ferros Puig Sallent (Sallent) | Estructura que ira a galvanizar en caliente. Ellos fabrican y preparan las piezas. |
| Corte laser en inoxidable | Taller de corte laser (Barcelona) | Piezas vistas de inoxidable que requieren corte de precision (pletinas, anclajes, elementos decorativos). |

Si el trabajo encaja con alguno de estos proveedores conocidos, contactar directamente sin necesidad de buscar en Notion.

---

## Conexión con Notion

### Base de datos de proveedores (Notion)

La base de datos en Notion debe tener esta estructura (o similar):

| Campo | Tipo | Ejemplo |
|---|---|---|
| Nombre | Texto | Hierros S.A. |
| Tipo de material | Select | acero / inoxidable / aluminio / vidrio / tratamiento / transporte |
| Subcategoría | Texto | IPE, HEB, tubo, chapa, pletina |
| Email de contacto | Email | pedidos@hierros.es |
| Teléfono | Teléfono | 912 345 678 |
| Persona de contacto | Texto | Juan López |
| Plazo de entrega estimado | Texto | 48-72 h |
| Zona de envío | Select | nacional / regional / local |
| Valoración | Number | 4/5 |
| Último pedido | Fecha | 2026-03-15 |
| Notas | Texto | Buen precio en inoxidable |

### Archivo de configuración

Crear un archivo `proveedores-config.json` (NO subir a git, contiene la API key):

```json
{
  "notion_api_key": "ntn_...",
  "database_id": "abcdef123456...",
  "email_config": {
    "smtp_server": "smtp.tucorreo.com",
    "smtp_port": 587,
    "email_from": "presupuestos@tuempresa.com",
    "email_name": "Departamento de Presupuestos"
  }
}
```

### Consulta al agente IA

Cuando el agente necesite precios, debe:

1. Identificar qué materiales necesita y en qué cantidades.
2. Extraer de Notion los proveedores que suministran ese tipo de material.
3. Filtrar por los mejor valorados o más usados recientemente.
4. Preparar un email para cada uno con la solicitud de precio.

---

## Generación de emails

### Plantilla de email para solicitud de precio

**Asunto:** Solicitud de presupuesto — [Nombre del proyecto/cliente] — [Material]

**Cuerpo:**

```
Estimado/a [Contacto],

Somos [Nombre empresa], fabricantes de estructuras metálicas y carpintería.

Estamos preparando un presupuesto para [descripción breve del trabajo] y necesitamos cotización para los siguientes materiales:

=== LISTA DE MATERIALES ===

[Material 1] — [Cantidad] — [Medida/dimensiones]
[Material 2] — [Cantidad] — [Medida/dimensiones]
[Material 3] — [Cantidad] — [Medida/dimensiones]

=== CONDICIONES ===

- Lugar de entrega: [Código postal, ciudad]
- Plazo estimado de recogida/entrega: [fecha aprox]
- Transporte: a incluir en la cotización
- Forma de pago: habitual / transferencia 30 días / a consultar

Agradeceríamos nos indiquen:
- Precio unitario y total.
- Plazo de entrega.
- Disponibilidad inmediata o bajo pedido.

Quedamos a la espera de su respuesta.

Un saludo,

[Nombre]
[Teléfono de contacto]
[Email del remitente]
```

### Variantes de plantilla

- **Tratamientos externos:** indicar dimensiones y peso de las piezas, no solo el material.
- **Transporte:** indicar origen, destino, peso y dimensiones de la carga.
- **Subcontratación de montaje:** indicar ubicación de obra, plazo, número de operarios.

---

## Flujo detallado paso a paso

### Paso 1: Detectar necesidades de compra

El agente, durante el cálculo del coste técnico base, identifica:

- Materiales que no están en stock (o se compran específicamente para el trabajo).
- Tratamientos externos (galvanizado, chorreado, anodizado).
- Transporte especial si no se hace con medios propios.
- Subcontratación de montaje si el taller está sobrecargado.

### Paso 2: Consultar proveedores en Notion

El agente usa la API de Notion para consultar proveedores por tipo de material.

**Consulta de ejemplo (SQL-like para Notion API):**
```
Filtrar: Tipo de material = "acero" AND Subcategoría CONTAINS "tubo"
Ordenar: Valoración DESC
Limitar: 3 resultados
```

### Paso 3: Preparar borradores de email

El agente genera un email personalizado para cada proveedor seleccionado con:

- Material especificado con medidas exactas (considerando medidas estándar).
- Cantidades reales a pedir (según cálculo de `costes-materiales.md`).
- Lugar de entrega.
- Plazo.

### Paso 4: Revisión del usuario

Los borradores se presentan al usuario para revisión. El usuario puede:

- ✅ Aprobar y enviar.
- ✏️ Modificar cantidades o proveedor.
- 🚫 Descartar y elegir otro.

### Paso 5: Envío

Una vez confirmados, el agente envía los emails desde la cuenta configurada (smtp).

### Paso 6: Registro de respuestas

El usuario o el agente registran las respuestas recibidas, y se incorpora el mejor precio al cálculo del coste técnico base.

---

## Consideraciones importantes

- **Medidas estándar:** Al solicitar precios, indicar la medida comercial (ej. "tubo redondo Ø40 mm, 6 m") no la medida neta. El proveedor cotiza sobre la barra completa.
- **Cantidades mínimas:** Algunos proveedores tienen cantidades mínimas de pedido. Verificar en la ficha de Notion.
- **Plazos:** El acero inoxidable y los lacados especiales suelen tener más plazo. Considerar en la planificación.
- **Transporte:** El coste de transporte puede ser significativo en pedidos pequeños. Preguntar siempre incluido.
- **Actualización:** Los precios de esta guía (`costes-materiales.md`) deben actualizarse con los precios reales obtenidos de proveedores.

---

## Configuración inicial

1. Crear la base de datos de proveedores en Notion con los campos indicados.
2. Rellenar con los proveedores habituales (mínimo 2-3 por categoría de material).
3. Crear el archivo `proveedores-config.json` con la API key de Notion y configuración SMTP.
4. Añadir `proveedores-config.json` a `.gitignore` (contiene credenciales).
5. Configurar la casilla de correo `presupuestos@tuempresa.com` (o la que se cree).

---

*Documento vivo — actualizar con cada nuevo proveedor o cambio de proceso.*
