@echo off
REM Launch Script for Gaybeck Starkids SMS
REM This works whether installed or not

echo.
echo ===================================================
echo  Gaybeck Starkids Academy - Management System
echo ===================================================
echo.
echo Starting application...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please install Python from https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM Try to launch the application (use pythonw to hide console)
start "" pythonw sms.py 2>nul || python sms.py

if errorlevel 1 (
    echo.
    echo Failed to start the application.
    echo.
    echo Please make sure:
    echo  1. You have run INSTALL.bat first, OR
    echo  2. Required packages are installed (tkcalendar, Pillow)
    echo.
    pause
)
