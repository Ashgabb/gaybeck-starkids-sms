"""
Test Data Seeding Script
Populates the database with realistic test data for development and testing
Version: 1.0.0
"""

import sqlite3
import random
import logging
from datetime import datetime, timedelta
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestDataSeeder:
    """Generate and seed realistic test data"""
    
    FIRST_NAMES = [
        "John", "Jane", "Michael", "Sarah", "David", "Emma", "James", "Olivia",
        "Robert", "Sophia", "William", "Ava", "Richard", "Isabella", "Joseph",
        "Mia", "Thomas", "Charlotte", "Charles", "Amelia"
    ]
    
    LAST_NAMES = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
        "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
        "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"
    ]
    
    GENDERS = ['M', 'F']
    
    CLASSES = ['Primary 1', 'Primary 2', 'Primary 3', 'Primary 4', 'Primary 5', 'Primary 6',
               'JHS 1', 'JHS 2', 'JHS 3']
    
    def __init__(self, db_path='school_management.db'):
        """Initialize seeder with database path"""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """Connect to database"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            logger.info(f"✓ Connected to database: {self.db_path}")
        except Exception as e:
            logger.error(f"✗ Failed to connect to database: {e}")
            raise
    
    def disconnect(self):
        """Disconnect from database"""
        if self.conn:
            self.conn.close()
            logger.info("✓ Disconnected from database")
    
    def seed_teachers(self, count=10):
        """Add test teachers"""
        logger.info(f"\nSeeding {count} test teachers...")
        
        try:
            for i in range(count):
                name = f"{random.choice(self.FIRST_NAMES)} {random.choice(self.LAST_NAMES)}"
                hire_date = (datetime.now() - timedelta(days=random.randint(365, 3650))).strftime('%Y-%m-%d')
                starting_salary = random.choice([1500, 2000, 2500, 3000, 3500])
                phone = f"024{random.randint(1000000, 9999999)}"
                email = f"teacher{i+1}@school.edu"
                qualifications = random.choice(['B.Ed', 'M.Ed', 'B.Sc', 'B.A'])
                
                self.cursor.execute('''
                    INSERT INTO teachers (name, hire_date, starting_salary, phone, email, qualifications)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (name, hire_date, starting_salary, phone, email, qualifications))
            
            self.conn.commit()
            logger.info(f"✅ Added {count} teachers")
            
        except Exception as e:
            logger.error(f"✗ Failed to seed teachers: {e}")
            self.conn.rollback()
    
    def seed_students(self, count=50, per_class=None):
        """Add test students"""
        logger.info(f"\nSeeding {count} test students...")
        
        try:
            # Get existing classes
            self.cursor.execute('SELECT id FROM classes LIMIT 10')
            class_ids = [row[0] for row in self.cursor.fetchall()]
            
            if not class_ids:
                logger.warning("No classes found. Please create classes first.")
                return
            
            for i in range(count):
                name = f"{random.choice(self.FIRST_NAMES)} {random.choice(self.LAST_NAMES)}"
                student_id = f"ST{1000 + i}"
                dob = (datetime.now() - timedelta(days=random.randint(4745, 6205))).strftime('%Y-%m-%d')  # Ages 13-17
                gender = random.choice(self.GENDERS)
                class_id = random.choice(class_ids)
                phone = f"024{random.randint(1000000, 9999999)}"
                parent_email = f"parent{i+1}@email.com"
                bus_fee = random.choice([50, 100, 150, 0])
                monthly_fee = random.choice([200, 300, 400, 500])
                
                self.cursor.execute('''
                    INSERT INTO students (student_id, name, date_of_birth, gender, class_id, 
                                        phone, parent_email, bus_fee, monthly_fee, date_of_admission)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (student_id, name, dob, gender, class_id, phone, parent_email, bus_fee, monthly_fee, datetime.now().strftime('%Y-%m-%d')))
            
            self.conn.commit()
            logger.info(f"✅ Added {count} students")
            
        except Exception as e:
            logger.error(f"✗ Failed to seed students: {e}")
            self.conn.rollback()
    
    def seed_attendance(self, days=30):
        """Add test attendance records"""
        logger.info(f"\nSeeding attendance records for {days} days...")
        
        try:
            self.cursor.execute('SELECT id FROM students LIMIT 20')
            student_ids = [row[0] for row in self.cursor.fetchall()]
            
            if not student_ids:
                logger.warning("No students found. Seed students first.")
                return
            
            count = 0
            for day_offset in range(days):
                attendance_date = (datetime.now() - timedelta(days=day_offset)).strftime('%Y-%m-%d')
                
                for student_id in student_ids:
                    present = random.choice([True, False, True, True])  # 75% present
                    
                    self.cursor.execute('''
                        INSERT INTO attendance (student_id, date, present)
                        VALUES (?, ?, ?)
                    ''', (student_id, attendance_date, present))
                    
                    count += 1
            
            self.conn.commit()
            logger.info(f"✅ Added {count} attendance records")
            
        except Exception as e:
            logger.error(f"✗ Failed to seed attendance: {e}")
            self.conn.rollback()
    
    def seed_fees(self, count=30):
        """Add test fee records"""
        logger.info(f"\nSeeding {count} fee records...")
        
        try:
            self.cursor.execute('SELECT id FROM students LIMIT ?', (count,))
            student_ids = [row[0] for row in self.cursor.fetchall()]
            
            if not student_ids:
                logger.warning("No students found. Seed students first.")
                return
            
            current_date = datetime.now()
            
            for student_id in student_ids:
                for month_offset in range(1, 4):  # Last 3 months
                    month = (current_date - timedelta(days=30*month_offset)).month
                    year = (current_date - timedelta(days=30*month_offset)).year
                    
                    amount_due = random.choice([200, 300, 400, 500])
                    amount_paid = random.choice([0, amount_due, amount_due * 0.5])
                    arrears = max(0, amount_due - amount_paid)
                    
                    self.cursor.execute('''
                        INSERT INTO fees (student_id, month, year, amount_due, amount_paid, arrears)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (student_id, month, year, amount_due, amount_paid, arrears))
            
            self.conn.commit()
            logger.info(f"✅ Added fee records for {len(student_ids)} students")
            
        except Exception as e:
            logger.error(f"✗ Failed to seed fees: {e}")
            self.conn.rollback()
    
    def seed_grades(self, count=30):
        """Add test grade records"""
        logger.info(f"\nSeeding grade records...")
        
        try:
            self.cursor.execute('SELECT id FROM students LIMIT ?', (count,))
            student_ids = [row[0] for row in self.cursor.fetchall()]
            
            if not student_ids:
                logger.warning("No students found. Seed students first.")
                return
            
            subjects = ['English', 'Mathematics', 'Science', 'Social Studies', 'ICT', 'Physical Education']
            
            for student_id in student_ids:
                for subject in subjects:
                    score = random.randint(40, 100)
                    grade = self._calculate_grade(score)
                    
                    self.cursor.execute('''
                        INSERT INTO grades (student_id, subject, score, grade, date_recorded)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (student_id, subject, score, grade, datetime.now().strftime('%Y-%m-%d')))
            
            self.conn.commit()
            logger.info(f"✅ Added grades for {len(student_ids)} students across {len(subjects)} subjects")
            
        except Exception as e:
            logger.error(f"✗ Failed to seed grades: {e}")
            self.conn.rollback()
    
    def _calculate_grade(self, score):
        """Calculate letter grade from score"""
        if score >= 90:
            return 'A'
        elif score >= 80:
            return 'B'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        else:
            return 'F'
    
    def seed_all(self, teacher_count=10, student_count=50, days=30, fee_count=30):
        """Seed all test data"""
        logger.info("=" * 70)
        logger.info("STARTING TEST DATA SEEDING")
        logger.info("=" * 70)
        
        try:
            self.connect()
            self.seed_teachers(teacher_count)
            self.seed_students(student_count)
            self.seed_attendance(days)
            self.seed_fees(fee_count)
            self.seed_grades(fee_count)
            
            logger.info("\n" + "=" * 70)
            logger.info("✅ TEST DATA SEEDING COMPLETE")
            logger.info("=" * 70)
            
        finally:
            self.disconnect()


def seed_test_data_if_needed(db_path='school_management.db', min_students=20, min_teachers=3):
    """Seed database only when data volume is below the configured minimums."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM students")
    student_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM teachers")
    teacher_count = cursor.fetchone()[0]
    conn.close()

    if student_count >= min_students and teacher_count >= min_teachers:
        logger.info(
            "Skipping seed: existing dataset is sufficient (students=%s, teachers=%s)",
            student_count,
            teacher_count,
        )
        return False

    logger.info(
        "Seeding required: current dataset below threshold (students=%s, teachers=%s)",
        student_count,
        teacher_count,
    )
    seeder = TestDataSeeder(db_path)
    seeder.seed_all()
    return True


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Seed test data into SMS database')
    parser.add_argument('--db', default='school_management.db', help='Database path')
    parser.add_argument('--teachers', type=int, default=10, help='Number of teachers')
    parser.add_argument('--students', type=int, default=50, help='Number of students')
    parser.add_argument('--days', type=int, default=30, help='Days of attendance history')
    parser.add_argument('--fees', type=int, default=30, help='Number of fee records')
    parser.add_argument('--if-empty', action='store_true', help='Seed only when baseline data is missing')
    parser.add_argument('--min-students', type=int, default=20, help='Minimum student threshold for --if-empty')
    parser.add_argument('--min-teachers', type=int, default=3, help='Minimum teacher threshold for --if-empty')
    
    args = parser.parse_args()
    
    if args.if_empty:
        seed_test_data_if_needed(args.db, args.min_students, args.min_teachers)
        return

    seeder = TestDataSeeder(args.db)
    seeder.seed_all(
        teacher_count=args.teachers,
        student_count=args.students,
        days=args.days,
        fee_count=args.fees
    )


if __name__ == "__main__":
    main()
