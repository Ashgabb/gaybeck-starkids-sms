#!/usr/bin/env python3
"""
Desktop Shortcut Creator for Gaybeck Starkids SMS
Automatically creates working desktop shortcuts on Windows with icon
"""

import os
import sys
from pathlib import Path

def create_desktop_shortcut():
    """Create a working Windows desktop shortcut with pythonw"""
    try:
        import win32com.client
    except ImportError:
        print("[!] pywin32 not installed. Using PowerShell method...")
        return create_shortcut_powershell()
    
    try:
        shell = win32com.client.Dispatch("WScript.Shell")
        desktop = Path(os.environ['USERPROFILE']) / 'Desktop'
        shortcut_path = desktop / 'Gaybeck Starkids SMS.lnk'
        
        app_dir = Path(__file__).parent
        run_app = app_dir / 'RUN_APP.bat'
        
        # Try to find a custom icon
        icon_path = app_dir / 'sms_icon.ico'
        if not icon_path.exists():
            icon_path = app_dir / 'sms_icon.png'
        if not icon_path.exists():
            icon_path = Path('C:\\Windows\\System32\\python.exe')
        
        shortcut = shell.CreateShortCut(str(shortcut_path))
        shortcut.TargetPath = str(run_app)
        shortcut.WorkingDirectory = str(app_dir)
        shortcut.Description = 'Gaybeck Starkids School Management System'
        shortcut.WindowStyle = 1  # Normal window (starts minimized due to pythonw)
        shortcut.IconLocation = str(icon_path)
        shortcut.save()
        
        print(f"[OK] Desktop shortcut created: {shortcut_path}")
        print(f"[OK] Icon set to: {icon_path}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to create shortcut: {e}")
        return create_shortcut_powershell()

def create_shortcut_powershell():
    """Alternative method using PowerShell"""
    try:
        import subprocess
        
        app_dir = Path(__file__).parent
        desktop = Path(os.environ['USERPROFILE']) / 'Desktop'
        shortcut_path = desktop / 'Gaybeck Starkids SMS.lnk'
        run_app_batch = app_dir / 'RUN_APP.bat'
        
        # Try to find a custom icon
        icon_path = app_dir / 'sms_icon.ico'
        if not icon_path.exists():
            icon_path = app_dir / 'sms_icon.png'
        if not icon_path.exists():
            icon_path = Path('C:\\Windows\\System32\\python.exe')
        
        ps_command = f'''
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut('{shortcut_path}')
$Shortcut.TargetPath = '{run_app_batch}'
$Shortcut.WorkingDirectory = '{app_dir}'
$Shortcut.Description = 'Gaybeck Starkids School Management System'
$Shortcut.IconLocation = '{icon_path}'
$Shortcut.WindowStyle = 1
$Shortcut.Save()
'''
        
        subprocess.run(
            ['powershell', '-NoProfile', '-Command', ps_command],
            check=True,
            capture_output=True
        )
        
        print(f"[OK] Desktop shortcut created: {shortcut_path}")
        print(f"[OK] Icon set to: {icon_path}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to create shortcut: {e}")
        return False

if __name__ == '__main__':
    print("=" * 70)
    print("Gaybeck Starkids SMS - Desktop Shortcut Creator")
    print("=" * 70)
    print()
    
    success = create_desktop_shortcut()
    
    print()
    if success:
        print("[OK] Shortcut created successfully!")
        print("You can now double-click 'Gaybeck Starkids SMS' on your desktop.")
        print("The application will launch with no visible console window.")
    else:
        print("[!] If shortcut creation failed, you can:")
        print("    1. Double-click RUN_APP.bat in the application folder")
        print("    2. Right-click RUN_APP.bat > Send to > Desktop (create shortcut)")
        print("    3. Run: powershell -File RUN_APP.ps1")
    print()

