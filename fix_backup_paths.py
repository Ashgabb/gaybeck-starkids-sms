#!/usr/bin/env python3
"""
Fix backup functions to use correct database name
"""

with open('sms.py', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Replace school.db with school_management.db
original_count = content.count("'school.db'")
content = content.replace("'school.db'", "'school_management.db'")
new_count = content.count("'school_management.db'")

with open('sms.py', 'w', encoding='utf-8', errors='ignore') as f:
    f.write(content)

print(f"[OK] Fixed backup functions")
print(f"    Replaced {original_count} instances of 'school.db'")
print(f"    Now using 'school_management.db'")
print()
print("Affected functions:")
print("  • backup_database()")
print("  • restore_database()")
print("  • list_recent_backups()")
print("  • export_database_to_csv()")
