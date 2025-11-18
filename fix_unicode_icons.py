#!/usr/bin/env python3
"""
Fix unicode emoji issues in sms.py
"""

import re

# Read the file
with open('sms.py', 'r', encoding='utf-8') as f:
    content = f.read()

#!/usr/bin/env python3
"""
Fix unicode emoji issues in sms.py
Comprehensive replacement of all corrupted unicode characters
"""

import re

# Read the file
with open('sms.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Define comprehensive mappings from corrupted unicode to proper emojis
replacements = {
    # Dashboard/Navigation
    r'≡ƒÜ½': '🏫',  # School building
    r'≡ƒÅá': '📊',  # Dashboard
    r'≡ƒÅ½': '📚',  # Books/Classes
    r'≡ƒæÑ': '👥',  # Students
    r'≡ƒæ¿ΓÇì≡ƒÅ½': '👨‍🏫',  # Teacher
    r'∩┐╜ΓÇì≡ƒÅ½': '👨‍🏫',  # Teacher (other variant)
    r'≡ƒæ¿ΓÇì': '👨‍',  # Person with job
    r'≡ƒÆ░': '💳',  # Money/Fee
    r'≡ƒÆ╡': '💰',  # Financial
    r'≡ƒô¥': '📝',  # Attendance/Checklist
    r'≡ƒñû': '🤖',  # AI
    r'≡ƒôÜ': 'ℹ️',  # Info
    r'≡ƒôê': '📈',  # Up arrow/positive
    r'≡ƒôë': '📉',  # Down arrow/negative
    r'≡ƒææ': '🔐',  # Admin/Lock
    r'≡ƒæ¿ΓÇì≡ƒÄô': '🎓',  # Scholarship
    r'≡ƒôè': '📊',  # Analytics
    
    # Reports & Tasks
    r'≡ƒôï': '📋',  # Reports/Tasks
    r'≡ƒÄ»': '📁',  # Projects
    r'≡ƒòÆ': '⏰',  # Timetable/Time
    
    # Buttons & Actions
    r'≡ƒôà': '✅',  # Checkmark/Attendance
    r'≡ƒæü∩╕Å': '👤',  # Profile
    r'≡ƒæü': '👤',  # Profile (variant)
    
    # Additional corrupted patterns
    r'ΓÜá∩╕Å': '⚠️',  # Warning
    r'Γä╣∩╕Å': 'ℹ️',  # Info
    r'≡ƒæñ': '👤',  # Person/Student name
}

# Apply replacements
for old, new in replacements.items():
    content = re.sub(old, new, content)

# Manual fixes for remaining corrupted text in specific contexts
# Fix "Detailed Analytics"
content = content.replace('≡ƒôè Detailed Analytics', '📊 Detailed Analytics')

# Fix any remaining mixed patterns
content = re.sub(r'≡ƒ[^"\']*?(\w)', r'\1', content)  # Remove any remaining corrupted ≡ƒ patterns

# Write the file back
with open('sms.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Fixed all unicode emoji issues in sms.py")

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
