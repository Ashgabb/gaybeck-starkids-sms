# Building Gaybeck SMS Standalone Installer

This guide explains how to build a standalone `.exe` installer from the Python installer script.

## What You'll Get

- **Single EXE File** (~50-100MB) that contains the complete installer
- **No Directory Copy Required** - Just distribute one file
- **Automatic Installation** - Detects missing files, installs dependencies, creates shortcuts
- **Admin Notifications** - Detailed installation logs and error reports
- **Cross-Device Compatible** - Works on any Windows device with sufficient disk space

---

## Prerequisites

Install PyInstaller:

```bash
pip install pyinstaller
```

---

## Building the Installer

### Step 1: Navigate to Project Directory

```bash
cd "c:\Users\USER\Desktop\Gaybeck SMS\gaybeck-starkids-sms"
```

### Step 2: Build EXE with PyInstaller

Run this command to create the standalone installer:

```bash
pyinstaller --onefile --windowed ^
  --name "Gaybeck_SMS_Setup_v2.0" ^
  --icon "sms.ico" ^
  --add-data "sms.py:." ^
  --add-data "requirements.txt:." ^
  --hidden-import tkinter ^
  installer.py
```

**Explanation:**
- `--onefile`: Creates single executable file (instead of folder)
- `--windowed`: No console window (GUI only)
- `--name`: Output executable name
- `--icon`: Application icon (optional)
- `--add-data`: Include essential files in exe
- `--hidden-import`: Include tkinter module

### Step 3: Find Your Installer

The created EXE will be in:
```
dist/Gaybeck_SMS_Setup_v2.0.exe
```

### Step 4: Test the Installer Locally

Before distribution, test it:

```bash
"dist/Gaybeck_SMS_Setup_v2.0.exe"
```

---

## Installation Process (User Experience)

When users run the installer on their device:

1. **System Check** ✓
   - Validates Python version (3.8+)
   - Checks disk space (2GB minimum)
   - Verifies pip availability

2. **Installation Directory** 
   - Defaults to: `C:\Users\[Username]\AppData\Local\Gaybeck_SMS`
   - User can confirm or modify

3. **File Extraction**
   - Copies all application files from exe to local disk
   - Validates file integrity

4. **Dependencies Installation**
   - Installs all Python packages from requirements.txt
   - Shows progress during pip install (may take 2-5 minutes)

5. **Shortcuts Creation**
   - Creates desktop shortcut for easy access
   - Creates Start Menu shortcut (optional)

6. **Completion & Login**
   - Generates installation report
   - Shows default credentials:
     - **Username:** `admin`
     - **Password:** `admin123`
   - User can immediately launch app

---

## Distribution

### Option A: Direct Distribution
Send the `Gaybeck_SMS_Setup_v2.0.exe` file to users via:
- Email
- Cloud storage (Google Drive, OneDrive)
- USB drive
- Network share

### Option B: Hosting on Web Server
```bash
# Upload to your server
scp dist/Gaybeck_SMS_Setup_v2.0.exe user@server:/var/www/downloads/
```

Users can then download and run it.

### Option C: Create Installation Package
Create a ZIP with additional documentation:

```
Gaybeck_SMS_Setup_Package.zip
├── Gaybeck_SMS_Setup_v2.0.exe
├── README.txt
├── SYSTEM_REQUIREMENTS.txt
└── QUICK_START_GUIDE.txt
```

---

## Advanced Options

### Build with Custom Icon

First, obtain or create an icon file (`sms.ico`). Then:

```bash
pyinstaller --onefile --windowed ^
  --name "Gaybeck_SMS_Setup_v2.0" ^
  --icon "sms.ico" ^
  --add-data "sms.py:." ^
  --add-data "requirements.txt:." ^
  --hidden-import tkinter ^
  installer.py
```

### Build with All Application Data

To bundle more files directly in the exe:

```bash
pyinstaller --onefile --windowed ^
  --name "Gaybeck_SMS_Setup_v2.0" ^
  --icon "sms.ico" ^
  --add-data "sms.py:." ^
  --add-data "requirements.txt:." ^
  --add-data "docs:docs" ^
  --add-data "database:database" ^
  --hidden-import tkinter ^
  installer.py
```

---

## Troubleshooting

### Build Error: "tkinter not found"
Solution:
```bash
pip install pillow
```

### EXE Too Large
The installer might be 100-150MB. This is normal for PyInstaller (includes Python runtime).

To reduce size:
```bash
pyinstaller --onefile --windowed --noupx ^
  --name "Gaybeck_SMS_Setup_v2.0" ^
  installer.py
```

### Installation Fails on User Machine
Check the installation log file:
```
C:\Users\[Username]\.gaybeck_sms\logs\install_*.log
```

---

## Installation Log & Admin Notifications

### Automatic Logging

Every installation creates:

1. **Installation Log File:**
   ```
   C:\Users\[Username]\.gaybeck_sms\logs\install_YYYYMMDD_HHMMSS.log
   ```

2. **Installation Report (JSON):**
   ```
   C:\Users\[Username]\AppData\Local\Gaybeck_SMS\INSTALLATION_REPORT.json
   ```

3. **Installation Report (Text):**
   ```
   C:\Users\[Username]\AppData\Local\Gaybeck_SMS\INSTALLATION_REPORT.txt
   ```

### Admin Notification Example

The installer generates this information for administrators:

```json
{
  "app_name": "Gaybeck Starkids SMS",
  "version": "2.0",
  "install_date": "2026-06-11T14:32:00",
  "install_path": "C:\\Users\\Admin\\AppData\\Local\\Gaybeck_SMS",
  "python_version": "3.13.0",
  "platform": "Windows-10-10.0.19045-SP1",
  "status": "SUCCESS",
  "errors": []
}
```

---

## Next Steps

After creating the EXE:

1. ✅ Test locally
2. ✅ Verify installation creates proper directories
3. ✅ Confirm shortcuts work
4. ✅ Check that app launches successfully
5. ✅ Create user documentation
6. ✅ Distribute to target devices

---

## Support

If users encounter issues:

1. Provide them with the log file location
2. Ensure Python is installed before running installer (or use pre-Python-installed bundles)
3. Check system requirements (2GB disk space, Windows 7+)
4. Retry installation if first attempt fails

---

**Created:** February 28, 2026  
**Application:** Gaybeck Starkids SMS v2.0  
**Installer Type:** Standalone GUI-based Installer
