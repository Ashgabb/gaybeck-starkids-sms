# Gaybeck Starkids SMS - Quick Start Guide

## 🚀 Getting Started (Choose One Method)

### Method 1: Simple Batch File (Easiest)
1. **Double-click** `RUN_APP.bat` in the application folder
2. The application will launch automatically

**Pros:** Single click, simple, works on all Windows systems  
**Cons:** Basic error messages

---

### Method 2: PowerShell Script (Recommended for Power Users)
1. **Right-click** `RUN_APP.ps1`
2. Select **"Run with PowerShell"**
3. The application will launch

**To run with diagnostics:**
```powershell
powershell -File RUN_APP.ps1 -Diagnostic
```

**Pros:** Better error messages, diagnostic support, colored output  
**Cons:** Requires PowerShell execution policy (usually enabled)

---

### Method 3: Command Line (For Developers)
Open Command Prompt or PowerShell and run:
```bash
python sms.py
```

**Pros:** Direct control, see all output, customizable  
**Cons:** Need command line knowledge

---

### Method 4: Installer (First Time Setup)
1. **Double-click** `SETUP.bat`
2. Follow on-screen instructions
3. Choose installation option
4. Once installed, use Method 1 or 2 above

**Pros:** Full installation, creates shortcuts, manages dependencies  
**Cons:** Takes longer, more steps

---

## ✅ Verify Everything Works

Before using the application, verify your system:

```bash
python test_launch.py
```

This will check:
- ✓ Python version (3.13+)
- ✓ Required modules
- ✓ Optional AI modules
- ✓ Database
- ✓ Tkinter GUI framework
- ✓ Application startup

**Expected Output:**
```
[Test 1] Python version: 3.13.x [OK]
[Test 2] Required modules: All present [OK]
[Test 3] Optional modules: All installed [OK]
[Test 4] Database: 652 KB, accessible [OK]
[Test 5] SMS module: Imports successfully [OK]
[Test 6] Tkinter GUI: Framework working [OK]
[Test 7] Application startup: Successful [OK]

Result: All required components present - Application should launch successfully!
```

If any test fails, see **Troubleshooting** section below.

---

## 🔧 Troubleshooting

### Issue: "Python is not installed or not in PATH"
**Solution:**
1. Install Python 3.13+ from https://www.python.org
2. **IMPORTANT:** During installation, check ✓ "Add Python to PATH"
3. Restart your computer
4. Try again

### Issue: Missing modules error
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "ModuleNotFoundError: No module named 'tkinter'"
**Solution:**
1. Tkinter usually comes with Python
2. If missing, reinstall Python with Tkinter enabled
3. On Windows, this is typically selected by default

### Issue: Database file not found
**Solution:**
1. Ensure `database/` folder exists in the application directory
2. If not, it will be created automatically on first run
3. You may need to run the installer: `SETUP.bat`

### Issue: Application opens then closes immediately
**Solution:**
1. Run the diagnostic: `python test_launch.py`
2. Check output for specific errors
3. If Tkinter error, reinstall Python with Tkinter
4. If module missing, run: `pip install -r requirements.txt`

### Issue: Black window appears but nothing happens
**This is NORMAL!** The application is starting. Wait 5-10 seconds for the GUI window to appear. This is not an error—it's just how Tkinter applications start on Windows.

---

## 📋 System Requirements

| Requirement | Minimum | Recommended |
|---|---|---|
| Python | 3.13+ | 3.13.3+ |
| RAM | 2 GB | 4 GB+ |
| Disk Space | 500 MB | 1 GB+ |
| Windows | Windows 7+ | Windows 10/11 |
| Screen Resolution | 1024x768 | 1366x768+ |

---

## 📁 What Gets Installed

```
Gaybeck Starkids SMS/
├── sms.py                          # Main application
├── advanced_ai_analytics.py         # AI/ML engine
├── database/
│   └── school_management.db         # SQLite database
├── RUN_APP.bat                      # Quick launcher (batch)
├── RUN_APP.ps1                      # Advanced launcher (PowerShell)
├── SETUP.bat                        # Installer
├── requirements.txt                 # Python dependencies
├── test_launch.py                   # Diagnostic tool
└── [Many other support files]
```

---

## 🎯 Next Steps

1. **First Time?** Run `SETUP.bat` to install
2. **Quick Start?** Double-click `RUN_APP.bat`
3. **Need Diagnostics?** Run `python test_launch.py`
4. **Problems?** Check Troubleshooting section above
5. **Documentation?** See `docs/` folder for detailed guides

---

## 📞 Getting Help

If you encounter issues:

1. **Run diagnostics:**
   ```bash
   python test_launch.py
   ```

2. **Check documentation:**
   - `INSTALLER_FIX_REPORT.md` - Installer and setup issues
   - `BUILD_COMPLETE_v2.0.3.md` - Feature overview
   - `docs/` folder - Detailed guides for each module

3. **Verify requirements:**
   ```bash
   pip list
   ```

4. **Check database:**
   - Ensure `database/school_management.db` exists
   - File should be ~650+ KB
   - If missing, run `SETUP.bat` to reinstall

---

## 📝 Version Info

**Application Version:** 3.0.0  
**Python Required:** 3.13+  
**Framework:** Tkinter + SQLite3  
**ML Engine:** scikit-learn, pandas, numpy, scipy  
**Last Updated:** 2024

---

**Ready to launch?** Use any method above. Most users prefer simply **double-clicking `RUN_APP.bat`** for convenience.

Good luck! 🎉
