# Gaybeck Starkids SMS - Desktop Launcher Guide

## Overview

This directory contains enhanced launcher scripts that make it easy to run the SMS application from your desktop. The application can be launched in multiple ways.

## Launcher Files

### 1. **launch_app.py** (Primary Launcher)
Python-based launcher with environment checking and error handling.

**Features:**
- Automatically checks Python version
- Verifies required packages are installed
- Checks database integrity
- Creates detailed launch logs
- Proper error messages if something is wrong

**Usage:**
```bash
python launch_app.py
```

Logs are saved to: `logs/launch_TIMESTAMP.log`

---

### 2. **sms_launcher.bat** (Windows Batch Launcher)
Simplified Windows batch file that activates virtual environment and launches the app.

**Usage:**
```bash
sms_launcher.bat
```

**What it does:**
- Activates Python virtual environment (if available)
- Launches the application with pythonw.exe (no console window)
- Falls back to python.exe if pythonw is not available

---

### 3. **create_sms_shortcut.vbs** (Desktop Shortcut Creator)
Creates a desktop shortcut for easy access.

**Usage:**
Double-click the VBS file or run:
```cmd
cscript.exe create_sms_shortcut.vbs
```

**What it does:**
- Creates "Gaybeck Starkids SMS" shortcut on your desktop
- Sets working directory to app folder
- Uses custom icon (if available)
- Allows easy application launching with a single click

---

## Quick Start for End Users

### Method 1: Desktop Shortcut (Recommended)
1. Open File Explorer and navigate to the application folder
2. Double-click `create_sms_shortcut.vbs`
3. Click "Yes" if prompted to confirm
4. Look for "Gaybeck Starkids SMS" on your desktop
5. Double-click the shortcut to launch the application

### Method 2: Command Line
Open Command Prompt in the application folder and run:
```cmd
sms_launcher.bat
```

### Method 3: With Python Directly
```bash
python sms.py
```

---

## Environment Requirements

- **Python:** 3.8 or higher (3.13+ recommended)
- **Required Packages:**
  - tkinter (GUI framework)
  - sqlite3 (Database)
  
- **Optional Packages:**
  - tkcalendar (Date picker)
  - reportlab (PDF generation)
  - Pillow/PIL (Image processing)
  - opencv-python (Camera support)
  - numpy, pandas (Data analysis)
  - scikit-learn (Machine learning)

### Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Troubleshooting

### Problem: "Python not found" or "command not recognized"
**Solution:** 
1. Ensure Python is installed and added to system PATH
2. Use the full path to python.exe
3. Check that venv is activated if using virtual environment

### Problem: "Module not found" errors
**Solution:**
```bash
pip install -r requirements.txt
```

### Problem: Application won't start
**Steps:**
1. Open `logs/launch_TIMESTAMP.log` file
2. Check the error message in the log
3. Verify database file exists at: `database/school_management.db`
4. Ensure write permissions in the application folder

### Problem: Console window appears when launching
**Solution:**
The app automatically uses pythonw.exe for GUI apps. If console appears anyway, use sms_launcher.bat instead of running sms.py directly.

---

## Clearing Application Data

The SMS application includes a "Clear All Data" feature for testing and development:

### Types of Clear Options:
1. **Clear All Students** - Removes all student records (keeps classes and teachers)
2. **Clear All Attendance** - Removes attendance records only
3. **Clear All Fees** - Removes fee payment records only
4. **Clear All Grades** - Removes grade records only
5. **Clear ALL Test Data** (Nuclear Option) - Removes everything except user accounts

### How to Use:
1. Launch the application
2. Log in as Admin
3. Go to **Settings → Data Management**
4. Select the clear option you want
5. Confirm the warning message
6. The data will be cleared

**⚠️ WARNING:** Data clearing operations cannot be undone! **Always backup your database first!**

### Backup Before Clearing:
1. Go to **Settings → Backup & Restore**
2. Click **"Full Database Backup"**
3. A backup file will be created in `database_backups/` folder
4. Now you're safe to clear data

---

## Testing the Installation

To verify everything is working:

```bash
python tests/test_clear_all_data.py
```

This will:
- Check database integrity
- Test all clear functions
- Verify launcher scripts
- Report any issues

---

## Virtual Environment Setup (Optional)

If using a virtual environment:

### Create Virtual Environment
```bash
python -m venv .venv-1
```

### Activate Virtual Environment
- **Windows:**
  ```bash
  .venv-1\Scripts\activate
  ```
- **Linux/Mac:**
  ```bash
  source .venv-1/bin/activate
  ```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Deactivate When Done
```bash
deactivate
```

---

## Log Files

Launcher logs are automatically saved to: `logs/launch_TIMESTAMP.log`

These logs are useful for troubleshooting if the app fails to start.

---

## Contact & Support

For questions or issues with the launcher:
1. Check the log file for detailed error messages
2. Review troubleshooting section above
3. Verify all dependencies are installed
4. Ensure database permissions are correct

---

## Version Information

- **Launcher Version:** 1.0.0
- **SMS Application Version:** 2.0.3
- **Database:** SQLite3
- **Last Updated:** February 28, 2026

---

**Gaybeck Starkids School Management System**

*A comprehensive school management solution with AI analytics and real-time synchronization.*
