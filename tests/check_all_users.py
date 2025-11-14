import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'school_management.db')
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("\n" + "="*70)
print("USER ACCOUNTS ANALYSIS")
print("="*70)

# Check all users
cursor.execute("SELECT id, username, password, full_name, role, is_active FROM users ORDER BY id")
users = cursor.fetchall()

print(f"\nTotal users in database: {len(users)}")
print("\nUser Details:")
print(f"{'ID':<5} {'Username':<15} {'Password':<15} {'Full Name':<20} {'Role':<12} {'Active':<8}")
print("-" * 85)

for user in users:
    user_id, username, password, full_name, role, is_active = user
    active_status = "Yes" if is_active else "No"
    print(f"{user_id:<5} {username:<15} {password:<15} {full_name:<20} {role:<12} {active_status:<8}")

# Check if we need to create default users
if len(users) == 1:
    print("\n" + "="*70)
    print("⚠️  ONLY ONE USER ACCOUNT FOUND")
    print("="*70)
    print("\nCreating default user accounts for testing...")
    
    # Create teacher account
    cursor.execute("""
        INSERT INTO users (username, password, full_name, role, is_active)
        VALUES ('teacher', 'teacher123', 'Teacher User', 'teacher', 1)
    """)
    
    # Create accountant account
    cursor.execute("""
        INSERT INTO users (username, password, full_name, role, is_active)
        VALUES ('accountant', 'accountant123', 'Accountant User', 'accountant', 1)
    """)
    
    # Create staff account
    cursor.execute("""
        INSERT INTO users (username, password, full_name, role, is_active)
        VALUES ('staff', 'staff123', 'Staff User', 'staff', 1)
    """)
    
    conn.commit()
    
    print("\n✓ Created the following accounts:")
    print("  1. teacher / teacher123 (Teacher)")
    print("  2. accountant / accountant123 (Accountant)")
    print("  3. staff / staff123 (Staff)")
    
    # Show updated list
    cursor.execute("SELECT id, username, password, full_name, role, is_active FROM users ORDER BY id")
    users = cursor.fetchall()
    
    print(f"\n\nUpdated User List:")
    print(f"{'ID':<5} {'Username':<15} {'Password':<15} {'Full Name':<20} {'Role':<12} {'Active':<8}")
    print("-" * 85)
    
    for user in users:
        user_id, username, password, full_name, role, is_active = user
        active_status = "Yes" if is_active else "No"
        print(f"{user_id:<5} {username:<15} {password:<15} {full_name:<20} {role:<12} {active_status:<8}")

print("\n" + "="*70)
print("LOGIN CREDENTIALS")
print("="*70)

cursor.execute("SELECT username, password, role FROM users WHERE is_active = 1 ORDER BY role")
active_users = cursor.fetchall()

print("\nActive login credentials:")
for username, password, role in active_users:
    role_emoji = {
        'admin': '👑',
        'teacher': '👨‍🏫',
        'accountant': '💰',
        'staff': '📋'
    }.get(role, '👤')
    print(f"  {role_emoji} {role.capitalize():<12} - Username: {username:<15} Password: {password}")

print("\n" + "="*70 + "\n")

conn.close()
