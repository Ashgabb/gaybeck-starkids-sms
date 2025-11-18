================================================================================
                GAYBECK STARKIDS SMS - INSTALLATION GUIDE
                           Version 3.0.0
================================================================================

WELCOME! This folder contains everything you need to install the professional
Gaybeck Starkids School Management System on your Windows computer.

================================================================================
                          QUICK START (30 SECONDS)
================================================================================

FOR MOST USERS: Simply double-click SETUP.bat

  Step 1: Double-click SETUP.bat
  Step 2: Click "Yes" when Windows asks for permission
  Step 3: Follow the on-screen prompts
  Step 4: Done! Your desktop will have a shortcut

================================================================================
                        INSTALLATION FILES INCLUDED
================================================================================

1. SETUP.bat
   - Easy installer launcher (RECOMMENDED)
   - Handles admin permissions automatically
   - Perfect for first-time users

2. GaybeckInstaller.py
   - Professional Python installer
   - Full version detection and management
   - Use if SETUP.bat doesn't work

3. installer.nsi
   - Traditional NSIS installer script
   - Creates standard Windows .exe installer
   - For users who prefer traditional setup

4. requirements.txt
   - Lists all Python dependencies
   - Used by installer automatically

5. This file (INSTALLER_README.txt)
   - Quick reference guide

================================================================================
                          SYSTEM REQUIREMENTS
================================================================================

MANDATORY:
  • Windows 10 or Windows 11
  • Python 3.13+ (installer will verify)
  • 4 GB RAM minimum
  • 2 GB free disk space
  • Internet connection (for downloading dependencies)

RECOMMENDED:
  • Windows 11 (latest)
  • 8 GB RAM
  • SSD disk (faster installation)
  • High-speed internet

OPTIONAL:
  • PyWin32 (for enhanced shortcut support)
  • Visual C++ Build Tools (auto-installed if needed)

================================================================================
                        THREE WAYS TO INSTALL
================================================================================

METHOD 1: SETUP.bat (EASIEST - Recommended for most users)
────────────────────────────────────────────────────────

  Step 1: Right-click SETUP.bat
  Step 2: Select "Run as Administrator" OR just double-click
  Step 3: Wait for installation to complete (5-15 minutes)
  Step 4: A desktop shortcut will be created automatically
  Step 5: Double-click the shortcut to launch the application

  Pros:
    ✓ Easiest method
    ✓ Handles admin permissions automatically
    ✓ No additional software needed
    ✓ Best for Windows 10/11

  Cons:
    ✗ Command window may be confusing for some users


METHOD 2: GaybeckInstaller.py (DIRECT PYTHON - Best if SETUP.bat fails)
─────────────────────────────────────────────────────────────────────

  Step 1: Open Command Prompt as Administrator
    • Press Windows key + R
    • Type: cmd
    • Press Ctrl+Shift+Enter (or right-click → Run as Administrator)

  Step 2: Navigate to the installer folder
    • Type: cd "C:\Users\[YourName]\Desktop\GAYBECK STARKIDS SMS"
    • Replace [YourName] with your actual username

  Step 3: Run the installer
    • Type: python GaybeckInstaller.py
    • Wait for installation to complete

  Step 4: Follow the on-screen prompts
    • You may need to choose "Upgrade" or "Clean Install"

  Pros:
    ✓ Full control over installation
    ✓ Better error messages
    ✓ Can manually resolve issues

  Cons:
    ✗ Requires command line knowledge
    ✗ Takes longer


METHOD 3: Traditional NSIS Installer (CLASSIC - If you prefer .exe)
───────────────────────────────────────────────────────────────────

  Step 1: Install NSIS (if not already installed)
    • Download from: https://nsis.sourceforge.io
    • Run the NSIS installer
    • Accept all defaults

  Step 2: Compile the installer script
    • Open Command Prompt as Administrator
    • Navigate to this folder
    • Type: "C:\Program Files (x86)\NSIS\makensis.exe" installer.nsi

  Step 3: Run the generated .exe
    • A file named Gaybeck_Starkids_SMS_v3.0.0_Setup.exe will be created
    • Double-click it to run the traditional Windows installer

  Step 4: Follow the installation wizard

  Pros:
    ✓ Familiar Windows installer experience
    ✓ Professional appearance
    ✓ Standard install/uninstall workflow

  Cons:
    ✗ Requires NSIS to be installed
    ✗ More complex process


================================================================================
                      WHAT GETS INSTALLED (v3.0.0)
================================================================================

