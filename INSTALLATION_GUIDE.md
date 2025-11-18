# Gaybeck Starkids SMS - Universal Installation Guide

## Quick Install (Recommended)

### Windows
```bash
python INSTALL.py
```

### macOS / Linux
```bash
python3 INSTALL.py
```

---

## What the Installer Does

✓ Checks Python 3.13+ is installed  
✓ Verifies Tkinter GUI framework  
✓ Installs all required dependencies  
✓ Sets up database (if needed)  
✓ Creates application shortcuts  
✓ Verifies installation  

---

## System Requirements

| Requirement | Minimum | Recommended |
|---|---|---|
| **Python** | 3.13+ | 3.13.3+ |
| **RAM** | 2 GB | 4 GB+ |
| **Disk Space** | 500 MB | 1 GB+ |
| **OS** | Windows 7+, macOS 10.13+, Ubuntu 18.04+ | Windows 10/11, macOS 12+, Ubuntu 20.04+ |

---

## Installation Instructions

### Step 1: Install Python
If you don't have Python 3.13+:
- **Windows**: Download from https://www.python.org (check "Add Python to PATH")
- **macOS**: `brew install python@3.13`
- **Linux**: `sudo apt-get install python3.13`

### Step 2: Download Application
Extract the application files to your preferred location.

### Step 3: Run Installer
Open Terminal/Command Prompt in the application folder and run:

**Windows:**
```bash
python INSTALL.py
```

**macOS/Linux:**
```bash
python3 INSTALL.py
```

### Step 4: Follow On-Screen Instructions
The installer will:
1. Check your Python installation
2. Verify Tkinter is available
3. Install dependencies from requirements.txt
4. Set up the database
5. Create shortcuts for easy launching
6. Verify everything works

---

## Launching the Application

### After Installation:

**Windows:**
- Double-click "Gaybeck Starkids SMS" shortcut on Desktop
- OR double-click "RUN_APP.bat" in the app folder
- OR run: `python sms.py`

**macOS:**
- Double-click "launch_app.command" in app folder
- OR run: `python3 sms.py`

**Linux:**
- Run: `./launch_app.sh`
- OR run: `python3 sms.py`

---

## Troubleshooting

### "Python is not installed or not found"
**Solution:** Install Python 3.13+ from https://www.python.org

### "Tkinter not found"
**Solution:**
- **Windows:** Reinstall Python with Tkinter enabled
- **macOS:** `brew install python-tk@3.13`
- **Linux:** `sudo apt-get install python3-tk`

### "Failed to install dependencies"
**Solution:** Run manually:
```bash
pip install -r requirements.txt
```

### "Database not found"
**Solution:** Don't worry - the database will be created automatically on first run

### Application won't start
**Solution:** Run the verification:
```bash
python test_launch.py
```

This will show which components are missing.

---

## Features Included

- 📚 **Student Management** - Add, edit, track students
- 👥 **Teacher Management** - Manage staff and assignments
- 📊 **Attendance Tracking** - Real-time attendance system
- 💰 **Fee Management** - Track fees and payments
- 📈 **Grade Management** - Record and analyze grades
- 💼 **Financial Reports** - Comprehensive financial analytics
- 🤖 **AI Analytics** - Predictive insights and risk analysis
- 🔐 **Role-Based Access** - Admin, Teacher, Accountant roles
- 💾 **Database Backups** - Automatic data protection

---

## First Login

Default admin credentials (can be changed in User Management):
- **Username:** admin
- **Password:** admin123

⚠️ **Security:** Change the password immediately after first login!

---

## Getting Help

1. Check the `docs/` folder for detailed guides
2. Review `QUICK_START.md` for feature tutorials
3. Run `test_launch.py` for system diagnostics
4. Check application logs for errors

---

## Uninstallation

Simply delete the application folder. All data is stored locally in the `database/` folder.

To keep your data:
1. Use Backup & Restore in Settings before uninstalling
2. Save the backup file
3. Delete the application folder

To restore later:
1. Reinstall the application
2. Use Backup & Restore → Restore to import your data

---

**Version:** 3.0.0  
**Last Updated:** November 2025  
**Support:** Check documentation files in `docs/` folder

Enjoy! 🎉
