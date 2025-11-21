#!/usr/bin/env python3
"""Test if the app can start without GUI issues"""

import sys
import os
from pathlib import Path

print("Testing application startup...")
print()

# Change to app directory
app_dir = Path(__file__).parent
os.chdir(app_dir)

print(f"Working directory: {os.getcwd()}")
print()

# Try importing the main module
try:
    print("Importing SMS module...")
    import sms
    print("✓ SMS module imported successfully")
    print()
    print("Application is ready to launch!")
    print("Starting GUI...")
    print()
    
    # This will start the actual application
    sms.start_application()
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