The installer will:

  ✓ Create installation folder: C:\Program Files\Gaybeck Starkids SMS\

  ✓ Install Application Files:
    - Main application (sms.py)
    - AI analytics module (advanced_ai_analytics.py)
    - Database schema
    - All documentation
    - Icons and logos

  ✓ Install Python Dependencies:
    - scikit-learn 1.7.2 (Machine Learning)
    - pandas 2.3.3 (Data Analysis)
    - numpy 2.2.6 (Numerical Computing)
    - scipy 1.16.3 (Scientific Computing)
    - tkcalendar 1.6.1 (Date Picker)
    - reportlab 4.4.5 (PDF Generation)
    - pillow 12.0.0 (Image Processing)
    - opencv-python 4.12.0.88 (Computer Vision)
    - And supporting libraries

  ✓ Create Shortcuts:
    - Desktop shortcut (for quick launch)
    - Start Menu folder (in Programs)
    - Taskbar pin (optional)

  ✓ Register in Windows:
    - For clean uninstall
    - For version detection
    - For upgrade support

TOTAL TIME: 10-15 minutes (first install)
            5-10 minutes (upgrade from previous version)

================================================================================
                        TROUBLESHOOTING
================================================================================

PROBLEM: "Python is not installed"
──────────────────────────────────
SOLUTION:
  1. Download Python 3.13+ from https://www.python.org/downloads
  2. Run the Python installer
  3. IMPORTANT: Check "Add Python to PATH" during installation
  4. Restart your computer
  5. Try running SETUP.bat again


PROBLEM: "Access Denied" or "You don't have permission"
───────────────────────────────────────────────────────
SOLUTION:
  1. Right-click SETUP.bat or GaybeckInstaller.py
  2. Select "Run as Administrator"
  3. Click "Yes" when Windows asks for permission
  4. Try again


PROBLEM: Installation hangs or takes too long
──────────────────────────────────────────────
SOLUTION:
  1. Check your internet connection
  2. Installer is downloading dependencies (this takes time)
  3. Wait at least 10 minutes before canceling
  4. If still stuck, close and try again


PROBLEM: Shortcuts don't appear after installation
──────────────────────────────────────────────────
SOLUTION:
  1. Check your Desktop for "Gaybeck Starkids SMS" icon
  2. Check Start Menu → Programs → Gaybeck Starkids SMS
  3. If missing, create manually:
     - Right-click on sms.py
     - Select "Create shortcut"
     - Move it to Desktop


PROBLEM: Application won't launch after installation
────────────────────────────────────────────────────
SOLUTION:
  1. Open Command Prompt as Administrator
  2. Navigate to: C:\Program Files\Gaybeck Starkids SMS
  3. Run: .venv\Scripts\python.exe sms.py
  4. Look for error messages
  5. Report the error if you can't fix it


PROBLEM: "pip install" fails or downloads are slow
──────────────────────────────────────────────────
SOLUTION:
  1. Check your internet connection
  2. Try again later (pip servers may be slow)
  3. For faster downloads, try:
     - Using ethernet instead of WiFi
     - Closing other internet applications
     - Running installer during off-peak hours


PROBLEM: "Virtual environment creation failed"
───────────────────────────────────────────────
SOLUTION:
  1. Make sure you have 2GB+ free disk space
  2. Ensure C:\Program Files\ is writable
  3. Try installing to a different location
  4. Restart your computer and try again


PROBLEM: Administrator password required
─────────────────────────────────────────
SOLUTION:
  1. This is normal - installation needs admin rights
  2. Enter your Windows password when prompted
  3. Don't have admin rights? Contact your IT department


MORE HELP:
──────────
  • Check documentation: docs/INSTALLER_GUIDE.md
  • Read troubleshooting: docs/INSTALLATION_FIX_SUMMARY.md
  • See launch guide: LAUNCH_GUIDE.md
  • Review README.md for overview

================================================================================
                          FIRST-TIME SETUP
================================================================================

After installation completes:

  1. LAUNCH THE APPLICATION
     • Double-click desktop shortcut
     • Or: Start Menu → Programs → Gaybeck Starkids SMS

  2. LOGIN
     • Default username: admin
     • Default password: admin123
     • IMPORTANT: Change password after first login!

  3. CONFIGURE SCHOOL INFO
     • School name
     • Academic year
     • Terms/semesters
     • Classes and grades

  4. ADD USERS
     • Teachers
     • Accountants
     • Other staff members

  5. IMPORT STUDENT DATA
     • Add students manually, or
     • Import from CSV file

  6. EXPLORE AI FEATURES
     • Click "🤖 AI Insights" in the menu
     • Try each of the 10 AI features
     • Generate reports

