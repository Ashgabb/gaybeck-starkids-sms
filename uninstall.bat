@echo off@echo off@echo off@echo off

cls

echo.cls

echo ========================================================

echo   GAYBECK STARKIDS ACADEMY - UNINSTALLERecho.REM ===================================================================REM Gaybeck Starkids SMS - Uninstaller Batch File

echo ========================================================

echo.echo ========================================================

echo This will remove:

echo   - Application shortcutsecho   GAYBECK STARKIDS ACADEMY - UNINSTALLERREM  Gaybeck Starkids Academy - Simple One-Click UninstallerREM Double-click this file to completely uninstall the application

echo   - Installed package

echo   - Console scriptsecho ========================================================

echo.

echo Application data can be removed when prompted.echo.REM  Double-click this file to completely remove the application

echo.

pauseecho  This will remove the application.



python -c "exec(open('uninstall.py', encoding='utf-8').read())"echo.REM ===================================================================echo.

pause

pause

echo ===================================================

python -c "import sys; sys.stdin = open('CON'); exec(open('uninstall.py', encoding='utf-8').read())"

color 0Cecho  Gaybeck Starkids Academy - Uninstaller

pause

title Gaybeck Starkids Academy Uninstallerecho ===================================================

echo.

clsecho This will remove:

echo.echo   - The installed application

echo ========================================================echo   - All shortcuts

echo   GAYBECK STARKIDS ACADEMYecho   - Application data (with confirmation)

echo   School Management System - Uninstallerecho.

echo ========================================================pause

echo.echo.

echo  This will remove the application from your computer.

echo.python uninstall.py

echo  What will be removed:

echo    * School Management Softwareif errorlevel 1 (

echo    * Desktop Shortcut    echo.

echo    * Start Menu Entry    echo ERROR: Uninstallation failed or was cancelled.

echo    * Application Data (you will be asked)    echo.

echo.    pause

echo ========================================================    exit /b 1

echo.)

echo  Are you sure you want to uninstall?

pauseecho.

echo Press any key to exit...

clspause > nul

echo.
echo ========================================================
echo   Uninstalling... Please wait...
echo ========================================================
echo.

python uninstall.py

if errorlevel 1 (
    echo.
    echo Uninstallation encountered an error.
    echo.
    pause
    exit /b 1
)

cls
echo.
echo ========================================================
echo   UNINSTALLATION COMPLETE!
echo ========================================================
echo.
echo  The application has been removed from your computer.
echo.
echo  Thank you for using Gaybeck Starkids Academy!
echo.
echo ========================================================
echo.
echo  Press any key to close this window...
pause >nul
