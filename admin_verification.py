"""
Gaybeck SMS - Installation Verification & Admin Tools
Purpose: Verify installation status and generate admin reports
For: Administrators to validate deployments and troubleshoot issues
"""

import os
import sys
import json
import subprocess
import platform
from pathlib import Path
from datetime import datetime

def print_header():
    print("\n" + "="*80)
    print("Gaybeck Starkids SMS - Installation Verification & Admin Report")
    print("="*80 + "\n")

def print_section(title):
    print(f"\n{'─'*80}")
    print(f"  {title}")
    print(f"{'─'*80}")

def check_python():
    """Check Python installation and version"""
    print_section("1. Python Installation")
    
    print(f"✓ Python Version: {sys.version}")
    print(f"✓ Executable: {sys.executable}")
    print(f"✓ Version Info: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    # Check if version is recommended
    if sys.version_info >= (3, 13):
        print(f"  ✓ Status: Recommended version (3.13+)")
        return True
    elif sys.version_info >= (3, 8):
        print(f"  ⚠ Status: Supported but older than recommended (3.8-3.12)")
        return True
    else:
        print(f"  ✗ Status: NOT SUPPORTED (minimum 3.8 required)")
        return False

def check_pip():
    """Check pip installation"""
    print_section("2. Package Manager (pip)")
    
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✓ pip is available: {result.stdout.strip()}")
            return True
        else:
            print(f"✗ pip not functional: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Error checking pip: {str(e)}")
        return False

def check_packages():
    """Check installed Python packages"""
    print_section("3. Required Python Packages")
    
    required_packages = {
        'PIL': 'Pillow (Image Processing)',
        'reportlab': 'ReportLab (PDF Generation)',
        'pandas': 'Pandas (Data Analysis)',
        'numpy': 'NumPy (Numerical Computing)',
        'sklearn': 'Scikit-Learn (Machine Learning)',
        'tkcalendar': 'TKCalendar (Calendar Widget)',
        'cv2': 'OpenCV (Computer Vision)',
    }
    
    all_found = True
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', 'list'], 
                              capture_output=True, text=True, timeout=10)
        installed = result.stdout.lower()
        
        for pkg_name, pkg_desc in required_packages.items():
            if pkg_name.lower() in installed:
                print(f"  ✓ {pkg_desc}")
            else:
                print(f"  ✗ {pkg_desc} (MISSING)")
                all_found = False
        
        return all_found
    except Exception as e:
        print(f"✗ Error checking packages: {str(e)}")
        return False

def check_installation_directory():
    """Check SMS installation directory"""
    print_section("4. Installation Directory")
    
    if platform.system() == "Windows":
        install_paths = [
            Path.home() / "AppData" / "Local" / "Gaybeck_SMS",
            Path.home() / "Desktop" / "Gaybeck_SMS",
            Path.home() / "Gaybeck_SMS",
        ]
    else:
        install_paths = [
            Path.home() / "Gaybeck_SMS",
            Path.home() / ".gaybeck_sms",
        ]
    
    found = False
    for path in install_paths:
        if path.exists():
            print(f"✓ Found: {path}")
            
            # Check for key files
            required_files = ['sms.py', 'requirements.txt']
            all_present = True
            for file in required_files:
                file_path = path / file
                if file_path.exists():
                    print(f"    ✓ {file}")
                else:
                    print(f"    ✗ {file} (MISSING)")
                    all_present = False
            
            # Check database directory
            db_dir = path / "database"
            if db_dir.exists():
                print(f"    ✓ database/ directory")
                db_file = db_dir / "school_management.db"
                if db_file.exists():
                    size_mb = db_file.stat().st_size / (1024*1024)
                    print(f"      ✓ Database: {size_mb:.2f} MB")
                else:
                    print(f"      ⚠ Database not found (will be created on first run)")
            else:
                print(f"    ✗ database/ directory (MISSING)")
                all_present = False
            
            # Check for installation report
            report_path = path / "INSTALLATION_REPORT.json"
            if report_path.exists():
                with open(report_path) as f:
                    report = json.load(f)
                    print(f"    ✓ Installation Report")
                    print(f"      Date: {report.get('install_date', 'Unknown')}")
                    print(f"      Status: {report.get('status', 'Unknown')}")
            
            found = True
    
    if not found:
        print("✗ No installation directory found")
        print("  (SMS may not be installed or in a non-standard location)")
    
    return found

