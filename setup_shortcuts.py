#!/usr/bin/env python3
"""
Gaybeck Starkids SMS - Desktop Launcher with Icon Support
Creates and manages desktop shortcuts for Windows systems
Version: 3.0.1
"""

import os
import sys
import subprocess
from pathlib import Path

def create_shortcut():
    """Create a Windows desktop shortcut with proper configuration"""
    try:
        import win32com.client
    except ImportError:
        print("[INFO] pywin32 not installed, trying alternative method...")
        return create_shortcut_cmd()
    
    try:
        shell = win32com.client.Dispatch("WScript.Shell")
        app_dir = Path(__file__).parent.absolute()
        desktop = Path.home() / "Desktop"
        
        shortcut_path = desktop / "Gaybeck Starkids SMS.lnk"
        target = app_dir / "launch_sms.py"
        icon = app_dir / "sms_icon.ico"
        
        if shortcut_path.exists():
            shortcut_path.unlink()
        
        shortcut = shell.CreateShortCut(str(shortcut_path))
        shortcut.TargetPath = str(target)
        shortcut.WorkingDirectory = str(app_dir)
        shortcut.IconLocation = f"{str(icon)},0"
        shortcut.Description = "Gaybeck Starkids School Management System"
        shortcut.save()
        
        print(f"[OK] Shortcut created: {shortcut_path}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to create shortcut: {e}")
        return False

def create_shortcut_cmd():
    """Fallback: Create shortcut using PowerShell"""
    try:
        app_dir = Path(__file__).parent.absolute()
        desktop = Path.home() / "Desktop"
        shortcut_path = desktop / "Gaybeck Starkids SMS.lnk"
        target = app_dir / "launch_sms.py"
        icon = app_dir / "sms_icon.ico"
        
        ps_command = f'''
        $shell = New-Object -ComObject WScript.Shell
        $shortcut = $shell.CreateShortcut('{shortcut_path}')
        $shortcut.TargetPath = '{target}'
        $shortcut.WorkingDirectory = '{app_dir}'
        $shortcut.IconLocation = '{icon},0'
        $shortcut.Description = 'Gaybeck Starkids School Management System'
        $shortcut.Save()
        Write-Host '[OK] Shortcut created'
        '''
        
        result = subprocess.run(
            ["powershell", "-Command", ps_command],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"[OK] Shortcut created: {shortcut_path}")
            return True
        else:
            print(f"[ERROR] PowerShell error: {result.stderr}")
            return False
    except Exception as e:
        print(f"[ERROR] Failed to create shortcut: {e}")
        return False

def create_start_menu_shortcut():
    """Create a Start Menu shortcut"""
    try:
        import win32com.client
    except ImportError:
        print("[INFO] pywin32 not available, skipping Start Menu shortcut")
        return False
    
    try:
        shell = win32com.client.Dispatch("WScript.Shell")
        app_dir = Path(__file__).parent.absolute()
        start_menu = Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs"
        
        shortcut_path = start_menu / "Gaybeck Starkids SMS.lnk"
        target = app_dir / "launch_sms.py"
        icon = app_dir / "sms_icon.ico"
        
        if shortcut_path.exists():
            shortcut_path.unlink()
        
        shortcut = shell.CreateShortCut(str(shortcut_path))
        shortcut.TargetPath = str(target)
        shortcut.WorkingDirectory = str(app_dir)
        shortcut.IconLocation = f"{str(icon)},0"
        shortcut.Description = "Gaybeck Starkids School Management System"
        shortcut.save()
        
        print(f"[OK] Start Menu shortcut created: {shortcut_path}")
        return True
    except Exception as e:
        print(f"[INFO] Could not create Start Menu shortcut: {e}")
        return False

if __name__ == "__main__":
    print("Setting up Gaybeck Starkids SMS Shortcuts...")
    print()
    
    success = create_shortcut()
    create_start_menu_shortcut()
    
    if success:
        print()
        print("✓ Setup complete! You can now launch the app from:")
        print("  - Desktop: Double-click 'Gaybeck Starkids SMS' shortcut")
        print("  - Start Menu: Search for 'Gaybeck Starkids SMS'")
    else:
        print()
        print("[WARNING] Some shortcuts could not be created.")
        print("[INFO] You can still launch the app by running: python launch_sms.py")
