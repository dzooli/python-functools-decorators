#!/usr/bin/env pwsh
# Run tests with coverage and open the HTML report

Write-Host "Running tests with coverage..." -ForegroundColor Cyan
uv run pytest

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nOpening coverage report..." -ForegroundColor Green
    Start-Process htmlcov\index.html
} else {
    Write-Host "`nTests failed. Check output above." -ForegroundColor Red
}
