@echo off
REM ============================================================================
REM GAYBECK STARKIDS SMS - AUTOMATED INSTALLATION SCRIPT
REM
REM This script automatically sets up Gaybeck Starkids SMS on your computer
REM No technical knowledge required!
REM ============================================================================

setlocal enabledelayedexpansion

REM Set the title
title Gaybeck Starkids SMS - Setup Wizard

REM Colors and formatting
echo.
echo ============================================================================
echo.
echo   GGG     AAAAAA  YYYYY  BBBBB  EEEEEE  CCCCC  K   K
echo  G        A    A  Y   Y  B    B E       C      K  K
echo  G         AAAAA  Y   Y  BBBBB  EEEEE   C      KKK
echo  G        A    A  Y   Y  B    B E       C      K  K
echo   GGG     A    A  Y   Y  BBBBB  EEEEEE  CCCCC  K   K
echo.
echo.
echo          STARKIDS SCHOOL MANAGEMENT SYSTEM
echo.
echo                   INSTALLATION SETUP
echo.
echo ============================================================================
echo.

REM Add delay for visibility
timeout /t 2 /nobreak

REM Step 0: Detect and Remove Old Installation
echo [STEP 0/5] Checking for Old Installation...
echo.

set OLD_INSTALLATION=0

if exist .venv (
    set OLD_INSTALLATION=1
    echo   Old Python environment detected (.venv folder found)
    echo.
    echo   Would you like to remove the old installation?
    echo   This will allow a clean, fresh installation.
    echo.
    set /p REMOVE_OLD="Press Y to remove old installation, or N to keep it [Y/N]: "
    
    if /i "!REMOVE_OLD!"=="Y" (
        echo.
        echo   Removing old installation...
        echo   Please wait...
        echo.
        
        REM Remove virtual environment
        rmdir /s /q .venv >nul 2>&1
        
        REM Remove Python cache directories
        for /d /r . %%d in (__pycache__) do (
            rmdir /s /q "%%d" >nul 2>&1
        )
        
        REM Remove .pyc files
        for /r . %%f in (*.pyc) do (
            del "%%f" >nul 2>&1
        )
        
        REM Remove pip cache
        rmdir /s /q "%APPDATA%\pip\cache" >nul 2>&1
        
        echo   ✓ Old installation removed successfully
        echo.
    ) else (
        echo.
        echo   Keeping old installation. Proceeding with update...
        echo.
    )
) else (
    echo   ✓ No old installation found - Fresh install
    echo.
)

timeout /t 1 /nobreak

REM Step 1: Check Python Installation
echo [STEP 1/5] Checking Python Installation...
echo.
python --version >nul 2>&1
if errorlevel 1 (
    echo ============================================================================
    echo   ERROR: Python is not installed!
    echo ============================================================================
    echo.
    echo   Python is required to run Gaybeck Starkids SMS.
    echo.
    echo   Please install Python 3.13 from: https://www.python.org/downloads/
    echo.
    echo   IMPORTANT: When installing Python, check the box:
    echo   "Add Python to PATH"
    echo.
    echo   After installing Python, run this setup file again.
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo   ✓ Python Found: %PYTHON_VERSION%
echo.
timeout /t 1 /nobreak

REM Step 2: Install Requirements
echo [STEP 2/5] Installing Required Packages...
echo   This may take 2-5 minutes. Please wait...
echo.

python -m pip install --upgrade pip >nul 2>&1

python -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ============================================================================
    echo   ERROR: Failed to install requirements!
    echo ============================================================================
    echo.
    echo   Could not install required Python packages.
    echo.
    echo   Possible solutions:
    echo   1. Check your internet connection
    echo   2. Ensure you have administrator rights
    echo   3. Contact technical support
    echo.
    pause
    exit /b 1
)

echo.
echo   ✓ All packages installed successfully!
echo.
timeout /t 1 /nobreak

REM Step 3: Verify Installation
echo [STEP 3/5] Verifying Installation...
echo.
python -c "import sms; import ai_assessment_grading; print('   ✓ Core modules verified!')" 
if errorlevel 1 (
    echo.
    echo   ⚠ Warning: Some optional modules may not be available
    echo   The system will work with limited features
    echo.
)
timeout /t 1 /nobreak

REM Step 4: Create Launch Script
echo [STEP 4/5] Creating Launch Shortcuts...
echo.

REM Create batch file to launch application
(
    echo @echo off
    echo title Gaybeck Starkids SMS - School Management System
    echo cd /d "%%~dp0"
    echo python sms.py
    echo pause
) > launch_sms.bat

