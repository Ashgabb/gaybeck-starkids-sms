#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gaybeck Starkids SMS - Professional Installer
Version: 3.0.0
Date: November 17, 2025

Features:
- Auto-detects existing installations
- Offers upgrade or clean install options
- Installs Python dependencies
- Creates desktop and taskbar shortcuts
- Registry integration for clean uninstall
"""

import os
import sys
import subprocess
import shutil
import json
import winreg
import ctypes
from pathlib import Path
from datetime import datetime

# Fix console encoding for Windows
if sys.platform == 'win32':
    try:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    except:
        pass

# Installer Configuration
PRODUCT_NAME = "Gaybeck Starkids SMS"
PRODUCT_VERSION = "3.0.0"
INSTALL_DIR = r"C:\Program Files\Gaybeck Starkids SMS"
PYTHON_MIN_VERSION = (3, 13)
PRODUCT_PUBLISHER = "Gaybeck Starkids School"
REGISTRY_KEY = r"Software\Gaybeck Starkids\SMS"

# Colors for console output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class GaybeckInstaller:
    def __init__(self):
        self.install_dir = INSTALL_DIR
        self.python_exe = sys.executable
        self.is_admin = self.check_admin()
        self.existing_install = None
        self.existing_version = None
        
    def print_header(self):
        """Display installer header"""
        print(f"\n{Colors.HEADER}{Colors.BOLD}")
        print("=" * 80)
        print(f"  {PRODUCT_NAME} - Professional Installer v{PRODUCT_VERSION}".center(80))
        print(f"  {PRODUCT_PUBLISHER}".center(80))
        print("=" * 80)
        print(f"{Colors.END}\n")
    
    def check_admin(self):
        """Check if running as administrator"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def print_step(self, step_num, title):
        """Print a step header"""
        print(f"\n{Colors.CYAN}{Colors.BOLD}[Step {step_num}] {title}{Colors.END}")
        print("-" * 80)
    
    def print_success(self, message):
        """Print success message"""
        print(f"{Colors.GREEN}[OK] {message}{Colors.END}")
    
    def print_warning(self, message):
        """Print warning message"""
        print(f"{Colors.WARNING}[!] {message}{Colors.END}")
    
    def print_error(self, message):
        """Print error message"""
        print(f"{Colors.FAIL}[ERROR] {message}{Colors.END}")
    
    def print_info(self, message):
        """Print info message"""
        print(f"{Colors.BLUE}[INFO] {message}{Colors.END}")
    
    def check_admin_and_elevate(self):
        """Check admin status and elevate if needed"""
        self.print_step(1, "Checking Administrator Privileges")
        
        if not self.is_admin:
            self.print_warning("This installer requires Administrator privileges")
            self.print_info("Attempting to elevate privileges...")
            
            # Rerun as admin
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            sys.exit(0)
        else:
            self.print_success("Running with Administrator privileges")
    
    def check_existing_installation(self):
        """Check for existing installations"""
        self.print_step(2, "Checking for Existing Installations")
        
        try:
            # Check registry
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, REGISTRY_KEY)
            version = winreg.QueryValueEx(key, "Version")[0]
            install_path = winreg.QueryValueEx(key, "InstallPath")[0]
            winreg.CloseKey(key)
            
            self.existing_install = install_path
            self.existing_version = version
            
            print(f"\n{Colors.WARNING}{Colors.BOLD}Found Existing Installation:{Colors.END}")
            print(f"  Product:     {PRODUCT_NAME}")
            print(f"  Version:     {version}")
            print(f"  Location:    {install_path}")
            print(f"  Date:        {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            return True
        except WindowsError:
            self.print_success("No existing installation found - Fresh install")
            return False
    
    def handle_existing_installation(self):
        """Handle upgrade or clean install choice"""
        self.print_step(3, "Installation Options")
        
        print("\nWhat would you like to do?\n")
        print("1) Upgrade to version " + Colors.BOLD + f"{PRODUCT_VERSION}" + Colors.END)
        print("   - Keeps your database and settings")
        print("   - Updates application files")
        print("   - Preserves configuration\n")
        
        print("2) Remove current version and install fresh")
        print("   - Completely removes " + Colors.BOLD + f"v{self.existing_version}" + Colors.END)
        print("   - Installs " + Colors.BOLD + f"v{PRODUCT_VERSION}" + Colors.END + " clean")
        print("   - WARNING: Database will be removed!\n")
        
        print("3) Cancel installation")
        print("   - Keep current version as-is\n")
        
        choice = input(f"{Colors.BOLD}Enter your choice (1-3): {Colors.END}").strip()
        
        if choice == "1":
            self.print_success("Upgrade selected")
            return "upgrade"
        elif choice == "2":
            confirm = input(f"\n{Colors.FAIL}{Colors.BOLD}WARNING: This will remove all data!{Colors.END}\n"
                          f"Are you sure? (yes/no): ").strip().lower()
            if confirm == "yes":
                self.uninstall_existing()
                self.print_success("Previous version removed")
                return "clean"
            else:
                self.print_info("Clean install cancelled")
                return "cancel"
        elif choice == "3":
            self.print_info("Installation cancelled by user")
            return "cancel"
        else:
            self.print_error("Invalid choice")
            return self.handle_existing_installation()
    
    def uninstall_existing(self):
        """Uninstall existing version"""
        self.print_info("Removing existing installation...")
        
        try:
            uninstall_exe = os.path.join(self.existing_install, "Uninstall.exe")
            if os.path.exists(uninstall_exe):
                subprocess.run([uninstall_exe, "/S"], timeout=60)
                import time
                time.sleep(2)
            
            # Force remove directory if still exists
            if os.path.exists(self.existing_install):
                shutil.rmtree(self.existing_install, ignore_errors=True)
            
            self.print_success("Existing installation removed")
        except Exception as e:
            self.print_warning(f"Could not fully remove: {e}")
    
    def verify_python(self):
        """Verify Python version"""
        self.print_step(4, "Python Version Check")
        
        version_info = sys.version_info
        print(f"Python Version:  {version_info.major}.{version_info.minor}.{version_info.micro}")
        print(f"Python Executable: {self.python_exe}")
        
        if version_info >= PYTHON_MIN_VERSION:
            self.print_success(f"Python {PYTHON_MIN_VERSION[0]}.{PYTHON_MIN_VERSION[1]}+ requirement met")
            return True
        else:
            self.print_error(f"Python {PYTHON_MIN_VERSION[0]}.{PYTHON_MIN_VERSION[1]}+ required")
            return False
    
    def create_install_directory(self):
        """Create installation directory"""
        self.print_step(5, "Creating Installation Directory")
        
        self.print_info(f"Installation directory: {self.install_dir}")
        
        try:
            os.makedirs(self.install_dir, exist_ok=True)
            self.print_success(f"Directory created: {self.install_dir}")
            return True
        except Exception as e:
            self.print_error(f"Failed to create directory: {e}")
            return False
    
    def copy_application_files(self):
        """Copy application files to install directory"""
        self.print_step(6, "Copying Application Files")
        
        source_dir = Path(__file__).parent
        files_to_copy = [
            "sms.py",
            "advanced_ai_analytics.py",
            "requirements.txt",
            "logo.png",
            "icon.ico",
            "README.md",
            "LICENSE.txt"
        ]
        
        dirs_to_copy = [
            "database",
            "docs",
            "scripts",
            "backups"
        ]
        
        try:
            # Copy individual files
            for file in files_to_copy:
                src = source_dir / file
                if src.exists():
                    dst = Path(self.install_dir) / file
                    shutil.copy2(src, dst)
                    self.print_info(f"Copied: {file}")
            
            # Copy directories
            for dir_name in dirs_to_copy:
                src = source_dir / dir_name
                if src.exists():
                    dst = Path(self.install_dir) / dir_name
                    if dst.exists():
                        shutil.rmtree(dst)
                    shutil.copytree(src, dst)
                    self.print_info(f"Copied: {dir_name}/")
            
            self.print_success("All application files copied")
            return True
        except Exception as e:
            self.print_error(f"Failed to copy files: {e}")
            return False
    
    def create_virtual_environment(self):
        """Create Python virtual environment"""
        self.print_step(7, "Creating Virtual Environment")
        
        venv_path = os.path.join(self.install_dir, ".venv")
        self.print_info(f"Virtual environment: {venv_path}")
        
        try:
            subprocess.run(
                [self.python_exe, "-m", "venv", venv_path],
                check=True,
                capture_output=True
            )
            self.print_success("Virtual environment created")
            return venv_path
        except Exception as e:
            self.print_error(f"Failed to create virtual environment: {e}")
            return None
    
    def install_dependencies(self, venv_path):
        """Install Python dependencies"""
        self.print_step(8, "Installing Python Dependencies")
        
        if not venv_path:
            self.print_error("Virtual environment not available")
            return False
        
        pip_exe = os.path.join(venv_path, "Scripts", "pip.exe")
        
        try:
            # Upgrade pip
            self.print_info("Upgrading pip...")
            subprocess.run(
                [pip_exe, "install", "--upgrade", "pip"],
                check=True,
                capture_output=True
            )
            self.print_success("pip upgraded")
            
            # Install requirements
            requirements_file = os.path.join(self.install_dir, "requirements.txt")
            if os.path.exists(requirements_file):
                self.print_info("Installing requirements from requirements.txt...")
                subprocess.run(
                    [pip_exe, "install", "-r", requirements_file],
                    check=True,
                    capture_output=False
                )
                self.print_success("All dependencies installed")
            
            return True
        except Exception as e:
            self.print_error(f"Failed to install dependencies: {e}")
            return False
    
    def create_shortcuts(self, venv_path):
        """Create desktop and start menu shortcuts"""
        self.print_step(9, "Creating Shortcuts")
        
        try:
            # Get desktop path
            desktop = Path.home() / "Desktop"
            
            # Create desktop shortcut
            shortcut_path = desktop / f"{PRODUCT_NAME}.lnk"
            self.create_lnk_shortcut(
                shortcut_path,
                os.path.join(venv_path, "Scripts", "pythonw.exe"),
                os.path.join(self.install_dir, "sms.py"),
                os.path.join(self.install_dir, "icon.ico"),
                self.install_dir
            )
            self.print_success(f"Desktop shortcut created: {shortcut_path}")
            
            # Create Start Menu shortcut
            start_menu = Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs"
            app_folder = start_menu / PRODUCT_NAME
            app_folder.mkdir(parents=True, exist_ok=True)
            
            shortcut_path = app_folder / f"{PRODUCT_NAME}.lnk"
            self.create_lnk_shortcut(
                shortcut_path,
                os.path.join(venv_path, "Scripts", "pythonw.exe"),
                os.path.join(self.install_dir, "sms.py"),
                os.path.join(self.install_dir, "icon.ico"),
                self.install_dir
            )
            self.print_success(f"Start Menu shortcut created")
            
            # Try to pin to taskbar
            self.pin_to_taskbar(shortcut_path)
            
            return True
        except Exception as e:
            self.print_warning(f"Shortcut creation partial: {e}")
            return True  # Don't fail installation for this
    
    def create_lnk_shortcut(self, lnk_path, target, args, icon, working_dir):
        """Create Windows shortcut (.lnk file) using COM"""
        try:
            import win32com.client
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(str(lnk_path))
            shortcut.Targetpath = target
            shortcut.Arguments = f'"{args}"'
            shortcut.IconLocation = icon
            shortcut.WorkingDirectory = working_dir
            shortcut.save()
        except ImportError:
            # Fallback: Create shortcut using VBScript
            vbs_content = f'''Set objShell = CreateObject("WScript.Shell")
Set objLink = objShell.CreateShortCut("{lnk_path}")
objLink.TargetPath = "{target}"
objLink.Arguments = "{args}"
objLink.IconLocation = "{icon}"
objLink.WorkingDirectory = "{working_dir}"
objLink.Save
'''
            vbs_path = os.path.join(self.install_dir, "CreateShortcut.vbs")
            with open(vbs_path, "w") as f:
                f.write(vbs_content)
            subprocess.run(["cscript.exe", vbs_path], capture_output=True)
    
    def pin_to_taskbar(self, shortcut_path):
        """Attempt to pin shortcut to taskbar"""
        try:
            # Create VBScript to pin to taskbar
            vbs_content = f'''
Set objShell = CreateObject("Shell.Application")
Set objFolder = objShell.NameSpace("{Path(shortcut_path).parent}")
Set objFile = objFolder.ParseName("{Path(shortcut_path).name}")
Set colVerbs = objFile.Verbs

For Each objVerb In colVerbs
    If Replace(objVerb.Name, "&", "") = "Pin to Taskbar" Then
        objVerb.DoIt
    End If
Next
'''
            vbs_path = os.path.join(self.install_dir, "PinToTaskbar.vbs")
            with open(vbs_path, "w") as f:
                f.write(vbs_content)
            
            subprocess.run(["cscript.exe", vbs_path], capture_output=True)
            self.print_success("Taskbar shortcut pinned")
        except:
            self.print_info("Taskbar pinning skipped (requires pywin32)")
    
    def register_in_registry(self, venv_path):
        """Register installation in Windows registry"""
        self.print_step(10, "Registering Installation")
        
        try:
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, REGISTRY_KEY)
            
            winreg.SetValueEx(key, "Version", 0, winreg.REG_SZ, PRODUCT_VERSION)
            winreg.SetValueEx(key, "InstallPath", 0, winreg.REG_SZ, self.install_dir)
            winreg.SetValueEx(key, "Publisher", 0, winreg.REG_SZ, PRODUCT_PUBLISHER)
            winreg.SetValueEx(key, "InstallDate", 0, winreg.REG_SZ, datetime.now().isoformat())
            winreg.SetValueEx(key, "UninstallString", 0, winreg.REG_SZ, os.path.join(self.install_dir, "Uninstall.exe"))
            
            winreg.CloseKey(key)
            self.print_success("Registry entries created")
            return True
        except Exception as e:
            self.print_warning(f"Registry registration failed: {e}")
            return True  # Don't fail installation
    
    def create_uninstaller(self):
        """Create uninstaller batch script"""
        self.print_step(11, "Creating Uninstaller")
        
        try:
            uninstall_bat = os.path.join(self.install_dir, "Uninstall.bat")
            uninstall_content = f"""@echo off
REM Gaybeck Starkids SMS Uninstaller
REM This script will remove the application

echo Gaybeck Starkids SMS Uninstaller
echo ================================
echo.
echo This will remove Gaybeck Starkids SMS from your system.
echo.

set /p confirm="Are you sure you want to uninstall? (yes/no): "
if /i not "%confirm%"=="yes" (
    echo Uninstall cancelled
    exit /b 0
)

echo.
echo Removing application files...
cd /d "%USERPROFILE%"
rmdir /s /q "{self.install_dir}"

echo Removing shortcuts...
del /f "{Path.home() / "Desktop" / f"{PRODUCT_NAME}.lnk"}" 2>nul
rmdir /s /q "{Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs" / PRODUCT_NAME}" 2>nul

echo Removing registry entries...
reg delete "HKEY_LOCAL_MACHINE\\{REGISTRY_KEY}" /f 2>nul

echo.
echo Uninstall complete!
echo {PRODUCT_NAME} has been removed from your system.
pause
"""
            
            with open(uninstall_bat, "w") as f:
                f.write(uninstall_content)
            
            self.print_success("Uninstaller created")
            return True
        except Exception as e:
            self.print_warning(f"Uninstaller creation failed: {e}")
            return True
    
    def run_installation(self):
        """Execute complete installation"""
        self.print_header()
        
        # Step 1: Admin check
        self.check_admin_and_elevate()
        
        # Step 2: Check existing installation
        has_existing = self.check_existing_installation()
        
        if has_existing:
            choice = self.handle_existing_installation()
            if choice == "cancel":
                self.print_error("Installation cancelled")
                return False
        
        # Step 3: Python check
        if not self.verify_python():
            self.print_error("Python version requirement not met")
            return False
        
        # Step 4: Create directory
        if not self.create_install_directory():
            return False
        
        # Step 5: Copy files
        if not self.copy_application_files():
            return False
        
        # Step 6: Virtual environment
        venv_path = self.create_virtual_environment()
        if not venv_path:
            return False
        
        # Step 7: Install dependencies
        if not self.install_dependencies(venv_path):
            self.print_warning("Some dependencies failed to install, but continuing...")
        
        # Step 8: Create shortcuts
        if not self.create_shortcuts(venv_path):
            self.print_warning("Some shortcuts were not created")
        
        # Step 9: Registry registration
        self.register_in_registry(venv_path)
        
        # Step 10: Create uninstaller
        self.create_uninstaller()
        
        # Installation complete
        self.print_step(12, "Installation Complete")
        print(f"\n{Colors.GREEN}{Colors.BOLD}[OK] Installation Successful!{Colors.END}\n")
        
        print(f"Product:          {PRODUCT_NAME}")
        print(f"Version:          {PRODUCT_VERSION}")
        print(f"Install Location: {self.install_dir}")
        print(f"Python:           {sys.version_info.major}.{sys.version_info.minor}")
        print(f"Date:             {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        print(f"{Colors.CYAN}Next Steps:{Colors.END}")
        print("1. Check your Desktop for the application shortcut")
        print("2. Click to launch Gaybeck Starkids SMS")
        print("3. Login with your administrator account")
        print("4. Start managing your school data\n")
        
        print(f"{Colors.BLUE}Quick Launch:{Colors.END}")
        desktop_shortcut = Path.home() / "Desktop" / f"{PRODUCT_NAME}.lnk"
        if desktop_shortcut.exists():
            print(f"Shortcut: {desktop_shortcut}\n")
        
        print(f"{Colors.WARNING}Support:{Colors.END}")
        print(f"Documentation:  {self.install_dir}\\docs\\")
        print(f"Uninstall:      {self.install_dir}\\Uninstall.bat\n")
        
        input(f"{Colors.BOLD}Press Enter to close this window...{Colors.END}")
        return True

def main():
    """Main installer entry point"""
    installer = GaybeckInstaller()
    success = installer.run_installation()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
