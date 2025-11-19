import sqlite3
import os

db_path = 'database/school_management.db'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Check tables
    print("=== DATABASE TABLES ===")
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = c.fetchall()
    for t in tables:
        print(f"✓ {t[0]}")
    
    # Check students table has is_scholarship
    print("\n=== STUDENTS TABLE SCHEMA ===")
    c.execute("PRAGMA table_info(students)")
    cols = c.fetchall()
    for col in cols:
        print(f"  {col[1]} ({col[2]})")
    
    # Check scholarship data
    print("\n=== SCHOLARSHIP DATA ===")
    c.execute("SELECT is_scholarship, COUNT(*) as count FROM students GROUP BY is_scholarship")
    for row in c.fetchall():
        status = "Fee-Paying" if row[0] == 0 else "Scholarship"
        print(f"  {status}: {row[1]} students")
    
    conn.close()
    print("\n✓ Database is healthy")
else:
    print(f"✗ Database not found at {db_path}")
