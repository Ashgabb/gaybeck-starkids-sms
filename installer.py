"""
Gaybeck Starkids SMS - Standalone Installer
Version: 2.0
Purpose: Deploy complete SMS application to any Windows device with admin notifications
"""

import os
import sys
import json
import shutil
import subprocess
import platform
import logging
import socket
import ctypes
import importlib.util
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import requests
import zipfile
import io

# ============================================================================
# CONFIGURATION
# ============================================================================

APP_NAME = "Gaybeck Starkids SMS"
APP_VERSION = "2.0"
PYTHON_MIN_VERSION = (3, 8)
PYTHON_RECOMMENDED = (3, 13)
MIN_DISK_SPACE_GB = 2  # Minimum required disk space in GB
MIN_RAM_GB = 4

# Required files/folders to validate
REQUIRED_FILES = [
    'sms.py',
    'requirements.txt',
    'database/school_management.db',
]

REQUIRED_PACKAGES = [
    'tkinter',  # Usually included with Python
    'pillow',
    'reportlab',
    'pandas',
    'numpy',
    'scikit-learn',
    'tkcalendar',
    'opencv-python',
]

PACKAGE_IMPORT_MAP = {
    'pillow': 'PIL',
    'reportlab': 'reportlab',
    'pandas': 'pandas',
    'numpy': 'numpy',
    'scikit-learn': 'sklearn',
    'tkcalendar': 'tkcalendar',
    'opencv-python': 'cv2',
    'opencv-contrib-python': 'cv2',
    'schedule': 'schedule',
    'openpyxl': 'openpyxl',
    'pywin32': 'win32api',
}

# ============================================================================
# LOGGER SETUP
# ============================================================================

def setup_logger():
    """Setup logging for installation process"""
    log_dir = Path.home() / ".gaybeck_sms" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    log_file = log_dir / f"install_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__), str(log_file)

logger, LOG_FILE = setup_logger()

# ============================================================================
# SYSTEM CHECKS
# ============================================================================

class SystemValidator:
    """Validate system requirements"""
    
    @staticmethod
    def check_python_version():
        """Check if Python version meets requirements"""
        current = sys.version_info[:2]
        if current < PYTHON_MIN_VERSION:
            return False, f"Python {'.'.join(map(str, current))} detected. Minimum required: {'.'.join(map(str, PYTHON_MIN_VERSION))}"
        
        is_recommended = current >= PYTHON_RECOMMENDED
        msg = f"Python {'.'.join(map(str, current))} detected. {'✓ Recommended version' if is_recommended else '(Older version, may have compatibility issues)'}"
        return True, msg
    
    @staticmethod
    def check_disk_space(path=None):
        """Check available disk space"""
        if path is None:
            path = Path.home() / "AppData" / "Local" if platform.system() == "Windows" else Path.home()
        
        path.mkdir(parents=True, exist_ok=True)
        stat = shutil.disk_usage(path)
        available_gb = stat.free / (1024**3)
        
        if available_gb < MIN_DISK_SPACE_GB:
            return False, f"Only {available_gb:.1f}GB available. Minimum required: {MIN_DISK_SPACE_GB}GB"
        
        return True, f"Disk space available: {available_gb:.1f}GB"
    
    @staticmethod
    def check_python_executable():
        """Check if python command is available in PATH"""
        try:
            result = subprocess.run(['python', '--version'], capture_output=True, text=True)
            return result.returncode == 0, result.stdout.strip()
        except FileNotFoundError:
            return False, "Python not found in PATH"
    
    @staticmethod
    def check_pip_available():
        """Check if pip is available"""
        try:
            result = subprocess.run(['pip', '--version'], capture_output=True, text=True)
            return result.returncode == 0, result.stdout.strip()
        except FileNotFoundError:
            return False, "pip not found in PATH"

    @staticmethod
    def check_os_support():
        """Validate supported operating system"""
        current_os = platform.system()
        if current_os != "Windows":
            return False, f"Detected OS: {current_os}. This installer currently supports Windows only."
        return True, f"Detected OS: {current_os}"

    @staticmethod
    def check_ram():
        """Check minimum RAM availability"""
        try:
            total_gb = 0.0
            if platform.system() == 'Windows':
                class MEMORYSTATUSEX(ctypes.Structure):
                    _fields_ = [
                        ('dwLength', ctypes.c_ulong),
                        ('dwMemoryLoad', ctypes.c_ulong),
                        ('ullTotalPhys', ctypes.c_ulonglong),
                        ('ullAvailPhys', ctypes.c_ulonglong),
                        ('ullTotalPageFile', ctypes.c_ulonglong),
                        ('ullAvailPageFile', ctypes.c_ulonglong),
                        ('ullTotalVirtual', ctypes.c_ulonglong),
                        ('ullAvailVirtual', ctypes.c_ulonglong),
                        ('ullAvailExtendedVirtual', ctypes.c_ulonglong),
                    ]

                stat = MEMORYSTATUSEX()
                stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
                ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
                total_gb = stat.ullTotalPhys / (1024 ** 3)
            else:
                return True, "RAM check skipped on non-Windows host"

            if total_gb < MIN_RAM_GB:
                return False, f"RAM detected: {total_gb:.1f}GB. Minimum recommended: {MIN_RAM_GB}GB"
            return True, f"RAM detected: {total_gb:.1f}GB"
        except Exception as e:
            return False, f"Unable to verify RAM: {e}"

    @staticmethod
    def check_internet():
        """Check internet availability for package installation"""
        try:
            socket.create_connection(("pypi.org", 443), timeout=5)
            return True, "Internet connection is available"
        except OSError:
            return False, "Internet connection unavailable. Package installation may fail."


