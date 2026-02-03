@echo off
REM ========================================================================
REM Gaybeck Starkids SMS - One-Click Installer Creator
REM ========================================================================
REM This script creates a production-ready installer executable for
REM non-technical users. It automates all build steps and creates a
REM Windows installer package.
REM
REM Requirements:
REM   - Python 3.13+
REM   - NSIS (Nullsoft Scriptable Install System)
REM   - PyInstaller
REM
REM Usage:
REM   Double-click this file to create the installer
REM ========================================================================

setlocal enabledelayedexpansion
cls

REM Define colors using escape codes (requires Windows 10+)
set "SUCCESS=[92m"
set "ERROR=[91m"
set "INFO=[94m"
set "RESET=[0m"

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║   GAYBECK STARKIDS SMS - INSTALLER CREATOR                   ║
echo ║                                                                ║
echo ║   This script will create a complete Windows installer for     ║
echo ║   non-technical users.                                        ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM ========================================================================
REM STEP 1: Check Python Installation
REM ========================================================================
echo [STEP 1/8] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ✗ ERROR: Python 3.13+ is required but not found!
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo.
    echo Steps:
    echo   1. Go to https://www.python.org/downloads/
    echo   2. Click "Downloads"
    echo   3. Download Python 3.13 or higher
    echo   4. Run the installer
    echo   5. IMPORTANT: Check "Add Python to PATH"
    echo   6. Restart your computer
    echo   7. Run this script again
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✓ Python %PYTHON_VERSION% found
echo.

REM ========================================================================
REM STEP 2: Create Virtual Environment
REM ========================================================================
echo [STEP 2/8] Setting up virtual environment...
if not exist "venv" (
    python -m venv venv
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)
echo.

REM ========================================================================
REM STEP 3: Activate Virtual Environment
REM ========================================================================
echo [STEP 3/8] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ✗ ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment activated
echo.

REM ========================================================================
REM STEP 4: Install Build Tools
REM ========================================================================
echo [STEP 4/8] Installing build tools...
echo Installing PyInstaller...
pip install --upgrade pip setuptools wheel >nul 2>&1
pip install pyinstaller>=6.1.0 >nul 2>&1
if errorlevel 1 (
    echo ✗ ERROR: Failed to install PyInstaller
    pause
    exit /b 1
)
echo ✓ PyInstaller installed
echo.

REM ========================================================================
REM STEP 5: Install Application Dependencies
REM ========================================================================
echo [STEP 5/8] Installing application dependencies...
pip install -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo ✗ ERROR: Failed to install application dependencies
    echo Please check requirements.txt
    pause
    exit /b 1
)
echo ✓ All dependencies installed
echo.

REM ========================================================================
REM STEP 6: Clean Previous Builds
REM ========================================================================
echo [STEP 6/8] Cleaning previous builds...
if exist "build" (
    rmdir /s /q build >nul 2>&1
    echo ✓ Removed old build folder
)
if exist "dist" (
    rmdir /s /q dist >nul 2>&1
    echo ✓ Removed old dist folder
)
echo.

REM ========================================================================
REM STEP 7: Build Executable
REM ========================================================================
echo [STEP 7/8] Building executable with PyInstaller...
echo This may take 2-3 minutes, please wait...
echo.

pyinstaller build_config.spec --onedir --noconfirm --log-level=WARNING

if not exist "dist\GaybeckStarKidsSMS\GaybeckStarKidsSMS.exe" (
    echo.
    echo ✗ ERROR: Executable creation failed!
    echo Please check the error messages above.
    pause
    exit /b 1
)
echo ✓ Executable created successfully
echo.

REM ========================================================================
REM STEP 8: Create Windows Installer (if NSIS is available)
REM ========================================================================
echo [STEP 8/8] Creating Windows installer package...

REM Check if NSIS is installed
where makensis >nul 2>&1
if %errorlevel% equ 0 (
    echo NSIS found, creating Windows installer...
    makensis /V2 installer.nsi
    
    if exist "GaybeckStarKidsSMS_Installer_2.0.3.exe" (
        echo ✓ Windows installer created successfully
        echo.
        echo Location: GaybeckStarKidsSMS_Installer_2.0.3.exe
    ) else (
        echo ⚠ NSIS compilation may have had issues
        echo ✓ But portable version is ready in: dist\GaybeckStarKidsSMS\
    )
) else (
    echo ⚠ NSIS not found (optional)
    echo ✓ Portable standalone executable is ready in: dist\GaybeckStarKidsSMS\
    echo.
    echo To create a proper Windows installer:
    echo   1. Install NSIS from: https://nsis.sourceforge.io/
    echo   2. Run this script again
)
echo.

REM ========================================================================
REM SUCCESS SUMMARY
REM ========================================================================
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                     BUILD COMPLETED!                          ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo Your installation files are ready:
echo.

if exist "GaybeckStarKidsSMS_Installer_2.0.3.exe" (
    echo ✓ WINDOWS INSTALLER (Recommended):
    echo   File: GaybeckStarKidsSMS_Installer_2.0.3.exe
    echo   Size: ~150-200 MB
    echo   Use this for distribution to end users
    echo.
)

echo ✓ PORTABLE EXECUTABLE:
echo   Location: dist\GaybeckStarKidsSMS\
echo   Main file: GaybeckStarKidsSMS.exe
echo   Use this to run directly without installation
echo.

echo ════════════════════════════════════════════════════════════════
echo NEXT STEPS FOR DISTRIBUTION:
echo ════════════════════════════════════════════════════════════════
echo.

if exist "GaybeckStarKidsSMS_Installer_2.0.3.exe" (
    echo 1. Send "GaybeckStarKidsSMS_Installer_2.0.3.exe" to users
    echo 2. Users simply double-click to install
    echo 3. Application appears in Start Menu
    echo 4. Desktop shortcut is created automatically
    echo.
) else (
    echo 1. Zip the "dist\GaybeckStarKidsSMS" folder
    echo 2. Send the ZIP file to users
    echo 3. Users extract and run GaybeckStarKidsSMS.exe
    echo.
)

echo For support: Contact your IT administrator
echo.
echo ════════════════════════════════════════════════════════════════
echo.

REM Deactivate virtual environment
call venv\Scripts\deactivate.bat >nul 2>&1

REM Keep the window open so user can read the output
echo Press any key to exit...
pause >nul
exit /b 0
