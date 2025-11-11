@echo off
REM Gaybeck Starkids Academy SMS - Build Script
REM Version: 2.0.3
REM Date: November 11, 2025

echo ========================================
echo  Gaybeck Starkids Academy SMS Builder
echo  Version 2.0.3
echo ========================================
echo.

REM Clean previous builds
echo [1/4] Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__
del /f /q *.pyc *.pyo 2>nul
echo      Done!
echo.

REM Build executable
echo [2/4] Building executable with PyInstaller...
C:\Users\USER\AppData\Local\Programs\Python\Python313\python.exe -m PyInstaller sms.spec --clean
if errorlevel 1 (
    echo      ERROR: Build failed!
    pause
    exit /b 1
)
echo      Done!
echo.

REM Copy additional files
echo [3/4] Copying additional files...
if not exist dist\database mkdir dist\database
copy database\*.db dist\database\ >nul 2>&1
copy logo.png dist\ >nul 2>&1
copy icon.ico dist\ >nul 2>&1
copy README.md dist\ >nul 2>&1
echo      Done!
echo.

REM Display build info
echo [4/4] Build completed successfully!
echo.
echo ========================================
echo  Build Information
echo ========================================
echo  Version: 2.0.3
echo  Date: November 11, 2025
echo  Output: dist\GaybeckStarkidsAcademy.exe
echo ========================================
echo.
echo Next steps:
echo  1. Test the executable in dist\ folder
echo  2. Run installer build (if needed)
echo  3. Deploy to production
echo.

pause
