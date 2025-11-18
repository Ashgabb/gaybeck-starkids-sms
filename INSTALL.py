#!/usr/bin/env python3
"""
Gaybeck Starkids SMS - Universal Installer
Works on Windows, macOS, and Linux
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

class Installer:
    def __init__(self):
        self.app_dir = Path(__file__).parent
        self.os_type = platform.system()
        self.python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        
    def print_header(self):
        """Print installation header"""
        print("\n" + "=" * 70)
        print("  Gaybeck Starkids SMS - Universal Installer v3.0.0")
        print("=" * 70)
        print(f"System: {self.os_type}")
        print(f"Python: {self.python_version}")
        print(f"Location: {self.app_dir}")
        print("=" * 70 + "\n")
    
    def check_python(self):
        """Verify Python version"""
        print("[1/6] Checking Python version...")
        
        major, minor = sys.version_info.major, sys.version_info.minor
        if major < 3 or (major == 3 and minor < 13):
            print(f"[ERROR] Python 3.13+ required (found {major}.{minor})")
            print("Download from: https://www.python.org")
            return False
        
        print(f"[OK] Python {major}.{minor} detected\n")
        return True
    
    def check_tkinter(self):
        """Verify Tkinter is available"""
        print("[2/6] Checking Tkinter...")
        
        try:
            import tkinter
            print("[OK] Tkinter is available\n")
            return True
        except ImportError:
            print("[ERROR] Tkinter not found")
            print("Install Tkinter:")
            if self.os_type == "Windows":
                print("  - Reinstall Python with Tkinter enabled")
            elif self.os_type == "Darwin":
                print("  - brew install python-tk@3.13")
            else:
                print("  - sudo apt-get install python3-tk")
            return False
    
    def install_requirements(self):
        """Install Python dependencies"""
        print("[3/6] Installing dependencies...")
        
        req_file = self.app_dir / "requirements.txt"
        if not req_file.exists():
            print("[WARNING] requirements.txt not found, skipping\n")
            return True
        
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", str(req_file), "-q"],
                check=True,
                cwd=str(self.app_dir)
            )
            print("[OK] Dependencies installed\n")
            return True
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Failed to install dependencies: {e}")
            print("Try running manually: pip install -r requirements.txt\n")
            return False
    
    def check_database(self):
        """Verify database exists"""
        print("[4/6] Checking database...")
        
        db_dir = self.app_dir / "database"
        db_file = db_dir / "school_management.db"
        
        if not db_dir.exists():
            db_dir.mkdir(parents=True, exist_ok=True)
            print("[INFO] Created database directory")
        
        if db_file.exists():
            size = db_file.stat().st_size / 1024
            print(f"[OK] Database found ({size:.1f} KB)\n")
        else:
            print("[WARNING] Database not found - will be created on first run\n")
        
        return True
    
    def create_shortcuts(self):
        """Create platform-specific shortcuts"""
        print("[5/6] Creating shortcuts...")
        
        if self.os_type == "Windows":
            self.create_windows_shortcuts()
        elif self.os_type == "Darwin":
            self.create_macos_shortcuts()
        else:
            self.create_linux_shortcuts()
        
        print("[OK] Shortcuts created\n")
        return True
    
    def create_windows_shortcuts(self):
        """Create Windows desktop shortcut"""
        try:
            desktop = Path.home() / "Desktop"
            shortcut_path = desktop / "Gaybeck Starkids SMS.lnk"
            
            # Use PowerShell to create the shortcut
            ps_command = f'''
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut('{shortcut_path}')
$Shortcut.TargetPath = '{self.app_dir / "RUN_APP.bat"}'
$Shortcut.WorkingDirectory = '{self.app_dir}'
$Shortcut.Description = 'Gaybeck Starkids School Management System'
$Shortcut.IconLocation = '{self.app_dir / "sms_icon.ico"}'
$Shortcut.Save()
'''
            subprocess.run(
                ["powershell", "-NoProfile", "-Command", ps_command],
                check=True,
                capture_output=True
            )
            print(f"[OK] Desktop shortcut created")
        except Exception as e:
            print(f"[WARNING] Could not create shortcut: {e}")
    
    def create_macos_shortcuts(self):
        """Create macOS launcher"""
        try:
            launcher = self.app_dir / "launch_app.command"
            launcher.write_text(f"""#!/bin/bash
