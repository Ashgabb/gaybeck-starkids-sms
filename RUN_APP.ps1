#!/usr/bin/env powershell
<#
.SYNOPSIS
    Gaybeck Starkids SMS - Application Launcher
    
.DESCRIPTION
    Launches the Gaybeck Starkids School Management System application
    with proper virtual environment activation
    
.VERSION
    3.0.1 - Fixed venv activation
    
.NOTES
    Requires Python 3.13+
#>

$ErrorActionPreference = "Continue"

# Change to script directory
$scriptPath = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition
Set-Location $scriptPath

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
$venvActivate = Join-Path $scriptPath ".venv\Scripts\Activate.ps1"

if (Test-Path $venvActivate) {
    & $venvActivate
    Write-Host "Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Virtual environment not found" -ForegroundColor Red
    Write-Host "Please run: python -m venv .venv" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if sms.py exists
$smsPath = Join-Path $scriptPath "sms.py"
if (-not (Test-Path $smsPath)) {
    Write-Host "[ERROR] sms.py not found" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Start the application
Write-Host "Starting Gaybeck Starkids SMS..." -ForegroundColor Green
Write-Host ""

python sms.py

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[ERROR] Application failed to start" -ForegroundColor Red
    Write-Host ""
    Write-Host "Troubleshooting:" -ForegroundColor Yellow
    Write-Host "  1. Run: pip install -r requirements.txt" -ForegroundColor Gray
    Write-Host "  2. Verify database exists: database\school_management.db" -ForegroundColor Gray
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}
