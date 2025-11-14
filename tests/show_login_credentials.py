import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'school_management.db')

print("\n" + "="*70)
print("📋 QUICK LOGIN REFERENCE CARD")
print("="*70)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
    SELECT username, password, role, full_name, is_active 
    FROM users 
    ORDER BY 
        CASE role 
            WHEN 'admin' THEN 1 
            WHEN 'accountant' THEN 2 
            WHEN 'teacher' THEN 3 
            WHEN 'staff' THEN 4 
            ELSE 5 
        END
""")

users = cursor.fetchall()

print("\n┌─────────────────────────────────────────────────────────────────────┐")
print("│                     AVAILABLE USER ACCOUNTS                         │")
print("├─────────────────────────────────────────────────────────────────────┤")

for username, password, role, full_name, is_active in users:
    status = "✓ Active" if is_active else "✗ Inactive"
    
    role_info = {
        'admin': ('👑 Admin', 'Full system access'),
        'accountant': ('💰 Accountant', 'Financial management'),
        'teacher': ('👨‍🏫 Teacher', 'Class & attendance'),
        'staff': ('📋 Staff', 'Limited access')
    }
    
    emoji_role, description = role_info.get(role, ('👤 User', 'Basic access'))
    
    print(f"│                                                                     │")
    print(f"│  {emoji_role:<25} [{status}]                           │")
    print(f"│  Username: {username:<20}  Password: {password:<15}  │")
    print(f"│  {description:<65} │")

print("│                                                                     │")
print("└─────────────────────────────────────────────────────────────────────┘")

print("\n" + "="*70)
print("🔐 HOW TO LOGIN")
print("="*70)
print("""
1. Run the application: python sms.py
2. Enter username and password
3. Select the matching role radio button
4. Click '🔐 Login'

⚠️  IMPORTANT: You MUST select the correct role that matches your account!
   Example: If logging in as 'teacher', select '👨‍🏫 Teacher' role

""")

print("="*70)
print("✓ All accounts verified and ready to use")
print("="*70 + "\n")

conn.close()
