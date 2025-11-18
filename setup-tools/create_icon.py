#!/usr/bin/env python3
"""
Create a custom application icon using PIL
This generates an icon for the Gaybeck Starkids SMS application
"""

import os
from pathlib import Path

def create_app_icon():
    """Create a simple application icon"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Create a new image (256x256 for high quality icon)
        size = 256
        image = Image.new('RGB', (size, size), color='#1e3a8a')  # Blue background
        draw = ImageDraw.Draw(image)
        
        # Draw a simple design
        # Outer circle
        draw.ellipse([10, 10, size-10, size-10], outline='#3b82f6', width=4)
        
        # Inner design - simple text-like shape
        # Top bar (representing school)
        draw.rectangle([50, 60, 206, 80], fill='#60a5fa')
        
        # Book/document shape
        draw.rectangle([60, 100, 196, 190], outline='#60a5fa', width=3)
        draw.line([(128, 100), (128, 190)], fill='#60a5fa', width=2)
        
        # Horizontal lines (representing text)
        draw.line([(70, 120), (190, 120)], fill='#93c5fd', width=2)
        draw.line([(70, 140), (190, 140)], fill='#93c5fd', width=2)
        draw.line([(70, 160), (180, 160)], fill='#93c5fd', width=2)
        
        # Save as ICO and PNG
        icon_path = Path(__file__).parent / 'sms_icon.png'
        ico_path = Path(__file__).parent / 'sms_icon.ico'
        
        image.save(str(icon_path), 'PNG')
        image.save(str(ico_path), 'ICO')
        
        print(f"[OK] Icon created: {icon_path}")
        print(f"[OK] Icon created: {ico_path}")
        return str(ico_path)
        
    except ImportError:
        print("[!] PIL/Pillow not installed. Skipping custom icon creation.")
        print("    Using default Python icon instead.")
        return None
    except Exception as e:
        print(f"[!] Error creating icon: {e}")
        return None

if __name__ == '__main__':
    print("=" * 70)
    print("Gaybeck Starkids SMS - Icon Creator")
    print("=" * 70)
    print()
    
    icon = create_app_icon()
    
    print()
    if icon:
        print("[OK] Icon created successfully!")
        print(f"Icon location: {icon}")
    else:
        print("[!] Using default Python icon for shortcut")
    print()
