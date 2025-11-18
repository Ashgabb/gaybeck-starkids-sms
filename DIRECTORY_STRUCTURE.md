# Gaybeck Starkids SMS - Directory Structure

## Root Directory (Main Files)

```
📦 Gaybeck Starkids SMS/
├── 📄 README.md                      # Main project documentation
├── 📄 QUICK_START.md                 # Quick start guide for users
├── 📄 INSTALLATION_GUIDE.md          # Installation instructions
├── 📄 LAUNCH_GUIDE.md                # How to launch the application
├── 📄 RELEASE_NOTES_v3.0.0.md        # Version 3.0.0 release notes
├── 📄 START_HERE.md                  # Start here for new users
├── 📄 INSTALL.py                     # Universal installer (RUN THIS)
├── 📄 sms.py                         # Main application (21,600+ lines)
├── 📄 advanced_ai_analytics.py       # AI/ML analytics engine
├── 📄 realtime_sync.py               # Real-time synchronization
├── 📄 requirements.txt               # Python dependencies
├── 📄 setup.py                       # Setup configuration
├── 📄 RUN_APP.bat                    # Windows launcher
├── 📄 RUN_APP.ps1                    # PowerShell launcher
├── 📄 SETUP.bat                      # Setup batch file
├── 📄 LAUNCH.bat                     # Quick launch batch
├── 📄 LAUNCH_SMS.bat                 # SMS launcher batch
├── 📄 uninstall.bat                  # Uninstaller
├── 📄 version.json                   # Version information
├── 📄 sms_icon.ico                   # Application icon
├── 📄 sms_icon.png                   # PNG icon
└── 📄 school_management.db           # Database file
```

## Important Folders

### 📁 `/database/` - Database Files
```
database/
└── school_management.db         # SQLite database (652 KB)
```
**Contains:** All application data (students, teachers, attendance, fees, grades)

### 📁 `/database_backups/` - Automated Backups
```
database_backups/
├── backup_20251110_*.db         # Timestamped backups
├── backup_20251111_*.db
└── [more backups...]
```
**Contains:** Automatic database backup files

### 📁 `/docs/` - Documentation
```
docs/
├── ATTENDANCE_FIX_DOCUMENTATION.md
├── COMPREHENSIVE_SYNC_DOCUMENTATION.md
├── DATE_PICKER_SCROLLABLE_FORMS_DOCUMENTATION.md
├── SETTINGS_MODULE_DOCUMENTATION.md
├── USER_MANAGEMENT_GUIDE.md
├── CATEGORY_FIX_SUMMARY.md
├── UNIVERSAL_INSTALLER_GUIDE.md
└── [other technical guides...]
```
**Contains:** Technical documentation, guides, and API references

### 📁 `/backups/` - Application Backups
```
backups/
├── sms_backup.py
├── sms_backup_20251026_*.py
├── sms_backup_before_ai_*.py
└── [versioned backups...]
```
**Contains:** Backup copies of main application files

## Organized Folders (Cleanup)

### 📁 `/installers/` - Installation Files
```
installers/
├── GaybeckInstaller.py          # Professional Python installer
├── installer.nsi                # NSIS installer script
├── installer.iss                # Inno Setup installer script
├── INSTALL.bat                  # Batch installer
├── INSTALL_v2.0.3.bat           # Version 2.0.3 installer
├── NEW_INSTALL.bat              # New installation script
└── install_dependencies.bat     # Dependency installer
```
**For:** Legacy installers and setup scripts

### 📁 `/setup-tools/` - Development/Setup Tools
```
setup-tools/
├── create_icon.py               # Icon generator
├── create_shortcut.py           # Shortcut creator
├── test_launch.py               # Application launch tester
└── test_categories.py           # Category feature tester
```
**For:** Development, testing, and setup utilities

### 📁 `/branding/` - Branding & Marketing
```
branding/
├── logo.png                     # Application logo
├── icon.ico                     # Icon file
├── index.html                   # Web page
├── PROMOTIONAL_BROCHURE.md      # Marketing brochure
└── PRICING_TABLE.md             # Pricing information
```
**For:** Branding, marketing materials, and web resources

### 📁 `/documentation-old/` - Archived Documentation
```
documentation-old/
├── 00_START_HERE_FINAL.md
├── INSTALLATION_COMPLETE.md
├── INSTALLER_README.txt
├── INSTALLER_FIX_REPORT.md
├── AUDIT_REPORT_v2.0.3.md
├── AI_FEATURES_DEPLOYMENT_REPORT.md
├── PROJECT_DELIVERY_COMPLETE.md
└── [other archived docs...]
```
**For:** Previous version documentation and deployment reports

## Other Important Folders

### 📁 `/reports/` - Generated Reports
Contains system-generated reports and analytics outputs

### 📁 `/scripts/` - Utility Scripts
Contains utility and helper scripts

### 📁 `/tests/` - Test Files
Contains test cases and test data

### 📁 `/dev-scripts/` - Development Scripts
Contains development, maintenance, and optimization scripts

### 📁 `/teacher_documents/` - Teacher Resources
Contains documents and resources for teachers

### 📁 `/.github/` - GitHub Configuration
Contains GitHub-specific files and workflows

### 📁 `/.venv/` - Virtual Environment
Python virtual environment (can be recreated)

## Quick Navigation

| Need | Location |
|---|---|
| **Install Application** | Run `INSTALL.py` in root |
| **Launch Application** | Double-click `RUN_APP.bat` or run `python sms.py` |
| **View Documentation** | `README.md` in root or `docs/` folder |
| **System Settings** | `Settings` menu in application |
| **Database Backup** | `Settings` → `Backup & Restore` |
| **Database Files** | `database/` folder |
| **Old Installers** | `installers/` folder |
| **Technical Guides** | `docs/` folder |
| **Marketing Materials** | `branding/` folder |

## File Cleanup Summary

✅ **Organized:** 40+ installation/setup files  
✅ **Categorized:** Old documentation archived  
✅ **Streamlined:** Root directory now shows only essential files  
✅ **Professional:** Clean structure for distribution  

## Starting Fresh

To get a fresh copy of the application:

1. **Download/Extract** all files from this directory
2. **Run installer:** `python INSTALL.py`
3. **Launch app:** Double-click `RUN_APP.bat` or run `python sms.py`
4. **Login:** Use default credentials (see `INSTALLATION_GUIDE.md`)

## Backup & Recovery

**To backup your data:**
1. Open Application
2. Go to `Settings` → `Backup & Restore`
3. Click `Create Backup`
4. Save file to safe location

**To restore:**
1. Re-run `INSTALL.py`
2. Open Application
3. Go to `Settings` → `Backup & Restore`
4. Click `Restore from Backup`
5. Select your backup file

---

**Version:** 3.0.0  
**Last Organized:** November 17, 2025  
**Status:** Clean and production-ready ✅

