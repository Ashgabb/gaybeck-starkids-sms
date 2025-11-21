@echo off
REM ================================================================
REM Gaybeck Starkids SMS - Installation Script
REM ================================================================
REM This script installs the School Management System on your device

echo.
echo ================================================================
echo Gaybeck Starkids SMS - Installation
echo ================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please download and install Python from:
    echo https://www.python.org/downloads/
    echo.
    echo IMPORTANT: During installation, check the box:
    echo "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo [1/4] Python version check... PASSED
echo.

REM Check if pip is available
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: pip is not installed
    echo Please reinstall Python with pip included
    pause
    exit /b 1
)

echo [2/4] Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [3/4] Dependencies installed successfully
echo.

REM Create desktop shortcut
echo [4/4] Creating desktop shortcut...

REM Create shortcut using PowerShell
powershell -Command "
try {
    $DesktopPath = [Environment]::GetFolderPath('Desktop')
    $AppPath = (Resolve-Path .\sms.py).Path
    $IconPath = (Resolve-Path .\sms_icon.ico).Path
    $ShortcutPath = Join-Path $DesktopPath 'Gaybeck Starkids SMS.lnk'
    $PythonExe = (Get-Command python).Source
    
    $WshShell = New-Object -ComObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut($ShortcutPath)
    $Shortcut.TargetPath = $PythonExe
    $Shortcut.Arguments = $AppPath
    $Shortcut.WorkingDirectory = (Split-Path $AppPath)
    $Shortcut.IconLocation = $IconPath
    $Shortcut.Save()
    
    Write-Host 'Desktop shortcut created successfully'
} catch {
    Write-Host 'Warning: Could not create desktop shortcut' -ForegroundColor Yellow
}
"

echo.
echo ================================================================
echo Installation Complete!
echo ================================================================
echo.
echo The application has been installed successfully.
echo.
echo To launch the application:
echo   1. Look for "Gaybeck Starkids SMS" icon on your Desktop
echo   2. Double-click to run
echo.
echo Default Login Credentials:
echo   Username: admin
echo   Password: admin123
echo.
echo ================================================================
echo.
pause
