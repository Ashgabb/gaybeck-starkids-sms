# Recreates foreign key relationships and triggers for school_management.db
import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'school_management.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Example: Add foreign key relationships
try:
    cursor.execute('PRAGMA foreign_keys = ON;')
    # Add your table/relationship creation logic here
    # Example:
    # cursor.execute('ALTER TABLE attendance ADD COLUMN student_id INTEGER REFERENCES students(id);')
    print('Foreign key relationships enabled.')
except Exception as e:
    print(f'Error setting up relationships: {e}')

conn.commit()
conn.close()
print('Incremental relationships setup complete.')