================================================================================
                            UNINSTALLING
================================================================================

To remove the application:

METHOD 1: Using Uninstall.bat
──────────────────────────────
  1. Open File Explorer
  2. Navigate to: C:\Program Files\Gaybeck Starkids SMS\
  3. Double-click Uninstall.bat
  4. Confirm removal
  5. Application will be removed

METHOD 2: Using Windows Settings
─────────────────────────────────
  1. Go to Settings → Apps → Installed Apps
  2. Search for "Gaybeck Starkids SMS"
  3. Click it and select "Uninstall"
  4. Confirm removal

METHOD 3: Manual Removal
────────────────────────
  1. Delete folder: C:\Program Files\Gaybeck Starkids SMS\
  2. Delete shortcut: C:\Users\[YourName]\Desktop\Gaybeck Starkids SMS.lnk
  3. Delete Start Menu: C:\Users\[YourName]\AppData\Microsoft\Windows\Start Menu\Programs\Gaybeck Starkids SMS\

================================================================================
                        ADDITIONAL RESOURCES
================================================================================

Documentation Files (in docs/ folder):

  • INSTALLER_GUIDE.md
    Comprehensive installation guide with screenshots

  • LAUNCH_GUIDE.md
    How to start the application

  • AI_FEATURES_GUIDE.md
    Complete guide to all 10 AI features

  • AI_QUICK_REFERENCE.md
    Quick start for using AI features

  • README.md
    General overview of the application

  • USER_MANAGEMENT_GUIDE.md
    How to manage users and permissions

  • COMPREHENSIVE_SYNC_DOCUMENTATION.md
    Database synchronization details

  • And many more...

================================================================================
                         VERSION INFORMATION
================================================================================

Current Version: 3.0.0
Released: November 17, 2025
Status: Production Ready

What's New in v3.0.0:
  ✓ 10 Advanced AI Features
  ✓ Professional Installer
  ✓ Automatic Dependency Installation
  ✓ Version Detection & Upgrade
  ✓ Enhanced Shortcuts
  ✓ Registry Integration

Python Required: 3.13+
Windows: 10 or 11
Database: SQLite3

================================================================================
                            GETTING HELP
================================================================================

If you need help:

  1. Check the documentation (see above)
  2. Review the TROUBLESHOOTING section above
  3. Check INSTALLER_GUIDE.md for detailed steps
  4. See LAUNCH_GUIDE.md if app won't start
  5. Contact support (email provided in docs)

Common Issues:
  • Python not found → Install Python 3.13+
  • Permission denied → Run as Administrator
  • Installation hangs → Check internet connection
  • Shortcut missing → Create manually
  • App won't launch → Check error message in console

================================================================================
                        IMPORTANT NOTES
================================================================================

✓ BACKUP YOUR DATA
  Before upgrading, backup your database:
  C:\Program Files\Gaybeck Starkids SMS\database\school_management.db

✓ INTERNET REQUIRED
  Installation needs internet to download dependencies

✓ ADMIN RIGHTS NEEDED
  Installation requires administrator privileges

✓ PYTHON 3.13+ ONLY
  This version requires Python 3.13+
  If you have Python 3.12 or lower, upgrade first!

✓ WINDOWS ONLY (for now)
  This installer is for Windows only
  Mac/Linux users can run Python directly (advanced users only)

✓ VIRTUAL ENVIRONMENT
  Application installs in isolated Python environment
  This keeps system Python clean

================================================================================
                            QUICK REFERENCE
================================================================================

Installation folder:    C:\Program Files\Gaybeck Starkids SMS\
Database location:      database\school_management.db
Documentation:          docs\ (42 files)
Uninstall:             Uninstall.bat or Windows Settings

Launch shortcut:        Desktop (after installation)
Default login:          admin / admin123
First action:           Change your password!

AI Features:            🤖 AI Insights menu (10 features available)
Reports:                📝 AI Reports menu
Settings:               ⚙️ Settings menu
Help:                   ? Help menu (in app)

================================================================================

                      🎉 READY TO INSTALL? 🎉

                      JUST DOUBLE-CLICK: SETUP.bat

                    Questions? See documentation files above.

================================================================================

Thank you for choosing Gaybeck Starkids SMS!

Version 3.0.0 - Production Ready - November 17, 2025

================================================================================
