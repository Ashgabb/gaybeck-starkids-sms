@echo off
REM Build script for Windows
REM Creates standalone executable using PyInstaller
REM Requires: Python 3.13+, pip

echo.
echo ╔════════════════════════════════════════════════════╗
echo ║  Gaybeck Starkids SMS - Build Script (Windows)     ║
echo ║  Version: 2.0.3                                    ║
echo ╚════════════════════════════════════════════════════╝
echo.

REM Check Python version
echo Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Python is required but not installed.
    echo Please install Python 3.13+ from https://www.python.org
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✓ Python %PYTHON_VERSION% detected
echo.

REM Create virtual environment
echo Setting up virtual environment...
if not exist "venv\" (
    python -m venv venv
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ✗ Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip >nul 2>&1
echo ✓ pip upgraded
echo.

REM Install PyInstaller
echo Installing PyInstaller...
pip install pyinstaller>=6.0 >nul 2>&1
if errorlevel 1 (
    echo ✗ Failed to install PyInstaller
    pause
    exit /b 1
)
echo ✓ PyInstaller installed
echo.

REM Install application dependencies
echo Installing application dependencies...
pip install -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo ✗ Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed
echo.

REM Clean previous builds
echo Cleaning previous builds...
for /d %%x in (build dist) do (
    if exist "%%x" rmdir /s /q "%%x"
)
del /q *.spec >nul 2>&1
echo ✓ Cleanup complete
echo.

REM Build executable
echo Building executable (this may take 2-3 minutes)...
pyinstaller build_config.spec --onedir
if errorlevel 1 (
    echo ✗ Build failed
    pause
    exit /b 1
)
echo.

REM Verify build
if exist "dist\GaybeckStarKidsSMS\GaybeckStarKidsSMS.exe" (
    echo ✓ Executable created successfully
) else (
    echo ✗ Build completed but executable not found
    pause
    exit /b 1
)
echo.

REM Create Windows installer (optional - requires NSIS)
echo.
echo Creating distribution package...
if exist "dist\GaybeckStarKidsSMS" (
    cd dist
    REM Create ZIP archive
    powershell -Command "Compress-Archive -Path 'GaybeckStarKidsSMS' -DestinationPath 'GaybeckStarKidsSMS_Windows_%date:~10,4%%date:~4,2%%date:~7,2%.zip' -Force"
    cd ..
    echo ✓ Windows package created
) else (
    echo ✗ Distribution folder not found
)
echo.

echo ╔════════════════════════════════════════════════════╗
echo ║  ✓ Build Complete!                                 ║
echo ║                                                    ║
echo ║  Executable location:                              ║
echo ║  → dist\GaybeckStarKidsSMS\GaybeckStarKidsSMS.exe   ║
echo ║                                                    ║
echo ║  To run:                                           ║
echo ║  → Double-click the exe file or run from terminal  ║
echo ║                                                    ║
echo ║  To create installer:                              ║
echo ║  → Install NSIS and run: installer.nsi             ║
echo ║                                                    ║
echo ╚════════════════════════════════════════════════════╝
echo.
pause