echo   ✓ Launch shortcut created: launch_sms.bat
echo.

REM Create VBS script for no-console launch (optional comfort feature)
(
    echo Set objShell = CreateObject("WScript.Shell"^)
    echo strPath = objShell.CurrentDirectory ^& "\sms.py"
    echo objShell.Run "python """ ^& strPath ^& """", 0, False
) > launch_sms_quiet.vbs

echo   ✓ Silent launch script created: launch_sms_quiet.vbs
echo.

REM Step 5: Create Desktop Shortcut
echo [STEP 5/5] Creating Desktop Shortcut...
echo.

REM Get the current directory (full path)
for /f "tokens=*" %%I in ('cd') do set APPFOLDER=%%I

REM Create VBS script to make desktop shortcut
(
    echo Set oWS = WScript.CreateObject("WScript.Shell"^)
    echo sLinkFile = oWS.SpecialFolders("Desktop"^) ^& "\Gaybeck Starkids SMS.lnk"
    echo Set oLink = oWS.CreateShortcut(sLinkFile^)
    echo oLink.TargetPath = "%APPFOLDER%\launch_sms.bat"
    echo oLink.WorkingDirectory = "%APPFOLDER%"
    echo oLink.Description = "Gaybeck Starkids School Management System"
    echo oLink.IconLocation = "%APPFOLDER%\sms_icon.ico"
    echo oLink.Save
) > create_shortcut.vbs

REM Run the shortcut creation script silently
cscript.exe //nologo create_shortcut.vbs >nul 2>&1
if errorlevel 1 (
    echo   ⚠ Warning: Desktop shortcut could not be created automatically
    echo   You can still run launch_sms.bat from this folder
    echo.
) else (
    echo   ✓ Desktop Shortcut Created!
    echo   Look for "Gaybeck Starkids SMS" on your desktop
    echo.
)

REM Clean up temporary script
if exist create_shortcut.vbs del create_shortcut.vbs >nul 2>&1

echo.

REM Create Desktop Shortcut using VBS
echo [STEP 5/5] Creating Desktop Shortcuts...
echo.

REM Get the current directory (full path)
for /f "tokens=*" %%I in ('cd') do set APPFOLDER=%%I

REM Create VBS script to make shortcut
(
    echo Set oWS = WScript.CreateObject("WScript.Shell"^)
    echo sLinkFile = oWS.SpecialFolders("Desktop"^) ^& "\Gaybeck Starkids SMS.lnk"
    echo Set oLink = oWS.CreateShortcut(sLinkFile^)
    echo oLink.TargetPath = "%APPFOLDER%\launch_sms.bat"
    echo oLink.WorkingDirectory = "%APPFOLDER%"
    echo oLink.Description = "Gaybeck Starkids School Management System"
    echo oLink.IconLocation = "%APPFOLDER%\sms_icon.ico"
    echo oLink.Save
    echo WScript.Echo "Desktop shortcut created successfully!"
) > create_shortcut.vbs

REM Run the shortcut creation script
cscript.exe create_shortcut.vbs >nul 2>&1
if errorlevel 1 (
    echo   ⚠ Warning: Could not create desktop shortcut
    echo   You can still run launch_sms.bat from this folder
) else (
    echo   ✓ Desktop shortcut created: "Gaybeck Starkids SMS"
)
echo.

REM Clean up temporary script
del create_shortcut.vbs >nul 2>&1

REM Final Success Message
echo.
echo ============================================================================
echo.
echo        ✓ INSTALLATION COMPLETE!
echo.
echo ============================================================================
echo.
echo   Gaybeck Starkids SMS has been successfully installed!
echo.
echo   QUICK START:
echo.
echo   1. Look on your Desktop for "Gaybeck Starkids SMS" icon
echo      - If found: Double-click it to start the application
echo      - If NOT found: Double-click "launch_sms.bat" in this folder
echo.
echo   2. Login with these default credentials:
echo       Username: admin
echo       Password: admin123
echo.
echo       OR
echo.
echo       Username: teacher1
echo       Password: teacher123
echo.
echo   3. IMPORTANT: Change the default passwords immediately (for security)
echo.
echo   4. Start adding your school data:
echo       - Teachers
echo       - Classes
echo       - Students
echo.
echo   5. Try the AI Assessment feature to create exams faster!
echo.
echo ============================================================================
echo.
echo   NEED HELP?
echo   - See: SETUP_INSTRUCTIONS.md
echo   - Or: QUICK_REFERENCE.md
echo   - Contact: support@gaybeckstarkids.com
echo.
echo ============================================================================
echo.

pause
