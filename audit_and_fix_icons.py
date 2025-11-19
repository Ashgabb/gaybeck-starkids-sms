#!/usr/bin/env python3
"""
Comprehensive icon corruption audit and fix
Finds and replaces all corrupted unicode characters with proper emoji
"""

import re

# Read the file
with open('sms.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Track replacements
replacements = [
    # Writing Task icons
    ("✏️∩╕Å Writing Task", "✏️ Writing Task"),
    ("✏️∩╕Å", "✏️"),
    
    # Medical section
    ("ÅÑ Medical & Health Information", "🏥 Medical & Health Information"),
    
    # Class Name
    ("Å╖∩╕Å Class Name", "📝 Class Name"),
    
    # Photo capture
    ("ô╕ Capture Photo", "📷 Capture Photo"),
    ("ô╕ Photo Capture", "📷 Photo Capture"),
    ("ô╕ Capture", "📷 Capture"),
    
    # Print Profile
    ("û¿∩╕Å Print Profile", "🖨️ Print Profile"),
    
    # Login Activity
    ("öÉ Today's Logins", "📱 Today's Logins"),
    ("öÉ Login Activity", "📱 Login Activity"),
    
    # Financial icons
    ("Åå", "✅"),  # Profit indicator
    
    # Top expenses
    ("ö¥ Top 10 Largest Expenses", "📊 Top 10 Largest Expenses"),
    
    # Backup
    ("ùé∩╕Å Full Database Backup", "💾 Full Database Backup"),
]

# Apply all replacements
original_content = content
for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        print(f"✓ Replaced: '{old}' → '{new}'")
    else:
        print(f"⚠ Not found: '{old}'")

# Count total replacements
replacement_count = sum(1 for old, new in replacements if old in original_content)

# Write back
with open('sms.py', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ Fixed {replacement_count} corrupted icons!")
print("✅ File updated successfully!")
