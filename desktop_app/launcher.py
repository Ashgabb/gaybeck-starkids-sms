#!/usr/bin/env python3
"""
Desktop Application Launcher - Standalone Application
This is the entry point for the Gaybeck Starkids SMS desktop application.
The desktop app is completely independent from the web app.

Run this file to start the desktop SMS application:
    python launcher.py
"""

import sys
import os
from pathlib import Path

# Set application directory as working directory
app_dir = Path(__file__).parent
os.chdir(app_dir)

# Add the desktop_app directory to Python path for imports
sys.path.insert(0, str(app_dir))

print("=" * 70)
print("GAYBECK STARKIDS ACADEMY - DESKTOP APPLICATION")
print("School Management System v2.0.3")
print("=" * 70)
print()

# Verify Python version
required_version = (3, 13)
if sys.version_info < required_version:
    print(f"❌ ERROR: Python 3.13+ is required")
    print(f"   You are running Python {sys.version_info.major}.{sys.version_info.minor}")
    print()
    sys.exit(1)

print(f"✓ Python version: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
print()

# Verify database directory
db_dir = app_dir / "database"
if not db_dir.exists():
    print(f"Creating database directory: {db_dir}")
    db_dir.mkdir(parents=True, exist_ok=True)

print(f"✓ Database location: {db_dir / 'school_management.db'}")
print()

# Try importing the main module
print("Initializing application modules...")
print()

try:
    # Import main SMS module
    import main
    
    print("✓ SMS module loaded successfully")
    print()
    
    # Start the application
    print("Starting GUI application...")
    print()
    main.start_application()
    
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print()
    print("Please ensure all dependencies are installed:")
    print("  pip install -r requirements.txt")
    print()
    sys.exit(1)
    
except Exception as e:
    print(f"❌ Application Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
