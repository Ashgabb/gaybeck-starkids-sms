#!/usr/bin/env python3
"""Initialize the school management database"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

print("Initializing School Management Database...")
print()

try:
    # Import the SMS module to initialize the database
    import sms
    from sms import SchoolManagementSystem
    import tkinter as tk
    
    # Create a hidden root window
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    print("[1/2] Creating database tables...")
    
    # Initialize the SchoolManagementSystem which will create all tables
    app = SchoolManagementSystem(root)
    
    print("[2/2] Verifying database...")
    
    # Check if tables were created
    import sqlite3
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    print()
    print(f"Database initialized successfully!")
    print(f"Tables created: {len(tables)}")
    for table in tables:
        print(f"  - {table[0]}")
    
    conn.close()
    root.destroy()
    
    print()
    print("Database is ready for use. You can now launch the app!")
    
except Exception as e:
    print(f"Error initializing database: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
