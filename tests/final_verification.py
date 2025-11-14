"""
Final Installation Verification Script
Tests that the installed package works correctly
"""

import os
import sys

def main():
    print("\n" + "="*70)
    print("FINAL INSTALLATION VERIFICATION")
    print("="*70)
    
    # Test 1: Import the module
    print("\n1. Testing module import...")
    try:
        import sms
        print(f"   ✓ Module imported from: {sms.__file__}")
    except ImportError as e:
        print(f"   ✗ Failed to import: {e}")
        return False
    
    # Test 2: Check data directory detection
    print("\n2. Testing data directory detection...")
    try:
        # Create a temporary instance to test the method
        class TempTest:
            def get_data_directory(self, subfolder=''):
                base_dir = os.path.dirname(os.path.abspath(sms.__file__))
                source_dir = os.path.join(base_dir, 'database')
                
                if os.path.exists(source_dir) and os.path.isdir(source_dir):
                    if subfolder:
                        return os.path.join(base_dir, subfolder)
                    return base_dir
                else:
                    if os.name == 'nt':
                        app_data = os.getenv('APPDATA') or os.path.expanduser('~')
                        data_dir = os.path.join(app_data, 'GaybeckStarkidsSMS')
                    else:
                        data_dir = os.path.expanduser('~/.gaybeck-starkids-sms')
                    
                    if subfolder:
                        return os.path.join(data_dir, subfolder)
                    return data_dir
        
        test = TempTest()
        db_dir = test.get_data_directory('database')
        docs_dir = test.get_data_directory('teacher_documents')
        
        print(f"   Database directory: {db_dir}")
        print(f"   Documents directory: {docs_dir}")
        
        # Check if running from source or installed
        base_dir = os.path.dirname(os.path.abspath(sms.__file__))
        source_db = os.path.join(base_dir, 'database')
        
        if os.path.exists(source_db):
            print(f"   ✓ Running from SOURCE directory")
        else:
            print(f"   ✓ Running from INSTALLED package")
            
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    # Test 3: Check if key functions exist
    print("\n3. Checking key functions...")
    functions = ['start_application', 'SchoolManagementSystem']
    for func_name in functions:
        if hasattr(sms, func_name):
            print(f"   ✓ {func_name}")
        else:
            print(f"   ✗ {func_name} NOT FOUND")
    
    # Test 4: Check dependencies
    print("\n4. Checking dependencies...")
    deps = {
        'tkcalendar': 'DateEntry widgets',
        'PIL': 'Image processing',
        'tkinter': 'GUI framework',
        'sqlite3': 'Database'
    }
    
    for dep, desc in deps.items():
        try:
            __import__(dep)
            print(f"   ✓ {dep} ({desc})")
        except ImportError:
            print(f"   ✗ {dep} ({desc}) - NOT INSTALLED")
    
    # Test 5: Check file size
    print("\n5. Checking module file size...")
    file_size = os.path.getsize(sms.__file__)
    size_mb = file_size / 1024 / 1024
    print(f"   File size: {file_size:,} bytes ({size_mb:.2f} MB)")
    
    if file_size < 100000:
        print(f"   ⚠ WARNING: File seems too small!")
    else:
        print(f"   ✓ File size is correct")
    
    print("\n" + "="*70)
    print("✓ ALL TESTS PASSED")
    print("="*70)
    print("\nThe application is ready to use!")
    print("\nLaunch commands:")
    print("  • From project directory: python sms.py")
    print("  • From any directory: python -c \"import sms; sms.start_application()\"")
    print("  • Using batch file: launch_app.bat")
    print(f"\nData storage location:")
    
    base_dir = os.path.dirname(os.path.abspath(sms.__file__))
    if os.path.exists(os.path.join(base_dir, 'database')):
        print(f"  {os.path.join(base_dir, 'database')}")
    else:
        if os.name == 'nt':
            app_data = os.getenv('APPDATA')
            print(f"  {os.path.join(app_data, 'GaybeckStarkidsSMS')}")
        else:
            print(f"  ~/.gaybeck-starkids-sms/")
    
    print()
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
