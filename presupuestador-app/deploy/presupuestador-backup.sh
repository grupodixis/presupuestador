#!/usr/bin/env bash
set -euo pipefail

APP_ROOT=/var/www/vhosts/hamenorca.com/presupuestador-runtime/Presupuestador
APP_DIR="$APP_ROOT/presupuestador-app"
BACKUP_ROOT=/var/backups/presupuestador/daily
RETENTION_DAYS="${RETENTION_DAYS:-14}"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
DEST="$BACKUP_ROOT/$STAMP"

install -d -m 0700 -o root -g root "$DEST"
exec 9>"$BACKUP_ROOT/.backup.lock"
flock -n 9 || { echo "Ya hay otro backup en curso." >&2; exit 1; }

sqlite3 "$APP_DIR/data/presupuestador.sqlite" ".backup '$DEST/presupuestador.sqlite'"
test "$(sqlite3 "$DEST/presupuestador.sqlite" 'PRAGMA integrity_check;')" = "ok"

tar --xattrs --acls -czf "$DEST/runtime-data.tgz" -C "$APP_ROOT" \
  presupuestos skills/aprendizaje productos/requisitos presupuestacion/costes \
  presupuestador-app/config.local.json presupuestador-app/token-usage.local.json
git -C "$APP_ROOT" status --porcelain=v1 > "$DEST/git-status.txt"
git -C "$APP_ROOT" rev-parse HEAD > "$DEST/git-head.txt"
sha256sum "$DEST/presupuestador.sqlite" "$DEST/runtime-data.tgz" > "$DEST/SHA256SUMS"

find "$BACKUP_ROOT" -mindepth 1 -maxdepth 1 -type d -mtime "+$RETENTION_DAYS" -exec rm -rf -- {} +
echo "Backup completado: $DEST"
