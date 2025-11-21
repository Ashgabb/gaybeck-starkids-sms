@echo off
REM ================================================================
REM Gaybeck Starkids SMS - Uninstallation Script
REM ================================================================

echo.
echo ================================================================
echo Gaybeck Starkids SMS - Uninstallation
echo ================================================================
echo.

REM Remove desktop shortcut
echo Removing shortcuts...
set DESKTOP=%USERPROFILE%\Desktop
if exist "%DESKTOP%\Gaybeck Starkids SMS.lnk" (
    del "%DESKTOP%\Gaybeck Starkids SMS.lnk"
    echo  - Desktop shortcut removed
)

REM Remove Start Menu folder
set START_MENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Gaybeck Starkids SMS
if exist "%START_MENU%" (
    rmdir /s /q "%START_MENU%"
    echo  - Start Menu shortcut removed
)

echo.
echo ================================================================
echo Uninstallation Complete
echo ================================================================
echo.
echo The application shortcuts have been removed from:
echo  - Desktop
echo  - Start Menu
echo.
echo Note: To completely remove the application files:
echo   1. Delete the folder: c:\Users\User\Desktop\GAYBECK STARKIDS SMS
echo.
pause
