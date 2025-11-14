import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'school_management.db')
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("\n" + "="*70)
print("UPDATING FEES TABLE SCHEMA")
print("="*70)

# Check if columns already exist
cursor.execute("PRAGMA table_info(fees)")
columns = cursor.fetchall()
column_names = [col[1] for col in columns]

# Add fee_type column if it doesn't exist
if 'fee_type' not in column_names:
    print("\n➤ Adding fee_type column...")
    cursor.execute("ALTER TABLE fees ADD COLUMN fee_type TEXT DEFAULT 'Tuition'")
    print("  ✓ fee_type column added")
else:
    print("\n✓ fee_type column already exists")

# Add payment_mode column if it doesn't exist
if 'payment_mode' not in column_names:
    print("\n➤ Adding payment_mode column...")
    cursor.execute("ALTER TABLE fees ADD COLUMN payment_mode TEXT DEFAULT 'Cash'")
    print("  ✓ payment_mode column added")
else:
    print("\n✓ payment_mode column already exists")

conn.commit()

# Verify the changes
print("\n" + "="*70)
print("UPDATED SCHEMA")
print("="*70)

cursor.execute("PRAGMA table_info(fees)")
columns = cursor.fetchall()

print("\nFees table columns:")
for col in columns:
    print(f"  - {col[1]} ({col[2]})")

print("\n" + "="*70)
print("SCHEMA UPDATE COMPLETED SUCCESSFULLY")
print("="*70 + "\n")

conn.close()
