@echo off
REM ========================================
REM Gaybeck Starkids Academy SMS - Full Build Script
REM Builds Executable + Installer with Dependencies
REM Version: 2.0.3
REM ========================================

echo ========================================
echo  Gaybeck Starkids Academy SMS
echo  Full Build with Installer
echo  Version 2.0.3
echo ========================================
echo.

REM Step 1: Clean previous builds
echo [1/5] Cleaning previous builds...
if exist build rmdir /s /q build 2>nul
if exist dist rmdir /s /q dist 2>nul
if exist __pycache__ rmdir /s /q __pycache__ 2>nul
if exist installer_output rmdir /s /q installer_output 2>nul
del /f /q *.pyc *.pyo 2>nul
echo      Done!
echo.

REM Step 2: Build executable with PyInstaller
echo [2/5] Building executable with PyInstaller...
C:\Users\USER\AppData\Local\Programs\Python\Python313\python.exe -m PyInstaller sms.spec --clean
if errorlevel 1 (
    echo      ERROR: PyInstaller build failed!
    pause
    exit /b 1
)
echo      Done!
echo.

REM Step 3: Copy additional files
echo [3/5] Copying additional files to dist...
if not exist dist\database mkdir dist\database
if exist database\*.db copy /y database\*.db dist\database\ >nul 2>&1
if exist logo.png copy /y logo.png dist\ >nul
if exist icon.ico copy /y icon.ico dist\ >nul
if exist README.md copy /y README.md dist\ >nul
if exist version.json copy /y version.json dist\ >nul
echo      Done!
echo.

REM Step 4: Build installer with Inno Setup
echo [4/5] Building installer with Inno Setup...
set INNO_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe

if exist "%INNO_PATH%" (
    "%INNO_PATH%" installer.iss
    if errorlevel 1 (
        echo      WARNING: Installer build failed!
        echo      But executable is ready in dist\ folder.
    ) else (
        echo      Installer created successfully!
    )
) else (
    echo      Inno Setup not found at: %INNO_PATH%
    echo      Skipping installer creation.
    echo.
    echo      To create installer:
    echo      1. Download Inno Setup from https://jrsoftware.org/isdl.php
    echo      2. Install to default location
    echo      3. Run this script again
    echo.
    echo      Executable is ready in dist\ folder.
)
echo      Done!
echo.

REM Step 5: Display results
echo [5/5] Build Summary
echo ========================================
echo  Build Information
echo ========================================
echo  Version: 2.0.3
echo  Build Date: November 11, 2025
echo  Python: 3.13.x
echo.
echo  Output Files:
echo  - Executable: dist\GaybeckStarkidsAcademy.exe

if exist installer_output\GaybeckStarkidsAcademy_Setup_v2.0.3.exe (
    echo  - Installer:  installer_output\GaybeckStarkidsAcademy_Setup_v2.0.3.exe
    echo.
    echo  STATUS: COMPLETE (Executable + Installer)
) else (
    echo.
    echo  STATUS: PARTIAL (Executable Only)
)

echo ========================================
echo.
echo Features Included:
echo  * All Python dependencies embedded
echo  * SQLite database support
echo  * PDF generation (ReportLab)
echo  * Calendar widgets (tkcalendar)
echo  * Image processing (Pillow)
echo  * AI/ML analytics (scikit-learn, pandas, numpy)
echo  * Enhanced navigation with keyboard support
echo  * Taskbar icon support (Windows)
echo.
echo Next Steps:
echo  1. Test: Run dist\GaybeckStarkidsAcademy.exe
if exist installer_output\GaybeckStarkidsAcademy_Setup_v2.0.3.exe (
    echo  2. Test Installer on clean system
    echo  3. Verify all features work
    echo  4. Deploy to production
) else (
    echo  2. (Optional) Install Inno Setup for installer
    echo  3. Deploy executable to production
)
echo.
echo ========================================
pause
