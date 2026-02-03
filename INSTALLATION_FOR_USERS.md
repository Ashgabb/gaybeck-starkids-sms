# Gaybeck Starkids SMS - Installation Guide for Non-Technical Users

## 📋 Overview

This guide provides step-by-step instructions for creating and distributing the Gaybeck Starkids SMS application to non-technical users. The application can be installed as a standard Windows application.

---

## 🚀 Quick Start (For End Users)

### **Option 1: One-Click Installer (Recommended)**

If you received `GaybeckStarKidsSMS_Installer_2.0.3.exe`:

1. **Double-click** the installer file
2. Click **"Next"** at each step
3. Choose installation location (or accept default: `C:\Program Files\Gaybeck Starkids SMS`)
4. Wait for installation to complete (2-3 minutes)
5. Click **"Finish"** and check the "Launch now" option
6. The application will start automatically

**Result:**
- ✓ Application installed in Program Files
- ✓ Start Menu shortcut created
- ✓ Desktop shortcut created
- ✓ Can be uninstalled from Control Panel

### **Option 2: Portable Version (No Installation)**

If you received a `GaybeckStarKidsSMS.exe` file or folder:

1. Copy the folder to any location (USB drive, Desktop, Documents, etc.)
2. Double-click `GaybeckStarKidsSMS.exe` to run

**Note:** No installation required. Can run from anywhere, including USB drives.

---

## 🛠️ Creating the Installer (For Administrators)

### **Prerequisites**

Your computer needs:
- **Windows 7 or later**
- **Python 3.13+** (free, open-source)
- **~500 MB free disk space**

### **Step 1: Verify Python Installation**

