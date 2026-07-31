# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

project_root = Path.cwd()


def build_datas(root: Path):
    datas = []

    # Include all top-level Python modules used by the desktop app.
    for py_file in root.glob('*.py'):
        datas.append((str(py_file), '.'))

    # Include runtime configuration and launcher assets.
    for file_name in [
        'requirements.txt',
        'setup.bat',
        'run_app.bat',
        'launch_app.py',
        'run_app.py',
        'launch_sms.bat',
        'sms_launcher.bat',
        'version.json',
        'logo.png',
        'sms_icon.ico',
    ]:
        file_path = root / file_name
        if file_path.exists():
            datas.append((str(file_path), '.'))

    # Include data directories required at runtime.
    for dir_name in [
        'database',
        'docs',
        'scripts',
        'tests',
        'biometric_data',
        'teacher_documents',
        'web_app',
    ]:
        dir_path = root / dir_name
        if not dir_path.exists():
            continue
        for item in dir_path.rglob('*'):
            if item.is_file():
                rel_dest = str(item.parent.relative_to(root))
                datas.append((str(item), rel_dest))

    return datas


datas = build_datas(project_root)


a = Analysis(
    ['installer.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=['tkinter'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Gaybeck_SMS_Setup_v2.0',
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
    icon=['sms_icon.ico'],
)
