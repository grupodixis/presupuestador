# Presupuestador App

Web local para crear presupuestos desde un prompt, adjuntar documentacion o imagenes, revisar lineas editables, editar contextos Markdown/YAML/JSON y memorizar sugerencias en skills.

## Despliegue Docker

La app incluye `Dockerfile` y `docker-compose.yml`.

Arranque local o en VPS:

```bash
cd presupuestador-app
docker compose up -d --build
```

El contenedor expone la app solo en localhost del servidor:

```text
127.0.0.1:4177
```

Datos persistentes:

```text
presupuestador-app/data/presupuestador.sqlite
```

El `docker-compose.yml` monta carpetas del repositorio para que el contenedor pueda leer/escribir contextos, presupuestos y aprendizaje:

- `../skills`
- `../presupuestacion`
- `../productos`
- `../plantillas`
- `../proveedores`
- `../glosario`
- `../presupuestos`

Para publicar en `api.hamenorca.com`, usar el proxy inverso apuntando a:

```text
http://127.0.0.1:4177
```

Hay una plantilla Nginx en:

```text
presupuestador-app/deploy/nginx-api.hamenorca.com.conf
```
## Arranque

```powershell
cd C:\Users\pablo\Documents\Presupuestador\presupuestador-app
node server.js
```

Abrir:

```text
http://localhost:4177
```

## Configuracion de API keys

La app tiene un area `Configuracion` para guardar claves de OpenAI y Gemini sin usar variables de entorno. Se guardan localmente en:

```text
presupuestador-app/config.local.json
```

Ese archivo queda fuera de git por la regla `*.local.json`.

Tambien puedes seguir usando variables de entorno si prefieres:

```powershell
$env:OPENAI_API_KEY="..."
$env:OPENAI_MODEL="gpt-4.1-mini"
node server.js
```

O bien:

```powershell
$env:GEMINI_API_KEY="..."
$env:GEMINI_MODEL="gemini-1.5-pro"
node server.js
```

## Contextos y Markdown

El area `Contextos MD` permite listar, abrir y editar archivos permitidos dentro de:

- `skills/`
- `presupuestacion/`
- `productos/`
- `plantillas/`
- `proveedores/`
- `glosario/`

Extensiones editables: `.md`, `.yaml`, `.yml`, `.json`.

## Persistencia SQLite

La app usa SQLite como base local estructurada en:

```text
presupuestador-app/data/presupuestador.sqlite
```

Tablas principales:

- `app_settings`: configuracion de proveedor/modelos/API keys guardadas.
- `token_usage`: uso de tokens registrado por modelo.
- `budgets`: indice y datos JSON editables de presupuestos guardados.

Los archivos siguen existiendo como salida humana y compatibilidad:

- `presupuestos/P-.../README.md`
- `presupuestos/P-.../presupuesto-final.html`
- `presupuestos/P-.../datos.json`
- `skills/*.md` para contexto y aprendizaje.

La carpeta `presupuestador-app/data/` esta pensada como dato local y queda fuera de git.

Endpoint de diagnostico:

```text
GET /api/db/status
```
## Presupuestos

La pantalla principal permite:

- Introducir datos de cliente, obra, NIF/CIF y referencia.
- Crear lineas desde prompt y adjuntos.
- Editar partidas, cantidades y precios unitarios.
- Ver una vista final imprimible.
- Usar `Imprimir / PDF` para abrir el dialogo de impresion del navegador.
- Usar `Guardar presupuesto` para crear una carpeta en `presupuestos/` con:
  - `README.md`
  - `presupuesto-final.html`
  - `datos.json`

## Nota

Los PDF adjuntos se reciben como archivo, pero esta version no extrae texto de PDF en navegador. Para mejores resultados, adjunta tambien texto, Markdown, imagenes o capturas del plano.

## Modelos y tokens

La app ya no requiere escribir el modelo a mano:

- `OpenAI`: consulta `GET /v1/models` con la API key guardada y lista los modelos disponibles para esa clave.
- `Gemini`: consulta `GET /v1beta/models` y muestra los modelos compatibles con `generateContent`.
- Cada modelo muestra disponibilidad, limite de entrada, limite de salida, tokens usados por esta app y saldo local restante si se configuro.
- Tras cada generacion real, la app guarda el uso devuelto por la API en `token-usage.local.json`.

Importante: una API key normal no expone un saldo universal de tokens restantes por modelo. Para poder bloquear modelos sin saldo, la app usa un presupuesto local configurable en `Configuracion`:

```json
{
  "gpt-4.1-mini": 500000,
  "gpt-4o-mini": 250000
}
```

Si no configuras presupuesto local para un modelo, la app lo deja usar si la API lo lista como disponible. Si configuras presupuesto local y el saldo restante estimado no alcanza, bloquea la generacion.

## Panel de presupuestos

El area `Presupuestos` lista automaticamente las carpetas guardadas en `presupuestos/` con formato `P-AAAA-NNNN-slug`.

Funciones:

- Agrupar y filtrar presupuestos por año.
- Ver codigo, titulo, cliente guardado y carpeta.
- Abrir archivos del presupuesto (`README.md`, HTML, PDF, Excel, JSON, etc.) desde la web local.
- Crear un `Nuevo presupuesto`, que limpia el formulario y vuelve a la pantalla principal.
- Usar `Editar` en presupuestos con `datos.json` para cargarlos en la pantalla principal.
- Al guardar un presupuesto editado, se actualiza la misma carpeta en vez de crear una nueva.

El listado se alimenta del endpoint local:

```text
GET /api/budgets
```


## Edicion IA por linea

Cada linea del presupuesto tiene un boton `IA`.

Funciones:

- Abre un prompt especifico para esa partida.
- Envia al agente la linea seleccionada y el presupuesto completo actual, incluyendo cambios manuales ya hechos.
- El agente devuelve el presupuesto completo actualizado, modificando solo esa linea salvo que el prompt pida ajustes relacionados.
- Incluye boton `Borrar linea` dentro del panel IA.
- En modo local sin API, anota el prompt en la descripcion de la linea; con OpenAI/Gemini recalcula usando el contexto completo.

Endpoint local:

```text
POST /api/line-ai
```

