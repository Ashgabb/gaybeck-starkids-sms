# -*- mode: python ; coding: utf-8 -*-
# PyInstaller Spec File for School Management System
# Build Date: November 10, 2025
# Version: 2.0.0

block_cipher = None

a = Analysis(
    ['sms.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('database', 'database'),
        ('docs', 'docs'),
        ('version.json', '.'),
        ('README.md', '.'),
    ],
    hiddenimports=[
        # Tkinter and related
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'tkinter.scrolledtext',
        
        # Date picker
        'tkcalendar',
        
        # Image processing
        'PIL',
        'PIL._tkinter_finder',
        'PIL.Image',
        'PIL.ImageTk',
        
        # PDF generation
        'reportlab',
        'reportlab.pdfgen',
        'reportlab.lib',
        
        # Database
        'sqlite3',
        
        # AI/ML (optional - comment out if not using)
        'sklearn',
        'sklearn.utils._weight_vector',
        'sklearn.neighbors._partition_nodes',
        'sklearn.tree',
        'sklearn.ensemble',
        'pandas',
        'numpy',
        
        # Standard library
        'datetime',
        'json',
        'os',
        'sys',
        'threading',
        'pathlib',
        'csv',
        'shutil',
        'zipfile',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude unnecessary packages to reduce size
        'matplotlib',
        'scipy',
        'IPython',
        'jupyter',
        'notebook',
        'pytest',
        'setuptools',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Collect all required data for sklearn
a.datas += Tree('C:\\Users\\USER\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\site-packages\\sklearn',
                prefix='sklearn', excludes=['*.pyc', '__pycache__'])

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
    console=False,  # Set to True for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None  # Add 'icon.ico' if you have an icon file
)

# Optionally create a directory-based distribution (smaller file, faster startup)
# Uncomment the following to use --onedir mode instead of --onefile:

# coll = COLLECT(
#     exe,
#     a.binaries,
#     a.zipfiles,
#     a.datas,
#     strip=False,
#     upx=True,
#     upx_exclude=[],
#     name='SchoolManagementSystem'
# )
