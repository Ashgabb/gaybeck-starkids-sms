import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'school_management.db')
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("\n" + "="*70)
print("FEES TABLE STRUCTURE")
print("="*70)

cursor.execute("PRAGMA table_info(fees)")
columns = cursor.fetchall()

print("\nCurrent columns:")
for col in columns:
    print(f"  - {col[1]} ({col[2]})")

print("\n" + "="*70)
print("CHECKING FOR FEE TYPE AND PAYMENT MODE COLUMNS")
print("="*70)

column_names = [col[1] for col in columns]
if 'fee_type' in column_names:
    print("✓ fee_type column exists")
else:
    print("✗ fee_type column MISSING")

if 'payment_mode' in column_names:
    print("✓ payment_mode column exists")
else:
    print("✗ payment_mode column MISSING")

print("\n" + "="*70 + "\n")

conn.close()
