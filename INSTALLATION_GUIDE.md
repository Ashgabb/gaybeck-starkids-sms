# Gaybeck Starkids SMS - Installation Guide

## 🚀 Cross-Platform Installation

This guide covers how to create standalone installation files for Windows, macOS, and Linux.

---

## Prerequisites

### All Platforms:
- **Python 3.13+** (Download from https://www.python.org)
- **pip** (comes with Python)
- **git** (optional, for version control)

### Windows Only:
- **NSIS** (for Windows installer) - Download from https://nsis.sourceforge.io
- **Administrator privileges** (for installation)

### macOS:
- **Xcode Command Line Tools** (run: `xcode-select --install`)

### Linux:
- **Build essentials** (run: `sudo apt-get install build-essential python3-dev`)

---

## Quick Start

### Windows

1. **Open Command Prompt** and navigate to the project:
```bash
cd C:\Users\YourUsername\Desktop\gaybeck-starkids-sms
```

2. **Run the build script**:
```bash
build.bat
```

3. **Wait for completion** (2-3 minutes)

4. **Find the executable**:
```
dist\GaybeckStarKidsSMS\GaybeckStarKidsSMS.exe
```

### macOS / Linux

1. **Open Terminal** and navigate to the project:
```bash
cd ~/Desktop/gaybeck-starkids-sms
```

2. **Make script executable**:
```bash
chmod +x build.sh
```

3. **Run the build script**:
```bash
./build.sh
```

4. **Find the executable**:
```
dist/GaybeckStarKidsSMS/GaybeckStarKidsSMS
```

---

## Detailed Build Process

### Step 1: Install Dependencies

```bash
# Python 3.13+ must be installed first!
python --version  # or python3 --version on Mac/Linux

# Install PyInstaller
pip install pyinstaller>=6.0

# Install application requirements
pip install -r requirements.txt
```

### Step 2: Build Executable

#### Windows:
```bash
pyinstaller build_config.spec --onedir
```

#### macOS/Linux:
```bash
pyinstaller build_config.spec --onedir
```

### Step 3: Verify Build

The executable will be in:
- **Windows**: `dist/GaybeckStarKidsSMS/GaybeckStarKidsSMS.exe`
- **macOS**: `dist/GaybeckStarKidsSMS/GaybeckStarKidsSMS`
- **Linux**: `dist/GaybeckStarKidsSMS/GaybeckStarKidsSMS`

---

## Creating Installers

### Windows Installer (.exe)

1. **Install NSIS** from https://nsis.sourceforge.io
2. **Right-click `installer.nsi`** → "Compile NSIS Script"
3. Or use command line:
```bash
"C:\Program Files (x86)\NSIS\makensis.exe" installer.nsi
```

This creates: `GaybeckStarKidsSMS_Installer_2.0.3.exe`

### macOS Package (.dmg)

```bash
# Create DMG file
hdiutil create -volname "Gaybeck Starkids SMS" \
  -srcfolder dist/GaybeckStarKidsSMS \
  -ov -format UDZO GaybeckStarKidsSMS.dmg
```

### Linux Package (.tar.gz)

```bash
# Create compressed archive
cd dist
tar -czf GaybeckStarKidsSMS_linux.tar.gz GaybeckStarKidsSMS/
cd ..
```

---

## Manual Build Steps (Without Scripts)

If the scripts don't work, follow these steps manually:

### 1. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install --upgrade pip
pip install pyinstaller>=6.0
pip install -r requirements.txt
```

### 3. Build with PyInstaller
```bash
pyinstaller build_config.spec --onedir
```

### 4. Verify
```bash
# Windows
dist\GaybeckStarKidsSMS\GaybeckStarKidsSMS.exe

# macOS/Linux
dist/GaybeckStarKidsSMS/GaybeckStarKidsSMS
```

---

## Build Configuration Explained

The `build_config.spec` file controls the build process:

```python
# Files to include in build
datas=[
    ('logo.png', '.'),           # App logo
    ('sms_icon.ico', '.'),        # App icon
    ('database', 'database'),     # Database folder
    ('docs', 'docs'),             # Documentation
]

# Hidden imports for PyInstaller
hiddenimports=[
    'tkinter',
    'tkcalendar',
    'PIL',
    'reportlab',
    'sqlite3',
]

# Build as GUI app (no console window)
console=False
```

---

## Distribution File Sizes

Expected sizes after build:

| Platform | Size | Format |
|----------|------|--------|
| Windows | ~200-250 MB | .exe or installer |
| macOS | ~200-250 MB | .dmg or .zip |
| Linux | ~200-250 MB | .tar.gz or .AppImage |

---

## Troubleshooting

### Issue: "Python not found"
**Solution**: Add Python to PATH or use full path:
```bash
C:\Python313\python.exe build.bat
```

### Issue: "PyInstaller not found"
**Solution**: Install it:
```bash
pip install pyinstaller>=6.0
```

### Issue: "Permission denied" on macOS/Linux
**Solution**: Make script executable:
```bash
chmod +x build.sh
```

### Issue: Build hangs or takes too long
**Solution**: The first build takes 2-3 minutes. Be patient. If it hangs for >5 minutes:
1. Press Ctrl+C to stop
2. Clean: `rm -rf build dist`
3. Try again

### Issue: "Icon file not found"
**Solution**: Ensure `sms_icon.ico` exists in the root directory:
```bash
ls sms_icon.ico  # or: dir sms_icon.ico on Windows
```

### Issue: Database not included in build
**Solution**: Check `build_config.spec` has:
```python
datas=[
    ('database', 'database'),
]
```

### Issue: "Tkinter not found"
**Solution**: Install tkinter:
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# macOS - should be included with Python
```

---

## Advanced Options

### Build Single Executable (Larger file, easier distribution)
```bash
pyinstaller --onefile build_config.spec
```

### Build with Console (for debugging)
Edit `build_config.spec`:
```python
console=True  # Change from False
```

### Add Splash Screen
```bash
pyinstaller --splash splash.png build_config.spec
```

### Sign Executable (macOS)
```bash
codesign --deep --force --verify --verbose --sign "Developer ID Application" \
  dist/GaybeckStarKidsSMS/GaybeckStarKidsSMS
```

---

## Distribution Checklist

Before distributing, verify:

- [ ] Executable runs on target OS without errors
- [ ] All features work (database, reports, printing)
- [ ] Icons display correctly
- [ ] Shortcuts/desktop icons work
- [ ] Uninstall works properly
- [ ] No missing dependencies
- [ ] Performance is acceptable
- [ ] File size is reasonable
- [ ] Antivirus doesn't flag executable
- [ ] Version number is correct

---

## Deployment Options

### Option 1: Direct Download
- Host `.exe`, `.dmg`, `.tar.gz` on website
- Users download and run installer
- Simplest distribution method

### Option 2: Package Managers

**Windows** (Chocolatey):
```bash
# Create package and submit
choco pack
choco push GaybeckStarKidsSMS.nupkg
```

**macOS** (Homebrew):
```bash
# Submit formula to Homebrew
```

**Linux** (Snap):
```bash
# Create snap package
snapcraft
snap push gaybeck-starkids-sms_2.0.3_amd64.snap --release=stable
```

### Option 3: Self-Updating App
Add auto-update functionality to check for new versions.

---

## Security Considerations

1. **Sign executables** (Windows SmartScreen, macOS Gatekeeper)
2. **Use HTTPS** for downloads
3. **Verify checksums** (SHA256)
4. **Scan with antivirus** before distribution
5. **Keep dependencies updated** for security patches
6. **Use code signing certificates** for trust

---

## Build Statistics

- **Build Time**: 2-3 minutes
- **Executable Size**: ~200-250 MB
- **Dependencies**: 15-20 packages
- **Python Version**: 3.13+
- **Supported OS**: Windows 7+, macOS 10.13+, Linux (most distributions)

---

## Next Steps

1. ✅ Run build script (`build.bat` or `build.sh`)
2. ✅ Test executable on target platform
3. ✅ Create installer (NSIS for Windows)
4. ✅ Package for distribution
5. ✅ Host on website or app stores
6. ✅ Document installation instructions for users

---

## Support

For issues or questions:
- Email: support@gaybeckstarkids.com
- GitHub Issues: https://github.com/Ashgabb/gaybeck-starkids-sms/issues
- Documentation: See `/docs` folder

---

**Version**: 2.0.3  
**Last Updated**: January 3, 2026  
**Status**: Production Ready
