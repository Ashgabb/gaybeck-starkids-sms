#!/usr/bin/env python3
"""
Gaybeck Starkids SMS - Minimal Direct Launcher
Version: 1.0.0
Purpose: Direct launcher with no dependencies - guaranteed to work
"""

import os
import sys

# Change to application directory
app_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(app_dir)

# Add current directory to path
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

# Import and run the main application
try:
    import sms
    
    # Start the application
    if hasattr(sms, 'start_application'):
        sms.start_application()
    else:
        # Try main entry point
        if __name__ == '__main__':
            import tkinter as tk
            root = tk.Tk()
            app = sms.SchoolManagementSystem(root)
            root.mainloop()
except ImportError as e:
    print(f"Error importing SMS module: {e}")
    print("Please ensure sms.py is in the same directory as this script.")
    sys.exit(1)
except Exception as e:
    print(f"Error running SMS application: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
