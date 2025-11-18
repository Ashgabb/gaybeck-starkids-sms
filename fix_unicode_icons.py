#!/usr/bin/env python3
"""
Fix unicode emoji issues in sms.py
"""

import re

# Read the file
with open('sms.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Define mappings from corrupted unicode to proper emojis
replacements = {
    # Corrupted unicode patterns
    r'≡ƒÜ½': '🏫',  # School building
    r'≡ƒÅá': '📊',  # Dashboard
    r'≡ƒÅ½': '📚',  # Books/Classes
    r'≡ƒæÑ': '👥',  # Students
    r'≡ƒæ¿ΓÇì≡ƒÅ½': '👨‍🏫',  # Teacher (with corrupted)
    r'≡ƒÆ░': '💳',  # Money/Fee
    r'≡ƒÆ╡': '💰',  # Financial
    r'≡ƒô¥': '📝',  # Attendance
    r'≡ƒñû': '🤖',  # AI
    r'≡ƒôÜ': 'ℹ️',  # Info
    r'≡ƒôê': '📈',  # Up arrow
    r'≡ƒôë': '📉',  # Down arrow
    r'≡ƒææ': '🔐',  # Admin/Lock
    r'∩┐╜ΓÇì≡ƒÅ½': '👨‍🏫',  # Teacher (other corruption)
    r'≡ƒæ¿ΓÇì≡ƒÄô': '🎓',  # Scholarship
    r'≡ƒôè': '📊',  # Analytics
    r'Detailed Analytics': '📊 Detailed Analytics',
}

# Apply replacements
for old, new in replacements.items():
    content = re.sub(old, new, content)

# Additional specific fixes for dialog/admin roles
content = content.replace('("🔐 Admin"', '("🔐 Admin"')
content = content.replace('("👨‍🏫 Teacher"', '("👨‍🏫 Teacher"')

# Write the file back
with open('sms.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Fixed all unicode emoji issues in sms.py")
