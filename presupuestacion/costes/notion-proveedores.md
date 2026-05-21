# Notion - Base de Datos de Proveedores

Estructura exacta recomendada para conectar Notion con el flujo de presupuestacion y poder usar proveedores reales en las estimaciones.

## Objetivo

La base de datos de Notion debe servir para que el agente pueda:

1. Buscar proveedores por categoria, material, proceso y zona.
2. Priorizar proveedores habituales y bien valorados.
3. Preparar solicitudes de precio con contactos correctos.
4. Registrar respuestas y precios historicos.
5. Decidir cuando basta con estimar y cuando hay que pedir presupuesto real.

## Nombre recomendado

`Proveedores - Presupuestador`

## Campos obligatorios

| Campo Notion | Tipo Notion | Uso |
|---|---|---|
| Nombre | Title | Nombre comercial del proveedor. |
| Estado | Select | activo / pendiente / descartado. |
| Categoria | Multi-select | acero / inoxidable / aluminio / vidrio / tornilleria / tratamiento / transporte / montaje / fabricacion / corte laser / pintura / galvanizado. |
| Subcategoria | Multi-select | IPE, HEB, tubo, chapa, pletina, AISI 304, AISI 316, anodizado, lacado, etc. |
| Procesos | Multi-select | suministro, corte, plegado, soldadura, galvanizado, lacado, transporte, montaje. |
| Zona | Select | Menorca / Mallorca / Barcelona / Cataluna / Peninsula / Nacional. |
| Email principal | Email | Email para pedir precios. |
| Telefono | Phone | Telefono general o directo. |
| Persona contacto | Text | Nombre de contacto habitual. |
| Plazo habitual | Text | Ej. 48-72 h, 1 semana, 2-4 semanas. |
| Valoracion | Number | De 1 a 5. |
| Proveedor habitual | Checkbox | Marcar si se puede usar por defecto. |
| Pedido minimo | Number | Importe minimo aproximado en euros. |
| Transporte incluido | Checkbox | Si suele incluir transporte en precio. |
| Ultimo pedido | Date | Fecha del ultimo pedido o consulta. |
| Notas | Text | Criterios, advertencias y condiciones. |

## Campos recomendados

| Campo Notion | Tipo Notion | Uso |
|---|---|---|
| CIF/NIF | Text | Dato administrativo. |
| Web | URL | Pagina web. |
| Direccion | Text | Direccion fisica. |
| Forma de pago | Select | contado / transferencia / 30 dias / habitual / consultar. |
| Rapidez respuesta | Number | De 1 a 5. |
| Calidad precio | Number | De 1 a 5. |
| Riesgo | Select | bajo / medio / alto. |
| Especialidades | Text | Texto libre para busquedas semanticas. |
| No usar para | Text | Casos donde no conviene usarlo. |
| Historico precios | Relation | Relacion futura con una base de historicos. |

## Filtros de uso por el agente

### Busqueda normal

Usar cuando falta precio real o hay que pedir cotizacion:

```text
Estado = activo
Categoria contiene [categoria necesaria]
Subcategoria contiene [material o proceso], si existe
Zona compatible con la entrega
Ordenar por Proveedor habitual DESC, Valoracion DESC, Ultimo pedido DESC
Limitar a 3 proveedores
```

### Busqueda rapida de proveedor habitual

Usar cuando el trabajo encaja con una relacion ya probada:

```text
Estado = activo
Proveedor habitual = true
Categoria contiene [categoria necesaria]
Valoracion >= 4
Limitar a 1-2 proveedores
```

### Busqueda para tratamientos externos

Usar para galvanizado, lacado, anodizado, pintura o chorreado:

```text
Estado = activo
Categoria contiene tratamiento
Procesos contiene [tratamiento requerido]
Zona = Barcelona / Cataluna / Peninsula, segun origen de la pieza
Ordenar por Valoracion DESC
```

## Reglas de decision

- Si hay proveedor conocido con precio historico suficiente, estimar sin pedir precio real.
- Si falta contacto, precio, plazo o categoria, pedir al usuario completar la ficha de Notion.
- Si el importe estimado supera los umbrales de `proveedores-conocidos.md`, preparar solicitud real.
- Si hay geometria especial, tolerancias criticas, galvanizado real no tabulado o montaje complejo, preparar solicitud real.
- Antes de enviar emails, el agente siempre debe mostrar el borrador y pedir confirmacion del usuario.

## Fichas iniciales a crear en Notion

### Ferros Puig Sallent

| Campo | Valor |
|---|---|
| Nombre | Ferros Puig Sallent |
| Estado | activo |
| Categoria | acero, fabricacion, montaje, tratamiento |
| Subcategoria | S235, S275, S355, IPN, IPE, HEB, tubo, chapa gruesa |
| Procesos | suministro, corte, soldadura, taladro, montaje, preparacion galvanizado |
| Zona | Barcelona / Cataluna / Peninsula |
| Email principal | ttejero@ferrospuig.com |
| Telefono | 936 33 37 93 / 661 909 920 |
| Persona contacto | Tomas Tejero / Josep Bramon / Tecnics Sallent |
| Plazo habitual | 2-4 semanas segun carga |
| Valoracion | 5 |
| Proveedor habitual | true |
| Notas | Usar para hierro grande, estructuras de acero negro y piezas que iran a galvanizado en caliente. Emails alternativos: jbramon@ferrospuig.com, tecnicsallent@ferrospuig.com. |

## Configuracion local

Crear localmente `presupuestacion/costes/proveedores-config.json` copiando `proveedores-config.example.json` y rellenando:

```json
{
  "notion": {
    "api_key": "ntn_xxx",
    "database_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  }
}
```

No subir `proveedores-config.json` a GitHub. Esta excluido por `.gitignore` porque contiene credenciales.

## Como obtener los datos de Notion

1. Crear una integracion en Notion desde `https://www.notion.so/my-integrations`.
2. Copiar el `Internal Integration Secret` como `api_key`.
3. Compartir la base de datos `Proveedores - Presupuestador` con esa integracion.
4. Copiar el ID de la base de datos desde la URL de Notion y guardarlo como `database_id`.

## Uso en presupuestos

Cuando se presupuesten materiales o subcontratas:

1. Consultar primero `proveedores-conocidos.md`.
2. Si no hay proveedor suficiente, consultar Notion con los filtros anteriores.
3. Seleccionar maximo 3 proveedores candidatos.
4. Preparar emails separados por categoria o servicio.
5. Esperar confirmacion del usuario antes de enviar.
6. Registrar la respuesta en Notion y, si genera una regla reutilizable, documentarla tambien en este repositorio.
