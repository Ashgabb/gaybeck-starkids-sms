#!/usr/bin/env python3
"""
Gaybeck Starkids SMS - Bootstrap Launcher
This script finds and activates the virtual environment, then launches the main app.
Version: 3.0.2 - Improved console handling
"""

import sys
import os
import subprocess

def main():
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Check if virtual environment exists
    venv_path = os.path.join(script_dir, '.venv')
    if not os.path.exists(venv_path):
        print("[ERROR] Virtual environment not found at:", venv_path)
        print("[INFO] Creating virtual environment...")
        subprocess.run([sys.executable, '-m', 'venv', venv_path], check=False)
    
    # Check if sms.py exists
    sms_path = os.path.join(script_dir, 'sms.py')
    if not os.path.exists(sms_path):
        print(f"[ERROR] sms.py not found at: {sms_path}")
        sys.exit(1)
    
    # Get the Python executable from the virtual environment
    if sys.platform == 'win32':
        python_exe = os.path.join(venv_path, 'Scripts', 'python.exe')
        pythonw_exe = os.path.join(venv_path, 'Scripts', 'pythonw.exe')
    else:
        python_exe = os.path.join(venv_path, 'bin', 'python')
        pythonw_exe = python_exe  # No pythonw on Unix
    
    if not os.path.exists(python_exe):
        print(f"[ERROR] Python executable not found in venv: {python_exe}")
        print("[INFO] Using system Python instead")
        python_exe = sys.executable
        pythonw_exe = python_exe
    
    # Change to script directory
    os.chdir(script_dir)
    
    # On Windows, use pythonw.exe to hide console window
    # On other platforms, use regular python
    if sys.platform == 'win32' and os.path.exists(pythonw_exe):
        launcher = pythonw_exe
    else:
        launcher = python_exe
    
    # Launch the application without showing console
    try:
        if sys.platform == 'win32':
            # Windows: Use CREATE_NO_WINDOW flag
            import subprocess
            creationflags = 0x08000000  # CREATE_NO_WINDOW
            subprocess.Popen([launcher, sms_path], 
                           cwd=script_dir,
                           creationflags=creationflags)
        else:
            # Unix/Linux/macOS: Use DEVNULL
            subprocess.Popen([launcher, sms_path], 
                           cwd=script_dir,
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"[ERROR] Failed to launch application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()

