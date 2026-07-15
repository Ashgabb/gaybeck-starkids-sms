#!/usr/bin/env python3
"""
Gaybeck Starkids SMS - Portable Setup Script
Version: 1.0.0
Purpose: Install dependencies and verify environment on any device
"""

import os
import subprocess
import sys


def print_header(title):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def install_requirements():
    """Install required packages from requirements.txt."""
    requirements_file = os.path.join(os.path.dirname(__file__), "requirements.txt")

    if not os.path.exists(requirements_file):
        print("[WARN] requirements.txt not found - skipping dependency installation")
        return False

    print_header("Installing Dependencies")
    print(f"Installing packages from: {requirements_file}\n")

    try:
        print("Upgrading pip...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

        print("\nInstalling packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])

        print("\n[OK] All dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n[WARN] Some packages could not be installed: {e}")
        print("The application may still work with fewer features.")
        return True
    except Exception as e:
        print(f"\n[ERROR] Installation failed: {e}")
        return False


def verify_environment():
    """Verify the local Python runtime and key imports."""
    print_header("Environment Verification")

    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version}")
    print(f"Python path: {sys.prefix}\n")

    required_packages = {
        "tkinter": "GUI Framework (Python stdlib)",
        "sqlite3": "Database (Python stdlib)",
    }

    print("Checking Python packages:\n")
    all_ok = True

    for package, description in required_packages.items():
        try:
            __import__(package)
            print(f"[OK] {package:20} - {description}")
        except ImportError:
            print(f"[ERROR] {package:20} - {description} - NOT FOUND")
            all_ok = False

    optional_packages = {
        "tkcalendar": "Date picker widget",
        "reportlab": "PDF generation",
        "PIL": "Image processing",
        "cv2": "Camera support",
        "numpy": "Numerical computing",
        "pandas": "Data analysis",
        "sklearn": "Machine learning (scikit-learn)",
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
    """Check if sms.py exists."""
    print_header("Application Files")

    sms_file = os.path.join(os.path.dirname(__file__), "sms.py")
    if os.path.exists(sms_file):
        print(f"[OK] SMS application found: {sms_file}")
        print(f"     Size: {os.path.getsize(sms_file) / 1024:.2f} KB")
        return True

    print(f"[ERROR] SMS application not found: {sms_file}")
    return False


def check_database():
    """Check if a database file exists."""
    print_header("Database")

    app_dir = os.path.dirname(__file__)
    possible_paths = [
        os.path.join(app_dir, "school_management.db"),
        os.path.join(app_dir, "database", "school_management.db"),
    ]

    for db_path in possible_paths:
        if os.path.exists(db_path):
            print(f"[OK] Database found: {db_path}")
            print(f"     Size: {os.path.getsize(db_path) / 1024:.2f} KB")
            return True

    print("[INFO] No database found - will be created on first run")
    return True


def create_desktop_shortcut():
    """Offer to create desktop shortcut on Windows."""
    print_header("Desktop Shortcut")

    if sys.platform != "win32":
        print("[INFO] Desktop shortcut creation only supported on Windows")
        return

    response = input("\nCreate desktop shortcut? (y/n): ").strip().lower()
    if response != "y":
        print("[INFO] Skipping desktop shortcut creation")
        return

    vbs_file = os.path.join(os.path.dirname(__file__), "create_sms_shortcut.vbs")
    if not os.path.exists(vbs_file):
        print(f"\n[ERROR] Shortcut creator not found: {vbs_file}")
        return

    try:
        subprocess.call(["cscript.exe", vbs_file])
        print("\n[OK] Desktop shortcut created!")
    except Exception as e:
        print(f"\n[ERROR] Could not create shortcut: {e}")


def main():
    """Run setup workflow."""
    print("\n" * 2)
    print("*" * 70)
    print("*" + " " * 68 + "*")
    print("*" + "  GAYBECK STARKIDS SMS - PORTABLE SETUP".center(68) + "*")
    print("*" + "  Version 1.0.0".center(68) + "*")
    print("*" + " " * 68 + "*")
    print("*" * 70)

    print("\n[INFO] This setup will prepare your device for running the SMS application.")
    print("[INFO] You will be prompted for each step.\n")

    env_ok = verify_environment()
    sms_ok = check_sms_file()
    db_ok = check_database()

    print()
    response = input("Install/update dependencies? (y/n): ").strip().lower()
    if response == "y":
        deps_ok = install_requirements()
    else:
        deps_ok = True

    create_desktop_shortcut()

    print_header("Setup Summary")
    print(f"[{'OK' if env_ok else 'WARN'}] Environment ready")
    print(f"[{'OK' if sms_ok else 'ERROR'}] SMS file found")
    print(f"[{'OK' if db_ok else 'WARN'}] Database status")
    print(f"[{'OK' if deps_ok else 'WARN'}] Dependencies")

    if env_ok and sms_ok:
        print("\n[OK] Setup completed. You can now run launch_sms.bat or python sms.py")
        return 0

    print("\n[WARN] Setup completed with issues. Please review messages above.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
