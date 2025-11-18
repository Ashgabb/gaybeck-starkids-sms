#!/usr/bin/env python3
"""
Create shortcut with proper icon for taskbar visibility
"""
import os
import sys
from pathlib import Path

# Add Python to path for shortcuts
python_exe = sys.executable

# Get paths
app_dir = Path(__file__).parent
desktop = Path.home() / 'Desktop'
shortcut_path = desktop / 'Gaybeck Starkids SMS.lnk'
icon_path = app_dir / 'sms_icon.ico'
batch_path = app_dir / 'RUN_APP.bat'

# Verify files exist
if not icon_path.exists():
    print(f"[ERROR] Icon not found: {icon_path}")
    sys.exit(1)

if not batch_path.exists():
    print(f"[ERROR] Batch file not found: {batch_path}")
    sys.exit(1)

# Delete old shortcut
if shortcut_path.exists():
    shortcut_path.unlink()
    print(f"[OK] Removed old shortcut")

# Create shortcut using PowerShell
ps_script = f'''
$WshShell = New-Object -ComObject WScript.Shell
$shortcut = $WshShell.CreateShortcut('{shortcut_path}')
$shortcut.TargetPath = '{batch_path}'
$shortcut.WorkingDirectory = '{app_dir}'
$shortcut.IconLocation = '{icon_path},0'
$shortcut.Description = 'Gaybeck Starkids School Management System'
$shortcut.WindowStyle = 1
$shortcut.Save()
Write-Host '[OK] Shortcut created with icon'
'''

# Execute PowerShell script
import subprocess
result = subprocess.run(['powershell', '-Command', ps_script], capture_output=True, text=True)

print(result.stdout)
if result.stderr:
    print(f"[WARNING] {result.stderr}")

# Verify shortcut was created
if shortcut_path.exists():
    print(f"[OK] Shortcut verified: {shortcut_path}")
    print(f"[OK] Icon path: {icon_path}")
    print()
    print("Next steps:")
    print("1. Right-click the shortcut on desktop")
    print("2. Select 'Properties'")
    print("3. Click 'Change Icon'")
    print("4. Browse to: sms_icon.ico in the app folder")
    print("5. Click OK twice")
    print()
    print("Or try:")
    print("- Refresh desktop (F5)")
    print("- Clear icon cache and restart")
else:
    print("[ERROR] Shortcut creation failed")
    sys.exit(1)
