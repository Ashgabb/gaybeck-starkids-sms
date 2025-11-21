#!/usr/bin/env python3
"""Create Windows shortcuts for Gaybeck Starkids SMS"""

import os
import sys
from pathlib import Path

try:
    from win32com.client import Dispatch
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False
    print("Installing pywin32...")
    os.system("pip install pywin32 --quiet")
    try:
        from win32com.client import Dispatch
        WIN32_AVAILABLE = True
    except ImportError:
        print("Could not install pywin32. Using alternative method.")

def create_shortcut(python_exe, script_path, shortcut_path, app_dir, icon_path=None):
    """Create a Windows shortcut with correct working directory"""
    try:
        shell = Dispatch("WScript.Shell")
        shortcut = shell.CreateShortcut(str(shortcut_path))
        shortcut.TargetPath = str(python_exe)
        shortcut.Arguments = str(script_path)
        shortcut.WorkingDirectory = str(app_dir)
        if icon_path and Path(icon_path).exists():
            shortcut.IconLocation = str(icon_path)
        shortcut.Save()
        return True
    except Exception as e:
        print(f"Error creating shortcut: {e}")
        return False

def main():
    app_dir = Path(__file__).parent.resolve()
    python_exe = sys.executable
    sms_py = app_dir / "sms.py"
    icon_file = app_dir / "sms_icon.ico"
    
    # Desktop shortcut
    desktop = Path.home() / "Desktop"
    desktop_shortcut = desktop / "Gaybeck Starkids SMS.lnk"
    
    # Start Menu shortcut
    start_menu = Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs"
    start_menu_dir = start_menu / "Gaybeck Starkids SMS"
    start_menu_dir.mkdir(parents=True, exist_ok=True)
    start_menu_shortcut = start_menu_dir / "Gaybeck Starkids SMS.lnk"
    
    print("Creating Windows shortcuts...")
    print()
    
    # Create desktop shortcut
    print(f"[1/2] Creating Desktop shortcut...")
    print(f"      Target: {python_exe}")
    print(f"      Script: {sms_py}")
    print(f"      Working Dir: {app_dir}")
    print(f"      Location: {desktop_shortcut}")
    
    if create_shortcut(python_exe, sms_py, desktop_shortcut, app_dir, icon_file):
        print(f"      ✓ Desktop shortcut created successfully")
    else:
        print(f"      ✗ Failed to create desktop shortcut")
    
    print()
    
    # Create Start Menu shortcut
    print(f"[2/2] Creating Start Menu shortcut...")
    print(f"      Location: {start_menu_shortcut}")
    
    if create_shortcut(python_exe, sms_py, start_menu_shortcut, app_dir, icon_file):
        print(f"      ✓ Start Menu shortcut created successfully")
    else:
        print(f"      ✗ Failed to create Start Menu shortcut")
    
    print()
    print("=" * 60)
    print("Shortcut creation complete!")
    print("=" * 60)
    print()
    print("You should now see:")
    print("  1. 'Gaybeck Starkids SMS' icon on your Desktop")
    print("  2. 'Gaybeck Starkids SMS' in your Start Menu")
    print()
    print("To launch the app:")
    print("  - Click the Desktop icon, OR")
    print("  - Press Windows key and type 'Gaybeck'")
    print()

if __name__ == "__main__":
    main()
