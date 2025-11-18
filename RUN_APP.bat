@echo off
REM Gaybeck Starkids SMS - Application Launcher
REM Version: 3.0.0

setlocal enabledelayedexpansion

cls

echo.
echo ================================================================================
echo  Gaybeck Starkids SMS - Application Launcher v3.0.0
echo ================================================================================
echo.

REM Check for Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo.
    echo Please install Python 3.13+ from https://www.python.org
    echo and make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

REM Get the directory of this script
cd /d "%~dp0"

REM Launch the application with hidden console
echo [INFO] Starting Gaybeck Starkids SMS...
echo.

REM Get the absolute path to the logo icon for taskbar display
set "ICON_PATH=%~dp0sms_icon.ico"
set "PYTHON_PATH=%~dp0sms.py"

REM Start application with icon visible in taskbar
start pythonw "%PYTHON_PATH%"

REM Exit immediately (console will close, app continues in background)
endlocal
exit /b 0
