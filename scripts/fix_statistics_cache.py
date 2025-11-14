import sqlite3

# Connect to database
conn = sqlite3.connect('school_management.db')
cursor = conn.cursor()

try:
    # Add the missing stat_type column
    cursor.execute('ALTER TABLE statistics_cache ADD COLUMN stat_type TEXT DEFAULT "general"')
    conn.commit()
    print("✓ Successfully added stat_type column to statistics_cache table")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("✓ Column stat_type already exists")
    else:
        print(f"✗ Error: {e}")

conn.close()