cd "{self.app_dir}"
python3 sms.py
""")
            launcher.chmod(0o755)
            print(f"[OK] macOS launcher created: launch_app.command")
        except Exception as e:
            print(f"[WARNING] Could not create launcher: {e}")
    
    def create_linux_shortcuts(self):
        """Create Linux launcher"""
        try:
            launcher = self.app_dir / "launch_app.sh"
            launcher.write_text(f"""#!/bin/bash
cd "{self.app_dir}"
python3 sms.py
""")
            launcher.chmod(0o755)
            print(f"[OK] Linux launcher created: launch_app.sh")
            
            # Create .desktop file
            desktop_file = self.app_dir / "gaybeck-sms.desktop"
            desktop_file.write_text(f"""[Desktop Entry]
Type=Application
Name=Gaybeck Starkids SMS
Exec={self.app_dir}/launch_app.sh
Path={self.app_dir}
Icon=system-run
Terminal=false
""")
            print(f"[OK] Desktop entry created")
        except Exception as e:
            print(f"[WARNING] Could not create launcher: {e}")
    
    def verify_installation(self):
        """Verify the application can be imported"""
        print("[6/6] Verifying installation...")
        
        try:
            # Add app dir to path
            sys.path.insert(0, str(self.app_dir))
            
            # Try importing main module
            import sms
            print("[OK] Application verified successfully\n")
            return True
        except ImportError as e:
            print(f"[WARNING] Could not import application: {e}")
            print("Application may still work, but dependencies might be missing\n")
            return True
        except Exception as e:
            print(f"[ERROR] Verification failed: {e}\n")
            return False
    
    def print_summary(self):
        """Print installation summary"""
        print("=" * 70)
        print("  Installation Complete!")
        print("=" * 70)
        print("\nHow to launch the application:\n")
        
        if self.os_type == "Windows":
            print("  Option 1: Double-click 'Gaybeck Starkids SMS' on Desktop")
            print("  Option 2: Double-click 'RUN_APP.bat' in application folder")
            print("  Option 3: Run: python sms.py")
        elif self.os_type == "Darwin":
            print("  Option 1: Double-click 'launch_app.command' in application folder")
            print("  Option 2: Run: python3 sms.py")
            print("  Option 3: Open Terminal and run: cd '<app-path>' && python3 sms.py")
        else:
            print("  Option 1: Run ./launch_app.sh in application folder")
            print("  Option 2: Run: python3 sms.py")
            print("  Option 3: Open Terminal and run: cd '<app-path>' && python3 sms.py")
        
        print("\n" + "=" * 70)
        print("System Requirements:")
        print(f"  ✓ Python 3.13+")
        print(f"  ✓ Tkinter GUI framework")
        print(f"  ✓ SQLite3 (bundled with Python)")
        print(f"  ✓ 500 MB+ disk space")
        print(f"  ✓ 2 GB+ RAM")
        print("=" * 70 + "\n")
    
    def run(self):
        """Run the installation"""
        self.print_header()
        
        steps = [
            ("Python Check", self.check_python),
            ("Tkinter Check", self.check_tkinter),
            ("Dependencies", self.install_requirements),
            ("Database", self.check_database),
            ("Shortcuts", self.create_shortcuts),
            ("Verification", self.verify_installation),
        ]
        
        for name, step_func in steps:
            try:
                if not step_func():
                    print(f"\n[ERROR] Installation failed at: {name}")
                    print("Please fix the error and try again.")
                    return False
            except Exception as e:
                print(f"\n[ERROR] Unexpected error during {name}: {e}")
                return False
        
        self.print_summary()
        return True


if __name__ == "__main__":
    installer = Installer()
    success = installer.run()
    
    if success:
        print("\n✓ Ready to use! Launch the application now.")
        sys.exit(0)
    else:
        print("\n✗ Installation encountered issues.")
        sys.exit(1)
