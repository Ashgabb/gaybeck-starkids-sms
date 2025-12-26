"""
Gaybeck Starkids Academy - Desktop Application
School Management System v2.0.3

DESKTOP APPLICATION - COMPLETELY INDEPENDENT
This application runs entirely offline and is NOT dependent on the web app.

Entry Point: launcher.py
"""

__version__ = "2.0.3"
__build_date__ = "2025-11-11"
__app_type__ = "DESKTOP_STANDALONE"
__independence_status__ = "FULLY_INDEPENDENT_FROM_WEB_APP"

import tkinter as tk
import os
import sys
from pathlib import Path

# Set application root directory
APP_ROOT = Path(__file__).parent
DATABASE_DIR = APP_ROOT / "database"
UTILS_DIR = APP_ROOT / "utils"
CONFIG_DIR = APP_ROOT / "config"

# Create required directories
for directory in [DATABASE_DIR, UTILS_DIR, CONFIG_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Add paths to sys.path for local imports
sys.path.insert(0, str(APP_ROOT))
sys.path.insert(0, str(UTILS_DIR))
sys.path.insert(0, str(CONFIG_DIR))

def start_application():
    """
    Start the Gaybeck Starkids SMS Desktop Application
    
    This function initializes and launches the complete desktop application.
    The application is 100% independent from the web version.
    """
    
    try:
        # Import the main SMS module (from parent sms.py)
        # The desktop app is a copy/wrapper of the Tkinter application
        
        # Create root window
        root = tk.Tk()
        root.title("Gaybeck Starkids Academy - Desktop Application")
        root.geometry("1400x900")
        
        # Try to import the SMS application
        # Since sms.py is large, we import it dynamically
        try:
            # Check if we can import from parent directory (when testing)
            # Otherwise use local copy
            import sms
            
            # Create login window with the main app
            from sms import LoginWindow, SchoolManagementSystem
            
            def on_login_success(user_info):
                # Close login window and show main app
                login_window.login_window.destroy()
                root.deiconify()
                
                # Create main application
                app = SchoolManagementSystem(root, user_info)
            
            # Show login window
            login_window = LoginWindow(root, on_login_success)
            
        except ImportError as e:
            print(f"Could not import SMS module: {e}")
            print("Creating fallback interface...")
            
            # Create a simple fallback interface
            root.deiconify()
            
            from tkinter import messagebox, ttk
            
            main_frame = tk.Frame(root, bg='#f0f0f0')
            main_frame.pack(fill='both', expand=True)
            
            # Header
            header = tk.Frame(main_frame, bg='#1e3a5f', height=100)
            header.pack(fill='x')
            header.pack_propagate(False)
            
            title = tk.Label(header, text="Gaybeck Starkids Academy", 
                           font=('Arial', 24, 'bold'), bg='#1e3a5f', fg='white')
            title.pack(pady=20)
            
            # Content
            content = tk.Frame(main_frame, bg='#ffffff')
            content.pack(fill='both', expand=True, padx=50, pady=50)
            
            info = tk.Label(content, 
                          text="DESKTOP APPLICATION - STANDALONE VERSION\n\n"
                               "This is the offline school management system.\n"
                               "All data is stored locally and independent from web version.\n\n"
                               "Database: " + str(DATABASE_DIR / "school_management.db"),
                          font=('Arial', 12), bg='#ffffff', justify='center')
            info.pack(pady=20)
            
            # Database info
            db_file = DATABASE_DIR / "school_management.db"
            if db_file.exists():
                size_mb = db_file.stat().st_size / (1024 * 1024)
                db_status = f"✓ Database found ({size_mb:.2f} MB)"
            else:
                db_status = "Database will be created on first use"
            
            status = tk.Label(content, text=db_status, 
                            font=('Arial', 11), fg='#28a745', bg='#ffffff')
            status.pack(pady=10)
        
        # Run the application
        root.mainloop()
        
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    start_application()
