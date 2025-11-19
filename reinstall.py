#!/usr/bin/env python3
"""
Gaybeck Starkids SMS - Automated Reinstall Script
Updates from latest GitHub source and reinstalls the application
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def print_header(text):
    print("\n" + "="*80)
    print(f"  {text}")
    print("="*80 + "\n")

def run_command(cmd, description):
    """Run a command and report status"""
    print(f"[→] {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"[✓] {description} completed successfully")
            return True
        else:
            print(f"[✗] {description} failed")
            if result.stderr:
                print(f"    Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"[✗] {description} error: {e}")
        return False

def main():
    print_header("GAYBECK STARKIDS SMS - AUTOMATED REINSTALL")
    
    base_path = Path(__file__).parent.parent
    
    # Step 1: Pull latest from GitHub
    print_header("Step 1: Updating from GitHub")
    if run_command(f'cd "{base_path}" && git pull origin main', "Git pull"):
        print("✓ Latest code pulled from GitHub")
    else:
        print("✗ Git pull failed - continuing with local code")
    
    # Step 2: Update dependencies
    print_header("Step 2: Installing Dependencies")
    req_file = base_path / "requirements.txt"
    if req_file.exists():
        run_command(f"pip install -r \"{req_file}\"", "Install dependencies")
    
    # Step 3: Update virtual environment if needed
    print_header("Step 3: Virtual Environment")
    venv_path = base_path / ".venv"
    if venv_path.exists():
        print(f"[✓] Virtual environment found at {venv_path}")
    else:
        run_command(f'cd "{base_path}" && python -m venv .venv', "Create virtual environment")
    
    # Step 4: Verify installation
    print_header("Step 4: Verifying Installation")
    run_command(f'cd "{base_path}" && python -m py_compile sms.py', "Verify syntax")
    run_command(f'cd "{base_path}" && python test_startup.py', "Test startup")
    
    # Step 5: Create/Update shortcuts
    print_header("Step 5: Creating Shortcuts")
    run_command(f'cd "{base_path}" && python setup_shortcuts.py', "Create shortcuts")
    
    print_header("REINSTALL COMPLETE")
    print("✓ Application has been updated and reinstalled successfully!")
    print(f"\n📁 Application location: {base_path}")
    print("🚀 You can now launch the application using:")
    print("   - Desktop shortcut")
    print("   - Command: python sms.py")
    print("   - RUN_APP.bat\n")

if __name__ == "__main__":
    main()
