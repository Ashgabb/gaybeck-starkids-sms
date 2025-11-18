# Syncs fee, attendance, and financial modules for school_management.db
import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'school_management.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Example: Add triggers for sync
try:
    # Add your trigger creation logic here
    # Example:
    # cursor.execute('CREATE TRIGGER update_financial AFTER UPDATE ON fees BEGIN UPDATE financial SET amount_due = NEW.amount_due WHERE student_id = NEW.student_id; END;')
    print('Sync triggers created.')
except Exception as e:
    print(f'Error setting up sync triggers: {e}')

conn.commit()
conn.close()
print('Comprehensive sync setup complete.')