def check_database():
    """Check database status"""
    print_section("5. Database Status")
    
    if platform.system() == "Windows":
        db_paths = [
            Path.home() / "AppData" / "Local" / "Gaybeck_SMS" / "database" / "school_management.db",
            Path.home() / "Desktop" / "Gaybeck_SMS" / "database" / "school_management.db",
            Path.home() / "Gaybeck_SMS" / "database" / "school_management.db",
        ]
    else:
        db_paths = [
            Path.home() / "Gaybeck_SMS" / "database" / "school_management.db",
        ]
    
    for db_path in db_paths:
        if db_path.exists():
            try:
                size_mb = db_path.stat().st_size / (1024*1024)
                print(f"✓ Database found: {db_path}")
                print(f"  Size: {size_mb:.2f} MB")
                
                # Try to connect and verify
                try:
                    conn = __import__('sqlite3').connect(str(db_path))
                    cursor = conn.cursor()
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                    tables = cursor.fetchall()
                    print(f"  Tables: {len(tables)}")
                    conn.close()
                    return True
                except Exception as e:
                    print(f"  ⚠ Database connection warning: {str(e)}")
                    return True  # Still found, even if connection failed
            except Exception as e:
                print(f"  ✗ Error accessing database: {str(e)}")
    
    print("ℹ Database not found (will be created on first run)")
    return True  # Not critical for first-time setup

def check_shortcuts():
    """Check application shortcuts"""
    print_section("6. Application Shortcuts")
    
    if platform.system() == "Windows":
        desktop = Path.home() / "Desktop"
        shortcut = desktop / "Gaybeck SMS.lnk"
        
        if shortcut.exists():
            print(f"✓ Desktop shortcut found: Gaybeck SMS.lnk")
            return True
        else:
            print(f"✗ Desktop shortcut not found")
            print(f"  Location: {desktop / 'Gaybeck SMS.lnk'}")
            print(f"  (You can manually create it by running 'create_sms_shortcut.vbs')")
            return False
    else:
        print("⚠ Shortcut check skipped (non-Windows system)")
        return True

def check_logs():
    """Check installation logs"""
    print_section("7. Installation Logs")
    
    log_dir = Path.home() / ".gaybeck_sms" / "logs"
    
    if log_dir.exists():
        log_files = sorted(log_dir.glob("install_*.log"))
        if log_files:
            print(f"✓ Found {len(log_files)} installation log file(s)")
            latest = log_files[-1]
            print(f"  Latest: {latest.name}")
            print(f"  Created: {datetime.fromtimestamp(latest.stat().st_mtime)}")
            return True
        else:
            print("ℹ No installation logs found yet")
            return True
    else:
        print("ℹ Log directory not created (fresh installation)")
        return True

def check_disk_space():
    """Check available disk space"""
    print_section("8. System Disk Space")
    
    if platform.system() == "Windows":
        check_path = Path.home() / "AppData" / "Local"
    else:
        check_path = Path.home()
    
    try:
        stat = os.statvfs(str(check_path))
        available_gb = stat.f_bavail * stat.f_frsize / (1024**3)
        total_gb = stat.f_blocks * stat.f_frsize / (1024**3)
        used_gb = total_gb - available_gb
        percent_used = (used_gb / total_gb * 100) if total_gb > 0 else 0
        
        print(f"✓ Disk: {check_path}")
        print(f"  Total: {total_gb:.2f} GB")
        print(f"  Used: {used_gb:.2f} GB ({percent_used:.1f}%)")
        print(f"  Available: {available_gb:.2f} GB")
        
        if available_gb < 0.5:
            print(f"  ✗ Critical: Less than 500MB available")
            return False
        elif available_gb < 2:
            print(f"  ⚠ Warning: Less than 2GB available")
            return False
        else:
            return True
    except Exception as e:
        print(f"✗ Error checking disk space: {str(e)}")
        return False

