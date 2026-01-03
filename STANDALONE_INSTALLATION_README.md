# 📦 Gaybeck Starkids SMS - Standalone Installation

## Overview

This package enables cross-platform standalone installation of Gaybeck Starkids SMS without requiring Python or dependencies to be installed by end-users.

---

## 🚀 Quick Start

### Windows
```bash
# Method 1: Python script (Recommended)
python setup.py build

# Method 2: Batch script
build.bat
```

### macOS / Linux
```bash
# Method 1: Python script (Recommended)
python3 setup.py build

# Method 2: Shell script
chmod +x build.sh
./build.sh
```

---

## 📋 What's Included

| File | Purpose |
|------|---------|
| `setup.py` | Python-based build automation (all platforms) |
| `build.bat` | Windows batch script builder |
| `build.sh` | macOS/Linux shell script builder |
| `build_config.spec` | PyInstaller configuration |
| `installer.nsi` | Windows NSIS installer script |
| `INSTALLATION_GUIDE.md` | Detailed build instructions |

---

## ✨ Features

✅ **Single-Click Installation**
- No Python required for end-users
- Professional installer for Windows
- Simple drag-and-drop for macOS
- Package manager ready for Linux

✅ **Cross-Platform**
- Windows (.exe installer)
- macOS (.dmg or .zip)
- Linux (.tar.gz or .AppImage)

✅ **Production-Ready**
- Includes all dependencies
- Database bundled
- Documentation included
- Icons and branding

✅ **Easy to Build**
- Automated scripts
- One command builds everything
- Clear progress feedback
- Error handling

---

## 📊 Build Specifications

### Build Configuration (`build_config.spec`)

Controls what gets included:
- **Application**: sms.py
- **Assets**: logo.png, sms_icon.ico
- **Database**: database folder
- **Documentation**: docs folder
- **Dependencies**: tkinter, tkcalendar, PIL, reportlab, sqlite3

### Output

**Size**: 200-250 MB per platform
**Format**: 
- Windows: `.exe` installer or standalone `.exe`
- macOS: `.app` bundle or `.dmg`
- Linux: `.tar.gz` archive or `.AppImage`

---

## 🔧 Installation Methods

### Method 1: Python Script (Easiest)
```bash
python setup.py build
```

**Advantages:**
- Cross-platform (same command everywhere)
- Automatic dependency installation
- Built-in error handling
- Progress feedback

### Method 2: Platform-Specific Scripts

**Windows:**
```bash
build.bat
```

**macOS/Linux:**
```bash
./build.sh
```

### Method 3: Manual PyInstaller
```bash
# Install PyInstaller
pip install pyinstaller>=6.0

# Build
pyinstaller build_config.spec --onedir
```

---

## 📦 Creating Installers

### Windows Installer (.exe)

**Using NSIS (Professional):**

1. Install NSIS: https://nsis.sourceforge.io
2. Right-click `installer.nsi` → "Compile NSIS Script"
3. Creates: `GaybeckStarKidsSMS_Installer_2.0.3.exe`

**Using build script:**
```bash
build.bat
```

### macOS Package (.dmg)

```bash
# Create DMG file
hdiutil create -volname "Gaybeck Starkids SMS" \
  -srcfolder dist/GaybeckStarKidsSMS \
  -ov -format UDZO GaybeckStarKidsSMS.dmg
```

### Linux Package

```bash
# Create AppImage
linuxdeploy-x86_64.AppImage --appdir dist/GaybeckStarKidsSMS --output appimage
```

---

## 📁 Output Structure

After building, you'll have:

```
dist/
├── GaybeckStarKidsSMS/          ← Standalone application
│   ├── GaybeckStarKidsSMS.exe   (Windows)
│   ├── GaybeckStarKidsSMS       (macOS/Linux)
│   ├── database/                ← Bundled database
│   ├── docs/                    ← Documentation
│   └── _internal/               ← Dependencies
│
├── GaybeckStarKidsSMS_Windows_*.zip   ← Distribution package
├── GaybeckStarKidsSMS_macOS_*.zip     ← Distribution package
└── GaybeckStarKidsSMS_linux_*.tar.gz  ← Distribution package
```

