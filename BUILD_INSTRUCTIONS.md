# Build Instructions for School Management System

## Overview
This document provides instructions for building a standalone executable from the School Management System Python application.

## Prerequisites

### Required Software
1. **Python 3.13** (installed and working)
2. **PyInstaller** (for building executables)
3. **All application dependencies** (from requirements.txt)

### Install Build Tools
```bash
pip install pyinstaller
```

## Build Steps

### Option 1: Using PyInstaller (Recommended)

1. **Install PyInstaller**:
   ```bash
   pip install pyinstaller
   ```

2. **Create the executable**:
   ```bash
   pyinstaller --name="SchoolManagementSystem" ^
               --onefile ^
               --windowed ^
               --icon=icon.ico ^
               --add-data="database;database" ^
               --add-data="docs;docs" ^
               --hidden-import=sklearn.utils._weight_vector ^
               --hidden-import=sklearn.neighbors._partition_nodes ^
               --collect-all=sklearn ^
               --collect-all=tkcalendar ^
               sms.py
   ```

3. **Build output** will be in `dist/` folder

### Option 2: Simplified Build (No AI features)

If scikit-learn causes build issues, use this simplified version:

```bash
pyinstaller --name="SchoolManagementSystem" ^
            --onefile ^
            --windowed ^
            --icon=icon.ico ^
            --add-data="database;database" ^
            sms.py
```

## Build Specification File

Create `sms.spec` file for custom build:

```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['sms.py'],
    pathex=[],
    binaries=[],
    datas=[('database', 'database'), ('docs', 'docs')],
    hiddenimports=[
        'sklearn.utils._weight_vector',
        'sklearn.neighbors._partition_nodes',
        'tkcalendar',
        'PIL._tkinter_finder'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SchoolManagementSystem',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico'
)
```

Then build with:
```bash
pyinstaller sms.spec
```

## Post-Build Steps

1. **Test the executable**:
   - Run `dist/SchoolManagementSystem.exe`
   - Test all major features
   - Verify database connectivity
   - Check AI features (if included)

2. **Create distribution package**:
   ```
   SchoolManagementSystem-v2.0/
   ├── SchoolManagementSystem.exe
   ├── database/
   │   └── school_management.db
   ├── docs/
   │   └── [documentation files]
   ├── README.md
   └── LICENSE.txt
   ```

3. **Compress for distribution**:
   - Zip the entire folder
   - Create installer using Inno Setup (optional)

## Troubleshooting Build Issues

### Issue: "Module not found" errors
**Solution**: Add missing modules to `hiddenimports` in spec file

### Issue: Large executable size
**Solution**: 
- Use `--exclude-module` for unused packages
- Consider using `--onedir` instead of `--onefile`

### Issue: Database not found
**Solution**: Ensure database is included in `--add-data` parameter

### Issue: AI features don't work in built version
**Solution**: Include all sklearn dependencies:
```bash
--collect-all sklearn --collect-all pandas --collect-all numpy
```

## Distribution Checklist

- [ ] Executable tested on clean Windows machine
- [ ] All features working (students, teachers, attendance, fees, grades)
- [ ] AI features functional (if included)
- [ ] Database operations working
- [ ] Reports generating correctly
- [ ] Backup/restore functional
- [ ] README.md included
- [ ] Sample database included (optional)
- [ ] Installation instructions provided

## Creating an Installer (Optional)

Use **Inno Setup** to create professional installer:

1. Download Inno Setup: https://jrsoftware.org/isdl.php
2. Create install script (`setup.iss`)
3. Build installer

## File Size Expectations

- **With AI**: ~150-250 MB (includes sklearn, pandas, numpy)
- **Without AI**: ~50-80 MB (basic features only)
- **Installer**: Add ~20% for compression

## Notes

- **Python 3.14 is NOT compatible** - use Python 3.13
- Test on target systems before mass deployment
- Include all required Visual C++ redistributables if needed
- Consider code signing for professional deployment

## Support

For build issues, check:
1. PyInstaller documentation
2. Hidden imports requirements
3. Data file paths
4. Console mode for debugging

---

**Last Updated:** November 10, 2025
