# Gaybeck SMS - Standalone Installer System

## Overview

The Gaybeck SMS Installer System allows you to create a **single standalone executable (.exe)** that can be distributed to any Windows device. The installer automatically:

- ✅ Validates system requirements
- ✅ Detects missing files and components  
- ✅ Installs Python dependencies
- ✅ Configures the application
- ✅ Creates desktop shortcuts
- ✅ Generates admin notifications and reports
- ✅ Logs all installation activities

**Result:** Users receive one file, double-click it, and Gaybeck SMS is fully installed and ready to use.

---

## Components

### 1. **installer.py** - Main Installer Script
Complete Python application with:
- GUI-based installation wizard
- System requirement validation (Python, pip, disk space)
- File extraction and dependency installation
- Real-time progress tracking
- Installation logging and reporting
- Admin notification system

**Features:**
- 🎨 Modern Tkinter GUI
- 📊 Real-time progress bar
- 📋 Detailed installation log
- 📝 JSON and text reports
- 🔍 System compatibility checks

### 2. **admin_verification.py** - Admin Verification Tool
Comprehensive verification tool for administrators:
- Check Python installation and version
- Verify all dependencies are installed
- Validate application directory
- Check database status
- Review system resources
- Generate admin reports

**Usage:**
```bash
python admin_verification.py
```

### 3. **BUILD_INSTALLER.md** - Build Instructions
Complete guide for building the standalone EXE:
- Step-by-step PyInstaller commands
- Customization options
- Troubleshooting guide
- Advanced configurations
- Distribution methods

### 4. **INSTALLER_QUICK_START.md** - Quick Start Guide
Fast-track setup for system administrators:
- 3-step build process
- Testing and verification
- Distribution options
- Troubleshooting guide
- Post-installation monitoring

---

## Quick Start (5 Minutes)

### For Admins Creating the Installer

**Step 1: Install PyInstaller**
```bash
pip install pyinstaller
```

**Step 2: Build the Installer (from project directory)**
```bash
pyinstaller --onefile --windowed ^
  --name "Gaybeck_SMS_Setup_v2.0" ^
  --add-data "sms.py:." ^
  --add-data "requirements.txt:." ^
  --hidden-import tkinter ^
  installer.py
```

**Step 3: Find and Test**
```bash
# Output file
dist/Gaybeck_SMS_Setup_v2.0.exe

# Test it
dist/Gaybeck_SMS_Setup_v2.0.exe
```

---

## For End Users

Users only need to:

1. **Download** `Gaybeck_SMS_Setup_v2.0.exe`
2. **Double-click** the file
3. **Follow** the installer wizard
4. **Wait** for installation (2-5 minutes)
5. **Login** with default credentials:
   - Username: `admin`
   - Password: `admin123`

---

## Installation Process

### What the Installer Does

```
1. System Validation (30 seconds)
   └─ Check Python version (3.8+)
   └─ Check disk space (2GB+)
   └─ Verify pip availability

2. File Selection (30 seconds)
   └─ User selects or confirms install location
   └─ Default: C:\Users\[User]\AppData\Local\Gaybeck_SMS

3. File Extraction (1 minute)
   └─ Copy all application files
   └─ Validate file integrity

4. Dependency Installation (2-5 minutes)
   └─ pip install from requirements.txt
   └─ Real-time progress display

5. Shortcut Creation (30 seconds)
   └─ Create desktop shortcut
   └─ Create Start Menu item

6. Finalization (1 minute)
   └─ Generate installation report
   └─ Display login credentials
   └─ Ready to use!
```

---

## Admin Tools & Monitoring

### For Administrators

#### Monitor Installations

Each user's installation creates:

**Logs** (for troubleshooting):
```
C:\Users\[Username]\.gaybeck_sms\logs\install_*.log
```

**Installation Report** (for records):
```
C:\Users\[Username]\AppData\Local\Gaybeck_SMS\INSTALLATION_REPORT.json
C:\Users\[Username]\AppData\Local\Gaybeck_SMS\INSTALLATION_REPORT.txt
```

#### Verify Installation Status

Run on user's device:
```bash
python admin_verification.py
```

**Output includes:**
- ✓ Python version check
- ✓ Dependency verification
- ✓ Application directory validation
- ✓ Database status
- ✓ System resources
- ✓ Admin verification report

#### Example Report

```
Gaybeck Starkids SMS - Installation Verification Report
────────────────────────────────────────────────────────

System Information
  Platform: Windows-10-10.0.19045-SP1
  Python: 3.13.0
  User: AdminUser

Verification Summary
  Total Checks: 9
  Passed: 9
  Failed: 0
  Success Rate: 100.0%

✓ Installation is COMPLETE and FULLY FUNCTIONAL
```

---

## Customization

### Branding

Edit `installer.py`:
```python
APP_NAME = "Your Company - School Management System"
APP_VERSION = "2.0"
```

### Installation Path

Edit `installer.py`:
```python
default_path = Path.home() / "My Custom Path"
```

### Additional Files

Modify `items_to_copy` in `installer.py`:
```python
items_to_copy = [
    'sms.py',
    'your_custom_module.py',
    # ... more files
]
```

---

## Distribution Options

### Option 1: Email Distribution
- Send `Gaybeck_SMS_Setup_v2.0.exe` via email
- Users download and run
- ✅ Simple, no infrastructure needed

### Option 2: USB/Network Drive
- Copy EXE to USB or network share
- Users run from shared location
- ✅ Offline installation available

### Option 3: Web Hosting
- Upload EXE to web server
- Users download via link
- ✅ Centralized distribution

