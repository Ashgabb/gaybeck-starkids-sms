@echo off
REM Gaybeck Starkids SMS - Updated Installation Script
REM Version: 2.0.3 (Post-Audit Build)
REM This script installs the School Management System on local device

echo.
echo ========================================
echo GAYBECK STARKIDS SMS - INSTALLER
echo Version: 2.0.3 (Post-Audit)
echo ========================================
echo.

REM Step 1: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python 3.13+ from https://www.python.org
    pause
    exit /b 1
)

echo [1/6] Python found. Proceeding with installation...
echo.

REM Step 2: Create virtual environment
echo [2/6] Creating virtual environment...
python -m venv .venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment.
    pause
    exit /b 1
)

REM Step 3: Activate virtual environment and upgrade pip
echo [3/6] Activating virtual environment and upgrading pip...
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip setuptools wheel

REM Step 4: Install dependencies
echo [4/6] Installing required dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies.
    pause
    exit /b 1
)

REM Step 5: Initialize database
echo [5/6] Initializing database...
python database\incremental_relationships.py
python database\comprehensive_sync_system.py

REM Step 6: Verify installation
echo [6/6] Verifying installation...
python -c "import tkinter; import sqlite3; import pandas; print('✓ All dependencies verified')"
if errorlevel 1 (
    echo WARNING: Some dependencies may not be fully installed, but continuing...
)

echo.
echo ========================================
echo INSTALLATION COMPLETE!
echo ========================================
echo.
echo To launch the application:
echo   1. Open Command Prompt or PowerShell
echo   2. Navigate to: %CD%
echo   3. Run: python sms.py
echo.
echo For more information, see:
echo   - README.md
echo   - docs/ folder
echo.
pause
