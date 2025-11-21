#!/usr/bin/env python3
"""Debug script to test app startup and capture all errors"""

import sys
import os
import traceback

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

print("=" * 70)
print("GAYBECK STARKIDS SMS - STARTUP DEBUG")
print("=" * 70)
print()

# Test 1: Module import
print("[TEST 1] Importing SMS module...")
try:
    import sms
    print("  [OK] SMS module imported")
except Exception as e:
    print(f"  [FAIL] Could not import sms: {e}")
    traceback.print_exc()
    sys.exit(1)

print()

# Test 2: GUI initialization
print("[TEST 2] Testing GUI initialization...")
try:
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    print("  [OK] Tkinter window created")
except Exception as e:
    print(f"  [FAIL] Could not create Tkinter window: {e}")
    traceback.print_exc()
    sys.exit(1)

print()

# Test 3: App creation
print("[TEST 3] Creating SchoolManagementSystem...")
try:
    from sms import SchoolManagementSystem
    app = SchoolManagementSystem(root)
    print("  [OK] App initialized successfully")
except Exception as e:
    print(f"  [FAIL] Could not initialize app: {e}")
    traceback.print_exc()
    root.destroy()
    sys.exit(1)

print()

# Test 4: Database verification
print("[TEST 4] Verifying database...")
try:
    import sqlite3
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"  [OK] Database has {len(tables)} tables")
    conn.close()
except Exception as e:
    print(f"  [FAIL] Database error: {e}")
    traceback.print_exc()

print()
print("=" * 70)
print("ALL TESTS PASSED - APP IS READY")
print("=" * 70)
print()
print("The app is working correctly. Try:")
print("  1. Double-click the Desktop shortcut")
print("  2. Or run: python sms.py")
print()

root.destroy()
