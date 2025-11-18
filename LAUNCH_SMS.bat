@echo off
REM Gaybeck Starkids SMS - Desktop Launcher
REM Launches the application and hides the console window

cd /d "%~dp0"

REM Check for Python first (quick validation)
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python 3.13+ from https://www.python.org
    pause
    exit /b 1
)

REM Use pythonw to launch without console window
start pythonw sms.py

REM Exit immediately - app runs in background
exit /b 0
