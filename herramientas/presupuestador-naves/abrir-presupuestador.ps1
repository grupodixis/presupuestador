# Lanzador del Presupuestador de Naves
$indexPath = Join-Path $PSScriptRoot "index.html"
Write-Host "Abriendo el Configurador y Presupuestador de Naves Industriales en el navegador..." -ForegroundColor Cyan
Start-Process $indexPath
