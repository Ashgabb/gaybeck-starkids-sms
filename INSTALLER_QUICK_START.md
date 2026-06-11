# Gaybeck SMS - Standalone Installer Quick Start

**Created:** February 28, 2026  
**For:** System Administrators & Deployment Teams

---

## What You Have

✅ **installer.py** - Complete Python installer with GUI  
✅ **admin_verification.py** - Admin tool for verifying installations  
✅ **BUILD_INSTALLER.md** - Detailed build instructions  
✅ **INSTALLER_QUICK_START.md** - This file  

---

## 3-Step Quick Start

### Step 1: Install PyInstaller (One-Time)

```bash
pip install pyinstaller
```

### Step 2: Build the Installer Executable

From the project directory, run:

```bash
pyinstaller --onefile --windowed ^
  --name "Gaybeck_SMS_Setup_v2.0" ^
  --add-data "sms.py:." ^
  --add-data "requirements.txt:." ^
  --hidden-import tkinter ^
  installer.py
```

**Takes:** 2-5 minutes  
**Output:** `dist/Gaybeck_SMS_Setup_v2.0.exe` (~80-120 MB)

### Step 3: Test & Distribute

```bash
# Test locally
dist/Gaybeck_SMS_Setup_v2.0.exe

# Then distribute to target devices
```

---

## What Happens When Users Run the Installer

1. **System Check** ✓
   - Validates Python is installed
   - Checks disk space (2GB minimum)
   - Verifies pip availability

2. **Installation** 
   - Extracts app files to `C:\Users\[User]\AppData\Local\Gaybeck_SMS`
   - Installs dependencies from requirements.txt (2-5 minutes)
   - Creates desktop shortcut

3. **Completion**
   - Generates installation report
   - Shows default credentials
   - User can launch immediately

---

## For Administrators

### Monitor Installations

After users install, they'll have:

**Installation Logs:**
```
C:\Users\[Username]\.gaybeck_sms\logs\install_YYYYMMDD_HHMMSS.log
```

**Installation Report (JSON):**
```
C:\Users\[Username]\AppData\Local\Gaybeck_SMS\INSTALLATION_REPORT.json
```

**Installation Report (Text):**
```
C:\Users\[Username]\AppData\Local\Gaybeck_SMS\INSTALLATION_REPORT.txt
```

### Verify Installation Status

On target device, run:

```bash
python admin_verification.py
```

This generates a detailed report showing:
- ✓ Python version
- ✓ All dependencies installed
- ✓ Application directory and files
- ✓ Database status
- ✓ System resources

---

## Distribution Options

### Option A: Email
Send `Gaybeck_SMS_Setup_v2.0.exe` to users  
Users double-click to install

### Option B: USB/Network Drive
Copy to shared location  
Users run from network or USB

### Option C: Host on Web Server
```bash
# Upload to web server
scp dist/Gaybeck_SMS_Setup_v2.0.exe user@server:/var/www/downloads/
```

Users download and run

### Option D: Create Installation Package

```
Gaybeck_SMS_Installation_Package.zip
├── Gaybeck_SMS_Setup_v2.0.exe
├── README.txt
├── SYSTEM_REQUIREMENTS.txt
└── FIRST_RUN_INSTRUCTIONS.txt
```

---

## Troubleshooting

### Installation Fails on User Device

**Step 1:** Check Python is installed
```bash
python --version
```

**Step 2:** Get the installation log
```
C:\Users\[Username]\.gaybeck_sms\logs\
```

**Step 3:** Run verification tool
```bash
python admin_verification.py
```

**Step 4:** Review the admin report
```
C:\Users\[Username]\.gaybeck_sms\reports\
```

### EXE File Too Large

Standard size: 80-120MB (includes Python runtime)

To reduce:
```bash
pyinstaller --onefile --windowed --noupx ^
  --name "Gaybeck_SMS_Setup_v2.0" ^
  installer.py
```

### Build Error: "tkinter not found"

Install Pillow:
```bash
pip install pillow
```

---

## After Installation

### First Launch

Users see login screen:
- **Username:** `admin`
- **Password:** `admin123`

### Verify Everything Works

As admin, run:
```bash
python admin_verification.py
```

Output shows:
- ✓ Python version
- ✓ All packages installed
- ✓ Database initialized
- ✓ Application ready

---

## Key Files Created During Installation

On each user device:

```
C:\Users\[Username]\AppData\Local\Gaybeck_SMS\
├── sms.py                          (Main application)
├── requirements.txt                (Dependencies)
├── database/
│   └── school_management.db        (Database)
├── docs/                           (Documentation)
├── biometric_data/                 (Biometric storage)
├── INSTALLATION_REPORT.json        (Installation metadata)
└── INSTALLATION_REPORT.txt         (Human-readable report)

C:\Users\[Username]\.gaybeck_sms\
├── logs/
│   └── install_*.log               (Installation logs)
└── reports/
    └── admin_verification_*.json   (Admin verification reports)

Desktop\
└── Gaybeck SMS.lnk                (Desktop shortcut)
```

---

## Advanced: Customize Installer

### Add Company Branding

Edit `installer.py`:
```python
APP_NAME = "Your Company - SMS"
```

### Change Installation Path

Edit `installer.py`:
```python
default_path = Path.home() / "YourCustomPath"
```

### Add Additional Files

Edit in `installer.py` in `prepare_files()`:
```python
items_to_copy = [
    'sms.py',
    'your_additional_file.py',
    # ...
]
```

---

## Support & Logs

All installation events logged to:
```
C:\Users\[Username]\.gaybeck_sms\logs\
```

Share these logs if issues occur.

---

## Next Steps

1. ✅ Run `pyinstaller` command (Step 2 above)
2. ✅ Find `dist/Gaybeck_SMS_Setup_v2.0.exe`
3. ✅ Test on your machine
4. ✅ Distribute to target devices
5. ✅ Users run installer → automatically configured
6. ✅ Verify with `admin_verification.py`

---

**For detailed build instructions, see:** `BUILD_INSTALLER.md`

**Questions?** Check installation logs or run admin verification tool.
