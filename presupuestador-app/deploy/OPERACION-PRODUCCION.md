# Operacion segura en produccion

## Fuentes de verdad

- `origin/master`: codigo de la aplicacion y conocimiento consolidado.
- SQLite: usuarios, sesiones, configuracion, consumo, indice de presupuestos y lista operativa de precios.
- `presupuestos/` y `skills/aprendizaje/`: datos vivos generados por la aplicacion.
- `presupuestacion/costes/lista-precios.*`: exportacion versionable de la lista operativa.

Nunca ejecutar `git reset --hard`, `git clean` o un `git pull` directo con el servicio activo.

## Despliegue

1. Ejecutar y verificar `systemctl start presupuestador-backup.service`.
2. Integrar primero en Git los cambios vivos de presupuestos, aprendizaje y precios.
3. Detener `presupuestador-app.service`.
4. Actualizar el checkout mediante avance rapido a `origin/master`.
5. Comprobar propietarios de las rutas escribibles y arrancar el servicio.
6. Validar `/api/health`, acceso HTTPS, login y lectura de presupuestos.

## Restauracion

1. Detener el servicio.
2. Verificar `SHA256SUMS` del backup elegido.
3. Restaurar `runtime-data.tgz` en la raiz del repositorio.
4. Restaurar SQLite con el servicio detenido.
5. Arrancar el servicio y repetir las comprobaciones.

## Alta inicial

Una base nueva ya no acepta `admin/admin`. Antes del primer arranque se debe definir temporalmente
`INITIAL_ADMIN_PASSWORD` con un minimo de 12 caracteres. La variable deja de ser necesaria cuando ya existe un usuario.
