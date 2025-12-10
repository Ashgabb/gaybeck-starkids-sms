@echo off
REM =========================================
REM Gaybeck Starkids SMS - Website Backend
REM =========================================

title Gaybeck Starkids SMS - Backend Server
color 0A

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║   Gaybeck Starkids SMS - Backend API Server                ║
echo ║   Starting...                                              ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python not found!
    echo.
    echo Please install Python 3.13+ from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

REM Navigate to website directory
cd /d "%~dp0"

REM Check if Flask is installed
pip list | findstr flask >nul 2>&1
if errorlevel 1 (
    echo ⏳ Installing required packages...
    pip install -r requirements-backend.txt
    echo.
)

echo.
echo ✅ Starting Flask server...
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo   🌐 Backend API:     http://localhost:5000
echo   📊 API Status:      http://localhost:5000/api/health
echo   💾 Features:        http://localhost:5000/api/features
echo   💲 Pricing:         http://localhost:5000/api/pricing
echo   🗣️  Testimonials:    http://localhost:5000/api/testimonials
echo   📈 Stats:           http://localhost:5000/api/stats
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo ⏲️  Press Ctrl+C to stop the server
echo.

python app.py
