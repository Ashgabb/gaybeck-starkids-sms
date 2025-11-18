#!/usr/bin/env python3
"""
Check and add is_scholarship column if missing
"""
import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'database', 'school_management.db')

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if is_scholarship column exists
    cursor.execute("PRAGMA table_info(students)")
    columns = cursor.fetchall()
    has_scholarship = any(col[1] == 'is_scholarship' for col in columns)
    
    if has_scholarship:
        print('✓ is_scholarship column exists')
        
        # Count students by scholarship status
        cursor.execute('SELECT COUNT(*) FROM students WHERE is_scholarship = 0')
        fee_paying = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM students WHERE is_scholarship = 1')
        scholarship = cursor.fetchone()[0]
        
        print(f'  Fee-paying students: {fee_paying}')
        print(f'  Scholarship students: {scholarship}')
        print(f'  Total students: {fee_paying + scholarship}')
    else:
        print('✗ is_scholarship column NOT found')
        print('  Available columns in students table:')
        for col in columns:
            print(f'    - {col[1]} ({col[2]})')
        
        print()
        print('Adding is_scholarship column...')
        cursor.execute('ALTER TABLE students ADD COLUMN is_scholarship INTEGER DEFAULT 0')
        conn.commit()
        print('✓ Column added successfully')
        
        # Verify it was added
        cursor.execute('SELECT COUNT(*) FROM students')
        total = cursor.fetchone()[0]
        print(f'  Total students in database: {total}')
    
    conn.close()

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
