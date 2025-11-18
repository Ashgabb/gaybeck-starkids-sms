@echo off
setlocal enabledelayedexpansion
cls

echo.
echo ================================================================================
echo  Gaybeck Starkids SMS - Professional Installer v3.0.0
echo  Gaybeck Starkids School
echo ================================================================================
echo.

REM Check for admin rights first
echo [Step 1] Checking Administrator privileges...
net session >nul 2>&1
if errorlevel 1 (
    echo.
    echo [!] This installer requires Administrator privileges
    echo [!] Attempting to elevate privileges...
    echo.
    
    REM Re-run as admin using PowerShell
    powershell -NoProfile -Command "Start-Process cmd -ArgumentList '/c \"%~0\"' -Verb RunAs" 2>nul
    if errorlevel 1 (
        echo [ERROR] Failed to elevate privileges
        echo [INFO] Please right-click SETUP.bat and select "Run as Administrator"
        pause
        exit /b 1
    )
    exit /b 0
)

echo [OK] Running with Administrator privileges
echo.

REM Check for Python
echo [Step 2] Checking for Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR] Python is not installed or not in PATH
    echo.
    echo Please install Python 3.13+ from https://www.python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version 2^>^&1') do set "PYTHON_VERSION=%%i"
echo [OK] Found %PYTHON_VERSION%
echo.

REM Run the Python installer
echo [Step 3] Launching installer...
echo.

python "%~dp0GaybeckInstaller.py"
set INSTALLER_EXIT=%errorlevel%

echo.
if %INSTALLER_EXIT% equ 0 (
    echo ================================================================================
    echo  [OK] Installation Complete!
    echo ================================================================================
    echo.
    echo Your Gaybeck Starkids SMS has been installed successfully.
    echo You should see shortcuts on your Desktop and Start Menu.
    echo.
    echo To launch the application:
    echo   - Double-click the "Gaybeck Starkids SMS" shortcut on your Desktop
    echo   - Or use the Start Menu
    echo.
    pause
) else (
    echo ================================================================================
    echo  [ERROR] Installation Failed
    echo ================================================================================
    echo.
    echo The installation did not complete successfully.
    echo Please check the messages above for details.
    echo.
    echo If you continue to have problems:
    echo   1. Make sure you have Python 3.13+ installed
    echo   2. Right-click SETUP.bat and select "Run as Administrator"
    echo   3. Check the INSTALLER_GUIDE.md for more help
    echo.
    pause
    exit /b 1
)

endlocal