1. Press `Win + R` and type: `python --version`
2. You should see something like: `Python 3.13.x`
3. If this fails, [download Python](https://www.python.org/downloads/):
   - Click "Downloads" → select version 3.13 or higher
   - Run the installer
   - **IMPORTANT:** Check "Add Python to PATH" during installation
   - Click "Install Now"
   - Restart your computer

### **Step 2: Create the Installer**

**Method A: Automatic (Easiest)**

1. Navigate to the project folder: `C:\Users\YourName\Documents\gaybeck-starkids-sms`
2. Find `CREATE_INSTALLER.bat`
3. **Double-click** it
4. Wait for the process to complete (5-10 minutes)
5. Look for: `GaybeckStarKidsSMS_Installer_2.0.3.exe`

**Method B: Manual Command Line**

1. Open PowerShell (Windows key + type "PowerShell")
2. Navigate to project folder:
   ```powershell
   cd C:\Users\YourName\Documents\gaybeck-starkids-sms
   ```
3. Run installer creator:
   ```powershell
   .\CREATE_INSTALLER.bat
   ```

### **Step 3: Verify Installation File**

After the build completes, you should see:

```
GaybeckStarKidsSMS_Installer_2.0.3.exe   (~150-200 MB)
```

**Test the installer:**
1. Double-click the `.exe` file
2. Complete the installation wizard
3. Launch the application
4. Verify it runs correctly

---

## 📦 Distribution to End Users

### **Option 1: Direct File Distribution**

1. **Send the installer file** (`GaybeckStarKidsSMS_Installer_2.0.3.exe`)
2. **Include these instructions:**

   ```
   Installation Instructions:
   1. Double-click GaybeckStarKidsSMS_Installer_2.0.3.exe
   2. Click "Next" at each step
   3. Accept the default installation location
   4. Click "Finish"
   5. The application will launch automatically
   
   Support: Contact your IT administrator if you have issues
   ```

### **Option 2: USB Drive Distribution**

1. Copy the `.exe` file to a USB drive
2. Include a text file with instructions (from Option 1)
3. Distribute to users

### **Option 3: Email Distribution**

The installer file (~150-200 MB) can be uploaded to:
- **Google Drive** / **OneDrive** - Share the link
- **Dropbox** - Create a shareable link
- **Email** - If your email system allows large attachments

---

## ⚙️ System Requirements

### **Minimum Requirements**

| Component | Requirement |
|-----------|-------------|
| **OS** | Windows 7 or later |
| **RAM** | 2 GB minimum (4 GB recommended) |
| **Storage** | 300 MB free space |
| **Display** | 1024x768 resolution minimum |

### **Recommended Requirements**

| Component | Recommendation |
|-----------|-------------|
| **OS** | Windows 10 or Windows 11 |
| **RAM** | 4 GB or more |
| **Storage** | 500 MB free space (for updates) |
| **Display** | 1366x768 or higher |
| **Internet** | Optional (for updates only) |

---

## 🔧 Troubleshooting

### **Issue: "Python is not installed"**

**Solution:**
1. Install Python 3.13+ from [python.org](https://www.python.org/downloads/)
2. **IMPORTANT:** Check "Add Python to PATH"
3. Restart your computer
4. Run `CREATE_INSTALLER.bat` again

### **Issue: Installation fails with error**

**Solution:**
1. Ensure you have Administrator privileges
2. Disable antivirus software temporarily
3. Try installing to a different folder
4. Contact IT support with the error message

### **Issue: Application won't start after installation**

**Solution:**
1. Verify the application installed correctly:
   - Go to `C:\Program Files\Gaybeck Starkids SMS`
   - Double-click `GaybeckStarKidsSMS.exe`
2. If it still doesn't work:
   - Uninstall from Control Panel
   - Restart your computer
   - Reinstall using the installer

### **Issue: "NSIS not found" warning during build**

**Solution (Optional - for advanced installers):**
If you want to create a more polished installer with NSIS:

1. Install NSIS from [nsis.sourceforge.io](https://nsis.sourceforge.io/download)
2. Run `CREATE_INSTALLER.bat` again
3. This creates a more compact installer (~50 MB instead of ~200 MB)

---

## 📋 File Locations After Installation

```
C:\Program Files\Gaybeck Starkids SMS\
├── GaybeckStarKidsSMS.exe          (Main application)
├── database/                        (School data)
│   └── school_management.db        (SQLite database)
├── database_backups/               (Automatic backups)
├── docs/                           (Documentation)
└── uninstall.exe                   (Uninstaller)
```

---

## 🔒 Security & Data

### **Data Location**

- **Database:** `C:\Program Files\Gaybeck Starkids SMS\database\`
- **Backups:** `C:\Program Files\Gaybeck Starkids SMS\database_backups\`

### **Data Safety**

The application:
- ✓ Stores data locally on the computer
- ✓ Creates automatic backups
- ✓ Does not require internet connection
- ✓ All data stays on your school's computers

### **Regular Backups**

Use the **Admin Menu → Backup** option to create manual backups:
1. Open the application
2. Login as Administrator
3. Click **Backup Database**
4. Save the backup file to a safe location

---

## 📚 Features After Installation

Once installed, the application includes:

- **Student Management** - Register and manage student records
- **Fee Collection** - Track student payments
- **Attendance** - Daily attendance logging
- **Grading** - Student grades and academic records
- **Financial Analytics** - Period comparison and revenue analysis
- **AI Insights** - Predictive analytics for risk assessment
- **Role-Based Access** - Different views for Admin, Teachers, Accountants

---

## 🔄 Updates & Maintenance

### **Updating to a New Version**

1. **Option A (Automatic):** If an update is available
   - A notification will appear in the application
   - Click "Update" and follow the prompts

2. **Option B (Manual):** Create a new installer with the latest version
   - Follow the "Creating the Installer" section again
   - Run the new installer (it will update the existing installation)

### **Uninstalling**

**Method 1 (Recommended):**
1. Go to **Control Panel** → **Programs and Features**
2. Find **"Gaybeck Starkids SMS"**
3. Click **Uninstall**
4. Click **Yes** to confirm

**Method 2 (Manual):**
1. Double-click `uninstall.exe` in the installation folder
2. Click **Yes** to confirm removal

---

## 📞 Support

### **Getting Help**

1. **Check Documentation:** Application includes built-in help files
2. **Contact IT Administrator:** For technical issues
3. **Email Support:** If available from your school

### **Reporting Issues**

When reporting problems, include:
- **Windows version:** (e.g., Windows 10, Windows 11)
- **Application version:** (see About → Version in app)
- **Error message:** (if any)
- **Steps to reproduce:** How the issue happened

---

## 📝 Build Information

**Build Date:** February 3, 2026  
**Version:** 2.0.3  
**Built With:** PyInstaller 6.1.0+, Python 3.13+  
**Target Platform:** Windows 7 and later  

---

## ✅ Pre-Installation Checklist

Before distributing to users, verify:

- [ ] Python 3.13+ installed on build computer
- [ ] `CREATE_INSTALLER.bat` runs without errors
- [ ] Installer file created: `GaybeckStarKidsSMS_Installer_2.0.3.exe`
- [ ] Tested installation on clean Windows machine
- [ ] Application launches correctly after installation
- [ ] Database file created in correct location
- [ ] Shortcuts appear on desktop and Start Menu
- [ ] Uninstaller works correctly

---

## 📄 License & Terms

[Include your organization's license information here]

---

**Last Updated:** February 3, 2026  
**Installation Type:** Windows Standalone Application  
**Support Level:** Community/Enterprise (depending on setup)
