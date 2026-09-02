# spec-builder Windows setup and run script
# Usage: powershell -ExecutionPolicy Bypass -File run_windows.ps1 [args...]
# Default: spec/input -> spec/output/staging + spec/output/docs

param(
    [switch]$Help,

    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$PassThru
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Push-Location $ScriptDir

try {
    if ($Help) {
        Write-Host "Usage: powershell -ExecutionPolicy Bypass -File run_windows.ps1 [--input <path>] [--staging <path>] [--docs <path>] [--checklist <path>] [--agent-ocr]" -ForegroundColor Cyan
        Write-Host "Example: powershell -ExecutionPolicy Bypass -File run_windows.ps1 --input ..\..\..\..\spec\input" -ForegroundColor Cyan
        exit 0
    }

    $pythonVersion = & python --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Python was not found. Install it from https://www.python.org/."
        exit 1
    }
    Write-Host "[OK] $pythonVersion" -ForegroundColor Green

    if (-not (Test-Path ".venv")) {
        Write-Host "[INFO] Creating virtual environment..." -ForegroundColor Cyan
        & python -m venv .venv
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    }

    Write-Host "[INFO] Installing dependencies..." -ForegroundColor Cyan
    & .\.venv\Scripts\pip install --quiet -r requirements.txt
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

    Write-Host "[INFO] Starting conversion..." -ForegroundColor Cyan
    if ($PassThru) {
        & .\.venv\Scripts\python convert_documents.py @PassThru
    } else {
        & .\.venv\Scripts\python convert_documents.py
    }
    exit $LASTEXITCODE

} finally {
    Pop-Location
}