def check_system_info():
    """Check system information"""
    print_section("System Information")
    
    print(f"Platform: {platform.platform()}")
    print(f"Processor: {platform.processor() or 'Unknown'}")
    print(f"Machine: {platform.machine()}")
    print(f"Node: {platform.node()}")
    print(f"Python Implementation: {platform.python_implementation()}")
    print(f"User: {os.getenv('USERNAME', os.getenv('USER', 'Unknown'))}")
    print(f"Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def check_core_modules():
    """Check core application modules"""
    print_section("9. Core Application Modules")
    
    core_modules = [
        'sms',
        'ui_components',
        'realtime_sync',
        'notification_service',
    ]
    
    all_found = True
    for module in core_modules:
        try:
            __import__(module)
            print(f"  ✓ {module}")
        except ImportError as e:
            print(f"  ✗ {module} (ImportError: {str(e)[:50]}...)")
            all_found = False
    
    return all_found

def generate_summary(checks):
    """Generate verification summary"""
    print_section("Verification Summary")
    
    total = len(checks)
    passed = sum(1 for c in checks if c[1])
    failed = total - passed
    
    print(f"\nTotal Checks: {total}")
    print(f"✓ Passed: {passed}")
    print(f"✗ Failed: {failed}")
    print(f"Success Rate: {(passed/total*100):.1f}%")
    
    if failed == 0:
        print(f"\n✓ Installation is COMPLETE and FULLY FUNCTIONAL")
        return "SUCCESS"
    elif failed <= 2:
        print(f"\n⚠ Installation is FUNCTIONAL with minor issues")
        print(f"  Please address the warnings above for optimal performance")
        return "SUCCESS_WITH_WARNINGS"
    else:
        print(f"\n✗ Installation has CRITICAL issues")
        print(f"  Please contact support and provide this report")
        return "FAILURE"

def generate_admin_report(checks, status):
    """Generate detailed admin report file"""
    report_dir = Path.home() / ".gaybeck_sms" / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    
    report_file = report_dir / f"admin_verification_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    report_data = {
        "verification_date": datetime.now().isoformat(),
        "status": status,
        "system_info": {
            "platform": platform.platform(),
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "user": os.getenv('USERNAME', os.getenv('USER', 'Unknown')),
        },
        "checks": [
            {
                "name": name,
                "passed": result
            }
            for name, result in checks
        ]
    }
    
    with open(report_file, 'w') as f:
        json.dump(report_data, f, indent=2)
    
    return str(report_file)

def main():
    """Run all verification checks"""
    print_header()
    
    check_system_info()
    
    checks = [
        ("Python Installation", check_python()),
        ("Package Manager", check_pip()),
        ("Required Packages", check_packages()),
        ("Installation Directory", check_installation_directory()),
        ("Database Status", check_database()),
        ("Shortcuts", check_shortcuts()),
        ("Installation Logs", check_logs()),
        ("Disk Space", check_disk_space()),
        ("Core Modules", check_core_modules()),
    ]
    
    status = generate_summary(checks)
    report_file = generate_admin_report(checks, status)
    
    print(f"\nAdmin Report: {report_file}")
    
    print("\n" + "="*80)
    if status == "SUCCESS":
        print("✓ You can launch Gaybeck SMS immediately")
    elif status == "SUCCESS_WITH_WARNINGS":
        print("⚠ You can launch Gaybeck SMS, but please address warnings")
    else:
        print("✗ Please address critical issues before launching")
    print("="*80 + "\n")
    
    return 0 if status != "FAILURE" else 1

if __name__ == "__main__":
    try:
        exit_code = main()
    except Exception as e:
        print(f"\n✗ Unexpected error: {str(e)}")
        exit_code = 1
    
    input("\nPress Enter to exit...")
    sys.exit(exit_code)
