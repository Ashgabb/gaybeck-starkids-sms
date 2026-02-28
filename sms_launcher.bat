@echo off
REM ============================================================
REM Gaybeck Starkids SMS - Windows Batch Launcher (v2.0)
REM ============================================================
REM This batch file launches the SMS application
REM It handles the Python environment and proper startup
REM Portable version - works on any device

setlocal enabledelayedexpansion

REM Get the directory where this batch file is located
cd /d "%~dp0"

REM Try to use launch_app.py with enhanced error handling
REM First, try pythonw.exe (no console window)
pythonw.exe launch_app.py > nul 2>&1
if errorlevel 1 (
    REM Fallback to python.exe if pythonw is not available
    python.exe launch_app.py
    if errorlevel 1 (
        REM Last resort: Try launching direct with sms.py
        pythonw.exe sms.py > nul 2>&1
        if errorlevel 1 (
            python.exe sms.py
        )
    )
)

exit /b 0
