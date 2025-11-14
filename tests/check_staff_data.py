import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'school_management.db')
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("\n" + "="*70)
print("STAFF DATA ANALYSIS")
print("="*70)

# Check teachers table
cursor.execute("SELECT COUNT(*) FROM teachers")
teacher_count = cursor.fetchone()[0]
print(f"\n📊 Teachers Table: {teacher_count} records")

cursor.execute("""
    SELECT id, name, qualifications, class_id, phone, email 
    FROM teachers 
    ORDER BY id
""")
teachers = cursor.fetchall()

print("\nTeachers in database:")
for t in teachers:
    teacher_id, name, qualifications, class_id, phone, email = t
    print(f"  ID {teacher_id}: {name} | Qualifications: {qualifications} | Class: {class_id} | Phone: {phone}")

# Check users table
cursor.execute("SELECT COUNT(*) FROM users")
user_count = cursor.fetchone()[0]
print(f"\n👥 Users Table: {user_count} records")

cursor.execute("""
    SELECT id, username, full_name, role, is_active 
    FROM users 
    ORDER BY id
""")
users = cursor.fetchall()

print("\nUsers in database:")
for u in users:
    user_id, username, full_name, role, is_active = u
    print(f"  ID {user_id}: {username} ({full_name}) | Role: {role} | Active: {is_active}")

# Check if there's a staff table
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='staff'")
staff_table = cursor.fetchone()

if staff_table:
    cursor.execute("SELECT COUNT(*) FROM staff")
    staff_count = cursor.fetchone()[0]
    print(f"\n💼 Staff Table: {staff_count} records")
    
    cursor.execute("SELECT * FROM staff LIMIT 5")
    staff_records = cursor.fetchall()
    if staff_records:
        print("\nStaff records:")
        for s in staff_records:
            print(f"  {s}")
else:
    print("\n⚠️  No 'staff' table found in database")

print("\n" + "="*70)
print("SUMMARY")
print("="*70)
print(f"Teachers: {teacher_count}")
print(f"Users: {user_count}")
if staff_table:
    print(f"Staff: {staff_count}")
else:
    print("Staff: No dedicated staff table")
print("="*70 + "\n")

conn.close()
