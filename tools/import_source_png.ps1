param(
  [string]$Matches = (Join-Path $PSScriptRoot 'source-png-match.csv'),
  [string]$Site = (Split-Path $PSScriptRoot -Parent)
)
$selected = Import-Csv -LiteralPath $Matches |
  Where-Object { [double]$_.Distance -le 19 -and ([double]$_.NextDistance - [double]$_.Distance) -ge 12 } |
  Group-Object Page | ForEach-Object { $_.Group | Sort-Object {[double]$_.Distance} | Select-Object -First 1 }
$destination = Join-Path $Site 'assets\source-png'
New-Item -ItemType Directory -Force -Path $destination | Out-Null
$map = @{}
foreach($item in $selected) {
  $name = 'slide-{0:D2}.png' -f [int]$item.Page
  Copy-Item -LiteralPath $item.Source -Destination (Join-Path $destination $name) -Force
  $map[[string]$item.Page] = "assets/source-png/$name"
}
$map | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $Site 'data\source-images.json') -Encoding utf8
"Imported $($selected.Count) confidently matched PNGs."
