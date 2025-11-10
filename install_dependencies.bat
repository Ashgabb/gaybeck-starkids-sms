@echo off
echo Installing required dependencies for STARKIDS School Management System...
echo.

echo Installing Pillow (for photo functionality)...
pip install Pillow
if %errorlevel% neq 0 (
    echo Failed to install Pillow. Please check your Python and pip installation.
    pause
    exit /b 1
)

echo.
echo Installing OpenCV (for camera functionality - optional)...
pip install opencv-python
if %errorlevel% neq 0 (
    echo Warning: Failed to install OpenCV. Camera features will not be available.
)

echo.
echo Installing tkcalendar (for enhanced date picker - optional)...
pip install tkcalendar
if %errorlevel% neq 0 (
    echo Warning: Failed to install tkcalendar. Basic date entry will be used.
)

echo.
echo Installing ReportLab (for PDF reports - optional)...
pip install reportlab
if %errorlevel% neq 0 (
    echo Warning: Failed to install ReportLab. PDF export features will not be available.
)

echo.
echo Installation complete!
echo.
echo Photo functionality should now work properly.
echo Run the school management system to test all features.
echo.
pause