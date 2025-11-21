@echo off
REM ================================================================
REM Gaybeck Starkids SMS - Uninstallation Script
REM ================================================================

echo.
echo ================================================================
echo Gaybeck Starkids SMS - Uninstallation
echo ================================================================
echo.

setlocal enabledelayedexpansion

REM Get username
for /f "tokens=3" %%A in ('whoami /all ^| find "User name"') do set USERNAME=%%A

REM Remove desktop shortcut
echo Removing desktop shortcut...
set DESKTOP=%USERPROFILE%\Desktop
if exist "%DESKTOP%\Gaybeck Starkids SMS.lnk" (
    del "%DESKTOP%\Gaybeck Starkids SMS.lnk"
    echo Desktop shortcut removed
) else (
    echo No desktop shortcut found
)

echo.
echo ================================================================
echo Uninstallation Complete
echo ================================================================
echo.
echo The application shortcut has been removed.
echo.
echo Note: To completely remove the application files:
echo   1. Delete the folder containing the application
echo.
pause
