"""
Verification script for installed gaybeck-starkids-sms package
Tests that all modules and features are accessible
"""

import sys
import importlib.util

def test_import():
    """Test that sms module can be imported"""
    print("\n" + "="*70)
    print("TESTING INSTALLED PACKAGE")
    print("="*70)
    
    print("\n1. Testing module import...")
    try:
        import sms
        print("   ✓ sms module imported successfully")
        
        # Check for key functions
        if hasattr(sms, 'start_application'):
            print("   ✓ start_application() function found")
        else:
            print("   ✗ start_application() function NOT FOUND")
            
        if hasattr(sms, 'SchoolManagementSystem'):
            print("   ✓ SchoolManagementSystem class found")
        else:
            print("   ✗ SchoolManagementSystem class NOT FOUND")
            
    except ImportError as e:
        print(f"   ✗ Failed to import sms module: {e}")
        return False
    
    print("\n2. Testing dependencies...")
    dependencies = {
        'tkcalendar': 'DateEntry widget support',
        'PIL': 'Image processing (Pillow)',
        'tkinter': 'GUI framework',
        'sqlite3': 'Database support'
    }
    
    for module_name, description in dependencies.items():
        try:
            spec = importlib.util.find_spec(module_name)
            if spec is not None:
                print(f"   ✓ {module_name} - {description}")
            else:
                print(f"   ✗ {module_name} - {description} (NOT FOUND)")
        except Exception as e:
            print(f"   ✗ {module_name} - {description} (ERROR: {e})")
    
    print("\n3. Checking installation details...")
    try:
        import pkg_resources
        dist = pkg_resources.get_distribution('gaybeck-starkids-sms')
        print(f"   Package: {dist.project_name}")
        print(f"   Version: {dist.version}")
        print(f"   Location: {dist.location}")
    except Exception as e:
        print(f"   ⚠ Could not get package info: {e}")
    
    print("\n4. Testing module file location...")
    try:
        import sms
        print(f"   Module file: {sms.__file__}")
        
        # Check file size
        import os
        file_size = os.path.getsize(sms.__file__)
        print(f"   File size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")
        
        if file_size < 100000:  # Less than 100KB is suspicious
            print("   ⚠ WARNING: File size seems too small!")
        else:
            print("   ✓ File size looks correct")
            
    except Exception as e:
        print(f"   ✗ Error checking module: {e}")
    
    print("\n" + "="*70)
    print("VERIFICATION COMPLETE")
    print("="*70)
    
    print("\nTo run the application:")
    print("  python -c \"import sms; sms.start_application()\"")
    print("  OR")
    print("  python sms.py (from the project directory)\n")
    
    return True

if __name__ == "__main__":
    success = test_import()
    sys.exit(0 if success else 1)
