"""
AI Assessment and Grading Module for School Management System
Comprehensive module for AI-powered assessment, grading, and academic analytics
Version: 1.0
"""

import sqlite3
from datetime import datetime, date, timedelta
import json
from collections import defaultdict
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import warnings
warnings.filterwarnings('ignore')


class AIAssessmentGrading:
    """Comprehensive AI Assessment and Grading System"""
    
    def __init__(self, db_connection):
        """Initialize AI Assessment module with database connection"""
        self.conn = db_connection
        self.cursor = db_connection.cursor()
        self.scaler = StandardScaler()
        self.create_assessment_tables()
    
    def create_assessment_tables(self):
        """Create necessary tables for AI assessment system"""
        try:
            # AI Assessments table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS ai_assessments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    class_id INTEGER NOT NULL,
                    teacher_id INTEGER,
                    assessment_name TEXT NOT NULL,
                    subject TEXT NOT NULL,
                    assessment_type TEXT DEFAULT 'Quiz',
                    description TEXT,
                    total_marks INTEGER DEFAULT 100,
                    difficulty_level TEXT DEFAULT 'Medium',
                    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    due_date DATE,
                    is_published BOOLEAN DEFAULT 0,
                    status TEXT DEFAULT 'Draft',
                    FOREIGN KEY (class_id) REFERENCES classes (id),
                    FOREIGN KEY (teacher_id) REFERENCES teachers (id)
                )
            ''')
            
            # AI Assessment Questions table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS ai_assessment_questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    assessment_id INTEGER NOT NULL,
                    question_text TEXT NOT NULL,
                    question_type TEXT DEFAULT 'Multiple Choice',
                    marks INTEGER DEFAULT 1,
                    difficulty_level TEXT DEFAULT 'Medium',
                    options TEXT,
                    correct_answer TEXT,
                    explanation TEXT,
                    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (assessment_id) REFERENCES ai_assessments (id) ON DELETE CASCADE
                )
            ''')
            
            # Student Responses table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS ai_student_responses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    assessment_id INTEGER NOT NULL,
                    student_id INTEGER NOT NULL,
                    response_data TEXT,
                    total_marks_obtained INTEGER,
                    percentage_score REAL,
                    time_taken_minutes INTEGER,
                    submission_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    is_graded BOOLEAN DEFAULT 0,
                    ai_feedback TEXT,
                    status TEXT DEFAULT 'Submitted',
                    FOREIGN KEY (assessment_id) REFERENCES ai_assessments (id),
                    FOREIGN KEY (student_id) REFERENCES students (id)
                )
            ''')
            
            # AI Grading Model table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS ai_grading_models (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    class_id INTEGER NOT NULL,
                    model_name TEXT NOT NULL,
                    model_type TEXT DEFAULT 'Random Forest',
                    accuracy_score REAL,
                    training_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    total_assessments_trained INTEGER DEFAULT 0,
                    is_active BOOLEAN DEFAULT 1,
                    FOREIGN KEY (class_id) REFERENCES classes (id)
                )
            ''')
            
            # Student Performance Analytics table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS ai_student_performance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER NOT NULL,
                    class_id INTEGER NOT NULL,
                    total_assessments INTEGER DEFAULT 0,
                    average_score REAL DEFAULT 0,
                    highest_score INTEGER DEFAULT 0,
                    lowest_score INTEGER DEFAULT 0,
                    performance_trend TEXT DEFAULT 'Stable',
                    predicted_final_grade REAL,
                    risk_level TEXT DEFAULT 'Low',
                    learning_areas TEXT,
                    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (student_id) REFERENCES students (id),
                    FOREIGN KEY (class_id) REFERENCES classes (id)
                )
            ''')
            
            # Classroom Grading Statistics table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS ai_classroom_statistics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    class_id INTEGER NOT NULL,
                    assessment_id INTEGER,
                    class_average_score REAL,
                    class_highest_score INTEGER,
                    class_lowest_score INTEGER,
                    pass_rate REAL,
                    fail_rate REAL,
                    below_average_students INTEGER,
                    above_average_students INTEGER,
                    top_performers TEXT,
                    at_risk_students TEXT,
                    calculation_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (class_id) REFERENCES classes (id),
                    FOREIGN KEY (assessment_id) REFERENCES ai_assessments (id)
                )
            ''')
            
            self.conn.commit()
            print("✓ AI Assessment tables created successfully")
            
        except Exception as e:
            print(f"Error creating assessment tables: {e}")
    
    # ==================== AI ASSESSMENT GENERATION ====================
    
    def generate_ai_assessment(self, class_id, subject, assessment_type='Quiz', 
                              difficulty_level='Medium', num_questions=10, teacher_id=None):
        """Generate AI-powered assessment based on curriculum and difficulty"""
        try:
            assessment = {
                'class_id': class_id,
                'subject': subject,
                'type': assessment_type,
                'difficulty': difficulty_level,
                'total_marks': num_questions * 10,
                'questions': []
            }
            
            # Generate questions based on subject and difficulty
            questions = self._generate_questions(subject, difficulty_level, num_questions)
            assessment['questions'] = questions
            
            # Save assessment to database
            self.cursor.execute('''
                INSERT INTO ai_assessments 
                (class_id, teacher_id, assessment_name, subject, assessment_type, 
                 total_marks, difficulty_level, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (class_id, teacher_id, f"AI {assessment_type}: {subject}",
                  subject, assessment_type, assessment['total_marks'], 
                  difficulty_level, 'Draft'))
            
            assessment_id = self.cursor.lastrowid
            
            # Save questions
            for q in questions:
                self.cursor.execute('''
                    INSERT INTO ai_assessment_questions
                    (assessment_id, question_text, question_type, difficulty_level, explanation)
                    VALUES (?, ?, ?, ?, ?)
                ''', (assessment_id, q['text'], 'Multiple Choice', difficulty_level, q.get('explanation', '')))
            
            self.conn.commit()
            return assessment_id
            
        except Exception as e:
            print(f"Error generating assessment: {e}")
            return None
    
    def _generate_questions(self, subject, difficulty_level, num_questions):
        """Generate questions for the assessment"""
        # Sample question generation (in production, this would use advanced NLP/ML)
        question_bank = {
            'Mathematics': {
                'Easy': [
                    {'text': 'What is 2 + 2?', 'explanation': 'Basic arithmetic addition'},
                    {'text': 'What is the value of 5 * 3?', 'explanation': 'Multiplication operation'},
                    {'text': 'Solve: x + 5 = 10', 'explanation': 'Linear equation'},
                ],
                'Medium': [
                    {'text': 'Calculate the area of a triangle with base=10cm and height=8cm', 'explanation': 'Triangle area formula: 1/2 * base * height'},
                    {'text': 'What is the square root of 144?', 'explanation': 'Finding square roots'},
                    {'text': 'Solve: 2x² + 3x - 2 = 0', 'explanation': 'Quadratic equations'},
                ],
                'Hard': [
                    {'text': 'Find the derivative of f(x) = 3x² + 2x + 1', 'explanation': 'Calculus differentiation'},
                    {'text': 'Solve the system: 2x + y = 5, x - y = 1', 'explanation': 'System of equations'},
                    {'text': 'What is the probability of drawing 2 red cards from a deck?', 'explanation': 'Probability theory'},
                ]
            },
            'English': {
                'Easy': [
                    {'text': 'What is the opposite of "hot"?', 'explanation': 'Identifying antonyms'},
                    {'text': 'Find the verb in: "The cat runs quickly"', 'explanation': 'Identifying parts of speech'},
                    {'text': 'What is the plural of "child"?', 'explanation': 'English grammar rules'},
                ],
                'Medium': [
                    {'text': 'Identify the main idea in the passage...', 'explanation': 'Reading comprehension'},
                    {'text': 'Which sentence uses correct punctuation?', 'explanation': 'Punctuation rules'},
                    {'text': 'What is the literary device in "The sun smiled down"?', 'explanation': 'Identifying literary devices'},
                ],
                'Hard': [
                    {'text': 'Analyze the author\'s use of symbolism in the novel...', 'explanation': 'Literary analysis'},
                    {'text': 'Compare and contrast the two characters...', 'explanation': 'Comparative analysis'},
                    {'text': 'What is the significance of the narrative structure?', 'explanation': 'Narrative techniques'},
                ]
            },
            'Science': {
                'Easy': [
                    {'text': 'What gas do plants absorb from the atmosphere?', 'explanation': 'Photosynthesis basics'},
                    {'text': 'What is the chemical formula for water?', 'explanation': 'Chemistry fundamentals'},
                    {'text': 'Name the largest planet in our solar system', 'explanation': 'Astronomy basics'},
                ],
                'Medium': [
                    {'text': 'Explain the water cycle', 'explanation': 'Environmental processes'},
                    {'text': 'What are the main steps of photosynthesis?', 'explanation': 'Biology processes'},
                    {'text': 'Calculate the force if mass=5kg and acceleration=2m/s²', 'explanation': 'Physics formulas'},
                ],
                'Hard': [
                    {'text': 'Explain quantum entanglement and its implications', 'explanation': 'Quantum physics'},
                    {'text': 'Discuss the role of enzymes in cellular respiration', 'explanation': 'Biochemistry'},
                    {'text': 'Analyze the factors affecting enzyme activity', 'explanation': 'Advanced biology'},
                ]
            }
        }
        
        questions = []
        subject_questions = question_bank.get(subject, {}).get(difficulty_level, [])
        
        # Select random questions up to num_questions
        import random
        selected = random.sample(subject_questions * 2, min(num_questions, len(subject_questions) * 2))
        
        for q in selected[:num_questions]:
            questions.append(q)
        
        return questions
    
    # ==================== AUTOMATED GRADING ====================
    
    def auto_grade_assessment(self, assessment_id, student_id, student_responses):
        """Automatically grade student responses using AI"""
        try:
            total_marks = 0
            max_marks = 0
            feedback_items = []
            
            # Get assessment details
            self.cursor.execute('SELECT total_marks FROM ai_assessments WHERE id = ?', (assessment_id,))
            result = self.cursor.fetchone()
            max_marks = result[0] if result else 100
            
            # Get questions and correct answers
            self.cursor.execute('''
                SELECT id, question_text, marks FROM ai_assessment_questions 
                WHERE assessment_id = ?
            ''', (assessment_id,))
            
            questions = self.cursor.fetchall()
            
            for question_id, question_text, marks in questions:
                # Check student response
                if question_id in student_responses:
                    student_answer = student_responses[question_id]
                    
                    # Get correct answer from database
                    self.cursor.execute(
                        'SELECT correct_answer, explanation FROM ai_assessment_questions WHERE id = ?',
                        (question_id,)
                    )
                    answer_result = self.cursor.fetchone()
                    
                    if answer_result:
                        correct_answer, explanation = answer_result
                        
                        # Compare answers
                        if student_answer.lower().strip() == correct_answer.lower().strip():
                            total_marks += marks
                            feedback_items.append({
                                'question': question_id,
                                'status': 'Correct',
                                'feedback': '✓ Well answered!'
                            })
                        else:
                            feedback_items.append({
                                'question': question_id,
                                'status': 'Incorrect',
                                'feedback': f'The correct answer is: {correct_answer}. {explanation}'
                            })
            
            # Calculate percentage
            percentage = (total_marks / max_marks * 100) if max_marks > 0 else 0
            
            # Save grades to database
            self.cursor.execute('''
                INSERT INTO ai_student_responses
                (assessment_id, student_id, total_marks_obtained, percentage_score, 
                 ai_feedback, is_graded, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (assessment_id, student_id, total_marks, percentage,
                  json.dumps(feedback_items), 1, 'Graded'))
            
            self.conn.commit()
            
            grading_result = {
                'student_id': student_id,
                'assessment_id': assessment_id,
                'marks_obtained': total_marks,
                'total_marks': max_marks,
                'percentage': round(percentage, 2),
                'grade': self._calculate_grade(percentage),
                'feedback': feedback_items,
                'timestamp': datetime.now().isoformat()
            }
            
            return grading_result
            
        except Exception as e:
            print(f"Error auto-grading assessment: {e}")
            return None
    
    def _calculate_grade(self, percentage):
        """Calculate letter grade from percentage"""
        if percentage >= 90:
            return 'A'
        elif percentage >= 85:
            return 'A-'
        elif percentage >= 80:
            return 'B+'
        elif percentage >= 75:
            return 'B'
        elif percentage >= 70:
            return 'B-'
        elif percentage >= 65:
            return 'C+'
        elif percentage >= 60:
            return 'C'
        elif percentage >= 55:
            return 'C-'
        elif percentage >= 50:
            return 'D'
        else:
            return 'F'
    
    # ==================== PERFORMANCE PREDICTION ====================
    
    def predict_student_final_performance(self, student_id, class_id):
        """Predict student's final performance using ML"""
        try:
            # Get all assessment scores for the student
            self.cursor.execute('''
                SELECT ar.percentage_score, ar.total_marks_obtained, ra.total_marks
                FROM ai_student_responses ar
                JOIN ai_assessments ra ON ar.assessment_id = ra.id
                WHERE ar.student_id = ? AND ra.class_id = ?
            ''', (student_id, class_id))
            
            scores = self.cursor.fetchall()
            
            if len(scores) < 3:
                return {
                    'status': 'Insufficient Data',
                    'message': 'Need at least 3 assessments for prediction'
                }
            
            # Prepare data for prediction
            percentages = np.array([score[0] for score in scores]).reshape(-1, 1)
            
            # Fit linear regression model
            model = LinearRegression()
            X = np.arange(len(percentages)).reshape(-1, 1)
            y = percentages.flatten()
            
            model.fit(X, y)
            
            # Predict future performance (next 5 assessments)
            future_X = np.array([[len(percentages) + i] for i in range(5)])
            future_predictions = model.predict(future_X)
            
            # Calculate average future prediction
            predicted_final = np.mean(future_predictions)
            predicted_final = np.clip(predicted_final, 0, 100)
            
            # Calculate confidence interval
            residuals = y - model.predict(X)
            std_error = np.std(residuals)
            confidence = max(0, min(100, 100 - std_error))
            
            # Determine trend
            current_avg = np.mean(percentages[-3:])
            previous_avg = np.mean(percentages[:-3])
            
            if current_avg > previous_avg + 5:
                trend = 'Improving'
            elif current_avg < previous_avg - 5:
                trend = 'Declining'
            else:
                trend = 'Stable'
            
            prediction = {
                'student_id': student_id,
                'current_average': round(np.mean(percentages), 2),
                'predicted_final_grade': round(predicted_final, 2),
                'predicted_letter_grade': self._calculate_grade(predicted_final),
                'confidence_level': round(confidence, 1),
                'trend': trend,
                'total_assessments': len(scores),
                'recommendation': self._generate_performance_recommendation(predicted_final, trend)
            }
            
            # Update student performance analytics
            self._update_student_performance_analytics(student_id, class_id, prediction)
            
            return prediction
            
        except Exception as e:
            print(f"Error predicting student performance: {e}")
            return {'error': str(e)}
    
    def _generate_performance_recommendation(self, predicted_grade, trend):
        """Generate recommendations based on predicted performance"""
        if predicted_grade >= 90:
            rec = "Excellent! Maintain current study habits and challenge yourself with advanced topics."
        elif predicted_grade >= 80:
            rec = "Good performance. Focus on areas needing improvement to achieve higher grades."
        elif predicted_grade >= 70:
            rec = "Satisfactory performance. Increase study time and seek additional help in weak areas."
        elif predicted_grade >= 60:
            rec = "Below average. Urgent: Consider tutoring and increase engagement with course material."
        else:
            rec = "Poor performance. Immediate intervention needed: consult with teacher, increase study time, consider tutoring."
        
        if trend == 'Improving':
            rec += " Your trend is positive - keep up the improvement!"
        elif trend == 'Declining':
            rec += " Your trend is declining - address this immediately!"
        
        return rec
    
    def _update_student_performance_analytics(self, student_id, class_id, prediction):
        """Update student performance analytics table"""
        try:
            # Check if record exists
            self.cursor.execute(
                'SELECT id FROM ai_student_performance WHERE student_id = ? AND class_id = ?',
                (student_id, class_id)
            )
            exists = self.cursor.fetchone()
            
            if exists:
                self.cursor.execute('''
                    UPDATE ai_student_performance
                    SET average_score = ?, predicted_final_grade = ?, 
                        risk_level = ?, last_updated = CURRENT_TIMESTAMP
                    WHERE student_id = ? AND class_id = ?
                ''', (prediction['current_average'], prediction['predicted_final_grade'],
                      'High' if prediction['predicted_final_grade'] < 60 else 'Low',
                      student_id, class_id))
            else:
                self.cursor.execute('''
                    INSERT INTO ai_student_performance
                    (student_id, class_id, average_score, predicted_final_grade, risk_level)
                    VALUES (?, ?, ?, ?, ?)
                ''', (student_id, class_id, prediction['current_average'], 
                      prediction['predicted_final_grade'],
                      'High' if prediction['predicted_final_grade'] < 60 else 'Low'))
            
            self.conn.commit()
        except Exception as e:
            print(f"Error updating performance analytics: {e}")
    
    # ==================== CLASSROOM ANALYTICS ====================
    
    def generate_classroom_assessment_analytics(self, class_id):
        """Generate comprehensive assessment analytics for a classroom"""
        try:
            analytics = {
                'class_id': class_id,
                'total_assessments': 0,
                'class_statistics': {},
                'student_rankings': [],
                'performance_distribution': {},
                'at_risk_students': [],
                'top_performers': [],
                'recommendations': []
            }
            
            # Get all assessment results for the class
            self.cursor.execute('''
                SELECT 
                    ar.percentage_score, 
                    s.name,
                    s.id,
                    aa.assessment_name
                FROM ai_student_responses ar
                JOIN students s ON ar.student_id = s.id
                JOIN ai_assessments aa ON ar.assessment_id = aa.id
                WHERE aa.class_id = ? AND ar.is_graded = 1
            ''', (class_id,))
            
            results = self.cursor.fetchall()
            
            if not results:
                return {'status': 'No assessment data available'}
            
            analytics['total_assessments'] = len(results)
            
            # Calculate statistics
            scores = [r[0] for r in results]
            student_scores = defaultdict(list)
            
            for score, student_name, student_id, assessment_name in results:
                student_scores[student_id].append({
                    'name': student_name,
                    'score': score
                })
            
            # Class-wide statistics
            analytics['class_statistics'] = {
                'average_score': round(np.mean(scores), 2),
                'highest_score': max(scores),
                'lowest_score': min(scores),
                'pass_rate': round((len([s for s in scores if s >= 60]) / len(scores) * 100), 2),
                'fail_rate': round((len([s for s in scores if s < 60]) / len(scores) * 100), 2)
            }
            
            # Performance distribution
            analytics['performance_distribution'] = {
                'A (90-100)': len([s for s in scores if s >= 90]),
                'B (80-89)': len([s for s in scores if 80 <= s < 90]),
                'C (70-79)': len([s for s in scores if 70 <= s < 80]),
                'D (60-69)': len([s for s in scores if 60 <= s < 70]),
                'F (<60)': len([s for s in scores if s < 60])
            }
            
            # Student rankings
            student_averages = {}
            for student_id, scores_list in student_scores.items():
                avg = np.mean([s['score'] for s in scores_list])
                student_averages[student_id] = {
                    'name': scores_list[0]['name'],
                    'average': round(avg, 2),
                    'assessment_count': len(scores_list)
                }
            
            ranked_students = sorted(student_averages.items(), 
                                   key=lambda x: x[1]['average'], reverse=True)
            
            # Top performers
            for rank, (sid, data) in enumerate(ranked_students[:5], 1):
                analytics['top_performers'].append({
                    'rank': rank,
                    'student_id': sid,
                    'name': data['name'],
                    'average_score': data['average']
                })
            
            # At-risk students
            for sid, data in student_averages.items():
                if data['average'] < 60:
                    analytics['at_risk_students'].append({
                        'student_id': sid,
                        'name': data['name'],
                        'average_score': data['average'],
                        'risk_level': 'High' if data['average'] < 50 else 'Medium'
                    })
            
            # Recommendations
            avg_score = analytics['class_statistics']['average_score']
            if avg_score < 70:
                analytics['recommendations'].append({
                    'priority': 'High',
                    'message': 'Class average is below 70%. Recommend review of teaching methods and content delivery.'
                })
            
            if analytics['class_statistics']['fail_rate'] > 20:
                analytics['recommendations'].append({
                    'priority': 'High',
                    'message': f"High failure rate ({analytics['class_statistics']['fail_rate']}%). Consider intervention programs."
                })
            
            if len(analytics['at_risk_students']) > 3:
                analytics['recommendations'].append({
                    'priority': 'Medium',
                    'message': f"{len(analytics['at_risk_students'])} students are at risk. Provide tutoring support."
                })
            
            return analytics
            
        except Exception as e:
            print(f"Error generating classroom analytics: {e}")
            return {'error': str(e)}
    
    # ==================== ASSESSMENT MANAGEMENT ====================
    
    def get_class_assessments(self, class_id, status='All'):
        """Get all assessments for a class"""
        try:
            if status == 'All':
                self.cursor.execute('''
                    SELECT id, assessment_name, subject, assessment_type, total_marks,
                           difficulty_level, created_date, is_published, status
                    FROM ai_assessments
                    WHERE class_id = ?
                    ORDER BY created_date DESC
                ''', (class_id,))
            else:
                self.cursor.execute('''
                    SELECT id, assessment_name, subject, assessment_type, total_marks,
                           difficulty_level, created_date, is_published, status
                    FROM ai_assessments
                    WHERE class_id = ? AND status = ?
                    ORDER BY created_date DESC
                ''', (class_id, status))
            
            assessments = self.cursor.fetchall()
            return [
                {
                    'id': a[0],
                    'name': a[1],
                    'subject': a[2],
                    'type': a[3],
                    'total_marks': a[4],
                    'difficulty': a[5],
                    'created': a[6],
                    'published': bool(a[7]),
                    'status': a[8]
                }
                for a in assessments
            ]
        except Exception as e:
            print(f"Error fetching assessments: {e}")
            return []
    
    def publish_assessment(self, assessment_id):
        """Publish an assessment for students"""
        try:
            self.cursor.execute('''
                UPDATE ai_assessments
                SET is_published = 1, status = 'Published'
                WHERE id = ?
            ''', (assessment_id,))
            
            self.conn.commit()
            return {'status': 'Success', 'message': 'Assessment published successfully'}
        except Exception as e:
            return {'status': 'Error', 'message': str(e)}
    
    def get_assessment_results(self, assessment_id):
        """Get all student results for an assessment"""
        try:
            self.cursor.execute('''
                SELECT 
                    ar.id,
                    s.name,
                    s.student_id,
                    ar.total_marks_obtained,
                    ar.percentage_score,
                    ar.submission_date,
                    ar.is_graded
                FROM ai_student_responses ar
                JOIN students s ON ar.student_id = s.id
                WHERE ar.assessment_id = ?
                ORDER BY ar.percentage_score DESC
            ''', (assessment_id,))
            
            results = self.cursor.fetchall()
            return [
                {
                    'id': r[0],
                    'student_name': r[1],
                    'student_id': r[2],
                    'marks': r[3],
                    'percentage': r[4],
                    'submitted': r[5],
                    'graded': bool(r[6])
                }
                for r in results
            ]
        except Exception as e:
            print(f"Error fetching assessment results: {e}")
            return []
    
    # ==================== STUDENT FEEDBACK & INSIGHTS ====================
    
    def generate_student_assessment_feedback(self, assessment_id, student_id):
        """Generate detailed feedback for a student's assessment"""
        try:
            # Get response data
            self.cursor.execute('''
                SELECT total_marks_obtained, percentage_score, ai_feedback
                FROM ai_student_responses
                WHERE assessment_id = ? AND student_id = ?
            ''', (assessment_id, student_id))
            
            result = self.cursor.fetchone()
            if not result:
                return {'status': 'No response found'}
            
            marks, percentage, feedback_json = result
            
            feedback = {
                'marks_obtained': marks,
                'percentage': percentage,
                'grade': self._calculate_grade(percentage),
                'question_feedback': json.loads(feedback_json) if feedback_json else [],
                'strengths': [],
                'areas_for_improvement': [],
                'next_steps': []
            }
            
            # Analyze response patterns
            if percentage >= 80:
                feedback['strengths'].append('Strong understanding of core concepts')
            if percentage >= 90:
                feedback['strengths'].append('Excellent performance - Consider advanced challenges')
            
            if percentage < 70:
                feedback['areas_for_improvement'].append('Needs review of fundamental concepts')
            if percentage < 50:
                feedback['areas_for_improvement'].append('Significant gaps - Immediate tutoring recommended')
            
            # Generate next steps
            if percentage < 60:
                feedback['next_steps'] = [
                    'Schedule one-on-one tutoring session',
                    'Review core concepts from previous lessons',
                    'Practice similar problems for mastery'
                ]
            elif percentage < 80:
                feedback['next_steps'] = [
                    'Focus on weak areas identified above',
                    'Practice similar problems',
                    'Seek clarification from teacher'
                ]
            else:
                feedback['next_steps'] = [
                    'Attempt more challenging problems',
                    'Help peers who need support',
                    'Move to next topic'
                ]
            
            return feedback
            
        except Exception as e:
            print(f"Error generating feedback: {e}")
            return {'error': str(e)}
    
    # ==================== ANALYTICS DASHBOARD DATA ====================
    
    def get_ai_assessment_dashboard_data(self, class_id=None, teacher_id=None):
        """Get comprehensive dashboard data for AI assessments"""
        try:
            dashboard = {
                'total_assessments': 0,
                'total_students_assessed': 0,
                'average_class_performance': 0,
                'recent_analyses': [],
                'pending_tasks': [],
                'performance_trends': []
            }
            
            # Count total assessments
            query = 'SELECT COUNT(*) FROM ai_assessments WHERE is_published = 1'
            params = []
            
            if class_id:
                query += ' AND class_id = ?'
                params.append(class_id)
            
            self.cursor.execute(query, params)
            dashboard['total_assessments'] = self.cursor.fetchone()[0]
            
            # Count assessed students
            self.cursor.execute('''
                SELECT COUNT(DISTINCT student_id)
                FROM ai_student_responses
                WHERE is_graded = 1
            ''')
            dashboard['total_students_assessed'] = self.cursor.fetchone()[0]
            
            # Get average performance
            self.cursor.execute('''
                SELECT AVG(percentage_score)
                FROM ai_student_responses
                WHERE is_graded = 1
            ''')
            result = self.cursor.fetchone()
            dashboard['average_class_performance'] = round(result[0], 2) if result[0] else 0
            
            return dashboard
            
        except Exception as e:
            print(f"Error generating dashboard data: {e}")
            return {'error': str(e)}


# ==================== EXPORT FUNCTIONS ====================

def get_ai_assessment_grading_service(db_connection=None):
    """Factory function to get AI Assessment and Grading service"""
    if db_connection is None:
        # Create a default connection if none provided
        try:
            db_connection = sqlite3.connect('database/school_management.db')
        except Exception as e:
            print(f"Error creating default database connection: {e}")
            return None
    return AIAssessmentGrading(db_connection)
