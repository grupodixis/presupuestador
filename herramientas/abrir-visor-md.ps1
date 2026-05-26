$ErrorActionPreference = "Stop"

$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path.TrimEnd("\")
$viewer = Join-Path $PSScriptRoot "visor-md.html"
$manifest = Join-Path $PSScriptRoot "md-manifest.js"

$files = Get-ChildItem -LiteralPath $root -Recurse -File -Filter "*.md" |
  Where-Object {
    $full = $_.FullName.Replace("/", "\")
    -not (
      $full.Contains("\.git\") -or
      $full.Contains("\node_modules\") -or
      $full.EndsWith("\herramientas\md-manifest.js")
    )
  } |
  Sort-Object FullName |
  ForEach-Object {
    $relative = $_.FullName.Substring($root.Length + 1).Replace("\", "/")
    [PSCustomObject]@{
      path = $relative
      name = $_.Name
      content = Get-Content -LiteralPath $_.FullName -Raw -Encoding UTF8
    }
  }

$json = $files | ConvertTo-Json -Depth 5 -Compress
if ([string]::IsNullOrWhiteSpace($json)) { $json = "[]" }

Set-Content -LiteralPath $manifest -Value "window.MD_VIEWER_FILES = $json;" -Encoding UTF8
Start-Process -FilePath $viewer

"Visor Markdown actualizado: $($files.Count) archivos indexados."
