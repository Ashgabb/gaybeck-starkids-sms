"""
HR Manager Database Initialization Script
Creates all necessary tables for HR module functionality
"""

import sqlite3
import os
from datetime import datetime

def initialize_hr_tables(db_path='database/school_management.db'):
    """Initialize HR-related tables in the database"""
    
    # Ensure database directory exists
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Enable foreign keys
        cursor.execute('PRAGMA foreign_keys = ON')
        
        # 1. Employees table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                position TEXT NOT NULL,
                department TEXT NOT NULL,
                salary REAL NOT NULL,
                email TEXT UNIQUE,
                phone TEXT,
                hire_date TEXT NOT NULL,
                status TEXT DEFAULT 'Active' CHECK(status IN ('Active', 'Inactive', 'On Leave')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("✓ Employees table created")
        
        # 2. Timesheets table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS timesheets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER NOT NULL,
                month INTEGER NOT NULL,
                year INTEGER NOT NULL,
                hours_worked REAL DEFAULT 0,
                overtime_hours REAL DEFAULT 0,
                leave_hours REAL DEFAULT 0,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE,
                UNIQUE(employee_id, month, year)
            )
        ''')
        print("✓ Timesheets table created")
        
        # 2a. Daily Timesheet Entries table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS timesheet_daily (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER NOT NULL,
                day INTEGER NOT NULL,
                month INTEGER NOT NULL,
                year INTEGER NOT NULL,
                hours_worked REAL DEFAULT 0,
                overtime_hours REAL DEFAULT 0,
                leave_hours REAL DEFAULT 0,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE,
                UNIQUE(employee_id, day, month, year)
            )
        ''')
        print("✓ Daily Timesheet Entries table created")
        
        # 3. Employee Attendance table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employee_attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                present INTEGER DEFAULT 1 CHECK(present IN (0, 1)),
                status TEXT DEFAULT 'Present' CHECK(status IN ('Present', 'Absent', 'Leave', 'Late')),
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE,
                UNIQUE(employee_id, date)
            )
        ''')
        print("✓ Employee Attendance table created")
        
        # 4. Payroll Deductions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS payroll_deductions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER NOT NULL,
                month INTEGER NOT NULL,
                year INTEGER NOT NULL,
                deduction_type TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE
            )
        ''')
        print("✓ Payroll Deductions table created")
        
        # 5. Payroll Allowances table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS payroll_allowances (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER NOT NULL,
                month INTEGER NOT NULL,
                year INTEGER NOT NULL,
                allowance_type TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE
            )
        ''')
        print("✓ Payroll Allowances table created")
        
        # 6. Payslips table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS payslips (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER NOT NULL,
                month INTEGER NOT NULL,
                year INTEGER NOT NULL,
                basic_pay REAL NOT NULL,
                overtime_pay REAL DEFAULT 0,
                allowances REAL DEFAULT 0,
                gross_pay REAL NOT NULL,
                deductions REAL DEFAULT 0,
                net_pay REAL NOT NULL,
                status TEXT DEFAULT 'Draft' CHECK(status IN ('Draft', 'Processed', 'Paid')),
                payment_date TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE,
                UNIQUE(employee_id, month, year)
            )
        ''')
        print("✓ Payslips table created")
        
        # 7. Employee Assessments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employee_assessments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER NOT NULL,
                assessment_type TEXT NOT NULL,
                performance_rating REAL CHECK(performance_rating >= 0 AND performance_rating <= 5),
                comments TEXT,
                assessor_id INTEGER,
                date TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE
            )
        ''')
        print("✓ Employee Assessments table created")
        
        # 8. Training Programs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS training_programs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                category TEXT NOT NULL,
                duration_days INTEGER,
                cost REAL DEFAULT 0,
                provider TEXT,
                status TEXT DEFAULT 'Active' CHECK(status IN ('Active', 'Inactive', 'Completed')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("✓ Training Programs table created")
        
        # 9. Employee Training table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employee_training (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER NOT NULL,
                training_id INTEGER NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT,
                status TEXT DEFAULT 'Scheduled' CHECK(status IN ('Scheduled', 'In Progress', 'Completed', 'Cancelled')),
                completion_score REAL CHECK(completion_score >= 0 AND completion_score <= 100),
                certification_date TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE,
                FOREIGN KEY (training_id) REFERENCES training_programs(id) ON DELETE CASCADE
            )
        ''')
        print("✓ Employee Training table created")
        
        # 10. HR Actions table - for tracking recommended actions
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hr_actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER NOT NULL,
                action_type TEXT NOT NULL,
                description TEXT,
                urgency TEXT DEFAULT 'Medium' CHECK(urgency IN ('Low', 'Medium', 'High')),
                due_date TEXT,
                status TEXT DEFAULT 'Open' CHECK(status IN ('Open', 'In Progress', 'Completed', 'Closed')),
                assigned_to TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE
            )
        ''')
        print("✓ HR Actions table created")
        
        # Create indexes for better query performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_employee_dept ON employees(department)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_timesheet_emp ON timesheets(employee_id, year, month)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_timesheet_daily_emp ON timesheet_daily(employee_id, year, month, day)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_attendance_emp ON employee_attendance(employee_id, date)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_payslip_emp ON payslips(employee_id, year, month)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_assessment_emp ON employee_assessments(employee_id, date)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_training_emp ON employee_training(employee_id, status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_hr_actions_emp ON hr_actions(employee_id, status)')
        print("✓ Indexes created")
        
        # Create triggers for automatic timestamp updates
        cursor.execute('''
            CREATE TRIGGER IF NOT EXISTS tr_employees_update
            AFTER UPDATE ON employees
            FOR EACH ROW
            BEGIN
                UPDATE employees SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
            END
        ''')
        
        cursor.execute('''
            CREATE TRIGGER IF NOT EXISTS tr_timesheets_update
            AFTER UPDATE ON timesheets
            FOR EACH ROW
            BEGIN
                UPDATE timesheets SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
            END
        ''')
        
        cursor.execute('''
            CREATE TRIGGER IF NOT EXISTS tr_timesheet_daily_update
            AFTER UPDATE ON timesheet_daily
            FOR EACH ROW
            BEGIN
                UPDATE timesheet_daily SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
            END
        ''')
        
        cursor.execute('''
            CREATE TRIGGER IF NOT EXISTS tr_payslips_update
            AFTER UPDATE ON payslips
            FOR EACH ROW
            BEGIN
                UPDATE payslips SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
            END
        ''')
        
        print("✓ Triggers created")
        
        # Commit all changes
        conn.commit()
        print("\n✅ HR Database Initialization Complete!")
        print(f"Database location: {db_path}")
        
        return True
    
    except Exception as e:
        print(f"\n❌ Error during initialization: {e}")
        conn.rollback()
        return False
    
    finally:
        conn.close()


def verify_hr_tables(db_path='database/school_management.db'):
    """Verify that all HR tables were created successfully"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    required_tables = [
        'employees',
        'timesheets',
        'employee_attendance',
        'payroll_deductions',
        'payroll_allowances',
        'payslips',
        'employee_assessments',
        'training_programs',
        'employee_training',
        'hr_actions'
    ]
    
    try:
        missing_tables = []
        
        for table in required_tables:
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            if not cursor.fetchone():
                missing_tables.append(table)
        
        if missing_tables:
            print(f"\n⚠️  Missing tables: {', '.join(missing_tables)}")
            return False
        else:
            print("\n✅ All HR tables verified successfully!")
            return True
    
    except Exception as e:
        print(f"\n❌ Verification error: {e}")
        return False
    
    finally:
        conn.close()


if __name__ == '__main__':
    print("╔════════════════════════════════════════════════════╗")
    print("║     HR Manager Database Initialization Script      ║")
    print("╚════════════════════════════════════════════════════╝\n")
    
    # Determine database path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Try root directory first
    if os.path.exists('school_management.db'):
        db_path = 'school_management.db'
    else:
        db_path = os.path.join(current_dir, 'database', 'school_management.db')
    
    print(f"Initializing HR tables in: {db_path}\n")
    
    if initialize_hr_tables(db_path):
        verify_hr_tables(db_path)
    else:
        print("\n❌ Initialization failed!")
