@echo off
REM ========================================
REM Gaybeck Starkids Academy SMS
REM Local Installation Script
REM ========================================

echo ========================================
echo  Gaybeck Starkids Academy SMS
echo  Local Installation
echo  Version 2.0.3
echo ========================================
echo.

REM Set installation directory
set "INSTALL_DIR=%LOCALAPPDATA%\GaybeckStarkidsAcademy"
set "START_MENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs"
set "DESKTOP=%USERPROFILE%\Desktop"

echo Installing to: %INSTALL_DIR%
echo.

REM Create installation directory
echo [1/5] Creating installation directory...
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
echo      Done!
echo.

REM Copy executable and files
echo [2/5] Copying application files...
copy /y "dist\GaybeckStarkidsAcademy.exe" "%INSTALL_DIR%\" >nul
if exist "dist\icon.ico" copy /y "dist\icon.ico" "%INSTALL_DIR%\" >nul
if exist "dist\logo.png" copy /y "dist\logo.png" "%INSTALL_DIR%\" >nul
if exist "dist\README.md" copy /y "dist\README.md" "%INSTALL_DIR%\" >nul

REM Create database directory
if not exist "%INSTALL_DIR%\database" mkdir "%INSTALL_DIR%\database"
if exist "dist\database\*.db" copy /y "dist\database\*.db" "%INSTALL_DIR%\database\" >nul 2>&1

echo      Done!
echo.

REM Create Start Menu shortcut
echo [3/5] Creating Start Menu shortcut...
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%START_MENU%\Gaybeck Starkids Academy.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\GaybeckStarkidsAcademy.exe'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.IconLocation = '%INSTALL_DIR%\icon.ico'; $Shortcut.Description = 'Gaybeck Starkids Academy Management System'; $Shortcut.Save()"
echo      Done!
echo.

REM Create Desktop shortcut (optional)
echo [4/5] Creating Desktop shortcut...
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP%\Gaybeck Starkids Academy.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\GaybeckStarkidsAcademy.exe'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.IconLocation = '%INSTALL_DIR%\icon.ico'; $Shortcut.Description = 'Gaybeck Starkids Academy Management System'; $Shortcut.Save()"
echo      Done!
echo.

REM Create uninstaller
echo [5/5] Creating uninstaller...
(
echo @echo off
echo echo Uninstalling Gaybeck Starkids Academy SMS...
echo echo.
echo echo This will remove:
echo echo - Application files in %INSTALL_DIR%
echo echo - Start Menu shortcut
echo echo - Desktop shortcut
echo echo.
echo set /p CONFIRM="Are you sure? (Y/N): "
echo if /i "%%CONFIRM%%"=="Y" (
echo     echo.
echo     echo Removing files...
echo     del /q "%DESKTOP%\Gaybeck Starkids Academy.lnk" 2^>nul
echo     del /q "%START_MENU%\Gaybeck Starkids Academy.lnk" 2^>nul
echo     timeout /t 1 /nobreak ^>nul
echo     rd /s /q "%INSTALL_DIR%"
echo     echo.
echo     echo Uninstallation complete!
echo     echo.
echo ^) else (
echo     echo Uninstallation cancelled.
echo ^)
echo pause
) > "%INSTALL_DIR%\uninstall.bat"
echo      Done!
echo.

REM Display installation summary
echo ========================================
echo  Installation Complete!
echo ========================================
echo.
echo Installation Location:
echo  %INSTALL_DIR%
echo.
echo Shortcuts Created:
echo  - Start Menu: %START_MENU%\Gaybeck Starkids Academy.lnk
echo  - Desktop: %DESKTOP%\Gaybeck Starkids Academy.lnk
echo.
echo To Launch:
echo  1. Double-click desktop shortcut
echo  2. Search "Gaybeck" in Start Menu
echo  3. Run from: %INSTALL_DIR%\GaybeckStarkidsAcademy.exe
echo.
echo To Uninstall:
echo  Run: %INSTALL_DIR%\uninstall.bat
echo.
echo ========================================
echo.

REM Ask to launch
set /p LAUNCH="Launch application now? (Y/N): "
if /i "%LAUNCH%"=="Y" (
    start "" "%INSTALL_DIR%\GaybeckStarkidsAcademy.exe"
)

pause
