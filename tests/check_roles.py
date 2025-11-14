import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'school_management.db')
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute('SELECT username, role FROM users')
users = cursor.fetchall()

print("\nRole values in database:")
for username, role in users:
    print(f'{username}: role="{role}" (type: {type(role).__name__})')

conn.close()
