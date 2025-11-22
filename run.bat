@echo off
REM Gaybeck Starkids SMS - Enhanced Launcher
REM This script ensures the app window is properly displayed

setlocal enabledelayedexpansion

REM Get the directory where this batch file is located
set APP_DIR=%~dp0

REM Change to app directory
cd /d "%APP_DIR%"

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed
    pause
    exit /b 1
)

REM Check if sms.py exists
if not exist "sms.py" (
    echo ERROR: sms.py not found
    pause
    exit /b 1
)

REM Start the application with proper window handling
python sms.py

REM If we reach here, the app closed
exit /b 0
