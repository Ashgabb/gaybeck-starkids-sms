# Quick Reference - Running SMS on Any Device

## 🚀 Fastest Way to Run (Choose One)

### Windows - Pick Any Method
```bash
# Method 1: Click batch file (Easiest)
run_app.bat

# Method 2: Windows command
python sms.py

# Method 3: Enhanced launcher
python launch_app.py

# Method 4: Simple batch
sms_launcher.bat  or  .\sms_launcher.bat
```

### Linux / Mac
```bash
python3 sms.py
```

---

## ⚙️ Setup (First Time Only)

```bash
# Interactive setup - installs dependencies and creates shortcuts
python setup_portable.py

# Or manual install
pip install -r requirements.txt
```

---

## 📋 What You Need

- Python 3.8+ (3.13+ recommended)
- That's it! Everything else is included or installed automatically

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Python not found" | Install Python from python.org, check "Add to PATH" |
| "Module not found" | Run `pip install -r requirements.txt` |
| App won't start | Check `logs/launch_*.log` for details |
| Broken shortcut | Run `create_sms_shortcut.vbs` again |

---

## 💾 Important Features

### Backup Your Data
1. Settings → Backup & Restore
2. Click "Full Database Backup"
3. Located in `database_backups/` folder

### Clear Test Data (Admin Only)
1. Settings → Data Management
2. Choose what to clear
3. ⚠️ Always backup first!

---

## 📁 Files to Know

```
sms.py                    ← Main application
run_app.bat               ← Windows launcher (simplest)
setup_portable.py         ← Setup wizard
requirements.txt          ← Package list
database/                 ← Your data (backup this!)
database_backups/         ← Backups
logs/                     ← Debug logs
```

---

## 🎯 Moving to Another Device

1. **Copy** the entire `gaybeck-starkids-sms` folder
2. **Run** `python sms.py` (or double-click `run_app.bat` on Windows)
3. **Done!** No manual setup needed

---

## 📞 Help

See these files for more information:
- **PORTABLE_INSTALLATION_GUIDE.md** - Complete guide
- **UPDATE_PORTABLE_INSTALLATION.md** - What's new
- **LAUNCHER_GUIDE.md** - Launcher options
- Check **logs/** folder for error details

---

**That's it! Enjoy!** 🎉
