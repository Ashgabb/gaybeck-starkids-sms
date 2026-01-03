# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller Build Configuration for Gaybeck Starkids SMS
Generates standalone executable for Windows, macOS, and Linux

Usage:
    pyinstaller build_config.spec
"""

block_cipher = None

a = Analysis(
    ['sms.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('logo.png', '.'),
        ('sms_icon.ico', '.'),
        ('database', 'database'),
        ('docs', 'docs'),
    ],
    hiddenimports=[
        'tkinter',
        'tkcalendar',
        'PIL',
        'reportlab',
        'sqlite3',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[],
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
    name='GaybeckStarKidsSMS',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to False for GUI app (no console window)
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='sms_icon.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='GaybeckStarKidsSMS',
)
