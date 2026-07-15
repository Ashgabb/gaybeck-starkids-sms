"""
Student Promotion Management System
Handles automatic and manual promotion of students to next class
Tracks promotion history and manages repetition
"""

import sqlite3
from datetime import datetime
from typing import List, Tuple, Dict, Optional


class PromotionManager:
    """Manages student promotions and class progression"""
    
    def __init__(self, db_path):
        """Initialize promotion manager with database path"""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self._ensure_promotion_tables()
    
    def connect(self):
        """Connect to database"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            return True
        except Exception as e:
            print(f"❌ Database connection error: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from database"""
        try:
            if self.conn:
                self.conn.close()
                self.conn = None
                self.cursor = None
        except Exception as e:
            print(f"❌ Disconnect error: {e}")
    
    def _ensure_promotion_tables(self):
        """Create promotion tracking tables if they don't exist"""
        try:
            self.connect()
            
            # Create promotion history table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS promotion_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id TEXT NOT NULL,
                    student_name TEXT NOT NULL,
                    from_class_id INTEGER,
                    to_class_id INTEGER,
                    from_class_name TEXT,
                    to_class_name TEXT,
                    promotion_type TEXT,  -- 'promotion', 'repetition', 'transfer'
                    promotion_date DATE,
                    academic_year TEXT,
                    promoted_by TEXT,
                    remarks TEXT,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create class progression table (defines which class comes after which)
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS class_progression (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    current_class_id INTEGER NOT NULL,
                    current_class_name TEXT NOT NULL,
                    next_class_id INTEGER NOT NULL,
                    next_class_name TEXT NOT NULL,
                    UNIQUE(current_class_id)
                )
            ''')
            
            # Create academic year settings table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS academic_years (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    year TEXT UNIQUE NOT NULL,
                    start_date DATE NOT NULL,
                    end_date DATE NOT NULL,
                    promotion_date DATE,
                    is_active BOOLEAN DEFAULT 1,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            self.conn.commit()
            self.disconnect()
            return True
            
        except Exception as e:
            print(f"❌ Error creating promotion tables: {e}")
            return False
    
    def get_class_hierarchy(self) -> List[Tuple]:
        """Get the class progression hierarchy"""
        try:
            if not self.connect():
                return []
            
            self.cursor.execute('''
                SELECT id, class_name FROM classes
                ORDER BY 
                    CASE 
                        WHEN class_name LIKE '%Creche%' THEN 1
                        WHEN class_name LIKE '%KG%' THEN 2
                        WHEN class_name LIKE '%Class 1%' THEN 3
                        WHEN class_name LIKE '%Class 2%' THEN 4
                        WHEN class_name LIKE '%Class 3%' THEN 5
                        WHEN class_name LIKE '%Class 4%' THEN 6
                        WHEN class_name LIKE '%Class 5%' THEN 7
                        WHEN class_name LIKE '%Class 6%' THEN 8
                        ELSE 99
                    END
            ''')
            
            classes = self.cursor.fetchall()
            self.disconnect()
            return classes
            
        except Exception as e:
            print(f"❌ Error getting class hierarchy: {e}")
            self.disconnect()
            return []
    
    def get_next_class(self, current_class_id: int) -> Optional[Tuple]:
        """Get the next class for a given class"""
        try:
            if not self.connect():
                return None
            
            # Check custom progression first
            self.cursor.execute('''
                SELECT next_class_id, next_class_name
                FROM class_progression
                WHERE current_class_id = ?
            ''', (current_class_id,))
            
            result = self.cursor.fetchone()
            if result:
                self.disconnect()
                return result
            
            # Get current class and auto-determine next
            self.cursor.execute('SELECT id, class_name FROM classes WHERE id = ?', (current_class_id,))
            current = self.cursor.fetchone()
            
            if not current:
                self.disconnect()
                return None
            
            current_class_name = current[1]
            
            # Auto progression logic
            progression_map = {
                'Creche': 'KG 1',
                'KG 1': 'KG 2',
                'KG 1A': 'KG 2A',
                'KG 1B': 'KG 2B',
                'KG 2': 'Class 1',
                'KG 2A': 'Class 1A',
                'KG 2B': 'Class 1B',
                'Class 1': 'Class 2',
                'Class 1A': 'Class 2A',
                'Class 1B': 'Class 2B',
                'Class 2': 'Class 3',
                'Class 3': 'Class 4',
                'Class 4': 'Class 5',
                'Class 5': 'Class 6',
                'Class 6': 'Class 6',  # Final class stays in 6
            }
            
            next_class_name = progression_map.get(current_class_name)
            if not next_class_name:
                self.disconnect()
                return None
            
            # Find next class ID
            self.cursor.execute(
                'SELECT id FROM classes WHERE class_name = ? LIMIT 1',
                (next_class_name,)
            )
            
            next_class = self.cursor.fetchone()
            self.disconnect()
            
            if next_class:
                return (next_class[0], next_class_name)
            
            return None
            
        except Exception as e:
            print(f"❌ Error getting next class: {e}")
            self.disconnect()
            return None
    
    def promote_student(self, student_id: str, to_class_id: int, 
                       promotion_type: str = 'promotion', 
                       promoted_by: str = 'System',
                       remarks: str = '') -> Tuple[bool, str]:
        """
        Promote or repeat a student to a new class
        
        Args:
            student_id: Student ID to promote
            to_class_id: Target class ID
            promotion_type: 'promotion', 'repetition', or 'transfer'
            promoted_by: Name of person doing promotion
            remarks: Additional remarks
        
        Returns:
            Tuple of (success, message)
        """
        try:
            if not self.connect():
                return False, "Database connection failed"
            
            # Get student info
            self.cursor.execute('''
                SELECT id, name, class_id FROM students WHERE student_id = ?
            ''', (student_id,))
            
            student = self.cursor.fetchone()
            if not student:
                self.disconnect()
                return False, f"Student {student_id} not found"
            
            student_record_id, student_name, current_class_id = student
            
            # Validate target class exists
            self.cursor.execute('SELECT class_name FROM classes WHERE id = ?', (to_class_id,))
            target_class = self.cursor.fetchone()
            if not target_class:
                self.disconnect()
                return False, f"Target class ID {to_class_id} not found"
            
            target_class_name = target_class[0]
            
            # Get current class name
            self.cursor.execute('SELECT class_name FROM classes WHERE id = ?', (current_class_id,))
            current_class_result = self.cursor.fetchone()
            current_class_name = current_class_result[0] if current_class_result else "Unknown"
            
            # Check capacity of target class
            self.cursor.execute(
                'SELECT current_students, capacity FROM classes WHERE id = ?',
                (to_class_id,)
            )
            capacity_info = self.cursor.fetchone()
            if capacity_info:
                current_students, capacity = capacity_info
                if capacity and current_students and current_students >= capacity:
                    self.disconnect()
                    return False, f"Target class {target_class_name} is at full capacity ({capacity})"
            
            # Update student's class
            self.cursor.execute('''
                UPDATE students
                SET previous_class_id = ?, class_id = ?
                WHERE student_id = ?
            ''', (current_class_id, to_class_id, student_id))
            
            # Update class student counts
            if current_class_id:
                self.cursor.execute('''
                    UPDATE classes
                    SET current_students = current_students - 1
                    WHERE id = ? AND current_students > 0
                ''', (current_class_id,))
            
            self.cursor.execute('''
                UPDATE classes
                SET current_students = current_students + 1
                WHERE id = ?
            ''', (to_class_id,))
            
            # Record promotion in history
            academic_year = datetime.now().strftime('%Y')
            promotion_date = datetime.now().strftime('%Y-%m-%d')
            
            self.cursor.execute('''
                INSERT INTO promotion_history
                (student_id, student_name, from_class_id, to_class_id, 
                 from_class_name, to_class_name, promotion_type, 
                 promotion_date, academic_year, promoted_by, remarks)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (student_id, student_name, current_class_id, to_class_id,
                  current_class_name, target_class_name, promotion_type,
                  promotion_date, academic_year, promoted_by, remarks))
            
            self.conn.commit()
            self.disconnect()
            
            promotion_label = {
                'promotion': 'promoted to',
                'repetition': 'repeated in',
                'transfer': 'transferred to'
            }.get(promotion_type, 'moved to')
            
            return True, f"✅ {student_name} successfully {promotion_label} {target_class_name}"
            
        except Exception as e:
            self.disconnect()
            return False, f"❌ Promotion error: {str(e)}"
    
    def promote_entire_class(self, from_class_id: int, 
                            promotion_type: str = 'promotion',
                            promoted_by: str = 'System',
                            remarks: str = '') -> Tuple[bool, str, Dict]:
        """
        Promote or repeat all students in a class
        
        Returns:
            Tuple of (success, message, results_dict)
        """
        try:
            if not self.connect():
                return False, "Database connection failed", {}
            
            # Get all students in the class
            self.cursor.execute('''
                SELECT student_id, name FROM students WHERE class_id = ? AND status != 'Inactive'
                ORDER BY name
            ''', (from_class_id,))
            
            students = self.cursor.fetchall()
            
            if not students:
                self.disconnect()
                return True, "No active students in this class to promote", {}
            
            # Get target class
            if promotion_type == 'repetition':
                to_class_id = from_class_id
            else:
                next_class_result = self.get_next_class(from_class_id)
                if not next_class_result:
                    self.disconnect()
                    return False, "Cannot determine next class for this class", {}
                to_class_id = next_class_result[0]
            
            self.disconnect()
            
            # Promote each student
            results = {
                'successful': 0,
                'failed': 0,
                'details': []
            }
            
            for student_id, student_name in students:
                success, message = self.promote_student(
                    student_id, to_class_id, promotion_type, promoted_by, remarks
                )
                
                if success:
                    results['successful'] += 1
                    results['details'].append(f"✅ {student_name}")
                else:
                    results['failed'] += 1
                    results['details'].append(f"❌ {student_name}: {message}")
            
            summary = f"Promoted {results['successful']}/{len(students)} students"
            if results['failed'] > 0:
                summary += f" ({results['failed']} failed)"
            
            return True, summary, results
            
        except Exception as e:
            self.disconnect()
            return False, f"❌ Bulk promotion error: {str(e)}", {}
    
    def get_promotion_history(self, student_id: Optional[str] = None,
                             academic_year: Optional[str] = None) -> List[Dict]:
        """Get promotion history records"""
        try:
            if not self.connect():
                return []
            
            query = 'SELECT * FROM promotion_history WHERE 1=1'
            params = []
            
            if student_id:
                query += ' AND student_id = ?'
                params.append(student_id)
            
            if academic_year:
                query += ' AND academic_year = ?'
                params.append(academic_year)
            
            query += ' ORDER BY promotion_date DESC LIMIT 100'
            
            self.cursor.execute(query, params)
            columns = [description[0] for description in self.cursor.description]
            rows = self.cursor.fetchall()
            
            self.disconnect()
            
            return [dict(zip(columns, row)) for row in rows]
            
        except Exception as e:
            print(f"❌ Error getting promotion history: {e}")
            self.disconnect()
            return []
    
    def undo_promotion(self, promotion_record_id: int) -> Tuple[bool, str]:
        """Undo a promotion and revert student to previous class"""
        try:
            if not self.connect():
                return False, "Database connection failed"
            
            # Get promotion record
            self.cursor.execute('''
                SELECT student_id, from_class_id, to_class_id FROM promotion_history
                WHERE id = ?
            ''', (promotion_record_id,))
            
            record = self.cursor.fetchone()
            if not record:
                self.disconnect()
                return False, "Promotion record not found"
            
            student_id, from_class_id, to_class_id = record
            
            # Revert student to previous class
            self.cursor.execute('''
                UPDATE students SET class_id = ? WHERE student_id = ?
            ''', (from_class_id, student_id))
            
            # Update class counts
            self.cursor.execute('''
                UPDATE classes SET current_students = current_students - 1
                WHERE id = ? AND current_students > 0
            ''', (to_class_id,))
            
            self.cursor.execute('''
                UPDATE classes SET current_students = current_students + 1
                WHERE id = ?
            ''', (from_class_id,))
            
            # Mark record as undone
            self.cursor.execute('''
                UPDATE promotion_history SET remarks = 'UNDONE'
                WHERE id = ?
            ''', (promotion_record_id,))
            
            self.conn.commit()
            self.disconnect()
            
            return True, "✅ Promotion successfully undone"
            
        except Exception as e:
            self.disconnect()
            return False, f"❌ Error undoing promotion: {str(e)}"
    
    def create_academic_year(self, year: str, start_date: str, 
                            end_date: str, promotion_date: str) -> Tuple[bool, str]:
        """Create a new academic year entry"""
        try:
            if not self.connect():
                return False, "Database connection failed"
            
            self.cursor.execute('''
                INSERT INTO academic_years (year, start_date, end_date, promotion_date)
                VALUES (?, ?, ?, ?)
            ''', (year, start_date, end_date, promotion_date))
            
            self.conn.commit()
            self.disconnect()
            
            return True, f"✅ Academic year {year} created"
            
        except sqlite3.IntegrityError:
            self.disconnect()
            return False, f"Academic year {year} already exists"
        except Exception as e:
            self.disconnect()
            return False, f"❌ Error creating academic year: {str(e)}"
    
    def get_academic_years(self) -> List[Dict]:
        """Get all academic years"""
        try:
            if not self.connect():
                return []
            
            self.cursor.execute('''
                SELECT * FROM academic_years ORDER BY year DESC LIMIT 10
            ''')
            
            columns = [description[0] for description in self.cursor.description]
            rows = self.cursor.fetchall()
            
            self.disconnect()
            
            return [dict(zip(columns, row)) for row in rows]
            
        except Exception as e:
            print(f"❌ Error getting academic years: {e}")
            self.disconnect()
            return []
    
    def get_class_statistics(self, class_id: int) -> Dict:
        """Get statistics for a class"""
        try:
            if not self.connect():
                return {}
            
            # Get class info
            self.cursor.execute('''
                SELECT class_name, current_students, capacity FROM classes WHERE id = ?
            ''', (class_id,))
            
            class_info = self.cursor.fetchone()
            if not class_info:
                self.disconnect()
                return {}
            
            class_name, current_students, capacity = class_info
            
            # Get student count by status
            self.cursor.execute('''
                SELECT status, COUNT(*) as count FROM students 
                WHERE class_id = ?
                GROUP BY status
            ''', (class_id,))
            
            status_counts = dict(self.cursor.fetchall())
            
            # Get promotion history
            self.cursor.execute('''
                SELECT promotion_type, COUNT(*) as count FROM promotion_history
                WHERE from_class_id = ? AND promotion_type IN ('promotion', 'repetition')
                GROUP BY promotion_type
            ''', (class_id,))
            
            promotion_counts = dict(self.cursor.fetchall())
            
            self.disconnect()
            
            return {
                'class_name': class_name,
                'current_students': current_students or 0,
                'capacity': capacity or 0,
                'occupancy_rate': (current_students / capacity * 100) if capacity and current_students else 0,
                'status_distribution': status_counts,
                'promotion_history': promotion_counts
            }
            
        except Exception as e:
            print(f"❌ Error getting class statistics: {e}")
            self.disconnect()
            return {}
    
    def search_students(self, search_term: str, limit: int = 20) -> List[Dict]:
        """
        Search for students by ID or name
        
        Args:
            search_term: Search query
            limit: Maximum number of results to return
        
        Returns:
            List of student records matching the search
        """
        try:
            if not self.connect():
                return []
            
            search_pattern = f"%{search_term}%"
            
            self.cursor.execute('''
                SELECT 
                    s.id,
                    s.student_id,
                    s.name,
                    s.class_id,
                    c.class_name,
                    s.date_of_birth,
                    s.status
                FROM students s
                LEFT JOIN classes c ON s.class_id = c.id
                WHERE (s.student_id LIKE ? OR s.name LIKE ?)
                AND s.status != 'Inactive'
                ORDER BY s.name ASC
                LIMIT ?
            ''', (search_pattern, search_pattern, limit))
            
            columns = ['id', 'student_id', 'name', 'class_id', 'class_name', 'date_of_birth', 'status']
            rows = self.cursor.fetchall()
            
            self.disconnect()
            
            return [dict(zip(columns, row)) for row in rows]
            
        except Exception as e:
            print(f"❌ Error searching students: {e}")
            self.disconnect()
            return []


