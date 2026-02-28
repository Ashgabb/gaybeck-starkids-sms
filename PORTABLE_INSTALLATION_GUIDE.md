# Gaybeck Starkids SMS - Portable Installation Guide

## Version: 2.0 (Cross-Device Compatible)
**Date:** February 28, 2026  
**Status:** Ready for Any Device

---

## Quick Start

### For Windows Users

Choose **ONE** of these options (all work on any Windows device):

#### Option 1: Desktop Shortcut (Recommended)
1. Double-click: `create_sms_shortcut.vbs`
2. A shortcut appears on your desktop
3. Double-click the shortcut to launch the app
4. Done!

#### Option 2: Run Direct Launcher
1. Double-click: `run_app.bat`
2. The app launches automatically

#### Option 3: Run via Python
```bash
python sms.py
```

---

## Installation on Any Device

### Step 1: Get Python
**Requirement:** Python 3.8+ (Python 3.13+ recommended)

- **Windows:** [Download from python.org](https://www.python.org/downloads/)
  - **IMPORTANT:** Check "Add Python to PATH" during installation
- **Linux:** `sudo apt-get install python3 python3-pip`
- **Mac:** `brew install python3`

### Step 2: Copy Application Files
Copy the entire `gaybeck-starkids-sms` folder to your device:
- Desktop
- Documents folder
- USB drive
- Network drive
- Anywhere on your computer

### Step 3: Install Dependencies (Optional but Recommended)

**Option A: Automatic Setup**
```bash
python setup_portable.py
```
This will install all required packages automatically.

**Option B: Manual Setup**
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
Choose any method below:

**Method 1: Double-click `run_app.bat`** (Windows only)
**Method 2: Double-click `python sms.py`** in file explorer
**Method 3: Command line: `python sms.py`**
**Method 4: Create desktop shortcut with `create_sms_shortcut.vbs`**

---

## Available Launcher Options

### 1. **run_app.bat** (Simplest - Windows Only)
- Direct launcher with no setup required
- Automatically finds Python
- Works on any device with Python in PATH
- **Best for:** First-time users on Windows

```bash
run_app.bat
```

### 2. **sms_launcher.bat** (Enhanced - Windows Only)
- Supports Python from system PATH or venv
- Has fallback options
- Better error handling
- **Best for:** Development and testing

```bash
.\sms_launcher.bat
```

### 3. **launch_app.py** (Universal - All Platforms)
- Works on Windows, Linux, Mac
- Environment checking and validation
- Detailed logging
- Creates launch logs automatically
- **Best for:** Troubleshooting and verification

```bash
python launch_app.py
```

### 4. **run_sms.py** (Minimal - All Platforms)
- Direct Python launcher
- No console output
- Minimal dependencies
- **Best for:** Embedded deployment

```bash
python run_sms.py
```

### 5. **Direct Execution** (Most Basic)
- No launcher needed
- Pure Python execution
- Universal compatibility
- **Best for:** Any situation

```bash
python sms.py
```

### 6. **setup_portable.py** (Setup Helper)
- Interactive setup wizard
- Installs dependencies
- Creates desktop shortcuts
- Verifies environment
- **Best for:** Initial setup

```bash
python setup_portable.py
```

---

## Troubleshooting

### Problem: "Python not found"
**Cause:** Python not in system PATH  
**Solution:**
1. Open Command Prompt
2. Type: `python --version`
3. If not found, reinstall Python with "Add to PATH" checked

### Problem: "Module not found" errors
**Cause:** Missing dependencies  
**Solution:**
```bash
pip install -r requirements.txt
```

### Problem: App launches with errors
**Solution 1:** Check the log files in `logs/` directory
```bash
type logs/launch_*.log
```

**Solution 2:** Verify environment
```bash
python setup_portable.py
```

**Solution 3:** Try simpler launcher
```bash
python sms.py
```

### Problem: Shortcut doesn't work
**Solution:**
1. Re-run: `create_sms_shortcut.vbs`
2. Or manually create shortcut pointing to: `run_app.bat`

### Problem: Database errors
**Usually fixes itself** on first run - database is created automatically

---

## What Each File Does

| File | Purpose | Platform |
|------|---------|----------|
| `sms.py` | Main application | All |
| `run_app.bat` | Direct launcher | Windows |
| `sms_launcher.bat` | Enhanced launcher | Windows |
| `launch_app.py` | Python launcher | All |
| `run_sms.py` | Minimal launcher | All |
| `setup_portable.py` | Setup wizard | All |
| `create_sms_shortcut.vbs` | Shortcut creator | Windows |
| `requirements.txt` | Dependencies list | All |
| `logs/` | Launch logs | All |
| `database/` | App database | All |

---

## Feature: Clear All Data

Access from within the app (Admin only):
1. Log in as Administrator
2. Settings → Data Management
3. Choose what to clear:
   - Clear All Students
   - Clear All Attendance
   - Clear All Fees
   - Clear All Grades
   - Clear ALL Test Data

**Warning:** Always backup first! (Settings → Backup & Restore)

---

## Backup and Restore

**Create Backup:** Settings → Backup & Restore → Full Database Backup
**Locate Backups:** `database_backups/` folder
**Restore:** Use "Restore from Backup File" button

---

## Performance Optimization

For **first launch on a new device**, the app may take longer to initialize:
1. Database tables are created
2. Indexes are set up
3. Sync system initializes
4. AI modules are loaded (if available)

**Subsequent launches are much faster!**

---

## System Requirements

### Minimum
- Python 3.8+
- 500 MB disk space
- 2 GB RAM
- Windows 7 or later / Linux / macOS

### Recommended
- Python 3.13+
- 1 GB disk space
- 4+ GB RAM
- Windows 10+ / Recent Linux / macOS 10.14+

### Optional (for extra features)
- `tkcalendar` - Date picker
- `reportlab` - PDF generation
- `Pillow/PIL` - Image processing
- `opencv-python` - Camera support
- `numpy`, `pandas` - Data analysis
- `scikit-learn` - Machine learning

---

## Deployment Guide

### For IT Administrators

**Step 1: Prepare Installation Package**
```bash
cd gaybeck-starkids-sms
python setup_portable.py
```

**Step 2: Create Installation Media**
- Copy entire folder to USB drive or network share
- Create a README with basic instructions
- Include shortcut to these docs

**Step 3: Distribute to Users**
- Have users copy folder to their device
- Run `setup_portable.py` (recommended) OR `run_app.bat`
- Create desktop shortcut with `create_sms_shortcut.vbs`

**Step 4: Verify Installation**
```bash
python tests/test_clear_all_data.py
```

---

## Advanced Options

### Command-Line Flags (Future Release)
```bash
python sms.py --admin              # Start as admin
python sms.py --portable           # Portable mode
python sms.py --reset-db           # Reset database
python sms.py --standalone         # No sync
```

### Environment Variables
```bash
SET SMS_DATA_DIR=C:\MyAppData
SET SMS_DATABASE=custom_db.db
SET SMS_LOG_LEVEL=DEBUG
python sms.py
```

### Configuration File (Future)
Create `sms_config.ini` for persistent settings:
```ini
[database]
path=database/school_management.db

[ui]
theme=dark
resolution=1366x768

[ai]
enabled=true
```

---

## Version History

### v2.0 (Current) - Portable Edition
- ✓ Works on any device
- ✓ No virtual environment required
- ✓ Multiple launcher options
- ✓ Automatic dependency detection
- ✓ Better error messages
- ✓ Enhanced portability

### v1.0 - Initial Release
- Basic launcher
- Virtual environment required
- Limited device support

---

## Technical Details

### Database Portability
- SQLite3 format (universal)
- Auto-detection of database location
- Fallbacks to multiple paths
- Automatic migration for older databases

### Path Resolution
The app automatically finds files in this order:
1. Application directory (where sms.py is located)
2. `database/` subdirectory
3. User's AppData folder (Windows)
4. Current working directory

This makes the app work regardless of installation location!

### Logging
All launcher activity logged to: `logs/launch_TIMESTAMP.log`
Use this for troubleshooting deployment issues.

---

## FAQ

**Q: Can I run this from a USB drive?**  
A: Yes! Copy the folder to a USB drive and run `run_app.bat` on any Windows PC with Python.

**Q: Can I move the folder after installation?**  
A: Yes! The app uses relative paths, so it works from any location.

**Q: Do I need admin rights?**  
A: No! Standard user rights are sufficient (unless installing system-wide Python).

**Q: What if Python is not installed?**  
A: Download and install Python with "Add to PATH" option checked.

**Q: Can multiple users use the same installation?**  
A: Yes! Each user can have their own login credentials.

**Q: How do I completely uninstall?**  
A: Just delete the `gaybeck-starkids-sms` folder. No files are left behind.

**Q: Is my data secure?**  
A: Yes! Database is local (not cloud). Backup regularly using Settings → Backup & Restore.

---

## Support

### Getting Help
1. Check log file: `logs/launch_*.log`
2. Run setup wizard: `python setup_portable.py`
3. Review this guide's Troubleshooting section
4. Check `tests/` folder for verification scripts

### Reporting Issues
When reporting problems, include:
- Contents of `logs/launch_*.log`
- Output of `python setup_portable.py`
- Your Python version: `python --version`
- Your operating system

---

## License & Copyright
Gaybeck Starkids School Management System  
Version 2.0.3  
© 2024-2026 Gaybeck Starkids School  
All Rights Reserved

---

**Last Updated:** February 28, 2026  
**Status:** Production Ready ✓
