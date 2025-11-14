import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'school_management.db')
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("\n" + "="*70)
print("USER ACCOUNTS IN DATABASE")
print("="*70)

cursor.execute("SELECT id, username, password, full_name, role, is_active FROM users")
users = cursor.fetchall()

if users:
    print(f"\nFound {len(users)} user(s):\n")
    for user in users:
        id, username, password, full_name, role, is_active = user
        status = "Active" if is_active else "Inactive"
        print(f"ID: {id}")
        print(f"  Username: {username}")
        print(f"  Password: {password}")
        print(f"  Full Name: {full_name}")
        print(f"  Role: {role}")
        print(f"  Status: {status}")
        print()
else:
    print("\n[!] No users found in database!")
    print("\nCreating admin user...")
    cursor.execute('''
        INSERT INTO users (username, password, full_name, role, is_active)
        VALUES ('admin', 'admin123', 'Administrator', 'Admin', 1)
    ''')
    conn.commit()
    print("✓ Admin user created successfully")
    print("\nLogin credentials:")
    print("  Username: admin")
    print("  Password: admin123")

print("="*70 + "\n")

conn.close()
