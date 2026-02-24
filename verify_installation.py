"""
Post-Installation Verification Script for Gaybeck Starkids SMS
This script verifies that all components are correctly installed and functional
"""

import sys
import os
import sqlite3

print("\n" + "="*70)
print("GAYBECK STARKIDS SMS - POST-INSTALLATION VERIFICATION")
print("="*70 + "\n")

errors = []
warnings = []

# Test 1: Python Version
print("[1] Checking Python Version...")
if sys.version_info < (3, 13):
    warnings.append(f"Python 3.13+ recommended, found {sys.version_info.major}.{sys.version_info.minor}")
    print(f"    ⚠️  Python {sys.version_info.major}.{sys.version_info.minor} (3.13+ recommended)")
else:
    print(f"    ✓ Python {sys.version_info.major}.{sys.version_info.minor}")

# Test 2: Core Module Imports
print("\n[2] Verifying Core Modules...")
core_modules = [
    ('sms', 'Main SMS Application'),
    ('ai_assessment_grading', 'AI Assessment Service'),
    ('notification_service', 'Notification Service'),
    ('enhanced_ews', 'Early Warning System'),
    ('ai_tutor_service', 'AI Tutor Service'),
]

for module_name, module_desc in core_modules:
    try:
        __import__(module_name)
        print(f"    ✓ {module_desc}")
    except ImportError as e:
        errors.append(f"Failed to import {module_name}: {str(e)}")
        print(f"    ✗ {module_desc} - FAILED")

# Test 3: UI Components Initialization
print("\n[3] Verifying UI Components...")
try:
    import tkinter as tk
    from ui_components import (
        NotificationCenterFrame,
        AITutorChatFrame,
        EWSDashboardFrame,
        NotificationSettingsFrame
    )
    
    # Test instantiation with parameters
    root = tk.Tk()
    root.withdraw()
    
    try:
        frame1 = NotificationCenterFrame(root, 1, 'admin')
        print("    ✓ NotificationCenterFrame initialized")
    except Exception as e:
        errors.append(f"NotificationCenterFrame init failed: {e}")
        print(f"    ✗ NotificationCenterFrame - {str(e)[:50]}")
    
    try:
        frame2 = AITutorChatFrame(root, 1, 'teacher')
        print("    ✓ AITutorChatFrame initialized")
    except Exception as e:
        errors.append(f"AITutorChatFrame init failed: {e}")
        print(f"    ✗ AITutorChatFrame - {str(e)[:50]}")
    
    try:
        frame3 = EWSDashboardFrame(root, 1, 'student')
        print("    ✓ EWSDashboardFrame initialized")
    except Exception as e:
        errors.append(f"EWSDashboardFrame init failed: {e}")
        print(f"    ✗ EWSDashboardFrame - {str(e)[:50]}")
    
    try:
        frame4 = NotificationSettingsFrame(root, 1, 'admin')
        print("    ✓ NotificationSettingsFrame initialized")
    except Exception as e:
        errors.append(f"NotificationSettingsFrame init failed: {e}")
        print(f"    ✗ NotificationSettingsFrame - {str(e)[:50]}")
    
    root.destroy()
except Exception as e:
    errors.append(f"UI Components test failed: {e}")
    print(f"    ✗ UI Components - FAILED: {str(e)[:50]}")

# Test 4: Database
print("\n[4] Verifying Database...")
try:
    if os.path.exists('database/school_management.db'):
        conn = sqlite3.connect('database/school_management.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
        table_count = cursor.fetchone()[0]
        conn.close()
        if table_count > 30:
            print(f"    ✓ Database verified ({table_count} tables)")
        else:
            warnings.append(f"Database has only {table_count} tables, expected 40+")
            print(f"    ⚠️  Database has {table_count} tables (expected 40+)")
    else:
        errors.append("Database file not found")
        print("    ✗ Database file not found")
except Exception as e:
    errors.append(f"Database check failed: {e}")
    print(f"    ✗ Database check failed: {str(e)[:50]}")

# Test 5: Launcher Scripts
print("\n[5] Verifying Launcher Scripts...")
launcher_files = [
    ('launch_sms.bat', 'Batch Launcher'),
    ('launch_sms.vbs', 'VBScript Launcher'),
]

for filename, desc in launcher_files:
    if os.path.exists(filename):
        print(f"    ✓ {desc} (found)")
    else:
        errors.append(f"Launcher script missing: {filename}")
        print(f"    ✗ {desc} - NOT FOUND")

# Test 6: Required Files
print("\n[6] Verifying Required Files...")
required_files = [
    ('sms.py', 'Main Application'),
    ('requirements.txt', 'Dependencies'),
    ('setup.bat', 'Setup Script'),
    ('database/school_management.db', 'Database'),
]

for filepath, desc in required_files:
    if os.path.exists(filepath):
        print(f"    ✓ {desc}")
    else:
        errors.append(f"Required file missing: {filepath}")
        print(f"    ✗ {desc} - NOT FOUND")

# Summary
print("\n" + "="*70)
print("VERIFICATION SUMMARY")
print("="*70 + "\n")

if errors:
    print("❌ ERRORS FOUND:")
    for i, error in enumerate(errors, 1):
        print(f"   {i}. {error}")
    print()

if warnings:
    print("⚠️  WARNINGS:")
    for i, warning in enumerate(warnings, 1):
        print(f"   {i}. {warning}")
    print()

if not errors:
    print("✅ ALL CRITICAL CHECKS PASSED!\n")
    print("Your Gaybeck Starkids SMS installation is complete and ready to use!")
    print("\nYou can now:")
    print("  • Double-click 'launch_sms.bat' or desktop shortcut to start the app")
    print("  • Login with: admin / admin123 (or teacher1 / teacher123)")
    print("  • Start using AI features, EWS, and all management tools")
    sys.exit(0)
else:
    print("❌ INSTALLATION INCOMPLETE\n")
    print("Please fix the errors above and run setup again.")
    print("\nFor support, check:")
    print("  • SETUP_INSTRUCTIONS.md")
    print("  • TROUBLESHOOTING.md")
    print("  • README.md")
    sys.exit(1)

print("="*70 + "\n")
