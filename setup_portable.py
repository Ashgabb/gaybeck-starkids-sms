#!/usr/bin/env python3
"""
Gaybeck Starkids SMS - Portable Setup Script
Version: 1.0.0
Purpose: Install dependencies and verify environment on any device
"""

import os
import sys
import subprocess
import importlib.util


def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def install_requirements():
    """Install required packages from requirements.txt"""
    requirements_file = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    
    if not os.path.exists(requirements_file):
        print("[WARN] requirements.txt not found - skipping dependency installation")
        return False
    
    print_header("Installing Dependencies")
    print(f"Installing packages from: {requirements_file}\n")
    
    try:
        # Upgrade pip first
        print("Upgrading pip...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
        
        # Install requirements
        print("\nInstalling packages...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', requirements_file])
        
        print("\n[OK] All dependencies installed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n[WARN] Some packages could not be installed: {e}")
        print("The application may still work with fewer features.")
        return True  # Continue anyway
    except Exception as e:
        print(f"\n[ERROR] Installation failed: {e}")
        return False


def verify_environment():
    """Verify Python environment is ready"""
    print_header("Environment Verification")
    
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version}")
    print(f"Python path: {sys.prefix}\n")
    
    # Check required packages
    required_packages = {
        'tkinter': 'GUI Framework (Python stdlib)',
        'sqlite3': 'Database (Python stdlib)',
    }
    
    print("Checking Python packages:\n")
    all_ok = True
    
    for package, description in required_packages.items():
        try:
            if package == 'tkinter':
                # Special handling for tkinter
                import tkinter
                print(f"[OK] {package:20} - {description}")
            else:
                __import__(package)
                print(f"[OK] {package:20} - {description}")
        except ImportError:
            print(f"[ERROR] {package:20} - {description} - NOT FOUND")
            all_ok = False
    
    # Check optional packages
    optional_packages = {
        'tkcalendar': 'Date picker widget',
        'reportlab': 'PDF generation',
        'PIL': 'Image processing',
        'cv2': 'Camera support',
        'numpy': 'Numerical computing',
        'pandas': 'Data analysis',
        'sklearn': 'Machine learning (scikit-learn)',
    }
    
    print("\nOptional packages:\n")
    for package, description in optional_packages.items():
        try:
            __import__(package)
            print(f"[OK] {package:20} - {description}")
        except ImportError:
            print(f"[--] {package:20} - {description} (not required)")
    
    return all_ok


def check_sms_file():
    """Check if sms.py exists"""
    print_header("Application Files")
    
    sms_file = os.path.join(os.path.dirname(__file__), 'sms.py')
    
    if os.path.exists(sms_file):
        print(f"[OK] SMS application found: {sms_file}")
        print(f"     Size: {os.path.getsize(sms_file) / 1024:.2f} KB")
        return True
    else:\n        print(f"[ERROR] SMS application not found: {sms_file}")
        return False


def check_database():
    \"\"\"Check if database file exists\"\"\"
    app_dir = os.path.dirname(__file__)
    possible_paths = [
        os.path.join(app_dir, 'school_management.db'),
        os.path.join(app_dir, 'database', 'school_management.db'),
    ]
    
    print()
    for db_path in possible_paths:
        if os.path.exists(db_path):
            print(f\"[OK] Database found: {db_path}\")\n            print(f\"     Size: {os.path.getsize(db_path) / 1024:.2f} KB\")\n            return True
    
    print(\"[INFO] No database found - will be created on first run\")\n    return True


def create_desktop_shortcut():
    \"\"\"Offer to create desktop shortcut\"\"\"
    print_header(\"Desktop Shortcut\")\n    \n    if sys.platform != 'win32':\n        print(\"[INFO] Desktop shortcut creation only supported on Windows\")\n        return\n    \n    response = input(\"\\nCreate desktop shortcut? (y/n): \").lower()\n    if response == 'y':\n        vbs_file = os.path.join(os.path.dirname(__file__), 'create_sms_shortcut.vbs')\n        if os.path.exists(vbs_file):\n            try:\n                subprocess.call(['cscript.exe', vbs_file])\n                print(\"\\n[OK] Desktop shortcut created!\")\n            except Exception as e:\n                print(f\"\\n[ERROR] Could not create shortcut: {e}\")\n        else:\n            print(f\"\\n[ERROR] Shortcut creator not found: {vbs_file}\")\n\n\ndef main():\n    \"\"\"Main setup process\"\"\"\n    print(\"\\n\" * 2)\n    print(\"*\" * 70)\n    print(\"*\" + \" \" * 68 + \"*\")\n    print(\"*\" + \"  GAYBECK STARKIDS SMS - PORTABLE SETUP\".center(68) + \"*\")\n    print(\"*\" + \"  Version 1.0.0\".center(68) + \"*\")\n    print(\"*\" + \" \" * 68 + \"*\")\n    print(\"*\" * 70)\n    \n    print(\"\\n[INFO] This setup will prepare your device for running the SMS application.\")\n    print(\"[INFO] You will be prompted for each step.\\n\")\n    \n    # Step 1: Verify environment\n    env_ok = verify_environment()\n    \n    # Step 2: Check SMS file\n    sms_ok = check_sms_file()\n    \n    # Step 3: Check database\n    db_ok = check_database()\n    \n    # Step 4: Install dependencies\n    print()\n    response = input(\"Install/update dependencies? (y/n): \").lower()\n    if response == 'y':\n        deps_ok = install_requirements()\n    else:\n        deps_ok = True\n    \n    # Step 5: Create desktop shortcut\n    create_desktop_shortcut()\n    \n    # Summary\n    print_header(\"Setup Summary\")\n    print(f\"[{'OK' if env_ok else 'WARN'}] Environment ready\")\n    print(f\"[{'OK' if sms_ok else 'ERROR'}] SMS file found\")\n    print(f\"[OK] Database\")\n    print(f\"[{'OK' if deps_ok else 'WARN'}] Dependencies\")\n    \n    # Final status\n    ready = sms_ok and db_ok\n    print()\n    if ready:\n        print(\"[OK] Setup complete! You can now run the SMS application.\")\n        print(\"\\nTo launch the application:\")\n        print(\"  - Double-click the desktop shortcut (if created)\")\n        print(\"  - Run: python sms.py\")\n        print(\"  - Run: python launch_app.py\")\n        print(\"  - Run: python run_sms.py\")\n    else:\n        print(\"[ERROR] Setup incomplete. Please review errors above.\")\n    \n    print(\"\\n\" + \"=\" * 70 + \"\\n\")\n    return 0 if ready else 1\n\n\nif __name__ == '__main__':\n    sys.exit(main())\n