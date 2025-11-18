#!/usr/bin/env python3
"""
Convert existing logo.png to ICO and use it for shortcuts
"""
from PIL import Image
import os
from pathlib import Path

def convert_logo_to_icon():
    """Convert logo.png to sms_icon.ico"""
    
    logo_path = Path('logo.png')
    ico_path = Path('sms_icon.ico')
    
    if not logo_path.exists():
        print(f"[ERROR] Logo not found: {logo_path}")
        return False
    
    try:
        # Open the logo
        img = Image.open(logo_path)
        print(f"[OK] Loaded logo: {img.size} pixels")
        
        # Convert to RGBA if needed
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
            print(f"[OK] Converted to RGBA")
        
        # Create multiple sizes for the ICO file (standard icon sizes)
        sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        
        # Resize and save as ICO
        img.save(ico_path, format='ICO', sizes=sizes)
        
        file_size = os.path.getsize(ico_path)
        print(f"[OK] Created icon: {ico_path}")
        print(f"     Size: {file_size} bytes")
        print(f"     Dimensions: {sizes}")
        
        return True
    
    except Exception as e:
        print(f"[ERROR] Failed to convert logo: {e}")
        return False

if __name__ == '__main__':
    if convert_logo_to_icon():
        print()
        print("Next: Run fix_shortcut_icon.py to update the shortcut")
    else:
        exit(1)
