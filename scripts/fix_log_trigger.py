import sqlite3

conn = sqlite3.connect('school_management.db')
cursor = conn.cursor()

print("Fixing log_financial_changes trigger...\n")

# Drop the old trigger
cursor.execute('DROP TRIGGER IF EXISTS log_financial_changes')
print("✓ Dropped old trigger")

# Recreate with simplified version (without the budget_plans update that references non-existent column)
cursor.execute('''
CREATE TRIGGER log_financial_changes
AFTER INSERT ON financial_transactions
BEGIN
    INSERT INTO user_activity_log (
        username, action_type, table_affected, record_id,
        new_values, timestamp
    ) VALUES (
        'system', 'INSERT', 'financial_transactions', NEW.id,
        json_object('amount', NEW.amount, 'type', NEW.transaction_type, 'category_id', NEW.category_id),
        datetime('now')
    );
END
''')
print("✓ Recreated trigger without budget_plans reference")

conn.commit()
conn.close()

print("\n" + "=" * 70)
print("Trigger fixed successfully!")
print("=" * 70)
