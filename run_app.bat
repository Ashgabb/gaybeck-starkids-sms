@echo off
REM ============================================================
REM Gaybeck Starkids SMS - Direct Application Launcher (v1.0)
REM ============================================================
REM This launcher directly runs sms.py with no dependencies
REM Works on any device with Python installed

setlocal enabledelayedexpansion

cd /d "%~dp0"

echo Launching Gaybeck Starkids SMS...
echo.

REM Try multiple Python executable options
for %%P in (pythonw.exe pythonw python.exe python) do (
    where %%P >nul 2>&1
    if !errorlevel! equ 0 (
        echo Found Python: %%P
        start "" %%P sms.py
        exit /b 0
    )
)

echo Error: Python not found in PATH
echo Please ensure Python is installed and added to system PATH
echo.
pause
exit /b 1\n