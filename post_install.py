"""
Gaybeck Starkids SMS - Post-Installation Setup
Creates shortcuts and sets up the application after pip install
"""

import os
import sys
from pathlib import Path

def create_shortcut_windows(name, target, icon_path=None, description=""):
    """Create a Windows shortcut (.lnk file)"""
    try:
        import win32com.client
        
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(str(name))
        shortcut.TargetPath = str(target)
        if icon_path and os.path.exists(icon_path):
            shortcut.IconLocation = str(icon_path)
        if description:
            shortcut.Description = description
        shortcut.save()
        return True
    except ImportError:
        print("Warning: pywin32 not installed. Cannot create shortcuts automatically.")
        print("Please install with: pip install pywin32")
        return False
    except Exception as e:
        print(f"Warning: Could not create shortcut: {e}")
        return False

def setup_shortcuts():
    """Create desktop and start menu shortcuts"""
    
    # Get Python executable path - use pythonw.exe to hide console window
    python_exe = sys.executable
    pythonw_exe = python_exe.replace('python.exe', 'pythonw.exe')
    if not os.path.exists(pythonw_exe):
        pythonw_exe = python_exe  # Fallback to python.exe if pythonw not found
    
    # Import statement to run the app
    import_cmd = f'"{pythonw_exe}" -c "import sms; sms.start_application()"'
    
    # Create batch file to launch the app in user's AppData
    app_data = Path(os.getenv('APPDATA'))
    launcher_dir = app_data / 'GaybeckStarkidsSMS'
    launcher_dir.mkdir(exist_ok=True, parents=True)
    
    launcher_bat = launcher_dir / 'launch.bat'
    with open(launcher_bat, 'w') as f:
        f.write('@echo off\n')
        f.write(f'start "" "{pythonw_exe}" -c "import sms; sms.start_application()"\n')
    
    print(f"✓ Created launcher: {launcher_bat}")
    
    # Find and copy icon to AppData
    icon_appdata_path = launcher_dir / 'icon.ico'
    icon_sources = [
        Path(__file__).parent / 'icon.ico',  # Same directory as this script
        Path.cwd() / 'icon.ico',  # Current working directory
        Path(sys.prefix) / 'icon.ico',  # Python prefix
        Path(sys.prefix) / 'share' / 'gaybeck-starkids-sms' / 'icon.ico',  # Data files location
    ]
    
    icon_found = False
    for icon_src in icon_sources:
        if icon_src.exists():
            try:
                import shutil
                shutil.copy2(icon_src, icon_appdata_path)
                print(f"✓ Copied icon to: {icon_appdata_path}")
                icon_found = True
                break
            except Exception as e:
                print(f"Warning: Could not copy icon from {icon_src}: {e}")
    
    if not icon_found:
        print(f"Warning: Icon file not found. Checked locations:")
        for src in icon_sources:
            print(f"  - {src}")
    
    # Try to create shortcuts
    try:
        # Use icon from AppData if it exists, otherwise try source locations
        icon_path = str(icon_appdata_path) if icon_appdata_path.exists() else None
        if not icon_path:
            for icon_src in icon_sources:
                if icon_src.exists():
                    icon_path = str(icon_src)
                    print(f"✓ Using icon from: {icon_path}")
                    break
        
        # Desktop shortcut
        desktop = Path.home() / 'Desktop'
        desktop_shortcut = desktop / 'Gaybeck Starkids Academy.lnk'
        
        # Start Menu shortcut
        start_menu = Path(os.getenv('APPDATA')) / 'Microsoft' / 'Windows' / 'Start Menu' / 'Programs'
        start_menu_shortcut = start_menu / 'Gaybeck Starkids Academy.lnk'
        
        if create_shortcut_windows(
            desktop_shortcut, 
            launcher_bat,
            icon_path=icon_path,
            description="Gaybeck Starkids Academy - School Management System"
        ):
            print(f"✓ Created desktop shortcut")
        
        if create_shortcut_windows(
            start_menu_shortcut, 
            launcher_bat,
            icon_path=icon_path,
            description="Gaybeck Starkids Academy - School Management System"
        ):
            print(f"✓ Created start menu shortcut")
            
    except Exception as e:
        print(f"Warning: Could not create shortcuts: {e}")

def main():
    print("\n" + "="*70)
    print("GAYBECK STARKIDS SMS - POST-INSTALLATION SETUP")
    print("="*70 + "\n")
    
    print("Setting up shortcuts and launchers...\n")
    setup_shortcuts()
    
    print("\n" + "="*70)
    print("✓ SETUP COMPLETE")
    print("="*70 + "\n")
    
    print("The application has been installed!")
    print("\nYou can launch it using:")
    print("  • Desktop shortcut (if created)")
    print("  • Start Menu shortcut (if created)")
    print("  • Command: python -c \"import sms; sms.start_application()\"")
    print("\nTo uninstall:")
    print("  • Run: python -m uninstall")
    print("  • Or: python uninstall.py")
    print()

if __name__ == "__main__":
    main()
