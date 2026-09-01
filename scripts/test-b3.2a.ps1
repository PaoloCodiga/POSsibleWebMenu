param()

$ErrorActionPreference = 'Stop'
$Database = 'possible_web_menu_b3_2a'
$ComposeFile = '.dev/docker-compose.test.yml'
$OdooArguments = @(
  'odoo', '-d', $Database,
  '--db_host=db', '--db_user=odoo', '--db_password=odoo',
  '--addons-path=/usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons'
)

function Invoke-ComposeOdoo([string[]] $Arguments) {
  & docker compose -f $ComposeFile run --rm odoo @Arguments
  if ($LASTEXITCODE -ne 0) {
    throw "Odoo command failed with exit code $LASTEXITCODE."
  }
}

docker compose -f $ComposeFile up -d db | Out-Host
$deadline = (Get-Date).AddSeconds(60)
do {
  $databaseService = docker compose -f $ComposeFile ps --format json db | ConvertFrom-Json
  if ($databaseService.Health -eq 'healthy') {
    break
  }
  Start-Sleep -Seconds 2
} while ((Get-Date) -lt $deadline)
if ($databaseService.Health -ne 'healthy') {
  throw 'PostgreSQL did not become healthy within 60 seconds.'
}
Write-Output '[1/9] PostgreSQL ready'

Write-Output '[2/9] Installing fresh test database'
Invoke-ComposeOdoo ($OdooArguments + @('-i', 'possible_web_menu', '--no-http', '--stop-after-init'))

$moduleState = & docker compose -f $ComposeFile exec -T db psql -U odoo -d $Database -Atqc "SELECT state FROM ir_module_module WHERE name = 'possible_web_menu'"
if ($LASTEXITCODE -ne 0 -or $moduleState -ne 'installed') {
  throw "possible_web_menu module state is '$moduleState', expected 'installed'."
}
Write-Output '[3/9] Module state verified'

$serverStarted = $false
$httpReady = $false
$chromeStarted = $false
& docker compose -f $ComposeFile run --rm odoo @OdooArguments -u possible_web_menu --test-enable --test-tags '/possible_web_menu:TestPossibleWebMenuBrowserBootstrap.test_public_menu_browser_js' --stop-after-init 2>&1 | ForEach-Object {
  $line = $_.ToString()
  if (-not $serverStarted -and $line -match 'HTTP service \(werkzeug\) running') {
    Write-Output '[4/9] Odoo HTTP server started'
    $serverStarted = $true
  }
  if (-not $httpReady -and $serverStarted -and $line -match 'Starting TestPossibleWebMenuBrowserBootstrap\.test_public_menu_browser_js') {
    Write-Output '[5/9] Odoo HTTP server ready'
    $httpReady = $true
  }
  if (-not $chromeStarted -and $line -match 'Chrome pid:') {
    Write-Output '[7/9] Chrome process started'
    $chromeStarted = $true
  }
  Write-Output $line
}
if ($LASTEXITCODE -ne 0) {
  throw "Focused browser_js test failed with exit code $LASTEXITCODE."
}
if (-not $serverStarted -or -not $httpReady -or -not $chromeStarted) {
  throw 'Focused browser_js test exited before all diagnostic phases were observed.'
}
