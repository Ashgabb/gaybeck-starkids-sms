@echo off
REM Gaybeck Starkids SMS - Application Launcher
REM This script launches the SMS application with a hidden console

cd /d "%~dp0"

REM Run the VBScript launcher which hides the console completely
if exist "launch_sms.vbs" (
    cscript.exe //nologo "launch_sms.vbs"
    exit /b 0
)

REM Fallback: Use pythonw.exe directly if VBScript not found
pythonw.exe sms.py