---

## 🎯 Distribution Guide

### For Your Website

1. **Windows Users:**
   - Direct download of `.exe` installer
   - Or self-contained `.exe` application

2. **macOS Users:**
   - Download `.dmg` file
   - Drag app to Applications folder

3. **Linux Users:**
   - Download `.tar.gz` file
   - Extract and run executable

### For App Stores

**Windows (Microsoft Store):**
```bash
# Requirements: .msix package
# Use: Windows App Packaging Tool
```

**macOS (Mac App Store):**
```bash
# Requirements: Notarization + signing
# Use: Xcode + Application Loader
```

**Linux (Snap Store):**
```bash
# Create snapcraft.yaml
snapcraft
snap push *.snap --release=stable
```

---

## 🔐 Security

### Code Signing (Recommended)

**Windows:**
```bash
# Sign executable
signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com GaybeckStarKidsSMS.exe
```

**macOS:**
```bash
# Sign app
codesign --deep --force --verify --verbose --sign "Developer ID Application" \
  dist/GaybeckStarKidsSMS/GaybeckStarKidsSMS
```

### Virus Scanning

Before distribution:
1. Scan with antivirus (VirusTotal.com)
2. Sign executables
3. Use HTTPS for downloads
4. Provide SHA256 checksums

---

## 📊 Build Statistics

| Metric | Value |
|--------|-------|
| Build Time | 2-3 minutes |
| Executable Size | 200-250 MB |
| Python Required | No (for end-users) |
| Dependencies Bundled | Yes |
| Database Included | Yes |
| Documentation Included | Yes |
| First-Time Setup | ~5 minutes |

---

## 🐛 Troubleshooting

### Build Fails on Windows
```bash
# Run as Administrator
# Or: Use full Python path
C:\Python313\python.exe setup.py build
```

### Permission Denied on macOS/Linux
```bash
# Make scripts executable
chmod +x build.sh setup.py
```

### PyInstaller Not Found
```bash
# Install it
pip install pyinstaller>=6.0

# Or: Use setup.py (auto-installs)
python setup.py build
```

### Build Takes Too Long
- First build: 2-3 minutes (normal)
- If >5 minutes: Clean and retry
  ```bash
  python setup.py clean
  python setup.py build
  ```

### Database Not Bundled
Check `build_config.spec`:
```python
datas=[
    ('database', 'database'),  # Must be present
]
```

### Icon Not Showing
Ensure `sms_icon.ico` exists in root:
```bash
ls sms_icon.ico  # Check file exists
```

---

## 🚀 Advanced Options

### Build Single File (.exe)
```bash
pyinstaller build_config.spec --onefile
```
**Note:** Slower startup time, larger file

### With Splash Screen
```bash
pyinstaller build_config.spec --splash splash.png
```

### With Console Window
Edit `build_config.spec`:
```python
console=True  # Change from False
```

### Custom Installation Path
Edit `installer.nsi`:
```nsis
InstallDir "$PROGRAMFILES\CustomPath"
```

---

## 📚 Additional Resources

- **PyInstaller Docs**: https://pyinstaller.org
- **NSIS Guide**: https://nsis.sourceforge.io/Docs/
- **Code Signing**: https://docs.microsoft.com/en-us/windows/win32/seccodeauth/code-signing
- **DMG Creation**: https://support.apple.com/en-us/HT308686

---

## 🎯 Next Steps

1. ✅ **Build**: Run `python setup.py build`
2. ✅ **Test**: Run the executable on target OS
3. ✅ **Package**: Create installer for distribution
4. ✅ **Sign**: Code sign for trust
5. ✅ **Distribute**: Upload to website or app store
6. ✅ **Support**: Provide installation help docs

---

## 📞 Support

- **Email**: support@gaybeckstarkids.com
- **Issues**: https://github.com/Ashgabb/gaybeck-starkids-sms/issues
- **Guide**: See `INSTALLATION_GUIDE.md`

---

**Version**: 2.0.3  
**Status**: Production Ready  
**Last Updated**: January 3, 2026
