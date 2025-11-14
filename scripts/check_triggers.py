import sqlite3

conn = sqlite3.connect('school_management.db')
cursor = conn.cursor()

cursor.execute('''
    SELECT name, sql 
    FROM sqlite_master 
    WHERE type="trigger" 
    AND (tbl_name IN ("fees", "financial_transactions") OR sql LIKE "%statistics_cache%")
''')

triggers = cursor.fetchall()
print(f"Found {len(triggers)} triggers:\n")

for name, sql in triggers:
    print(f"\nTrigger: {name}")
    print("=" * 70)
    print(sql)
    print("=" * 70)

conn.close()