### Option 4: Installation Package
Create ZIP with documentation:
```
Gaybeck_SMS_Installation_v2.0.zip
├── Gaybeck_SMS_Setup_v2.0.exe
├── README.txt
├── SYSTEM_REQUIREMENTS.txt
├── QUICK_START.txt
└── TROUBLESHOOTING.txt
```

---

## System Requirements

**Minimum:**
- Windows 7 or later
- Python 3.8+
- 2GB available disk space
- 512MB RAM

**Recommended:**
- Windows 10 or later
- Python 3.13
- 5GB available disk space
- 2GB+ RAM

**Note:** Installer includes Python runtime, so users don't need to pre-install Python separately.

---

## Troubleshooting

### Installation Fails

1. **Check System Requirements:**
   ```bash
   python admin_verification.py
   ```

2. **Review Installation Log:**
   ```
   C:\Users\[Username]\.gaybeck_sms\logs\
   ```

3. **Common Issues:**
   - **"Python not found"** → Install Python 3.8+
   - **"Not enough disk space"** → Free up 2GB+
   - **"Permission denied"** → Run as administrator
   - **"pip install failed"** → Check internet connection

### Build Error: "tkinter not found"

```bash
pip install pillow
```

### EXE File Too Large (> 150MB)

Standard size with Python runtime: 100-150MB (normal)

To optimize:
```bash
pyinstaller --onefile --windowed --noupx ^
  --name "Gaybeck_SMS_Setup_v2.0" ^
  installer.py
```

### Installation Hangs

- Check internet connection (downloading packages)
- Check disk space
- Verify pip is working

---

## File Organization

### After Installation on User Device

```
C:\Users\[Username]\AppData\Local\Gaybeck_SMS\
├── sms.py                          (Main app)
├── requirements.txt                (Dependencies list)
├── database/
│   └── school_management.db        (Database)
├── docs/                           (Documentation)
├── biometric_data/                 (Biometric configs)
├── launch_sms.bat                  (Launch shortcut)
├── INSTALLATION_REPORT.json        (Install metadata)
└── INSTALLATION_REPORT.txt         (Install report)

C:\Users\[Username]\.gaybeck_sms\
├── logs/
│   └── install_*.log               (Installation logs)
└── reports/
    └── admin_verification_*.json   (Admin reports)

Desktop\
└── Gaybeck SMS.lnk                (Desktop shortcut)
```

---

## Post-Installation

### For Users

1. **First Run:**
   - Login with `admin` / `admin123`
   - Change password in settings
   - Configure your school profile

2. **Getting Help:**
   - Check documentation in `docs/` folder
   - Review installation logs if issues occur
   - Contact your administrator

### For Administrators

1. **Verify Installations:**
   ```bash
   python admin_verification.py
   ```

2. **Monitor Activity:**
   - Check installation logs
   - Review admin reports
   - Verify database integrity

3. **Support Users:**
   - Ask users to run verification tool
   - Collect logs for troubleshooting
   - Provide installation support

---

## Advanced

### Build with Custom Icon

```bash
# Get an icon first (or create one)
# Then:

pyinstaller --onefile --windowed ^
  --name "Gaybeck_SMS_Setup_v2.0" ^
  --icon "your_icon.ico" ^
  --add-data "sms.py:." ^
  --add-data "requirements.txt:." ^
  --hidden-import tkinter ^
  installer.py
```

### Build with Additional Data Files

```bash
pyinstaller --onefile --windowed ^
  --name "Gaybeck_SMS_Setup_v2.0" ^
  --add-data "sms.py:." ^
  --add-data "requirements.txt:." ^
  --add-data "docs:docs" ^
  --add-data "database:database" ^
  --hidden-import tkinter ^
  installer.py
```

### One-Line Build (Windows)

```bash
pyinstaller --onefile --windowed --name "Gaybeck_SMS_Setup_v2.0" --add-data "sms.py:." --add-data "requirements.txt:." --hidden-import tkinter installer.py
```

---

## Support

### Get Detailed Reports

1. **During Installation:** Check the progress log in the GUI
2. **After Installation:** View logs in `C:\Users\[Username]\.gaybeck_sms\logs\`
3. **For Admin Review:** Run `python admin_verification.py`

### Common Commands

```bash
# Build installer
pyinstaller --onefile --windowed --name "Gaybeck_SMS_Setup_v2.0" installer.py

# Test installer
dist/Gaybeck_SMS_Setup_v2.0.exe

# Verify installation
python admin_verification.py

# Check Python version
python --version

# Check pip
pip --version
```

---

## Summary

| Task | Time | Who | How |
|------|------|-----|-----|
| Build Installer | 5 min | Admin | Run PyInstaller command |
| Test Installer | 10 min | Admin | Double-click and follow wizard |
| Distribute | 5 min | Admin | Email/USB/Cloud/Web |
| Install on Device | 3-5 min | User | Double-click and wait |
| Verify Installation | 2 min | Admin | Run admin_verification.py |
| Support User | Varies | Admin | Check logs and reports |

---

## Files Included

- ✅ `installer.py` - Main installer (Python script)
- ✅ `admin_verification.py` - Verification tool
- ✅ `BUILD_INSTALLER.md` - Detailed build guide
- ✅ `INSTALLER_QUICK_START.md` - Quick start for admins
- ✅ `INSTALLER_README.md` - This file

---

**Version:** 2.0  
**Created:** February 28, 2026  
**Application:** Gaybeck Starkids School Management System  
**Status:** Ready for Production Deployment
