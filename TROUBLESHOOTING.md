# 🆘 Can't Open App? Troubleshooting Guide

## Quick Fixes

### ✅ Method 1: Use the Desktop Shortcut
1. Look for **"Gaybeck Starkids SMS"** icon on your Desktop
2. **Double-click** it
3. The app should open in a few seconds

If this doesn't work, try Method 2...

---

### ✅ Method 2: Use the Launcher
1. Open File Explorer
2. Navigate to: `c:\Users\User\Desktop\GAYBECK STARKIDS SMS`
3. Look for **`launch.bat`** file
4. **Double-click** it
5. A window will appear - this is normal, the app is starting
6. The GUI will open in a few seconds

If this doesn't work, try Method 3...

---

### ✅ Method 3: Run from Command Line

#### For Windows Command Prompt:
```
cd c:\Users\User\Desktop\GAYBECK STARKIDS SMS
python sms.py
```

#### For PowerShell:
```powershell
cd "c:\Users\User\Desktop\GAYBECK STARKIDS SMS"
python sms.py
```

---

## Common Problems & Solutions

### Problem 1: "Python is not installed" Error

**Cause**: Python is not on your system PATH

**Solution**:
1. Download Python from: https://www.python.org/downloads/
2. **IMPORTANT**: During installation, CHECK the box: **"Add Python to PATH"**
3. Restart your computer
4. Try launching the app again

---

### Problem 2: App Opens but Shows an Error

**Check the error message** - here are common ones:

#### "No module named 'tkcalendar'"
```
pip install tkcalendar
```

#### "No module named 'PIL'"
```
pip install Pillow
```

#### "No module named 'pandas'" or 'numpy' or 'sklearn'
```
pip install pandas numpy scikit-learn
```

Then try running the app again.

---

### Problem 3: "ModuleNotFoundError: No module named 'sms'"

**Cause**: You're not in the correct directory

**Solution**:
1. Open Command Prompt or PowerShell
2. Navigate to the app folder:
   ```
   cd "c:\Users\User\Desktop\GAYBECK STARKIDS SMS"
   ```
3. Run:
   ```
   python sms.py
   ```

---

### Problem 4: App Opens but Nothing Happens

**This is normal!** The app takes a few seconds to load. 

- Wait 5-10 seconds
- You should see a login window appear
- If nothing appears after 30 seconds, try Method 3 above

---

### Problem 5: "Database is locked" Error

**Cause**: The database is already open in another window

**Solution**:
1. Close all open instances of the app
2. Wait 5 seconds
3. Try opening again

If this persists:
1. Restart your computer
2. Try opening again

---

## Verification Test

To verify everything is installed correctly, run:

```
python test_app.py
```

You should see:
```
[TEST 1] Python Version
  Version: 3.13.3
  ✓ PASS

[TEST 2] Working Directory
  ...
  ✓ PASS

... etc
```

If any tests show `✗ FAIL`, you need to install the missing packages.

---

## Still Not Working?

Try these steps in order:

### Step 1: Reinstall Dependencies
```
pip install -r requirements.txt
```

### Step 2: Repair Installation
```
./install.bat
```

### Step 3: Full Diagnostic
1. Run in PowerShell as Administrator:
   ```powershell
   cd "c:\Users\User\Desktop\GAYBECK STARKIDS SMS"
   python test_app.py
   ```
2. Report all `✗ FAIL` messages

### Step 4: Reset Database
If you keep getting database errors:
1. Close the app completely
2. Go to: `database_backups/` folder
3. Copy any `.db` file
4. Replace `school_management.db` in the main folder
5. Try opening app again

---

## Getting Help

When reporting issues, provide:
1. **Error message** (copy the exact text)
2. **Your Windows version** (Windows 10/11)
3. **Python version**: Run `python --version`
4. **Output of**: `python test_app.py`

---

## Expected Startup Behavior

✅ **Correct sequence**:
1. You run the launcher
2. Python starts (may see command window)
3. After 5-10 seconds, a **Login Window** appears
4. Enter username: `admin` and password: `admin123`
5. Main app window opens

If you see anything different, check the error message above.

---

## Quick Start Once App Opens

### First Login:
- **Username**: `admin`
- **Password**: `admin123`

### Change Password (Recommended):
1. Click on **Settings** (top menu)
2. Click **Change Password**
3. Enter current and new password

### Add Your First Student:
1. Click **Student Management**
2. Click **Add Student**
3. Fill in the details
4. Click **Save Student**

---

**The app is designed to work! Most issues are just environment setup. Follow the steps above and you'll be up and running.** 🎉
