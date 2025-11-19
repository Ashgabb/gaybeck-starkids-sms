"""
Comprehensive fix script for all remaining corrupted unicode and issues
"""
import re

# Read the file
with open('sms.py', 'r', encoding='utf-8') as f:
    content = f.read()

# All unicode replacements
replacements = [
    # Line 7687 - second stats icon
    ('("#27ae60", "Æ│")', '("#27ae60", "📊")'),
    # Line 16418 - icon in analysis
    ("'icon': 'Æ│'", "'icon': '📊'"),
    # Line 21179 - Payment Pattern
    ('f"Æ│ Payment Pattern:', 'f"📊 Payment Pattern:'),
    
    # Clear/Delete buttons - "ùæ∩╕Å" -> "🧹"
    ('text="ùæ∩╕Å Clear Photo"', 'text="🧹 Clear Photo"'),
    ('text="ùæ∩╕Å Clear All"', 'text="🧹 Clear All"'),
    ('text="ùæ∩╕Å Delete Selected"', 'text="🧹 Delete Selected"'),
    ('text="ùæ∩╕Å Delete"', 'text="🧹 Delete"'),
    ('text="ùæ∩╕Å Delete User"', 'text="🧹 Delete User"'),
    ('text="ùæ∩╕Å Delete Payment"', 'text="🧹 Delete Payment"'),
    ('text="ùæ∩╕Å Delete Transaction"', 'text="🧹 Delete Transaction"'),
    ('text="ùæ∩╕Å Delete Category"', 'text="🧹 Delete Category"'),
    ('text="ùæ∩╕Å Delete Budget"', 'text="🧹 Delete Budget"'),
    ('text="ùæ∩╕Å Clear Form"', 'text="🧹 Clear Form"'),
    ('text="ùæ∩╕Å Clear All"', 'text="🧹 Clear All"'),
    ('text="ùæ∩╕Å Data Management"', 'text="🧹 Data Management"'),
    ('text="ùæ∩╕Å', 'text="🧹'),
    ('text=\'ùæ∩╕Å', 'text=\'🧹'),
    
    # Save buttons - "Æ╛" -> "💾"
    ('text="Æ╛ Save Changes"', 'text="💾 Save Changes"'),
    ('text="Æ╛ Save Homework"', 'text="💾 Save Homework"'),
    ('text="Æ╛ Save User"', 'text="💾 Save User"'),
    ('text="Æ╛ Database Overview"', 'text="💾 Database Overview"'),
    ('text="Æ╛ Add Payment"', 'text="💾 Add Payment"'),
    ('text="Æ╛ Save Transaction"', 'text="💾 Save Transaction"'),
    ('text="Æ╛ Save Category"', 'text="💾 Save Category"'),
    ('text="Æ╛ Save Budget"', 'text="💾 Save Budget"'),
    ('text="Æ╛ Export Options:"', 'text="💾 Export Options:"'),
    ('text="Æ╛', 'text="💾'),
    ('text=\'Æ╛', 'text=\'💾'),
    
    # Tips/Instructions - "Æí" -> "💡"
    ('text="Æí Instructions:"', 'text="💡 Instructions:"'),
    ('text="Æí Additional Skills"', 'text="💡 Additional Skills"'),
    ('text="Æí Additional Skills & Competencies"', 'text="💡 Additional Skills & Competencies"'),
    ('text="Æí Budget Planning"', 'text="💡 Budget Planning"'),
    ('text="Æí Create/Edit Budget"', 'text="💡 Create/Edit Budget"'),
    ('text="Æí Tip:', 'text="💡 Tip:'),
    ('text="Æí Alternative:', 'text="💡 Alternative:'),
    ('text="Æí', 'text="💡'),
    ('text=\'Æí', 'text=\'💡'),
    
    # Expense - "Æ╕" -> "💸"
    ('text="Æ╕ Expense"', 'text="💸 Expense"'),
    ('text="Æ╕ Total Expenses"', 'text="💸 Total Expenses"'),
    ('text="Æ╕ Top Expense Categories"', 'text="💸 Top Expense Categories"'),
    ('text="Æ╕ Expense Analysis"', 'text="💸 Expense Analysis"'),
    ('text="Æ╕ Expense Analysis Report"', 'text="💸 Expense Analysis Report"'),
    ('text=\'Æ╕', 'text=\'💸'),
    ('"Æ╕', '"💸'),
    ("'Æ╕", "'💸"),
    ('text=f"', 'text=f"'),  # Placeholder
    
    # Role/Permissions - "æö" / "öæ"
    ('text="æö Role Distribution"', 'text="👥 Role Distribution"'),
    ('text="öæ Permissions"', 'text="🔐 Permissions"'),
    
    # Cash Flow - "Æ╣" -> "📊"
    ('text="Æ╣ Cash Flow Report"', 'text="📊 Cash Flow Report"'),
    
    # Income indicator
    ("'icon': 'ÆÄ'", "'icon': '📈'"),
    
    # Arrow navigation - "ΓåÆ" -> "→"
    ('ΓåÆ', '→'),
]

for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        print(f"✓ Fixed: {old[:30]}... -> {new[:30]}...")

# Remove DEBUG print statements
debug_patterns = [
    r'print\("DEBUG:[^"]*"\)',
    r'print\(f"DEBUG:[^"]*"\)',
    r'print\("DEBUG:[^"]*",  # Debug output\)',
    r'print\(f"DEBUG:[^"]*",  # Debug output\)',
]

removed_count = 0
for pattern in debug_patterns:
    matches = re.findall(pattern, content)
    if matches:
        for match in matches:
            content = content.replace(match + '\n', '')
            content = content.replace(match, '')
            removed_count += 1
            print(f"✓ Removed debug statement: {match[:50]}...")

print(f"\n✅ Removed {removed_count} debug print statements")

# Write back
with open('sms.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ All fixes applied successfully!")
