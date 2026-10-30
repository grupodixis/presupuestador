# Script de sincronización automática con Git para Presupuestador
$ErrorActionPreference = "Continue"

Set-Location "c:\Users\pablo\Documents\Presupuestador"

$status = git status --porcelain
if ($status) {
    $branch = (git branch --show-current).Trim()
    if (-not $branch) {
        $branch = "ordenador-trabajo"
    }
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Output "[$timestamp] Detectados cambios en la rama $branch. Sincronizando..."
    git add .
    git commit -m "Auto-sync presupuestos: $timestamp"
    git push origin $branch
    Write-Output "[$timestamp] Sincronización con GitHub completada exitosamente."
} else {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Output "[$timestamp] No hay cambios pendientes para sincronizar."
}
