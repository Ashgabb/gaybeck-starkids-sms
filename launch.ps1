# Gaybeck Starkids SMS - PowerShell Launcher
# This script launches the School Management System

$AppDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Check if Python is installed
try {
    $PythonVersion = python --version 2>&1
    Write-Host "Python found: $PythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python is not installed" -ForegroundColor Red
    Write-Host ""
    Write-Host "To fix this:"
    Write-Host "1. Download Python from: https://www.python.org/downloads/"
    Write-Host "2. During installation, CHECK 'Add Python to PATH'"
    Write-Host "3. Restart your computer"
    Write-Host "4. Try again"
    Read-Host "Press Enter to exit"
    exit 1
}

# Change to app directory
Set-Location $AppDir

# Launch the application
Write-Host ""
Write-Host "Starting Gaybeck Starkids SMS..." -ForegroundColor Cyan
Write-Host ""

python sms.py

Write-Host ""
Write-Host "Application has closed." -ForegroundColor Yellow
Read-Host "Press Enter to exit"
