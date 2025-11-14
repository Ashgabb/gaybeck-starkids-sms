import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'school_management.db')
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("\n" + "="*70)
print("FIXING USER ROLES")
print("="*70)

# Update admin user to have lowercase role
cursor.execute('''
    UPDATE users 
    SET role = 'admin' 
    WHERE username = 'admin' AND role = 'Admin'
''')

rows_updated = cursor.rowcount
conn.commit()

if rows_updated > 0:
    print(f"\n✓ Updated {rows_updated} user(s) to have correct role format")
else:
    print("\n✓ Roles already in correct format")

# Verify the fix
cursor.execute("SELECT id, username, password, full_name, role FROM users")
users = cursor.fetchall()

print("\nCurrent user accounts:")
for user in users:
    id, username, password, full_name, role = user
    print(f"\n  Username: {username}")
    print(f"  Password: {password}")
    print(f"  Full Name: {full_name}")
    print(f"  Role: {role}")

print("\n" + "="*70)
print("Login with:")
print("  Username: admin")
print("  Password: admin123")
print("  Role: Select 'Admin' (👑)")
print("="*70 + "\n")

conn.close()
