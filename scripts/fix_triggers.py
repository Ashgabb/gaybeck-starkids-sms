import sqlite3

conn = sqlite3.connect('school_management.db')
cursor = conn.cursor()

print("Fixing database triggers to use correct column names...\n")

# Drop the old triggers that use wrong column names
old_triggers = [
    'student_enrollment_sync',
    'teacher_assignment_sync',
    'attendance_sync',
    'financial_transaction_stats_sync',
    'fee_payment_stats_sync'
]

for trigger_name in old_triggers:
    try:
        cursor.execute(f'DROP TRIGGER IF EXISTS {trigger_name}')
        print(f"✓ Dropped trigger: {trigger_name}")
    except Exception as e:
        print(f"✗ Error dropping {trigger_name}: {e}")

# Recreate triggers with correct column names

# 1. Student enrollment sync
cursor.execute('''
CREATE TRIGGER student_enrollment_sync
AFTER INSERT ON students
BEGIN
    INSERT INTO user_activity_log (user_id, activity_type, description, activity_data, timestamp)
    VALUES (
        1, -- Default system user
        'student_enrollment',
        'New student enrolled: ' || NEW.first_name || ' ' || NEW.last_name,
        json_object('student_id', NEW.id, 'class_id', NEW.class_id),
        datetime('now')
    );

    -- Update class enrollment statistics
    INSERT OR REPLACE INTO statistics_cache (metric_name, metric_value, calculated_at)
    SELECT
        'class_' || NEW.class_id || '_enrollment',
        (SELECT COUNT(*) FROM students WHERE class_id = NEW.class_id),
        datetime('now');

    -- Update total enrollment statistics
    INSERT OR REPLACE INTO statistics_cache (metric_name, metric_value, calculated_at)
    VALUES (
        'total_enrollment',
        (SELECT COUNT(*) FROM students),
        datetime('now')
    );
END
''')
print("✓ Recreated trigger: student_enrollment_sync")

# 2. Teacher assignment sync
cursor.execute('''
CREATE TRIGGER teacher_assignment_sync
AFTER INSERT ON teachers
BEGIN
    INSERT INTO user_activity_log (user_id, activity_type, description, activity_data, timestamp)
    VALUES (
        1,
        'teacher_assignment',
        'New teacher assigned: ' || NEW.name,
        json_object('teacher_id', NEW.id, 'class_id', NEW.class_id),
        datetime('now')
    );

    -- Update teacher count statistics
    INSERT OR REPLACE INTO statistics_cache (metric_name, metric_value, calculated_at)
    VALUES (
        'total_teachers',
        (SELECT COUNT(*) FROM teachers),
        datetime('now')
    );
END
''')
print("✓ Recreated trigger: teacher_assignment_sync")

# 3. Attendance sync
cursor.execute('''
CREATE TRIGGER attendance_sync
AFTER INSERT ON attendance
BEGIN
    INSERT INTO user_activity_log (user_id, activity_type, description, activity_data, timestamp)
    VALUES (
        1,
        'attendance_recorded',
        'Attendance recorded for student ID ' || NEW.student_id,
        json_object('student_id', NEW.student_id, 'date', NEW.date, 'present', NEW.present),
        datetime('now')
    );

    -- Update daily attendance statistics
    INSERT OR REPLACE INTO statistics_cache (metric_name, metric_value, calculated_at)
    SELECT
        'attendance_' || NEW.date,
        (SELECT COUNT(*) FROM attendance WHERE date = NEW.date AND present = 1),
        datetime('now');
END
''')
print("✓ Recreated trigger: attendance_sync")

# 4. Financial transaction stats sync
cursor.execute('''
CREATE TRIGGER financial_transaction_stats_sync
AFTER INSERT ON financial_transactions
BEGIN
    -- Update income statistics
    INSERT OR REPLACE INTO statistics_cache (metric_name, metric_value, calculated_at)
    VALUES (
        'total_income',
        COALESCE((SELECT SUM(amount) FROM financial_transactions WHERE transaction_type = 'income'), 0),
        datetime('now')
    );

    -- Update expense statistics
    INSERT OR REPLACE INTO statistics_cache (metric_name, metric_value, calculated_at)
    VALUES (
        'total_expenses',
        COALESCE((SELECT SUM(amount) FROM financial_transactions WHERE transaction_type = 'expense'), 0),
        datetime('now')
    );

    -- Update monthly income/expense
    INSERT OR REPLACE INTO statistics_cache (metric_name, metric_value, calculated_at)
    VALUES (
        'monthly_income_' || strftime('%Y-%m', NEW.transaction_date),
        COALESCE((SELECT SUM(amount) FROM financial_transactions
                 WHERE transaction_type = 'income'
                 AND strftime('%Y-%m', transaction_date) = strftime('%Y-%m', NEW.transaction_date)), 0),
        datetime('now')
    );
END
''')
print("✓ Recreated trigger: financial_transaction_stats_sync")

# 5. Fee payment stats sync
cursor.execute('''
CREATE TRIGGER fee_payment_stats_sync
AFTER UPDATE ON fees
WHEN OLD.amount_paid != NEW.amount_paid
BEGIN
    -- Update total fees collected
    INSERT OR REPLACE INTO statistics_cache (metric_name, metric_value, calculated_at)
    VALUES (
        'total_fees_collected',
        COALESCE((SELECT SUM(amount_paid) FROM fees), 0),
        datetime('now')
    );

    -- Update outstanding fees
    INSERT OR REPLACE INTO statistics_cache (metric_name, metric_value, calculated_at)
    VALUES (
        'total_outstanding_fees',
        COALESCE((SELECT SUM(arrears) FROM fees), 0),
        datetime('now')
    );

    -- Update monthly fee collection
    INSERT OR REPLACE INTO statistics_cache (metric_name, metric_value, calculated_at)
    VALUES (
        'monthly_fees_' || NEW.year || '_' || NEW.month,
        COALESCE((SELECT SUM(amount_paid) FROM fees WHERE year = NEW.year AND month = NEW.month), 0),
        datetime('now')
    );
END
''')
print("✓ Recreated trigger: fee_payment_stats_sync")

conn.commit()
conn.close()

print("\n" + "=" * 70)
print("All triggers have been fixed successfully!")
print("=" * 70)