class InstallerGUI:
    """GUI for installation process"""
    
    def __init__(self, root):
        self.root = root
        self.root.title(f"{APP_NAME} v{APP_VERSION} - Installer")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        
        self.setup_ui()
        self.installation_log = []
        self.errors = []
        
    def setup_ui(self):
        """Setup UI components"""
        # Header
        header = tk.Frame(self.root, bg='#2c3e50', height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title = tk.Label(header, text=f"🎓 {APP_NAME} Setup Wizard",
                        font=('Segoe UI', 18, 'bold'), bg='#2c3e50', fg='white')
        title.pack(pady=10)
        
        subtitle = tk.Label(header, text=f"Version {APP_VERSION} - Installing to your device",
                           font=('Segoe UI', 10), bg='#2c3e50', fg='#bdc3c7')
        subtitle.pack()
        
        # Main content
        content = ttk.Frame(self.root)
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Progress section
        progress_label = tk.Label(content, text="Installation Progress", font=('Segoe UI', 12, 'bold'))
        progress_label.pack(anchor='w', pady=(0, 10))
        
        self.progress = ttk.Progressbar(content, mode='determinate', length=400)
        self.progress.pack(fill=tk.X, pady=(0, 15))
        
        # Status log
        log_label = tk.Label(content, text="Status Log", font=('Segoe UI', 11, 'bold'))
        log_label.pack(anchor='w', pady=(10, 5))
        
        # Scrollable log area
        log_frame = ttk.Frame(content)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        scrollbar = ttk.Scrollbar(log_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_text = tk.Text(log_frame, height=10, width=80, wrap=tk.WORD,
                               yscrollcommand=scrollbar.set, font=('Courier New', 9))
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.log_text.yview)
        self.log_text.config(state=tk.DISABLED)
        
        # Button frame
        button_frame = ttk.Frame(content)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.start_btn = ttk.Button(button_frame, text="Start Installation", command=self.start_installation)
        self.start_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.close_btn = ttk.Button(button_frame, text="Close", command=self.on_close, state=tk.DISABLED)
        self.close_btn.pack(side=tk.LEFT)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready for installation")
        status = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status.pack(fill=tk.X, side=tk.BOTTOM, padx=2, pady=2)
    
    def log_message(self, message, level="INFO"):
        """Log message to GUI and file"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted = f"[{timestamp}] {message}"
        
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, formatted + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        self.installation_log.append(formatted)
        logger.info(message)
        
        if level == "ERROR":
            self.errors.append(message)
    
    def update_progress(self, value):
        """Update progress bar"""
        self.progress['value'] = value
        self.root.update_idletasks()
    
    def update_status(self, message):
        """Update status bar"""
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def start_installation(self):
        """Start installation in separate thread"""
        self.start_btn.config(state=tk.DISABLED)
        self.log_message("=== Gaybeck SMS Installation Started ===", "INFO")
        
        # Run installation in separate thread to prevent UI freezing
        install_thread = threading.Thread(target=self.run_installation)
        install_thread.daemon = True
        install_thread.start()
    
    def run_installation(self):
        """Run full installation process"""
        try:
            steps = [
                ("Validating System Requirements", self.validate_system),
                ("Selecting Installation Directory", self.select_install_dir),
                ("Preparing Installation Files", self.prepare_files),
                ("Installing Python Dependencies", self.install_dependencies),
                ("Verifying Runtime Requirements", self.verify_runtime_requirements),
                ("Creating Application Shortcuts", self.create_shortcuts),
                ("Finalizing Installation", self.finalize),
            ]
            
            total_steps = len(steps)
            
            for i, (step_name, step_func) in enumerate(steps):
                self.update_status(step_name)
                self.log_message(f"\n>>> {step_name}...", "INFO")
                
                if not step_func():
                    self.log_message(f"✗ Installation failed at step: {step_name}", "ERROR")
                    self.show_error_report()
                    return
                
                self.update_progress((i + 1) / total_steps * 100)
            
            self.installation_complete()
            
        except Exception as e:
            self.log_message(f"Unexpected error: {str(e)}", "ERROR")
            self.errors.append(str(e))
            self.show_error_report()
    
    def validate_system(self):
        """Validate system requirements"""
        checks = [
            ("Operating System", SystemValidator.check_os_support),
            ("Python Version", SystemValidator.check_python_version),
            ("Python Executable", SystemValidator.check_python_executable),
            ("pip Package Manager", SystemValidator.check_pip_available),
            ("System RAM", SystemValidator.check_ram),
            ("Disk Space", SystemValidator.check_disk_space),
            ("Internet Connection", SystemValidator.check_internet),
        ]
        
        all_passed = True
        for check_name, check_func in checks:
            passed, message = check_func()
            status = "✓" if passed else "✗"
            self.log_message(f"  {status} {check_name}: {message}")
            if not passed:
                all_passed = False
        
        if not all_passed:
            self.log_message("System validation failed. Please check requirements.", "ERROR")
            return False
        
        return True
    
    def select_install_dir(self):
        """Let user select installation directory"""
        if platform.system() == "Windows":
            default_path = Path.home() / "AppData" / "Local" / "Gaybeck_SMS"
        else:
            default_path = Path.home() / "Gaybeck_SMS"
        
        default_path.mkdir(parents=True, exist_ok=True)
        
        self.install_dir = str(default_path)
        self.log_message(f"Installation directory: {self.install_dir}")
        
        # Check if directory is writable
        try:
            test_file = Path(self.install_dir) / ".write_test"
            test_file.touch()
            test_file.unlink()
            return True
        except Exception as e:
            self.log_message(f"Cannot write to {self.install_dir}: {str(e)}", "ERROR")
            return False
    
    def prepare_files(self):
        """Prepare and copy application files"""
        try:
            source_dir = Path(__file__).parent
            target_dir = Path(self.install_dir)
            
            # List of directories and files to copy
            items_to_copy = [
                'sms.py',
                'requirements.txt',
                'database',
                'docs',
                'backups',
                'database_backups',
                'biometric_data',
                'logs',
                'reports',
                'restore_points',
                'scripts',
                'tests',
                'ui_components.py',
                'realtime_sync.py',
                'advanced_ai_analytics.py',
                'ai_assessment_grading.py',
                'ai_learning_support.py',
                'ai_learning_ui.py',
                'ai_tutor_service.py',
                'biometric_auth.py',
                'biometric_ui.py',
                'enhanced_ews.py',
                'hr_manager.py',
                'initialize_hr_database.py',
                'notification_service.py',
                'teacher_learning_sync.py',
                'launch_sms.bat',
                'run_app.bat',
                'run_app.py',
                'launch_app.py',
                'setup.bat',
                'setup_portable.py',
            ]
            
            copied_count = 0
            for item in items_to_copy:
                source = source_dir / item
                if not source.exists():
                    self.log_message(f"  ⚠ Warning: {item} not found in source")
                    continue
                
                target = target_dir / item
                
                try:
                    if source.is_dir():
                        if target.exists():
                            shutil.rmtree(target)
                        shutil.copytree(source, target)
                    else:
                        target.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(source, target)
                    
                    copied_count += 1
                    self.log_message(f"  ✓ Copied: {item}")
                except Exception as e:
                    self.log_message(f"  ✗ Failed to copy {item}: {str(e)}", "ERROR")
                    return False
            
            self.log_message(f"Successfully copied {copied_count} files/folders")
            return True
            
        except Exception as e:
            self.log_message(f"File preparation failed: {str(e)}", "ERROR")
            return False
    
    def install_dependencies(self):
        """Install Python packages from requirements.txt"""
        try:
            req_file = Path(self.install_dir) / "requirements.txt"
            
            if not req_file.exists():
                self.log_message("requirements.txt not found, skipping pip installation", "WARNING")
                return True
            
            self.log_message("Installing Python packages (this may take 2-5 minutes)...")
            
            cmd = [sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip']
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                self.log_message(f"pip upgrade warning: {result.stderr}", "WARNING")
            
            cmd = [sys.executable, '-m', 'pip', 'install', '--upgrade', '-r', str(req_file)]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                self.log_message(f"Dependency installation failed: {result.stderr}", "ERROR")
                return False
            
            self.log_message("✓ All dependencies installed successfully")
            return True
            
        except Exception as e:
            self.log_message(f"Dependency installation error: {str(e)}", "ERROR")
            return False

    def verify_runtime_requirements(self):
        """Verify and remediate runtime imports after pip installation"""
        try:
            req_file = Path(self.install_dir) / "requirements.txt"
            if not req_file.exists():
                self.log_message("requirements.txt missing; runtime verification skipped", "WARNING")
                return True

            packages = self._parse_requirements(req_file)
            missing = self._get_missing_packages(packages)

            if not missing:
                self.log_message("✓ Runtime requirement verification passed")
                return True

            self.log_message(f"Missing runtime packages detected: {', '.join(missing)}", "WARNING")
            self.log_message("Attempting remediation installation for missing packages...")

            cmd = [sys.executable, '-m', 'pip', 'install'] + missing
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                self.log_message(f"Runtime package remediation failed: {result.stderr}", "ERROR")
                return False

            still_missing = self._get_missing_packages(packages)
            if still_missing:
                self.log_message(f"Still missing after remediation: {', '.join(still_missing)}", "ERROR")
                return False

            self.log_message("✓ Runtime requirements verified and remediated")
            return True
        except Exception as e:
            self.log_message(f"Runtime verification error: {str(e)}", "ERROR")
            return False

    def _parse_requirements(self, req_file):
        """Parse installable package names from requirements.txt"""
        packages = []
        with open(req_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if line.startswith('-'):
                    continue
                normalized = line.split(';')[0].strip()
                for sep in ['>=', '==', '<=', '~=', '!=', '>', '<']:
                    if sep in normalized:
                        normalized = normalized.split(sep)[0].strip()
                        break
                if normalized:
                    packages.append(normalized.lower())
        return packages

    def _get_missing_packages(self, packages):
        """Return package names whose mapped import cannot be resolved"""
        missing = []
        for package in packages:
            module_name = PACKAGE_IMPORT_MAP.get(package, package.replace('-', '_'))
            if importlib.util.find_spec(module_name) is None:
                missing.append(package)
        return missing
    
    def create_shortcuts(self):
        """Create application shortcuts"""
        try:
            if platform.system() != "Windows":
                self.log_message("Shortcuts creation skipped (non-Windows system)")
                return True
            
            # Create desktop shortcut
            desktop = Path.home() / "Desktop"
            shortcut_path = desktop / "Gaybeck SMS.lnk"
            
            app_path = Path(self.install_dir) / "run_app.bat"
            
            # Create shortcut using VBScript approach
            vbs_content = f'''
Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "{shortcut_path}"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "{app_path}"
oLink.WorkingDirectory = "{self.install_dir}"
oLink.Description = "Gaybeck Starkids SMS v{APP_VERSION}"
oLink.IconLocation = "{Path(self.install_dir) / 'sms.py'}"
oLink.Save
'''
            
            vbs_file = Path(self.install_dir) / "create_shortcut.vbs"
            vbs_file.write_text(vbs_content)
            
            subprocess.run(['cscript', str(vbs_file)], capture_output=True)
            vbs_file.unlink()
            
            self.log_message(f"✓ Desktop shortcut created")
            return True
            
        except Exception as e:
            self.log_message(f"Shortcut creation warning: {str(e)}", "WARNING")
            return True  # Non-critical
    
    def finalize(self):
        """Finalize installation"""
        try:
            self.log_message("Creating configuration and initialization files...")
            
            # Create startup script
            startup_script = Path(self.install_dir) / "FIRST_RUN.bat"
            startup_script.write_text(f"@echo off\ncd /d \"{self.install_dir}\"\npython sms.py\npause\n")
            
            # Create installation report
            self.create_installation_report()
            
            self.log_message("✓ Installation finalized")
            return True
            
        except Exception as e:
            self.log_message(f"Finalization error: {str(e)}", "ERROR")
            return False
    
    def create_installation_report(self):
        """Create installation report for admin"""
        try:
            report = {
                'app_name': APP_NAME,
                'version': APP_VERSION,
                'install_date': datetime.now().isoformat(),
                'install_path': self.install_dir,
                'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
                'platform': platform.platform(),
                'installation_log': self.installation_log,
                'errors': self.errors,
                'status': 'SUCCESS' if not self.errors else 'SUCCESS_WITH_WARNINGS',
            }
            
            report_path = Path(self.install_dir) / "INSTALLATION_REPORT.json"
            with open(report_path, 'w') as f:
                json.dump(report, f, indent=2)
            
            # Also create text version
            text_report = Path(self.install_dir) / "INSTALLATION_REPORT.txt"
            text_report.write_text(
                f"{'='*70}\n"
                f"Gaybeck SMS Installation Report\n"
                f"{'='*70}\n\n"
                f"Installation Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"Application: {APP_NAME} v{APP_VERSION}\n"
                f"Installation Path: {self.install_dir}\n"
                f"Python Version: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}\n"
                f"Platform: {platform.platform()}\n\n"
                f"Installation Log:\n"
                f"{'-'*70}\n"
                + '\n'.join(self.installation_log) +
                f"\n{'-'*70}\n\n"
                f"Status: {'SUCCESSFUL' if not self.errors else 'COMPLETED WITH WARNINGS'}\n"
                f"Errors/Warnings: {len(self.errors)}\n"
            )
            
            logger.info(f"Installation report created at {report_path}")
            
        except Exception as e:
            logger.error(f"Failed to create installation report: {str(e)}")
    
    def installation_complete(self):
        """Show completion message"""
        self.update_progress(100)
        self.update_status("Installation Completed Successfully!")
        
        self.log_message("\n=== Installation Completed Successfully! ===", "INFO")
        self.log_message(f"Installation Path: {self.install_dir}", "INFO")
        self.log_message("Default Credentials:", "INFO")
        self.log_message("  Username: admin", "INFO")
        self.log_message("  Password: admin123", "INFO")
        self.log_message("\nTo launch the application:", "INFO")
        self.log_message("  1. Double-click the 'Gaybeck SMS' shortcut on your desktop", "INFO")
        self.log_message("  2. Or navigate to installation folder and run 'run_app.bat'", "INFO")
        
        self.start_btn.config(state=tk.NORMAL, text="Done")
        self.close_btn.config(state=tk.NORMAL)
        
        messagebox.showinfo("Installation Complete",
                           f"{APP_NAME} has been installed successfully!\n\n"
                           f"Installation Path: {self.install_dir}\n\n"
                           f"Default Credentials:\n"
                           f"Username: admin\n"
                           f"Password: admin123\n\n"
                           f"You can now launch the application from the desktop shortcut.")
    
    def show_error_report(self):
        """Show error report"""
        self.start_btn.config(state=tk.NORMAL, text="Retry")
        self.close_btn.config(state=tk.NORMAL)
        
        error_msg = "\n".join(self.errors) if self.errors else "Unknown error occurred"
        messagebox.showerror("Installation Failed",
                            f"Installation encountered errors:\n\n{error_msg}\n\n"
                            f"Check the log for details.\n"
                            f"Log file: {LOG_FILE}")
    
    def on_close(self):
        """Handle window close"""
        self.root.quit()
        self.root.destroy()


def main():
    """Main entry point"""
    root = tk.Tk()
    gui = InstallerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
