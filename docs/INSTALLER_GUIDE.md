# Professional Installer Guide
## Gaybeck Starkids SMS v3.0.0

**Date**: November 17, 2025  
**Version**: 3.0.0  
**Status**: ✅ Production Ready  

---

## 📋 Overview

The Gaybeck Starkids SMS now includes a professional installer that:

✅ **Auto-detects** existing installations  
✅ **Offers choices**: Upgrade or clean install  
✅ **Installs dependencies** automatically  
✅ **Creates shortcuts** on Desktop and Start Menu  
✅ **Pins to taskbar** for quick access  
✅ **Registers** in Windows for clean uninstall  

---

## 🚀 Quick Start

### Method 1: Using Batch Installer (Recommended)

1. **Download** `SETUP.bat` from the installation folder
2. **Right-click** → "Run as Administrator"
3. **Follow the prompts**
4. **Done!** Shortcuts will appear on your Desktop

### Method 2: Using Python Installer Directly

```bash
# Open Command Prompt as Administrator
python GaybeckInstaller.py
```

---

## 📦 What Gets Installed

### Application Files
- ✅ Main application (sms.py)
- ✅ AI analytics module (advanced_ai_analytics.py)
- ✅ Database engine (SQLite3)
- ✅ All documentation
- ✅ Script utilities
- ✅ Logo and icons

### Python Dependencies
```
scikit-learn       1.7.2
pandas             2.3.3
numpy              2.2.6
scipy              1.16.3
tkcalendar         1.6.1
reportlab          4.4.5
pillow             12.0.0
opencv-python      4.12.0.88
pywin32            (optional, for enhanced shortcuts)
And more...
```

### Shortcuts Created
- **Desktop Shortcut** - Quick launch from desktop
- **Start Menu Entry** - Access from Windows menu
- **Taskbar Pin** - Click icon to launch (optional)

---

## 💾 Installation Locations

### Default Installation Directory
```
C:\Program Files\Gaybeck Starkids SMS\
├── sms.py
├── advanced_ai_analytics.py
├── requirements.txt
├── logo.png
├── icon.ico
├── .venv/                    (Virtual environment)
├── database/
│   └── school_management.db
├── docs/
│   ├── AI_FEATURES_GUIDE.md
│   ├── AI_QUICK_REFERENCE.md
│   └── ... (other docs)
├── scripts/
├── backups/
└── Uninstall.bat
```

### Shortcuts Created
```
Desktop:
└── Gaybeck Starkids SMS.lnk

Start Menu:
└── Programs\Gaybeck Starkids SMS\
    ├── Gaybeck Starkids SMS.lnk
    ├── Documentation.lnk (opens guides)
    └── Uninstall.lnk
```

---

## ⚙️ Installation Process

### Step-by-Step Walkthrough

#### Step 1: Admin Privileges Check ✅
```
SETUP.bat automatically requests administrator privileges.
If not running as admin, it will prompt for elevation.
```

#### Step 2: Python Version Verification ✅
```
Checks for Python 3.13+
If not found, installation stops with instructions.
```

#### Step 3: Existing Installation Detection ✅
```
If you have a previous version installed:
  Option 1: Upgrade (keep database, update files)
  Option 2: Clean install (remove everything, fresh start)
  Option 3: Cancel (keep current version)
```

#### Step 4: Create Installation Directory ✅
```
Creates: C:\Program Files\Gaybeck Starkids SMS\
```

#### Step 5: Copy Application Files ✅
```
Copies all necessary files to installation directory:
  - Python scripts
  - Database
  - Documentation
  - Icons and logos
```

#### Step 6: Create Virtual Environment ✅
```
Creates isolated Python environment at: .venv/
This keeps dependencies separate from system Python.
```

#### Step 7: Install Dependencies ✅
```
Installs all packages from requirements.txt:
  - Machine learning (scikit-learn, pandas, numpy)
  - GUI (tkinter, tkcalendar)
  - Reports (reportlab)
  - Imaging (pillow, opencv)
  - And more...

Time: 5-15 minutes depending on internet speed
```

