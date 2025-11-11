import sys

with open('sms.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the User Management line and insert after it
for i, line in enumerate(lines):
    if 'User Management' in line and 'show_user_management' in line:
        # Insert new line after this one
        indent = '            '
        emoji = '\U0001F5D1\uFE0F'  # Wastebasket emoji
        new_line = indent + '("' + emoji + '   Data Management", self.show_data_management, "data_management", "admin"),  # Admin only - Clear test data\n'
        lines.insert(i+1, new_line)
        print(f'Inserted Data Management menu at line {i+2}')
        break

with open('sms.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
    
print('File updated successfully')
