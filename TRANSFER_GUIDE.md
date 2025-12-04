# 📦 GAYBECK STARKIDS SMS - Transfer & Installation Guide

## What's Included in the Package

The `GAYBECK_STARKIDS_SMS_*.zip` file contains:
- ✅ `sms.py` - Main application file (22,467 lines)
- ✅ `requirements.txt` - Python dependencies
- ✅ `school_management.db` - SQLite database with all records
- ✅ `database/` - Database backup files
- ✅ `docs/` - Documentation and guides
- ✅ `version.json` - Version information
- ✅ `logo.png` & `sms_icon.ico` - Application icons
- ✅ `run_app.py` - Startup script

## Installation on New Device

### Step 1: Extract the Package
```bash
# Extract the zip file to desired location
# Example: C:\GAYBECK STARKIDS SMS\
```

### Step 2: Install Python
- **Requirement**: Python 3.13.x (Python 3.14+ has Tkinter issues)
- Download from: https://www.python.org/downloads/
- ⚠️ **Important**: Check "Add Python to PATH" during installation

### Step 3: Install Dependencies
```bash
# Open Command Prompt/PowerShell in the extracted folder
cd path/to/GAYBECK_STARKIDS_SMS

# Install required packages
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
# Option 1: Using run_app.py
python run_app.py

# Option 2: Direct execution
python sms.py
```

## Key Features Ready to Use

✅ **Student Management**
- Add/Edit/Delete students with popup forms
- Auto-generate student IDs (STU{YEAR}{SEQUENCE})
- Student list with filtering
- All fields: Personal, Academic, Contact, Fees, Emergency, Medical

✅ **Teacher Management**
- Add/Edit/Delete teachers with full details
- Staff directory with search
- Salary tracking
- Document management

✅ **Attendance System**
- Mark attendance by student or teacher
- Real-time sync
- Reports and analytics

✅ **Financial Management**
- Fee tracking and invoicing
- Payment records
- Financial reports

✅ **Database**
- Pre-configured SQLite database
- All tables and relationships ready
- Backup system built-in

## Troubleshooting

### Python Not Found
```bash
# Verify Python installation
python --version

# If not found, check PATH or use full path
C:\Python313\python.exe run_app.py
```

### Missing Dependencies
```bash
# Reinstall all packages
pip install -r requirements.txt --force-reinstall
```

### Database Issues
- Database file (`school_management.db`) is included
- Backups stored in `database/` folder
- First run will auto-initialize if needed

### Tkinter Issues (Python 3.14+)
- Switch to Python 3.13.x
- Use: `python -m pip install tk`

## System Requirements

| Component | Requirement |
|-----------|-------------|
| **OS** | Windows 7+ |
| **Python** | 3.13.x (NOT 3.14+) |
| **RAM** | Minimum 2GB |
| **Storage** | 100MB+ |
| **Screen** | 1366x768 or higher |

## Database & Data

✅ All student/teacher records are in `school_management.db`
✅ Database is portable - moves with the zip file
✅ No separate server needed - SQLite is embedded
✅ Backups available in `database/` folder

## First Run

1. Extract the zip file
2. Install Python 3.13
3. Run: `pip install -r requirements.txt`
4. Run: `python sms.py`
5. Login with your credentials
6. Start using the system!

## Version Info

Check `version.json` for current version and features.

## Support

- Check `docs/` folder for detailed documentation
- Review `TROUBLESHOOTING.md` for common issues
- Application logs available in execution console

---

**Ready to transfer!** The entire SMS system is now portable. 🎓
