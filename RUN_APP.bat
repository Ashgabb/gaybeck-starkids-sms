@echo off
REM Gaybeck Starkids SMS - Application Launcher
REM Version: 3.0.1 - Uses Python launcher for better compatibility

setlocal enabledelayedexpansion

REM Get the directory of this script
cd /d "%~dp0"

REM Launch the Python bootstrap script which handles venv
python launch_sms.py

REM Exit
endlocal
exit /b 0
