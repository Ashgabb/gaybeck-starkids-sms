@echo off
REM Gaybeck Starkids SMS - Website Local Server
REM This script serves the website locally for testing

cd /d "%~dp0website"

echo.
echo ================================
echo Gaybeck Starkids SMS - Website
echo ================================
echo.
echo Starting local server...
echo.
echo Open your browser and navigate to: http://localhost:8000
echo.
echo Press Ctrl+C to stop the server.
echo.

python -m http.server 8000
