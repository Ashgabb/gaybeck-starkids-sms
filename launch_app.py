#!/usr/bin/env python3
"""
Gaybeck Starkids SMS - Desktop Application Launcher
Version: 2.0.0 (Portable Edition)
Purpose: Launch the SMS application with proper environment setup
Portability: Works on any device with Python installed
"""

import os
import sys
import subprocess
import json
import logging
from pathlib import Path
from datetime import datetime


class SMSLauncher:
    """Handles launching the SMS application - Portable Edition"""
    
    def __init__(self):
        """Initialize the launcher"""
        self.app_dir = Path(__file__).parent.resolve()
        self.sms_file = self.app_dir / "sms.py"
        self.log_dir = self.app_dir / "logs"
        self.log_file = self.log_dir / f"launch_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        self.silent_mode = self.check_silent_mode()
        
        # Setup logging
        self.log_dir.mkdir(exist_ok=True)
        self.setup_logging()
    
    def check_silent_mode(self):
        """Detect if running in silent mode (no console output expected)"""
        return not sys.stdout.isatty()
    
    def setup_logging(self):
        """Setup logging for the launcher"""
        handlers = [logging.FileHandler(self.log_file)]
        
        # Only add console output if not in silent/GUI mode
        if not self.silent_mode:
            handlers.append(logging.StreamHandler())
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=handlers
        )
        self.logger = logging.getLogger(__name__)
    
    def check_environment(self):
        """Check if the environment is ready to run the app"""
        self.logger.info("=" * 60)
        self.logger.info("Gaybeck Starkids SMS - Application Launcher")
        self.logger.info("=" * 60)
        
        # Check if sms.py exists
        if not self.sms_file.exists():
            self.logger.error(f"[ERROR] SMS file not found: {self.sms_file}")
            return False
        
        self.logger.info(f"[OK] SMS file found: {self.sms_file}")
        
        # Check Python version
        python_version = sys.version_info
        self.logger.info(f"[OK] Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
        
        if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
            self.logger.warning("[WARN] Python 3.8+ is recommended for best compatibility")
        
        # Check if database exists
        db_path = self.app_dir / "database" / "school.db"
        if not db_path.exists():
            self.logger.warning(f"[WARN] Database not found at {db_path}")
            self.logger.info("  The app will create it on first run")
        else:
            self.logger.info(f"[OK] Database found: {db_path}")
        
        return True
    
    def check_dependencies(self):
        """Check if required Python packages are installed"""
        required_packages = {
            'tkinter': 'Python standard library',
            'sqlite3': 'Python standard library',
        }
        
        optional_packages = {
            'tkcalendar': 'Date picker widget',
            'reportlab': 'PDF generation',
            'PIL': 'Image processing (pillow)',
            'cv2': 'Camera support (opencv-python)',
            'numpy': 'Numerical computing',
            'pandas': 'Data analysis',
            'scikit-learn': 'Machine learning',
        }
        
        self.logger.info("\nChecking required packages...")
        for package, description in required_packages.items():
            try:
                __import__(package)
                self.logger.info(f"[OK] {package}: OK ({description})")
            except ImportError:
                self.logger.error(f"[ERROR] {package}: MISSING ({description})")
                return False
        
        self.logger.info("\nChecking optional packages...")
        for package, description in optional_packages.items():
            try:
                __import__(package)
                self.logger.info(f"[OK] {package}: Available ({description})")
            except ImportError:
                self.logger.warning(f"[WARN] {package}: Not installed ({description})")
        
        return True
    
    def launch_app(self):
        """Launch the SMS application - Portable Edition"""
        try:
            self.logger.info("\n" + "=" * 60)
            self.logger.info("Launching SMS Application...")
            self.logger.info("=" * 60)
            
            # Try multiple Python executables for maximum compatibility
            python_executables = []
            
            if sys.platform == "win32":
                # Windows: try pythonw first (no console), then python
                python_executables = [
                    "pythonw.exe",
                    "pythonw",
                    "python.exe",
                    "python",
                    sys.executable  # Fallback to current Python interpreter
                ]
            else:
                # Linux/Mac: try python directly
                python_executables = [
                    "python3",
                    "python",
                    sys.executable
                ]
            
            # Try each Python executable
            last_error = None
            for python_exe in python_executables:
                try:
                    self.logger.info(f"Trying Python executable: {python_exe}")
                    
                    # Launch the application
                    if sys.platform == "win32" and python_exe in ["pythonw.exe", "pythonw"]:
                        # Hide console window on Windows
                        process = subprocess.Popen(
                            [python_exe, str(self.sms_file)],
                            cwd=str(self.app_dir),
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                            creationflags=0x08000000 if sys.platform == "win32" else 0
                        )
                    else:
                        process = subprocess.Popen(
                            [python_exe, str(self.sms_file)],
                            cwd=str(self.app_dir)
                        )
                    
                    self.logger.info(f"[OK] Application launched with {python_exe} (PID: {process.pid})")
                    self.logger.info("[OK] SMS window should appear in a moment...")
                    return process
                    
                except (FileNotFoundError, OSError) as e:
                    last_error = e
                    self.logger.debug(f"Python executable '{python_exe}' not available: {str(e)}")
                    continue
            
            # If all executables failed, report the error
            if last_error:
                self.logger.error(f"[ERROR] Could not find any working Python executable")
                self.logger.error(f"Last error: {str(last_error)}")
                self.logger.info("Please ensure Python is properly installed and added to PATH")
            
            return None
            
        except Exception as e:
            self.logger.error(f"[ERROR] Failed to launch application: {str(e)}")
            return None
    
    def run(self):
        """Run the launcher"""
        try:
            # Check environment
            if not self.check_environment():
                self.logger.error("Environment check failed. Cannot proceed.")
                input("Press Enter to exit...")
                return False
            
            # Check dependencies
            if not self.check_dependencies():
                self.logger.warning("Some required packages are missing.")
                self.logger.info("Run: pip install -r requirements.txt")
                input("Press Enter to exit...")
                return False
            
            # Launch application
            process = self.launch_app()
            if not process:
                input("Press Enter to exit...")
                return False
            
            self.logger.info(f"\nLog file: {self.log_file}")
            self.logger.info("Application is running. You can close this window.")
            
            return True
        
        except Exception as e:
            self.logger.error(f"Fatal error: {str(e)}")
            input("Press Enter to exit...")
            return False


def main():
    """Main entry point"""
    launcher = SMSLauncher()
    success = launcher.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
