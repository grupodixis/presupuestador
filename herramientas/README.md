# Herramientas

## Visor Markdown

El visor Markdown permite revisar la documentación del repositorio desde el navegador con búsqueda y navegación lateral.

### Uso desde PowerShell

```powershell
powershell -ExecutionPolicy Bypass -File herramientas\abrir-visor-md.ps1
```

El script:

1. Recorre el repositorio buscando archivos `*.md`.
2. Genera `herramientas/md-manifest.js` con el contenido indexado.
3. Abre `herramientas/visor-md.html` en el navegador.

### Uso desde OpenCode

Usar el comando configurado:

```text
/visor-md
```

Después de añadir o modificar archivos Markdown, volver a ejecutar el visor para regenerar el índice.

### Notas

- `md-manifest.js` es generado automáticamente y no debe editarse a mano.
- El visor funciona sin servidor local porque el contenido Markdown queda embebido en el manifiesto generado.
