import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'school_management.db')
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Get schema for key tables
tables = ['classes', 'students', 'teachers', 'fees', 'users']

for table in tables:
    print(f"\n{table} table columns:")
    cursor.execute(f"PRAGMA table_info({table})")
    columns = cursor.fetchall()
    for col in columns:
        print(f"  - {col[1]} ({col[2]})")

conn.close()
