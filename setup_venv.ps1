# Setup .venv-marker on a new machine
# Run: powershell -ExecutionPolicy Bypass -File setup_venv.ps1
# Requires: uv installed (https://github.com/astral-sh/uv)

$ErrorActionPreference = "Stop"

Write-Host "=== TOEIC Knowledge Base — Environment Setup ===" -ForegroundColor Cyan

# 1. Check uv
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "Installing uv..." -ForegroundColor Yellow
    irm https://astral.sh/uv/install.ps1 | iex
    $env:PATH = "$env:USERPROFILE\.local\bin;$env:PATH"
}
Write-Host "[OK] uv found: $(uv --version)" -ForegroundColor Green

# 2. Create venv with Python 3.12
Write-Host "Creating .venv-marker with Python 3.12..." -ForegroundColor Yellow
uv venv .venv-marker --python 3.12
Write-Host "[OK] .venv-marker created" -ForegroundColor Green

# 3. Install packages
Write-Host "Installing marker-pdf + pymupdf (may take 5-10 min)..." -ForegroundColor Yellow
uv pip install marker-pdf pymupdf --python .venv-marker\Scripts\python.exe
Write-Host "[OK] Packages installed" -ForegroundColor Green

# 4. First run to trigger model download (~3GB, one-time)
Write-Host ""
Write-Host "NOTE: First Marker run will download ~3GB of models." -ForegroundColor Yellow
Write-Host "Models are cached at: $env:LOCALAPPDATA\datalab\" -ForegroundColor Yellow
Write-Host ""
Write-Host "=== Setup complete! ===" -ForegroundColor Cyan
Write-Host "Run extraction: .venv-marker\Scripts\python.exe scripts\extract\run_marker.py reading"
