@echo off
REM Gaybeck Starkids SMS - New Installation Script
REM This script sets up the environment and dependencies for the School Management System

REM Step 1: Create virtual environment
python -m venv .venv

REM Step 2: Activate virtual environment
call .venv\Scripts\activate.bat

REM Step 3: Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

REM Step 4: Run database setup scripts
python database\incremental_relationships.py
python database\comprehensive_sync_system.py

REM Step 5: Launch application
python sms.py

REM Step 6: Instructions
ECHO Installation complete. To run the application in future, activate the virtual environment and run sms.py.
ECHO For documentation, see the docs folder.
ECHO For troubleshooting, see INSTALLATION_FIX_SUMMARY.md.

pause
