# 🚀 BUILD INSTALLER - Quick Start Guide

## What This Does

This guide walks you through creating a professional Windows installer (`GaybeckStarKidsSMS_Installer_2.0.3.exe`) that non-technical users can simply double-click to install the application.

---

## ⏱️ Quick Version (5 minutes)

### **Step 1: Open File Explorer**
- Press `Win + E` on your keyboard
- Navigate to: `C:\Users\YourUsername\Documents\gaybeck-starkids-sms`

### **Step 2: Run the Build Script**
- Find file: `CREATE_INSTALLER.bat`
- **Double-click** it
- A command window will appear

### **Step 3: Wait for Completion**
- The script will:
  - Check Python (3-5 seconds)
  - Create virtual environment (1-2 minutes)
  - Install dependencies (2-3 minutes)
  - Build executable (2-3 minutes)
  - Create installer (1-2 minutes)
- **Total time: ~10 minutes**

### **Step 4: Find Your Installer**
After completion, you'll see:
```
GaybeckStarKidsSMS_Installer_2.0.3.exe
```

**This is your installer file!**

---

## 📋 Detailed Step-by-Step

### **Prerequisites Checklist**

- [ ] Windows 7 or later
- [ ] Python 3.13+ installed
- [ ] 500+ MB free disk space
- [ ] Administrator access

**Don't have Python?**
1. Go to: https://www.python.org/downloads/
2. Download Python 3.13 or higher
3. Run installer → Check "Add Python to PATH" → Install
4. Restart your computer

### **Building the Installer**

**Option A: Simple (Recommended)**

1. Open the project folder
2. Right-click `CREATE_INSTALLER.bat`
3. Select **"Run as Administrator"**
4. Wait for completion

**Option B: Using PowerShell**

1. Press `Win + R`
2. Type: `powershell`
3. Copy-paste this command:
   ```powershell
   cd C:\Users\YourUsername\Documents\gaybeck-starkids-sms
   .\CREATE_INSTALLER.bat
   ```
4. Wait for completion

**Option C: Using Command Prompt**

1. Press `Win + R`
2. Type: `cmd`
3. Copy-paste this command:
   ```cmd
   cd C:\Users\YourUsername\Documents\gaybeck-starkids-sms
   CREATE_INSTALLER.bat
   ```
4. Wait for completion

---

## ✅ Verification Checklist

After the script completes, verify:

- [ ] No error messages in the console
- [ ] File exists: `GaybeckStarKidsSMS_Installer_2.0.3.exe`
- [ ] File size: ~150-200 MB
- [ ] Can double-click the `.exe` to test installation

**Test the installer:**
1. Double-click `GaybeckStarKidsSMS_Installer_2.0.3.exe`
2. Click "Next" through the wizard
3. Click "Finish"
4. Verify the application launches

---

## 🛠️ What Happens Behind the Scenes

### **BUILD PROCESS:**

```
1. Python Check
   ↓
2. Virtual Environment Setup
   ↓
3. Install PyInstaller
   ↓
4. Install App Dependencies
   ↓
5. Build Standalone Executable
   ↓
6. Create Windows Installer (NSIS)
   ↓
7. Final Executable Ready
```

### **OUTPUT FILES:**

```
Project Folder/
├── GaybeckStarKidsSMS_Installer_2.0.3.exe    ← YOUR INSTALLER
├── dist/
│   └── GaybeckStarKidsSMS/                    ← Portable version
│       ├── GaybeckStarKidsSMS.exe             ← Standalone app
│       └── [all dependencies]
└── build/                                      ← Build cache
```

---

## 🚨 Troubleshooting

### **"Python is not installed"**

```
ERROR: Python 3.13+ is required but not found!
```

**FIX:**
1. Install Python from: https://www.python.org/downloads/
2. **IMPORTANT:** During installation, CHECK "Add Python to PATH"
3. Restart your computer
4. Run `CREATE_INSTALLER.bat` again

### **"Failed to install PyInstaller"**

```
ERROR: Failed to install PyInstaller
```

**FIX:**
1. Right-click `CREATE_INSTALLER.bat` → "Run as Administrator"
2. Disable antivirus temporarily (may block pip)
3. Ensure internet connection is working
4. Try again

### **"Insufficient disk space"**

```
ERROR: Not enough free space
```

**FIX:**
1. Free up at least 500 MB
2. Delete old files from Downloads/Temp
3. Run `CREATE_INSTALLER.bat` again

### **"Build failed" or build hangs**

**FIX:**
1. Wait 5-10 minutes (building takes time)
2. Check Task Manager → CPU/Memory usage
3. If stuck, press Ctrl+C to stop
4. Run again (it will resume)