# Test and demo functions
def test_promotion_manager():
    """Test the promotion manager"""
    manager = PromotionManager('school_management.db')
    
    print("\n" + "="*80)
    print("PROMOTION MANAGER TEST")
    print("="*80)
    
    # Test 1: Get class hierarchy
    print("\n✓ Class Hierarchy:")
    classes = manager.get_class_hierarchy()
    for class_id, class_name in classes:
        print(f"  {class_id}: {class_name}")
    
    # Test 2: Get next class
    if classes:
        current_class_id = classes[0][0]
        next_class = manager.get_next_class(current_class_id)
        print(f"\n✓ Next class after {classes[0][1]}: {next_class}")
    
    # Test 3: Get academic years
    print("\n✓ Academic Years:")
    years = manager.get_academic_years()
    if years:
        for year in years:
            print(f"  {year['year']}: {year['start_date']} to {year['end_date']}")
    else:
        print("  No academic years configured")
    
    # Test 4: Get promotion history
    print("\n✓ Recent Promotions:")
    history = manager.get_promotion_history()
    if history:
        for record in history[:5]:
            print(f"  {record['student_name']}: {record['from_class_name']} → {record['to_class_name']}")
    else:
        print("  No promotion history")
    
    print("\n" + "="*80)


if __name__ == '__main__':
    test_promotion_manager()
