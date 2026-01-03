#!/usr/bin/env python3
"""
Gaybeck Starkids SMS - Installation Setup Script
Creates standalone installation for Windows, macOS, and Linux
Cross-platform build automation

Usage:
    python setup.py build
    python setup.py install
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

class Installer:
    def __init__(self):
        self.platform = platform.system()
        self.project_root = Path(__file__).parent
        self.build_dir = self.project_root / "build"
        self.dist_dir = self.project_root / "dist"
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def print_header(self):
        """Print welcome header"""
        print("\n" + "="*60)
        print("  Gaybeck Starkids SMS - Installation Builder")
        print("  Version: 2.0.3")
        print(f"  Platform: {self.platform}")
        print("="*60 + "\n")
        
    def check_python(self):
        """Verify Python version"""
        print("Checking Python version...")
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 13):
            print(f"✗ Python 3.13+ required (you have {version.major}.{version.minor})")
            print("  Download from: https://www.python.org")
            sys.exit(1)
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} detected\n")
        
    def check_dependencies(self):
        """Check required tools"""
        print("Checking dependencies...")
        
        # Check PyInstaller
        try:
            import PyInstaller
            print("✓ PyInstaller found")
        except ImportError:
            print("✗ PyInstaller not found - installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller>=6.0"])
            
        # Check for build requirements
        requirements_file = self.project_root / "requirements.txt"
        if requirements_file.exists():
            print("✓ requirements.txt found")
            print("  Installing dependencies...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)])
        else:
            print("! requirements.txt not found")
        print()
        
    def clean_build(self):
        """Clean previous builds"""
        print("Cleaning previous builds...")
        
        for dir_path in [self.build_dir, self.dist_dir]:
            if dir_path.exists():
                shutil.rmtree(dir_path)
                print(f"✓ Removed {dir_path.name}/")
                
        # Clean .spec files
        for spec_file in self.project_root.glob("*.spec"):
            if spec_file.name != "build_config.spec":
                spec_file.unlink()
        print()
        
    def build_executable(self):
        """Build standalone executable"""
        print("Building standalone executable...")
        print("(This may take 2-3 minutes)\n")
        
        spec_file = self.project_root / "build_config.spec"
        if not spec_file.exists():
            print(f"✗ {spec_file.name} not found")
            sys.exit(1)
            
        try:
            subprocess.check_call([
                sys.executable, "-m", "PyInstaller",
                str(spec_file),
                "--onedir"
            ])
            print("\n✓ Build successful!\n")
        except subprocess.CalledProcessError as e:
            print(f"\n✗ Build failed: {e}\n")
            sys.exit(1)
            
    def verify_build(self):
        """Verify build output"""
        print("Verifying build...")
        
        if self.platform == "Windows":
            exe_path = self.dist_dir / "GaybeckStarKidsSMS" / "GaybeckStarKidsSMS.exe"
        else:
            exe_path = self.dist_dir / "GaybeckStarKidsSMS" / "GaybeckStarKidsSMS"
            
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"✓ Executable created successfully")
            print(f"  Location: {exe_path}")
            print(f"  Size: {size_mb:.1f} MB\n")
            return True
        else:
            print(f"✗ Executable not found at {exe_path}\n")
            return False
            
    def create_package(self):
        """Create distribution package"""
        print("Creating distribution package...")
        
        app_dir = self.dist_dir / "GaybeckStarKidsSMS"
        if not app_dir.exists():
            print("✗ Application directory not found\n")
            return False
            
        try:
            if self.platform == "Windows":
                # Create ZIP archive
                zip_name = f"GaybeckStarKidsSMS_Windows_{self.timestamp}.zip"
                zip_path = self.dist_dir / zip_name
                shutil.make_archive(str(zip_path.with_suffix("")), 'zip', app_dir.parent, app_dir.name)
                print(f"✓ Created: {zip_name}\n")
                
            elif self.platform == "Darwin":  # macOS
                # Create ZIP archive
                zip_name = f"GaybeckStarKidsSMS_macOS_{self.timestamp}.zip"
                zip_path = self.dist_dir / zip_name
                shutil.make_archive(str(zip_path.with_suffix("")), 'zip', app_dir.parent, app_dir.name)
                print(f"✓ Created: {zip_name}")
                print("  (For distribution, consider creating a .dmg file)\n")
                
            elif self.platform == "Linux":
                # Create TAR.GZ archive
                tar_name = f"GaybeckStarKidsSMS_linux_{self.timestamp}.tar.gz"
                tar_path = self.dist_dir / tar_name
                shutil.make_archive(str(tar_path.with_suffix("")), 'gztar', app_dir.parent, app_dir.name)
                print(f"✓ Created: {tar_name}\n")
                
            return True
        except Exception as e:
            print(f"✗ Package creation failed: {e}\n")
            return False
            
    def print_summary(self):
        """Print build summary"""
        print("="*60)
        print("  BUILD COMPLETE!")
        print("="*60)
        print()
        print("📁 Output Location:")
        print(f"   {self.dist_dir}/")
        print()
        
        if self.platform == "Windows":
            exe = self.dist_dir / "GaybeckStarKidsSMS" / "GaybeckStarKidsSMS.exe"
            print("🚀 To Run:")
            print(f"   {exe}")
            print()
            print("📦 To Create Installer:")
            print("   1. Install NSIS: https://nsis.sourceforge.io")
            print("   2. Run: installer.nsi (right-click → Compile)")
            print("   3. This creates: GaybeckStarKidsSMS_Installer_2.0.3.exe")
        else:
            exe = self.dist_dir / "GaybeckStarKidsSMS" / "GaybeckStarKidsSMS"
            print("🚀 To Run:")
            print(f"   {exe}")
            print()
            if self.platform == "Darwin":
                print("📦 For macOS Distribution:")
                print("   Create .dmg file for professional distribution")
            else:
                print("📦 For Linux Distribution:")
                print("   Archive is ready: GaybeckStarKidsSMS_linux_*.tar.gz")
                
        print()
        print("📚 Documentation:")
        print("   See: INSTALLATION_GUIDE.md")
        print()
        print("="*60 + "\n")
        
    def run(self):
        """Execute full build process"""
        try:
            self.print_header()
            self.check_python()
            self.check_dependencies()
            self.clean_build()
            self.build_executable()
            
            if self.verify_build():
                self.create_package()
                self.print_summary()
                print("✓ Installation build successful!")
                return 0
            else:
                print("✗ Build verification failed")
                return 1
                
        except KeyboardInterrupt:
            print("\n\n✗ Build cancelled by user")
            return 1
        except Exception as e:
            print(f"\n✗ Unexpected error: {e}")
            return 1

def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] in ['build', 'install', 'clean']:
        command = sys.argv[1]
        installer = Installer()
        
        if command == 'clean':
            installer.clean_build()
            print("✓ Cleanup complete\n")
        else:
            return installer.run()
    else:
        installer = Installer()
        return installer.run()

if __name__ == "__main__":
    sys.exit(main() or 0)