---

## 📦 Distributing Your Installer

### **Option 1: Direct File (Easiest)**

```
Send file: GaybeckStarKidsSMS_Installer_2.0.3.exe

User instructions:
1. Double-click the installer
2. Click "Next" at each step
3. Click "Finish"
4. Done!
```

### **Option 2: Via USB Drive**

1. Copy `GaybeckStarKidsSMS_Installer_2.0.3.exe` to USB
2. Give USB to user
3. User plugs in USB and runs the file

### **Option 3: Via Email**

1. Attach file to email (~170 MB)
2. Or upload to Google Drive/OneDrive and share link
3. Include installation instructions

### **Option 4: Via Network Share**

1. Copy installer to network folder
2. Users access: `\\ServerName\Share\GaybeckStarKidsSMS_Installer_2.0.3.exe`
3. Users double-click to install

---

## 📊 Build Output Example

```
================================================================================
                    GAYBECK STARKIDS SMS - INSTALLER CREATOR
================================================================================

[STEP 1/8] Checking Python installation...
✓ Python 3.13.0 found

[STEP 2/8] Setting up virtual environment...
✓ Virtual environment created

[STEP 3/8] Activating virtual environment...
✓ Virtual environment activated

[STEP 4/8] Installing build tools...
✓ PyInstaller installed

[STEP 5/8] Installing application dependencies...
✓ All dependencies installed

[STEP 6/8] Cleaning previous builds...
✓ Removed old build folder
✓ Removed old dist folder

[STEP 7/8] Building executable with PyInstaller...
This may take 2-3 minutes, please wait...
✓ Executable created successfully

[STEP 8/8] Creating Windows installer package...
NSIS found, creating Windows installer...
✓ Windows installer created successfully

Location: GaybeckStarKidsSMS_Installer_2.0.3.exe

================================================================================
                         BUILD COMPLETED!
================================================================================

Your installation files are ready:

✓ WINDOWS INSTALLER (Recommended):
   File: GaybeckStarKidsSMS_Installer_2.0.3.exe
   Size: ~150-200 MB
   Use this for distribution to end users

✓ PORTABLE EXECUTABLE:
   Location: dist\GaybeckStarKidsSMS\
   Main file: GaybeckStarKidsSMS.exe
   Use this to run directly without installation

================================================================================
NEXT STEPS FOR DISTRIBUTION:
================================================================================

1. Send "GaybeckStarKidsSMS_Installer_2.0.3.exe" to users
2. Users simply double-click to install
3. Application appears in Start Menu
4. Desktop shortcut is created automatically

For support: Contact your IT administrator

================================================================================
```

---

## 🎯 Key Points

✓ **One-Click Build:** Just run `CREATE_INSTALLER.bat`  
✓ **User-Friendly:** Recipients simply double-click to install  
✓ **Professional:** Appears in Windows Control Panel  
✓ **Complete:** Includes shortcuts, uninstaller, registry entries  
✓ **Portable:** Also works as standalone (no installation needed)  

---

## 📞 Getting Help

If something goes wrong:

1. **Check the error message** in the command window
2. **Wait longer** - builds can take 5-10 minutes
3. **Try again** - some network issues are temporary
4. **Check prerequisites:**
   - Python 3.13+ installed
   - Administrator access
   - Antivirus not blocking
   - 500+ MB free space

---

## 🔄 Rebuilding or Updates

To create a new installer (for updates):

1. Pull latest code from repository (if applicable)
2. Run `CREATE_INSTALLER.bat` again
3. New version of installer is created

Each build is independent - you can create multiple installer versions.

---

## 📁 File Locations

After running `CREATE_INSTALLER.bat`:

```
Your Project Folder/
│
├── CREATE_INSTALLER.bat              ← What you run
├── GaybeckStarKidsSMS_Installer_2.0.3.exe  ← Your installer
├── build/                            ← Temporary build files
├── dist/                             ← Portable version
└── venv/                             ← Virtual environment
```

---

## ✨ Next: Distribute to Users

Once you have `GaybeckStarKidsSMS_Installer_2.0.3.exe`, you can:

1. **Email** it to users (with instructions)
2. **Put on USB** and hand it out
3. **Upload** to Google Drive/OneDrive and share link
4. **Host** on network share for multiple installations
5. **Deploy** via Group Policy (advanced)

See `INSTALLATION_FOR_USERS.md` for user instructions.

---

**Created:** February 3, 2026  
**Build Version:** 2.0.3  
**For:** Windows 7+ Systems  

*Questions? Check INSTALLATION_FOR_USERS.md or DEPLOYMENT_GUIDE.md*
