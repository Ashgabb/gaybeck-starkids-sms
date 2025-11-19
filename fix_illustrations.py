"""Fix all remaining corrupted illustration/icon characters"""

with open('sms.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Comprehensive mapping of corrupted patterns to proper emoji
replacements = {
    # Attendance & Status
    'Γ£à': '✅',      # Present/Active
    'Γ¥î': '❌',      # Absent/Inactive
    'ΓÅ░': '⏱️',       # Late
    'Γ£ô': '✓',       # Checkmark/Good
    'Γ¥ô': '❓',      # Unknown
    'Γ£ì': '✏️',       # Writing
    
    # Gender
    'ΓÖé∩╕Å': '♂️',    # Male
    'ΓÖÇ∩╕Å': '♀️',    # Female
    
    # Actions & Common
    'Γ₧ò': '➕',      # Add
    'Γ£Å∩╕Å': '🔄',    # Update
    'öä': '🔄',      # Refresh
    'öì': '🔍',      # Search/Filter
    'ö┤': '📭',      # Empty
    'öö': '📝',      # Activity
    'Γ₧í∩╕Å': '➝',    # Stable
    
    # UI Elements
    'ΓÜí': '⚡',      # Quick
    'ΓÜÖ∩╕Å': '⚙️',    # Settings
    'ôä': '📊',      # Report
    'ôÄ': '📄',      # Document
    
    # Financial
    'Γé╡': '₡',       # Currency
    
    # Lists/Bullets
    'ΓÇó': '•',       # Bullet
    'Γûí': '☑️',      # Checklist
    
    # Research/Creative
    'ö¼': '🔬',      # Research
    'Ä¿': '🎨',      # Creative
}

print("Starting comprehensive corruption fix...")
replaced_count = 0

for corrupt, proper in replacements.items():
    if corrupt in content:
        old_count = content.count(corrupt)
        content = content.replace(corrupt, proper)
        replaced_count += old_count
        print(f"✓ Replaced {old_count:3d} instances of '{corrupt}' → '{proper}'")

# Write back
with open('sms.py', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ Total replacements: {replaced_count}")
print("✅ All corrupted illustrations fixed!")
