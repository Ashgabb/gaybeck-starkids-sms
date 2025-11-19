"""Fix final remaining corrupted patterns"""

with open('sms.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Specific line fixes (0-indexed)
fixes = [
    (828, 'Γ¡É', '⭐'),     # Line 829 - Excellent
    (12097, 'ΓùÅ', '❌'),   # Line 12098
    (12141, 'ΓùÅ', '❌'),   # Line 12142
    (12158, 'ΓùÅ', '❌'),   # Line 12159
    (12186, 'ΓùÅ', '❌'),   # Line 12187
    (12342, 'ΓùÅ', '❌'),   # Line 12343
    (12649, 'ΓÅ╕∩╕Å', '🔄'),  # Line 12650
    (13124, 'ΓÜ¬', '⛔'),   # Line 13125
    (13689, 'ΓÅ╕∩╕Å', '🔄'),  # Line 13690
]

for line_num, old_char, new_char in fixes:
    if line_num < len(lines):
        if old_char in lines[line_num]:
            lines[line_num] = lines[line_num].replace(old_char, new_char)
            print(f"✓ Fixed line {line_num + 1}: '{old_char}' → '{new_char}'")

with open('sms.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("\n✅ Final fixes applied!")