#### Step 8: Create Desktop Shortcuts ✅
```
Creates .lnk shortcut files:
  - Desktop (C:\Users\[YourName]\Desktop\)
  - Start Menu (Programs folder)
```

#### Step 9: Pin to Taskbar ✅
```
Attempts to pin application to Windows taskbar
for one-click launching.
```

#### Step 10: Register in Windows Registry ✅
```
Stores installation info for:
  - Clean uninstall
  - Version checking
  - Future upgrades
```

#### Step 11: Create Uninstaller ✅
```
Creates Uninstall.bat in installation directory
for easy removal of application.
```

---

## 🔄 Upgrade vs Clean Install

### Upgrade Installation
✅ **What keeps**:
- Your database (student records, etc.)
- Your settings and configuration
- Custom data

✅ **What updates**:
- Application files (sms.py, etc.)
- All dependencies
- Documentation
- AI modules

⏱️ **Time**: 5-10 minutes

### Clean Installation
✅ **What happens**:
- Completely removes previous version
- Installs fresh copy
- Creates new database (empty)
- All settings reset to default

⚠️ **Warning**: Your data will be deleted!

⏱️ **Time**: 10-15 minutes

---

## 🆘 Troubleshooting Installation

### Issue: "Python is not installed"
**Solution**:
1. Install Python 3.13+ from https://www.python.org
2. During installation, CHECK "Add Python to PATH"
3. Restart your computer
4. Run SETUP.bat again

### Issue: "Not running as Administrator"
**Solution**:
1. Right-click SETUP.bat
2. Select "Run as Administrator"
3. Click "Yes" when prompted

### Issue: Installation stalls on "Installing dependencies"
**Solution**:
1. Close installer (Ctrl+C in command window)
2. Open Command Prompt as Administrator
3. Run: `cd "C:\Program Files\Gaybeck Starkids SMS"`
4. Run: `.venv\Scripts\pip install -r requirements.txt`
5. Wait for completion

### Issue: Shortcuts don't appear
**Solution**:
1. Check Desktop for .lnk files
2. Check Start Menu under "Programs"
3. If missing, manually create:
   - Right-click on sms.py
   - "Create shortcut"
   - Move to Desktop

### Issue: Application won't launch
**Solution**:
1. Check .venv folder exists: `C:\Program Files\Gaybeck Starkids SMS\.venv\`
2. Try launching from command line:
   ```bash
   cd "C:\Program Files\Gaybeck Starkids SMS"
   .venv\Scripts\python.exe sms.py
   ```
3. Check for error messages
4. Review documentation for specific errors

### Issue: Database not found
**Solution**:
1. Check `database/` folder exists in installation
2. Database should auto-create on first launch
3. If missing, copy from backup: `database_backups/`

---

## 🔧 Manual Installation (Advanced)

If the automated installer doesn't work:

```bash
# 1. Navigate to installation directory
cd "C:\Program Files\Gaybeck Starkids SMS"

# 2. Create virtual environment
python -m venv .venv

# 3. Activate virtual environment
.venv\Scripts\activate

# 4. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 5. Test installation
python sms.py

# 6. If successful, create shortcuts manually
```

---

## 🗑️ Uninstalling the Application

### Method 1: Using Uninstall.bat
1. Open File Explorer
2. Navigate to: `C:\Program Files\Gaybeck Starkids SMS\`
3. Double-click `Uninstall.bat`
4. Confirm removal
5. Automatic cleanup performed

### Method 2: Using Control Panel
1. Go to **Settings** → **Apps** → **Installed Apps**
2. Search for "Gaybeck Starkids SMS"
3. Click and select "Uninstall"
4. Confirm removal

### Method 3: Manual Removal
```bash
# Delete installation folder
rmdir /s /q "C:\Program Files\Gaybeck Starkids SMS"

# Delete Start Menu folder
rmdir /s /q "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Gaybeck Starkids SMS"

