@echo off
cls
echo.
echo ========================================================
echo   GAYBECK STARKIDS ACADEMY - INSTALLER
echo ========================================================
echo.
pause

cls
echo [1/5] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not installed!
    pause
    exit /b 1
)
echo       OK

echo [2/5] Installing dependencies...
python -m pip install tkcalendar Pillow pywin32 --quiet --upgrade
echo       OK

echo [3/5] Installing application...
python -m pip install dist\gaybeck_starkids_sms-2.0.0-py3-none-any.whl --quiet --force-reinstall --no-deps
echo       OK

echo [4/5] Creating shortcuts...
python post_install.py
echo       OK

cls
echo.
echo INSTALLATION COMPLETE!
echo.
echo Launch from Desktop or Start Menu
echo Username: admin
echo Password: admin123
pause