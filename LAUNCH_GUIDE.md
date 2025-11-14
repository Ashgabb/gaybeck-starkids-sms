# Gaybeck Starkids SMS - Launch Guide

## Installation Status: ✅ VERIFIED (v2.0.0)

**Installation Location:** `C:\Users\User\AppData\Roaming\Python\Python314\site-packages`  
**Package Size:** 0.96 MB (1,011,525 bytes)  
**Database Location:** `C:\Users\User\AppData\Roaming\GaybeckStarkidsSMS\database`  
**All Dependencies:** ✅ Installed (tkcalendar, Pillow, tkinter, sqlite3)

---

## How to Launch the Application

### Method 1: Double-Click Launch Script (Easiest)
1. Navigate to the project folder: `c:\Users\User\Desktop\GAYBECK STARKIDS SMS`
2. Double-click `launch_app.bat`

### Method 2: Python Import (Recommended for Installed Version)
```powershell
python -c "import sms; sms.start_application()"
```
**Note:** This works from any directory!

### Method 3: Direct Execution (From Project Directory)
```powershell
cd "c:\Users\User\Desktop\GAYBECK STARKIDS SMS"
python sms.py
```

### Method 4: Console Command (Requires PATH Configuration)
```powershell
starkids-sms
```
**Note:** This requires adding Python Scripts directory to your system PATH:
- Location: `C:\Users\User\AppData\Roaming\Python\Python314\Scripts`
- Add to PATH in Windows Environment Variables

---

## Data Storage Locations

### When Running from Installed Package
- **Database:** `C:\Users\User\AppData\Roaming\GaybeckStarkidsSMS\database\school_management.db`
- **Teacher Documents:** `C:\Users\User\AppData\Roaming\GaybeckStarkidsSMS\teacher_documents\`
- **Reports:** `C:\Users\User\AppData\Roaming\GaybeckStarkidsSMS\reports\`

### When Running from Source Directory
- **Database:** `c:\Users\User\Desktop\GAYBECK STARKIDS SMS\database\school_management.db`
- **Teacher Documents:** `c:\Users\User\Desktop\GAYBECK STARKIDS SMS\teacher_documents\`
- **Reports:** `c:\Users\User\Desktop\GAYBECK STARKIDS SMS\reports\`

**Note:** The application automatically detects which mode it's running in and uses the appropriate location.

---

## Default User Accounts

| Username   | Password       | Role        |
|------------|----------------|-------------|
| admin      | admin123       | admin       |
| teacher    | teacher123     | teacher     |
| accountant | accountant123  | accountant  |
| staff      | staff123       | staff       |

---

## Key Features (Latest Build)

### ✅ Completed Enhancements
- **DateEntry Widgets:** All date fields use calendar pickers
- **Fee Management:**
  - Fee Types: Tuition, Feeding, Bus
  - Payment Modes: Cash, MoMo, Bank
  - Auto-calculation: Amount Due = Arrears + Monthly Fee
- **Class Filtering:** Students and Fees management can filter by class
- **Staff Overview:** Fixed to display correct salary statistics
- **User Management:** All roles (admin, teacher, accountant, staff) functional

### 📊 Application Modules
- **Dashboard:** Real-time statistics and analytics
- **Student Management:** Registration, list, class filtering
- **Teacher Management:** Registration, list, profile printing
- **Class Management:** Class creation, student assignment
- **Attendance:** Daily tracking with non-expandable interface
- **Fees Management:** Payment tracking with auto-calculation
- **Financial Management:** Budget, transactions, analytics
- **Staff Directory:** Staff profiles and statistics
- **Reports:** Comprehensive reporting system

---

## Troubleshooting

### Issue: "starkids-sms not recognized"
**Solution:** Use Method 1 (launch_app.bat) or Method 2 (Python import) instead

### Issue: Missing UI components or data
**Solution:** 
1. Check which mode you're running (installed vs source)
2. For installed version: Data is in `%APPDATA%\GaybeckStarkidsSMS`
3. For source version: Data is in the project directory
4. Both versions have separate databases!

### Issue: Fresh database with no data
**Solution:** This is normal for a new installation. The installed version creates its own database in AppData. To populate with test data:
```powershell
cd "c:\Users\User\Desktop\GAYBECK STARKIDS SMS"
python tests\comprehensive_data_test.py
```
**Note:** This only affects the source directory database, not the installed version.

### Issue: Database errors
**Solution:** Database auto-creates on first run. Warnings about missing columns during first run are normal.

### Issue: "Could not add column" warnings
**Solution:** These warnings are normal when running a fresh database for the first time. They can be safely ignored.

---

## Recent Fixes (v2.0.0)

1. **Package Build Fix:** 
   - Added `py_modules=['sms']` to setup.py
   - Added `include sms.py` to MANIFEST.in
   - Ensures sms.py is properly included in wheel distribution

2. **Installation Verification:**
   - Module properly installed to site-packages
   - All dependencies resolved
   - File integrity verified (0.96 MB)

3. **Database Schema Updates:**
   - Added `fee_type` column to fees table
   - Added `payment_mode` column to fees table
   - Fixed staff overview to use `starting_salary` column

---

## Development Commands

### Rebuild and Reinstall Package
```powershell
python rebuild.py
```

### Verify Installation
```powershell
python tests\verify_installation.py
```

### Check All User Accounts
```powershell
python tests\check_all_users.py
```

### Show Login Credentials
```powershell
python tests\show_login_credentials.py
```

---

## Database Location
- **Development:** `c:\Users\User\Desktop\GAYBECK STARKIDS SMS\database\school_management.db`
- **Installed:** Database creates in project directory regardless of installation

---

## Support Files
- **Documentation:** See `docs/` folder for comprehensive guides
- **Test Scripts:** See `tests/` folder for verification tools
- **Backups:** Located in `backups/` folder

---

**Last Updated:** January 2025  
**Version:** 2.0.0  
**Build Status:** ✅ Verified and Working
