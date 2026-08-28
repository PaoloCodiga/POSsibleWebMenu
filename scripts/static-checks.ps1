$ErrorActionPreference = 'Stop'
py -m compileall -q .
Get-ChildItem views,data -Recurse -Filter *.xml | ForEach-Object { [xml](Get-Content $_.FullName -Raw) | Out-Null }
rg -n 'publicWidget|options\.registry|web\.ajax|ajax\.jsonRpc|console\.log|^\s*print\(' --glob '!docs/**' --glob '!tests/**' --glob '!scripts/**' .
if ($LASTEXITCODE -eq 0) { throw 'Forbidden production API found.' }
if ($LASTEXITCODE -gt 1) { exit $LASTEXITCODE }
