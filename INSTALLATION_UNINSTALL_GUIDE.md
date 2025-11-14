# Gaybeck Starkids SMS - Installation & Uninstall Features

## ✅ Installation Complete (v2.0.0)

### What's Installed

1. **Python Package**: `gaybeck-starkids-sms` installed via pip
2. **Desktop Shortcut**: `Gaybeck Starkids Academy.lnk`
3. **Start Menu Shortcut**: In Windows Start Menu
4. **Launcher Script**: `C:\Users\User\AppData\Roaming\GaybeckStarkidsSMS\launch.bat`
5. **Console Commands**:
   - `starkids-sms` (launch app)
   - `starkids-sms-uninstall` (run uninstaller)

### Launch Methods

| Method | Command/Action |
|--------|----------------|
| **Desktop Shortcut** | Double-click "Gaybeck Starkids Academy" on Desktop |
| **Start Menu** | Search for "Gaybeck Starkids Academy" in Windows Start Menu |
| **Python Command** | `python -c "import sms; sms.start_application()"` |
| **Batch File** | Run `launch_app.bat` from project directory |
| **Direct Script** | `python sms.py` (from project directory) |

### Data Storage

- **Installed Version**: `C:\Users\User\AppData\Roaming\GaybeckStarkidsSMS\`
  - `database\school_management.db`
  - `teacher_documents\`
  - `reports\`
  - `launch.bat`

- **Source Version**: `c:\Users\User\Desktop\GAYBECK STARKIDS SMS\`
  - `database\school_management.db`
  - `teacher_documents\`
  - `reports\`

---

## 🗑️ Uninstallation Features

### Automatic Uninstaller (`uninstall.py`)

The uninstaller performs a complete cleanup:

1. **Stops Running Processes**
   - Detects any running instances
   - Force stops all Gaybeck/Starkids processes

2. **Removes Python Package**
   - Uninstalls via pip: `gaybeck-starkids-sms`
   - Removes from site-packages

3. **Removes Shortcuts**
   - Desktop shortcut
   - Start Menu shortcut
   - System-wide shortcuts (if any)

4. **Removes Application Data** (with confirmation)
   - Database files
   - Teacher documents
   - Reports
   - Launcher scripts

5. **Removes Console Scripts**
   - `starkids-sms.exe`
   - `starkids-sms-uninstall.exe`

### How to Uninstall

| Method | Command/Action |
|--------|----------------|
| **Batch File** | Double-click `uninstall.bat` |
| **Python Script** | `python uninstall.py` |
| **Python Module** | `python -m uninstall` |
| **Console Command** | `starkids-sms-uninstall` (if PATH configured) |
| **Manual Pip** | `python -m pip uninstall gaybeck-starkids-sms` |

### What Gets Removed

✅ Installed Python package  
✅ Desktop shortcut  
✅ Start Menu shortcut  
✅ Application data (with confirmation)  
✅ Console script executables  
✅ Running processes  

### What Does NOT Get Removed

❌ Source code folders (`GAYBECK STARKIDS SMS`, `STARKIDS-SCHOOL-MANAGER`)  
❌ Development files  
❌ Backup files  
❌ Build artifacts (`dist/`, `build/`)  

These must be deleted manually if desired.

---

## 📦 Installation Scripts

### `install.bat`
Complete installation with shortcuts:
```batch
python -m pip install dist\gaybeck_starkids_sms-2.0.0-py3-none-any.whl --force-reinstall
python post_install.py
```

### `post_install.py`
Post-installation setup:
- Creates launcher batch file
- Creates desktop shortcut (requires pywin32)
- Creates Start Menu shortcut (requires pywin32)

### `uninstall.bat`
Complete uninstallation:
```batch
python uninstall.py
```

### `uninstall.py`
Comprehensive uninstaller that:
- Finds and stops running processes
- Uninstalls pip package
- Removes all shortcuts
- Cleans up application data
- Removes console scripts

---

## 🔧 Requirements

### For Installation
- Python 3.8+
- pip
- tkcalendar >= 1.6.1
- Pillow >= 10.0.0

### For Shortcut Creation
- pywin32 (optional, for automatic shortcut creation)
- Install with: `pip install pywin32`

### For Uninstallation
- No special requirements
- Works standalone

---

## 📝 Usage Examples

### Clean Installation
```powershell
cd "c:\Users\User\Desktop\GAYBECK STARKIDS SMS"
.\install.bat
```

### Manual Installation
```powershell
python -m pip install dist\gaybeck_starkids_sms-2.0.0-py3-none-any.whl
python post_install.py
```

### Complete Uninstallation
```powershell
.\uninstall.bat
# OR
python uninstall.py
```

### Reinstallation
```powershell
python uninstall.py
python -m pip install dist\gaybeck_starkids_sms-2.0.0-py3-none-any.whl
python post_install.py
```

---

## 🎯 Default User Accounts

| Username   | Password       | Role        |
|------------|----------------|-------------|
| admin      | admin123       | admin       |
| teacher    | teacher123     | teacher     |
| accountant | accountant123  | accountant  |
| staff      | staff123       | staff       |

---

## ✨ Features

### Application Features
- Student Management (with class filtering)
- Teacher Management (with profile printing)
- Class Management
- Attendance Tracking (non-expandable interface)
- Fee Management (auto-calculation, fee types, payment modes)
- Financial Management (budgets, transactions, analytics)
- Staff Directory (with salary statistics)
- Comprehensive Reports
- Real-time Dashboard
- User Management (role-based access)

### Installation Features
- One-click installation via batch file
- Automatic shortcut creation
- Smart data directory detection (source vs installed)
- Separate databases for development and production

### Uninstallation Features
- Complete cleanup (shortcuts, data, processes)
- Interactive data removal (requires confirmation)
- Multiple uninstall methods
- Safe uninstall (preserves source code)

---

## 📌 Notes

1. **Separate Databases**: The installed version and source version use different databases
2. **Data Persistence**: Application data in AppData persists across reinstalls
3. **Source Code**: Uninstaller does not remove source code folders
4. **Shortcuts**: Created in user profile (no admin rights needed)
5. **PATH**: Console commands require Scripts directory in PATH

---

**Last Updated**: November 14, 2025  
**Version**: 2.0.0  
**Status**: ✅ Fully Functional