# Delete Desktop shortcut
del "%USERPROFILE%\Desktop\Gaybeck Starkids SMS.lnk"

# Remove registry entry (requires admin)
reg delete "HKEY_LOCAL_MACHINE\Software\Gaybeck Starkids\SMS" /f
```

---

## 📊 Installation Requirements

### System Requirements
- **OS**: Windows 10 or Windows 11
- **RAM**: 4GB minimum (8GB recommended)
- **Disk Space**: 2GB (for installation + database)
- **Internet**: Required for dependency download (5-10 minutes)

### Software Requirements
- **Python**: 3.13+ (from https://www.python.org)
- **Administrator Rights**: Required for installation
- **Internet Connection**: Required for pip install

### Optional
- **PyWin32**: For enhanced shortcut creation
- **Visual C++ Build Tools**: For some packages (auto-installed)

---

## 🔐 Security & Privacy

### What the Installer Does
✅ Creates isolated Python environment  
✅ Installs only official packages from PyPI  
✅ Stores data locally (no cloud sync)  
✅ Registers in Windows for proper uninstall  

### What the Installer DOES NOT Do
❌ Upload any data to external servers  
❌ Collect usage information  
❌ Modify system files beyond scope  
❌ Track user activity  

### Database Security
- Student data stored locally in SQLite
- No external database access
- Regular backups recommended
- Encryption available (optional setup)

---

## 📚 Post-Installation

### First Launch
1. **Desktop Shortcut**: Double-click icon
2. **Start Menu**: Click in Programs folder
3. **Command Line**: Run `.venv\Scripts\python.exe sms.py`

### Initial Setup
1. Login with admin account
2. Configure school information
3. Add teachers and classes
4. Upload student data
5. Set up fee schedules

### Getting Help
- **Documentation**: `C:\Program Files\Gaybeck Starkids SMS\docs\`
- **Quick Reference**: AI_QUICK_REFERENCE.md
- **Features Guide**: AI_FEATURES_GUIDE.md
- **Troubleshooting**: Check documentation folder

---

## 🔄 Updates & Upgrades

### Checking for Updates
1. Click "About" in application
2. Check current version
3. Visit GitHub for latest version

### Updating the Application
1. Download new installer (SETUP.bat)
2. Run as Administrator
3. Select "Upgrade" option
4. Your data is preserved

### Downgrading (if needed)
1. Uninstall current version
2. Install previous version
3. Restore database backup if needed

---

## 📞 Support

### Common Issues
See **Troubleshooting** section above

### Documentation Files
Located in: `C:\Program Files\Gaybeck Starkids SMS\docs\`

### Getting Help
1. Check documentation first
2. Review troubleshooting guide
3. Check installation log
4. Contact system administrator

---

## 📋 Installation Checklist

After installation, verify:
- [ ] Desktop shortcut created
- [ ] Start Menu folder populated
- [ ] Application launches successfully
- [ ] Database loads without errors
- [ ] Login screen appears
- [ ] Can access Dashboard
- [ ] AI Insights visible
- [ ] Settings accessible
- [ ] Uninstaller works

---

## 🎉 Success Indicators

✅ **Installation successful if**:
- No errors during installation
- Shortcuts appear on Desktop/Start Menu
- Application launches without crashes
- Database loads with tables
- Login screen displays properly
- All features accessible

---

## Version Information

**Installer Version**: 3.0.0  
**Application Version**: 2.0.3+  
**Python Required**: 3.13+  
**Installation Date**: November 17, 2025  

---

## Change Log

### v3.0.0 (Current)
✅ Automatic version detection  
✅ Upgrade/remove dialog  
✅ Dependency installation  
✅ Desktop shortcut creation  
✅ Taskbar pinning  
✅ Registry integration  
✅ Comprehensive error handling  

### v2.0
✅ Basic installation  
✅ Dependency install  
✅ Shortcut creation  

### v1.0
✅ Simple file copy  

---

**Installation Guide Complete**  
**Status**: ✅ Ready for Production  
**Last Updated**: November 17, 2025  
