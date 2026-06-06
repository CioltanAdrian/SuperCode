$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot

$venvPath = Join-Path $projectRoot "venv"
$venvPython = Join-Path $venvPath "Scripts\python.exe"
$activateScript = Join-Path $venvPath "Scripts\Activate.ps1"
$requirements = Join-Path $projectRoot "requirements.txt"

if (-not (Test-Path $requirements)) {
    throw "Fisierul requirements.txt nu a fost gasit."
}

if (Test-Path $venvPath) {
    Write-Host "Se sterge mediul virtual existent..."
    Remove-Item -LiteralPath $venvPath -Recurse -Force
}

Write-Host "Se creeaza un mediu virtual nou..."
if (Get-Command py -ErrorAction SilentlyContinue) {
    & py -m venv $venvPath
}
elseif (Get-Command python -ErrorAction SilentlyContinue) {
    & python -m venv $venvPath
}
else {
    throw "Python nu este instalat sau nu este disponibil in PATH."
}

Write-Host "Se actualizeaza pip..."
& $venvPython -m pip install --upgrade pip

Write-Host "Se instaleaza dependentele..."
& $venvPython -m pip install --no-cache-dir -r $requirements

Write-Host "Mediul virtual este pregatit si activat."
. $activateScript
