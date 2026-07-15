"""
Teacher Learning Sync Module
Synchronizes learning data between teachers and the main system
"""
import sqlite3
from datetime import datetime
from types import SimpleNamespace

class TeacherLearningSyncDB:
    """Database for teacher learning synchronization"""
    
    def __init__(self, db_path="database/teacher_learning_sync.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Teacher learning sessions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS teacher_learning_sessions (
                    id INTEGER PRIMARY KEY,
                    teacher_id TEXT,
                    subject TEXT,
                    topic TEXT,
                    lesson_date TEXT,
                    duration_minutes INTEGER,
                    content TEXT,
                    created_at TEXT
                )
            ''')
            
            # Student learning progress table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS student_learning_progress (
                    id INTEGER PRIMARY KEY,
                    student_id TEXT,
                    teacher_id TEXT,
                    subject TEXT,
                    topic TEXT,
                    completion_percentage REAL,
                    quiz_score REAL,
                    last_updated TEXT
                )
            ''')
            
            # Teaching resources table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS teaching_resources (
                    id INTEGER PRIMARY KEY,
                    teacher_id TEXT,
                    subject TEXT,
                    resource_type TEXT,
                    resource_name TEXT,
                    resource_path TEXT,
                    created_at TEXT
                )
            ''')
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error initializing database: {e}")
    
    def add_learning_session(self, teacher_id, subject, topic, duration, content):
        """Add a learning session"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO teacher_learning_sessions 
                (teacher_id, subject, topic, lesson_date, duration_minutes, content, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (teacher_id, subject, topic, datetime.now().strftime("%Y-%m-%d"), 
                  duration, content, datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error adding learning session: {e}")
            return False
    
    def update_student_progress(self, student_id, teacher_id, subject, topic, completion, score):
        """Update student learning progress"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO student_learning_progress 
                (student_id, teacher_id, subject, topic, completion_percentage, quiz_score, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (student_id, teacher_id, subject, topic, completion, score, datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating student progress: {e}")
            return False
    
    def add_resource(self, teacher_id, subject, resource_type, resource_name, resource_path):
        """Add a teaching resource"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO teaching_resources 
                (teacher_id, subject, resource_type, resource_name, resource_path, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (teacher_id, subject, resource_type, resource_name, resource_path, datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error adding resource: {e}")
            return False
    
    def get_teacher_sessions(self, teacher_id):
        """Get all learning sessions for a teacher"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM teacher_learning_sessions 
                WHERE teacher_id = ? 
                ORDER BY lesson_date DESC
            ''', (teacher_id,))
            
            sessions = cursor.fetchall()
            conn.close()
            return sessions
        except Exception as e:
            print(f"Error getting teacher sessions: {e}")
            return []
    
    def get_student_progress(self, student_id):
        """Get student learning progress"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM student_learning_progress 
                WHERE student_id = ?
            ''', (student_id,))
            
            progress = cursor.fetchall()
            conn.close()
            return progress
        except Exception as e:
            print(f"Error getting student progress: {e}")
            return []

    def get_teacher_lesson_notes(self, teacher_id):
        """Return lesson notes for UI consumption"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT subject, topic, content
                FROM teacher_learning_sessions
                WHERE teacher_id = ?
                ORDER BY lesson_date DESC, id DESC
            ''', (str(teacher_id),))
            rows = cursor.fetchall()
            conn.close()
            return [
                SimpleNamespace(subject=r[0] or "", topic=r[1] or "", content=r[2] or "")
                for r in rows
            ]
        except Exception as e:
            print(f"Error getting teacher lesson notes: {e}")
            return []

    def get_teacher_curriculum(self, teacher_id):
        """Return curriculum resources for UI consumption"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT subject, resource_name
                FROM teaching_resources
                WHERE teacher_id = ? AND LOWER(COALESCE(resource_type, '')) LIKE '%curriculum%'
                ORDER BY id DESC
            ''', (str(teacher_id),))
            rows = cursor.fetchall()
            conn.close()
            return [
                SimpleNamespace(
                    subject=r[0] or "General",
                    grade_level="N/A",
                    curriculum_content=r[1] or ""
                )
                for r in rows
            ]
        except Exception as e:
            print(f"Error getting teacher curriculum: {e}")
            return []

    def get_teacher_assignments(self, teacher_id):
        """Return assignment resources for UI consumption"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT subject, resource_name, created_at
                FROM teaching_resources
                WHERE teacher_id = ? AND LOWER(COALESCE(resource_type, '')) LIKE '%assignment%'
                ORDER BY id DESC
            ''', (str(teacher_id),))
            rows = cursor.fetchall()
            conn.close()
            return [
                SimpleNamespace(
                    assignment_name=r[1] or "Untitled Assignment",
                    subject=r[0] or "General",
                    total_marks=100,
                    due_date=(r[2] or "").split('T')[0] if r[2] else "N/A"
                )
                for r in rows
            ]
        except Exception as e:
            print(f"Error getting teacher assignments: {e}")
            return []

    def get_teacher_quizzes(self, teacher_id):
        """Return quiz resources for UI consumption"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT subject, resource_name
                FROM teaching_resources
                WHERE teacher_id = ? AND LOWER(COALESCE(resource_type, '')) LIKE '%quiz%'
                ORDER BY id DESC
            ''', (str(teacher_id),))
            rows = cursor.fetchall()
            conn.close()
            return [
                SimpleNamespace(
                    quiz_name=r[1] or "Untitled Quiz",
                    subject=r[0] or "General",
                    topic="General",
                    num_questions=0,
                    total_marks=0,
                    is_published=0
                )
                for r in rows
            ]
        except Exception as e:
            print(f"Error getting teacher quizzes: {e}")
            return []

    def get_teacher_resources(self, teacher_id, resource_types=None):
        """Return uploaded teacher resources with file paths"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            if resource_types:
                normalized_types = [str(t).strip().lower() for t in resource_types if str(t).strip()]
                placeholders = ','.join(['?'] * len(normalized_types))
                cursor.execute(f'''
                    SELECT id, subject, resource_type, resource_name, resource_path, created_at
                    FROM teaching_resources
                    WHERE teacher_id = ?
                      AND LOWER(COALESCE(resource_type, '')) IN ({placeholders})
                    ORDER BY id DESC
                ''', [str(teacher_id)] + normalized_types)
            else:
                cursor.execute('''
                    SELECT id, subject, resource_type, resource_name, resource_path, created_at
                    FROM teaching_resources
                    WHERE teacher_id = ?
                    ORDER BY id DESC
                ''', (str(teacher_id),))

            rows = cursor.fetchall()
            conn.close()

            return [
                SimpleNamespace(
                    id=r[0],
                    subject=r[1] or "General",
                    resource_type=(r[2] or "learning_material").lower(),
                    resource_name=r[3] or "Untitled Resource",
                    resource_path=r[4] or "",
                    created_at=r[5] or ""
                )
                for r in rows
            ]
        except Exception as e:
            print(f"Error getting teacher resources: {e}")
            return []

    def get_teacher_learning_summary(self, teacher_id):
        """Return summary counts expected by the teacher learning support tab"""
        lesson_notes = self.get_teacher_lesson_notes(teacher_id)
        curriculum = self.get_teacher_curriculum(teacher_id)
        assignments = self.get_teacher_assignments(teacher_id)
        quizzes = self.get_teacher_quizzes(teacher_id)

        return {
            'lesson_notes': len(lesson_notes),
            'curriculum_documents': len(curriculum),
            'assignments': len(assignments),
            'quizzes': len(quizzes)
        }
    
    def sync_with_main_db(self):
        """Sync learning data with main database"""
        try:
            # Placeholder for sync logic
            return True
        except Exception as e:
            print(f"Error syncing with main database: {e}")
            return False

# Create a singleton instance
_teacher_learning_sync_db = None

def get_teacher_learning_sync_db():
    """Get or create the teacher learning sync database instance"""
    global _teacher_learning_sync_db
    if _teacher_learning_sync_db is None:
        _teacher_learning_sync_db = TeacherLearningSyncDB()
    return _teacher_learning_sync_db
