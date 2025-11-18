#!/usr/bin/env python3
"""
Create a high-quality SMS icon (ICO format)
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_sms_icon():
    """Create a colorful SMS school icon"""
    
    # Create image with better size for icon
    size = 256
    img = Image.new('RGB', (size, size), color='#2E86AB')  # Blue background
    draw = ImageDraw.Draw(img)
    
    # Draw rounded rectangle background
    margin = 20
    draw.rectangle(
        [margin, margin, size-margin, size-margin],
        fill='#2E86AB',
        outline='#1A4D6D',
        width=3
    )
    
    # Draw book/school symbol (white)
    # Left page
    book_left = size // 4
    book_top = size // 3
    book_right = size // 2 - 10
    book_bottom = 2 * size // 3
    
    draw.rectangle(
        [book_left, book_top, book_right, book_bottom],
        fill='white',
        outline='#1A4D6D',
        width=2
    )
    
    # Right page
    book_right2 = 3 * size // 4
    draw.rectangle(
        [size // 2 + 10, book_top, book_right2, book_bottom],
        fill='#E8F4F8',
        outline='#1A4D6D',
        width=2
    )
    
    # Draw lines on left page (text)
    line_color = '#2E86AB'
    line_start = book_top + 25
    for i in range(3):
        y = line_start + (i * 18)
        draw.line([(book_left + 15, y), (book_right - 15, y)], fill=line_color, width=2)
    
    # Draw lines on right page
    for i in range(3):
        y = line_start + (i * 18)
        draw.line([(size // 2 + 25, y), (book_right2 - 15, y)], fill=line_color, width=2)
    
    # Draw graduation cap on top
    cap_center_x = size // 2
    cap_center_y = book_top - 40
    
    # Cap square
    cap_size = 30
    draw.rectangle(
        [cap_center_x - cap_size, cap_center_y - cap_size//2, 
         cap_center_x + cap_size, cap_center_y + cap_size//2],
        fill='#F18F01',
        outline='#1A4D6D',
        width=2
    )
    
    # Tassel
    draw.line(
        [(cap_center_x + cap_size + 10, cap_center_y - cap_size//2),
         (cap_center_x + cap_size + 10, cap_center_y + cap_size + 10)],
        fill='#F18F01',
        width=3
    )
    
    # Save as ICO (convert to RGBA for transparency support)
    ico_path = 'sms_icon.ico'
    img = img.convert('RGBA')
    img.save(ico_path, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
    
    print(f"[OK] Created {ico_path}")
    print(f"     Size: {os.path.getsize(ico_path)} bytes")
    return ico_path

if __name__ == '__main__':
    create_sms_icon()
