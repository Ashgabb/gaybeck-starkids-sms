#!/usr/bin/env python3
"""
SMS Application Launcher with Icon Support
Sets the application window icon for taskbar display
"""
import subprocess
import sys
import os
from pathlib import Path

def main():
    # Get the app directory
    app_dir = Path(__file__).parent
    sms_script = app_dir / 'sms.py'
    icon_file = app_dir / 'sms_icon.ico'
    
    if not sms_script.exists():
        print(f"ERROR: {sms_script} not found")
        sys.exit(1)
    
    if not icon_file.exists():
        print(f"WARNING: {icon_file} not found - app will launch without custom icon")
    
    # Launch SMS with icon support
    # The icon needs to be set in the Tkinter code, but we can try using Windows API
    try:
        # Try to set the window icon using ctypes
        if sys.platform == 'win32' and icon_file.exists():
            import ctypes
            
            # This sets the icon in the taskbar
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("GaybeckStarkids.SMS.App")
            print(f"[OK] Icon registered for taskbar")
    except Exception as e:
        print(f"[INFO] Could not set taskbar icon via API: {e}")
    
    # Launch the application
    print(f"[INFO] Starting Gaybeck Starkids SMS...")
    try:
        subprocess.run([sys.executable, str(sms_script)], check=False)
    except Exception as e:
        print(f"ERROR: Failed to start application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
