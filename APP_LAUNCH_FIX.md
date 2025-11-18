# App Launch Fix - Complete Solution

## Problem
The SMS application was not launching from:
- Desktop icon/shortcut
- Start Menu entry
- Command line

## Root Cause
The original launch mechanism (`RUN_APP.bat` with `pythonw`) didn't properly:
1. Activate the virtual environment
2. Handle working directory paths
3. Execute the main Python application

## Solution Implemented

### 1. Created Python Bootstrap Launcher (`launch_sms.py`)
- Automatically finds and activates the virtual environment
- Properly handles all paths and dependencies
- Works cross-platform (Windows, Linux, macOS)
- More reliable than batch/shell scripts

### 2. Updated Batch File (`RUN_APP.bat`)
- Now delegates to the Python launcher
- Simplified and more maintainable
- Works from any directory

### 3. Updated PowerShell Launcher (`RUN_APP.ps1`)
- Added proper venv activation
- Better error handling
- Consistent with batch file approach

### 4. Generated Proper Windows Shortcuts
- Desktop shortcut: `Gaybeck Starkids SMS.lnk`
- Start Menu shortcut: `Gaybeck Starkids SMS.lnk`
- Both point to `launch_sms.py` for reliability
- Proper working directory set
- Custom icon configured

### 5. Added Testing Utilities
- `test_startup.py`: Validates all dependencies
- `setup_shortcuts.py`: Creates/updates Windows shortcuts

## How to Use

### From Desktop
Double-click the **"Gaybeck Starkids SMS"** icon on your desktop

### From Start Menu
1. Click Windows Start menu
2. Search for "Gaybeck Starkids SMS"
3. Click the result

### From Command Line
```bash
# Method 1: Run the launcher directly
python launch_sms.py

# Method 2: Run the batch file
RUN_APP.bat

# Method 3: Run the PowerShell script
powershell -File RUN_APP.ps1
```

## Verification

To verify the app launches correctly, run:
```bash
python test_startup.py
```

Expected output:
```
✓ Tkinter available
✓ Database found: database/school_management.db
✓ SMS module imports successfully
✓ Tkinter root window created
```

## Files Modified/Created

| File | Purpose |
|------|---------|
| `launch_sms.py` | Python bootstrap launcher (NEW) |
| `RUN_APP.bat` | Simplified batch launcher (UPDATED) |
| `RUN_APP.ps1` | PowerShell launcher (UPDATED) |
| `test_startup.py` | Startup validation script (NEW) |
| `setup_shortcuts.py` | Shortcut manager (NEW) |

## Troubleshooting

### App still won't launch?
1. Run `python test_startup.py` to diagnose issues
2. Check if Python is installed: `python --version` (should be 3.13+)
3. Verify database exists: `database/school_management.db`
4. Install dependencies: `pip install -r requirements.txt`

### Icon not showing?
1. Verify `sms_icon.ico` exists in the app directory
2. Regenerate shortcuts: `python setup_shortcuts.py`
3. Clear Windows icon cache (restart Windows Explorer)

### Start Menu not working?
1. Run `python setup_shortcuts.py` to recreate Start Menu entry
2. Wait a few seconds for Windows to refresh
3. Restart Windows Explorer if needed

## Version Information
- **Fix Version:** 3.0.1
- **Date:** November 18, 2025
- **Python Requirement:** 3.13+

## Next Steps

The app should now launch properly from both desktop and Start Menu. If you encounter any issues:

1. Check the diagnostic output from `python test_startup.py`
2. Verify all dependencies are installed
3. Ensure the database file is present and accessible

For additional help, check the documentation in the `docs/` directory.
