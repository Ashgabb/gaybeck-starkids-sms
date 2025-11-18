#!/usr/bin/env powershell
<#
.SYNOPSIS
    Gaybeck Starkids SMS - Application Launcher
    
.DESCRIPTION
    Launches the Gaybeck Starkids School Management System application
    
.VERSION
    3.0.0
    
.NOTES
    Requires Python 3.13+
#>

param(
    [switch]$Diagnostic
)

$ErrorActionPreference = "Continue"

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "  Gaybeck Starkids SMS - Application Launcher v3.0.0" -ForegroundColor Green
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

# Check for Python
Write-Host "[INFO] Checking for Python..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Python 3.13+ from https://www.python.org" -ForegroundColor Yellow
    Write-Host "Make sure to check 'Add Python to PATH' during installation." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[OK] Found: $pythonVersion" -ForegroundColor Green
Write-Host ""

# Run diagnostic if requested
if ($Diagnostic) {
    Write-Host "[INFO] Running diagnostic tests..." -ForegroundColor Yellow
    Write-Host ""
    python test_launch.py
    Write-Host ""
    Read-Host "Press Enter to continue"
}

# Change to script directory
$scriptPath = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition
Set-Location $scriptPath

# Start the application
Write-Host "[INFO] Starting Gaybeck Starkids SMS..." -ForegroundColor Yellow
Write-Host ""

python sms.py

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[ERROR] Application failed to start" -ForegroundColor Red
    Write-Host ""
    Write-Host "Troubleshooting steps:" -ForegroundColor Yellow
    Write-Host "  1. Run: pip install -r requirements.txt" -ForegroundColor Gray
    Write-Host "  2. Make sure database exists: database\school_management.db" -ForegroundColor Gray
    Write-Host "  3. Check Python version: python --version (should be 3.13+)" -ForegroundColor Gray
    Write-Host "  4. Try running: powershell -File RUN_APP.ps1 -Diagnostic" -ForegroundColor Gray
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}
