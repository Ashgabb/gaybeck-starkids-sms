# -*- coding: utf-8 -*-
"""
Gaybeck Starkids SMS - Complete Uninstaller
Removes all traces of the application from the system
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def find_shortcuts():
    """Find all shortcuts to the application"""
    shortcuts = []
    
    # Check user Start Menu
    start_menu_user = Path(os.getenv('APPDATA')) / 'Microsoft' / 'Windows' / 'Start Menu' / 'Programs'
    for file in start_menu_user.rglob('*Gaybeck*.lnk'):
        shortcuts.append(file)
    for file in start_menu_user.rglob('*Starkids*.lnk'):
        shortcuts.append(file)
    
    # Check system Start Menu
    start_menu_system = Path(os.getenv('PROGRAMDATA', 'C:\\ProgramData')) / 'Microsoft' / 'Windows' / 'Start Menu' / 'Programs'
    for file in start_menu_system.rglob('*Gaybeck*.lnk'):
        shortcuts.append(file)
    for file in start_menu_system.rglob('*Starkids*.lnk'):
        shortcuts.append(file)
    
    # Check Desktop
    desktop = Path.home() / 'Desktop'
    for file in desktop.glob('*Gaybeck*.lnk'):
        shortcuts.append(file)
    for file in desktop.glob('*Starkids*.lnk'):
        shortcuts.append(file)
    
    return shortcuts

def find_app_data():
    """Find application data directories"""
    data_dirs = []
    
    # Windows AppData
    appdata = Path(os.getenv('APPDATA', ''))
    if appdata:
        gaybeck_dir = appdata / 'GaybeckStarkidsSMS'
        if gaybeck_dir.exists():
            data_dirs.append(gaybeck_dir)
    
    # User home directory
    home_dir = Path.home() / '.gaybeck-starkids-sms'
    if home_dir.exists():
        data_dirs.append(home_dir)
    
    return data_dirs

def find_running_processes():
    """Find running application processes"""
    try:
        if os.name == 'nt':  # Windows
            result = subprocess.run(
                ['powershell', '-Command', 
                 'Get-Process | Where-Object {$_.ProcessName -like "*Gaybeck*" -or $_.ProcessName -like "*Starkids*"} | Select-Object Id, ProcessName, MainWindowTitle'],
                capture_output=True, text=True
            )
            return result.stdout
        else:
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            lines = [line for line in result.stdout.split('\n') if 'gaybeck' in line.lower() or 'starkids' in line.lower()]
            return '\n'.join(lines)
    except Exception as e:
        return f"Could not check processes: {e}"

def stop_running_processes():
    """Stop all running application processes"""
    try:
        if os.name == 'nt':  # Windows
            subprocess.run(
                ['powershell', '-Command', 
                 'Get-Process | Where-Object {$_.ProcessName -like "*Gaybeck*" -or $_.ProcessName -like "*Starkids*"} | Stop-Process -Force'],
                capture_output=True
            )
            return True
        else:
            subprocess.run(['pkill', '-9', '-f', 'gaybeck'], capture_output=True)
            subprocess.run(['pkill', '-9', '-f', 'starkids'], capture_output=True)
            return True
    except Exception as e:
        print(f"Warning: Could not stop processes: {e}")
        return False

def uninstall_pip_package():
    """Uninstall the pip package"""
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'uninstall', 'gaybeck-starkids-sms', '-y'],
            capture_output=True, text=True
        )
        return 'Successfully uninstalled' in result.stdout or 'not installed' in result.stderr
    except Exception as e:
        print(f"Warning: Could not uninstall pip package: {e}")
        return False

def main():
    # Set UTF-8 encoding for Windows console
    if sys.platform == 'win32':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except:
            pass
    
    print("\n" + "="*70)
    print("GAYBECK STARKIDS SMS - COMPLETE UNINSTALLER")
    print("="*70 + "\n")
    
    # Step 1: Find running processes
    print("1. Checking for running processes...")
    processes = find_running_processes()
    if processes and len(processes.strip()) > 0:
        print("   Found running processes:")
        print(processes)
        print("\n   Stopping processes...")
        if stop_running_processes():
            print("   ✓ Processes stopped")
        else:
            print("   ⚠ Could not stop all processes")
    else:
        print("   ✓ No running processes found")
    
    # Step 2: Uninstall pip package
    print("\n2. Uninstalling pip package...")
    if uninstall_pip_package():
        print("   ✓ Pip package uninstalled")
    else:
        print("   ⚠ Pip package not found or could not uninstall")
    
    # Step 3: Remove shortcuts
    print("\n3. Removing shortcuts...")
    shortcuts = find_shortcuts()
    if shortcuts:
        for shortcut in shortcuts:
            try:
                shortcut.unlink()
                print(f"   ✓ Removed: {shortcut}")
            except Exception as e:
                print(f"   ✗ Could not remove {shortcut}: {e}")
    else:
        print("   ✓ No shortcuts found")
    
    # Step 4: Remove application data
    print("\n4. Removing application data...")
    data_dirs = find_app_data()
    if data_dirs:
        for data_dir in data_dirs:
            try:
                size = sum(f.stat().st_size for f in data_dir.rglob('*') if f.is_file())
                size_mb = size / (1024 * 1024)
                
                response = input(f"\n   Remove {data_dir} ({size_mb:.2f} MB)? This will delete all data! [y/N]: ")
                if response.lower() == 'y':
                    shutil.rmtree(data_dir)
                    print(f"   ✓ Removed: {data_dir}")
                else:
                    print(f"   ⊘ Skipped: {data_dir}")
            except Exception as e:
                print(f"   ✗ Could not remove {data_dir}: {e}")
    else:
        print("   ✓ No application data found")
    
    # Step 5: Clean up console scripts
    print("\n5. Checking for console scripts...")
    scripts_dir = Path(sys.executable).parent / 'Scripts'
    starkids_exe = scripts_dir / 'starkids-sms.exe'
    if starkids_exe.exists():
        try:
            starkids_exe.unlink()
            print(f"   ✓ Removed: {starkids_exe}")
        except Exception as e:
            print(f"   ✗ Could not remove {starkids_exe}: {e}")
    else:
        print("   ✓ No console scripts found")
    
    print("\n" + "="*70)
    print("✓ UNINSTALLATION COMPLETE")
    print("="*70 + "\n")
    
    print("The following items were NOT removed (if they exist):")
    print("  • Source code folders on Desktop")
    print("  • Development files in project directory")
    print("  • Backup files")
    print("\nYou can manually delete these if needed.\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nUninstallation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nError during uninstallation: {e}")
        sys.exit(1)
