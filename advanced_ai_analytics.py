"""
Advanced AI Analytics Module for School Management System
=========================================================
Implements 10 comprehensive AI features for student, teacher, and financial analytics.
Version: 1.0
"""

import sqlite3
from datetime import datetime, date, timedelta
import json
from collections import defaultdict
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')


class AdvancedAIAnalytics:
    """Comprehensive AI analytics engine with 10 advanced features"""
    
    def __init__(self, db_connection):
        self.conn = db_connection
        self.cursor = db_connection.cursor()
        self.le_dict = {}
        self.scaler = StandardScaler()
    
    # ==================== FEATURE 1: PREDICTIVE ANALYTICS ====================
    
    def predict_student_final_grade(self, student_id):
        """Predict final grade based on current performance"""
        try:
            # Get student grades history
            self.cursor.execute('''
                SELECT grade, subject, exam_type, date_recorded
                FROM grades
                WHERE student_id = ?
                ORDER BY date_recorded DESC
                LIMIT 20
            ''', (student_id,))
            
            grades = self.cursor.fetchall()
            if not grades:
                return {
                    'predicted_grade': None,
                    'confidence': 0,
                    'trend': 'No data',
                    'recommendation': 'Insufficient data for prediction'
                }
            
            grades_list = [g[0] for g in grades]
            
            # Calculate trend
            if len(grades_list) >= 3:
                recent = np.mean(grades_list[:5])
                older = np.mean(grades_list[5:])
                trend = 'Improving' if recent > older else 'Declining' if recent < older else 'Stable'
            else:
                trend = 'Insufficient history'
            
            # Predict final grade using linear regression
            X = np.arange(len(grades_list)).reshape(-1, 1)
            y = np.array(grades_list)
            
            # Simple linear prediction
            coeffs = np.polyfit(np.arange(len(grades_list)), grades_list, 1)
            predicted_final = np.polyval(coeffs, len(grades_list) + 5)
            predicted_final = max(0, min(100, predicted_final))
            
            # Calculate confidence based on data consistency
            std_dev = np.std(grades_list)
            confidence = max(0, min(100, 100 - (std_dev * 2)))
            
            recommendation = self._generate_grade_recommendation(predicted_final, trend)
            
            return {
                'predicted_grade': round(predicted_final, 1),
                'current_average': round(np.mean(grades_list), 1),
                'confidence': round(confidence, 1),
                'trend': trend,
                'recommendation': recommendation
            }
        except Exception as e:
            print(f"Grade prediction error: {e}")
            return {'error': str(e)}
    
    def _generate_grade_recommendation(self, predicted_grade, trend):
        """Generate personalized grade recommendation"""
        if predicted_grade >= 90:
            rec = "Excellent performance! Continue current study habits."
        elif predicted_grade >= 80:
            rec = "Good performance. Focus on improvement areas to reach excellence."
        elif predicted_grade >= 70:
            rec = "Satisfactory performance. Increase study time and seek tutoring."
        elif predicted_grade >= 60:
            rec = "Below average. Urgent intervention required. Consider tutoring program."
        else:
            rec = "Critical performance. Immediate intervention and support needed."
        
        if trend == 'Declining':
            rec += " WARNING: Performance is declining!"
        elif trend == 'Improving':
            rec += " POSITIVE: Performance is improving!"
        
        return rec
    
    def predict_grade_trend(self, student_id, days=90):
        """Predict grade trajectory for next period"""
        try:
            cutoff_date = date.today() - timedelta(days=days)
            
            self.cursor.execute('''
                SELECT grade, date_recorded
                FROM grades
                WHERE student_id = ? AND date_recorded >= ?
                ORDER BY date_recorded
            ''', (student_id, cutoff_date.isoformat()))
            
            records = self.cursor.fetchall()
            if len(records) < 3:
                return {'trend': 'Insufficient data', 'prediction': None}
            
            grades = [r[0] for r in records]
            dates = [datetime.strptime(r[1], '%Y-%m-%d').timestamp() for r in records]
            
            # Polynomial fit for trend
            coeffs = np.polyfit(dates, grades, 2)
            
            # Project next 30 days
            future_timestamp = dates[-1] + (30 * 24 * 3600)
            future_grade = np.polyval(coeffs, future_timestamp)
            future_grade = max(0, min(100, future_grade))
            
            # Trend classification
            if coeffs[0] < -0.001:
                trend_type = 'Declining sharply'
            elif coeffs[0] < 0:
                trend_type = 'Slowly declining'
            elif coeffs[0] > 0.001:
                trend_type = 'Improving sharply'
            elif coeffs[0] > 0:
                trend_type = 'Slowly improving'
            else:
                trend_type = 'Stable'
            
            return {
                'trend_type': trend_type,
                'projected_grade_30days': round(future_grade, 1),
                'current_average': round(np.mean(grades), 1),
                'volatility': round(np.std(grades), 1)
            }
        except Exception as e:
            return {'error': str(e)}
    
    # ==================== FEATURE 2: DROPOUT RISK DETECTION ====================
    
    def detect_dropout_risk_enhanced(self):
        """Enhanced dropout risk detection with multiple factors"""
        try:
            self.cursor.execute('''
                SELECT s.id, s.name, s.class_id,
                       COUNT(a.id) as total_attendance,
                       SUM(CASE WHEN a.present = 1 THEN 1 ELSE 0 END) as days_present,
                       AVG(g.grade) as avg_grade,
                       COUNT(DISTINCT f.id) as total_fees,
                       SUM(CASE WHEN f.arrears > 0 THEN 1 ELSE 0 END) as unpaid_fees
                FROM students s
                LEFT JOIN attendance a ON s.id = a.student_id
                LEFT JOIN grades g ON s.id = g.student_id
                LEFT JOIN fees f ON s.id = f.student_id
                WHERE s.status = 'Active'
                GROUP BY s.id
            ''')
            
            records = self.cursor.fetchall()
            at_risk = []
            
            for record in records:
                student_id, name, class_id = record[0], record[1], record[2]
                total_att, days_present, avg_grade = record[3], record[4], record[5]
                total_fees, unpaid_fees = record[6], record[7]
                
                risk_score = 0
                risk_factors = []
                
                # Attendance factor (40 points)
                if total_att and total_att > 0:
                    attendance_rate = (days_present / total_att) * 100
                    if attendance_rate < 60:
                        risk_score += 40
                        risk_factors.append(f"Critical attendance (${attendance_rate:.1f}%)")
                    elif attendance_rate < 75:
                        risk_score += 25
                        risk_factors.append(f"Low attendance ({attendance_rate:.1f}%)")
                
                # Grade factor (30 points)
                if avg_grade:
                    if avg_grade < 50:
                        risk_score += 30
                        risk_factors.append(f"Very low grades ({avg_grade:.1f})")
                    elif avg_grade < 65:
                        risk_score += 15
                        risk_factors.append(f"Low grades ({avg_grade:.1f})")
                
                # Fee factor (30 points)
                if total_fees and total_fees > 0:
                    unpaid_rate = (unpaid_fees / total_fees) * 100
                    if unpaid_rate > 70:
                        risk_score += 30
                        risk_factors.append(f"High fee arrears ({unpaid_rate:.1f}%)")
                    elif unpaid_rate > 30:
                        risk_score += 15
                        risk_factors.append(f"Fee payment issues ({unpaid_rate:.1f}%)")
                
                if risk_score >= 50:
                    risk_level = 'High'
                elif risk_score >= 30:
                    risk_level = 'Medium'
                else:
                    risk_level = 'Low'
                
                if risk_level in ['High', 'Medium']:
                    at_risk.append({
                        'id': student_id,
                        'name': name,
                        'class_id': class_id,
                        'risk_score': risk_score,
                        'risk_level': risk_level,
                        'risk_factors': risk_factors,
                        'attendance_rate': round((days_present / total_att * 100) if total_att else 0, 1),
                        'avg_grade': round(avg_grade, 1) if avg_grade else 0
                    })
            
            at_risk.sort(key=lambda x: x['risk_score'], reverse=True)
            return at_risk
        except Exception as e:
            print(f"Dropout risk detection error: {e}")
            return []
    
    # ==================== FEATURE 3: BEHAVIORAL ANOMALY DETECTION ====================
    
    def detect_behavioral_anomalies(self):
        """Detect unusual patterns in student behavior"""
        try:
            anomalies = []
            
            self.cursor.execute("SELECT id, name FROM students WHERE status = 'Active'")
            students = self.cursor.fetchall()
            
            for student_id, name in students:
                # Check for sudden grade drop
                grade_anomaly = self._check_grade_anomaly(student_id)
                if grade_anomaly:
                    anomalies.append({
                        'student_id': student_id,
                        'name': name,
                        'anomaly_type': 'Sudden Grade Drop',
                        'severity': grade_anomaly['severity'],
                        'details': grade_anomaly['details'],
                        'date_detected': date.today().isoformat()
                    })
                
                # Check for attendance spike
                att_anomaly = self._check_attendance_anomaly(student_id)
                if att_anomaly:
                    anomalies.append({
                        'student_id': student_id,
                        'name': name,
                        'anomaly_type': 'Attendance Spike',
                        'severity': att_anomaly['severity'],
                        'details': att_anomaly['details'],
                        'date_detected': date.today().isoformat()
                    })
            
            return anomalies
        except Exception as e:
            print(f"Anomaly detection error: {e}")
            return []
    
    def _check_grade_anomaly(self, student_id):
        """Check for sudden grade drops"""
        try:
            self.cursor.execute('''
                SELECT grade, date_recorded
                FROM grades
                WHERE student_id = ?
                ORDER BY date_recorded DESC
                LIMIT 10
            ''', (student_id,))
            
            grades = [g[0] for g in self.cursor.fetchall()]
            if len(grades) >= 3:
                recent = np.mean(grades[:3])
                previous = np.mean(grades[3:])
                drop = previous - recent
                
                if drop >= 15:
                    return {
                        'severity': 'High',
                        'details': f'Grade dropped by {drop:.1f} points'
                    }
                elif drop >= 8:
                    return {
                        'severity': 'Medium',
                        'details': f'Grade dropped by {drop:.1f} points'
                    }
            return None
        except:
            return None
    
    def _check_attendance_anomaly(self, student_id):
        """Check for unusual attendance patterns"""
        try:
            self.cursor.execute('''
                SELECT COUNT(*), SUM(CASE WHEN present = 1 THEN 1 ELSE 0 END)
                FROM attendance
                WHERE student_id = ? AND date >= date('now', '-30 days')
            ''', (student_id,))
            
            result = self.cursor.fetchone()
            if result and result[0] > 0:
                recent_rate = (result[1] / result[0]) * 100
                
                # Compare with historical
                self.cursor.execute('''
                    SELECT COUNT(*), SUM(CASE WHEN present = 1 THEN 1 ELSE 0 END)
                    FROM attendance
                    WHERE student_id = ? AND date < date('now', '-30 days')
                    LIMIT 100
                ''', (student_id,))
                
                hist_result = self.cursor.fetchone()
                if hist_result and hist_result[0] > 10:
                    hist_rate = (hist_result[1] / hist_result[0]) * 100
                    diff = abs(recent_rate - hist_rate)
                    
                    if diff >= 30:
                        return {
                            'severity': 'High',
                            'details': f'Attendance changed by {diff:.1f}% compared to history'
                        }
            return None
        except:
            return None
    
    # ==================== FEATURE 4: INTELLIGENT RECOMMENDATIONS ====================
    
    def generate_personalized_study_plans(self, student_id):
        """Generate AI-based personalized study recommendations"""
        try:
            self.cursor.execute('''
                SELECT AVG(grade), MIN(grade)
                FROM grades
                WHERE student_id = ?
            ''', (student_id,))
            
            avg_grade, min_grade = self.cursor.fetchone()
            
            # Get weak subjects
            self.cursor.execute('''
                SELECT subject, AVG(grade) as avg
                FROM grades
                WHERE student_id = ?
                GROUP BY subject
                ORDER BY avg
                LIMIT 3
            ''', (student_id,))
            
            weak_subjects = self.cursor.fetchall()
            
            plan = {
                'overall_average': round(avg_grade, 1) if avg_grade else 0,
                'recommendations': [],
                'study_focus_areas': [],
                'time_allocation': {}
            }
            
            # Generate recommendations
            if avg_grade and avg_grade < 60:
                plan['recommendations'].append('URGENT: Enroll in intensive tutoring program')
                plan['recommendations'].append('Increase daily study time to 3-4 hours')
                plan['recommendations'].append('Schedule weekly progress reviews with teachers')
            elif avg_grade and avg_grade < 75:
                plan['recommendations'].append('Attend group study sessions')
                plan['recommendations'].append('Focus on weak subjects')
                plan['recommendations'].append('Complete all homework assignments')
            else:
                plan['recommendations'].append('Maintain current performance level')
                plan['recommendations'].append('Explore advanced topics')
                plan['recommendations'].append('Consider peer tutoring to help others')
            
            # Focus areas
            for subject, avg in weak_subjects:
                plan['study_focus_areas'].append(f"{subject}: {avg:.1f} - needs improvement")
                hours = 4 if avg < 50 else 3 if avg < 65 else 2
                plan['time_allocation'][subject] = f"{hours} hours/week"
            
            return plan
        except Exception as e:
            return {'error': str(e)}
    
    def optimize_teacher_assignments(self):
        """Recommend optimal teacher-class assignments based on expertise"""
        try:
            self.cursor.execute('''
                SELECT t.id, t.name, COUNT(DISTINCT g.class_id) as classes_taught,
                       AVG(g.grade) as avg_student_grade
                FROM teachers t
                LEFT JOIN grades g ON g.teacher_id = t.id
                GROUP BY t.id
            ''')
            
            teachers = self.cursor.fetchall()
            recommendations = []
            
            for teacher_id, name, classes_taught, avg_grade in teachers:
                performance_score = (avg_grade / 100 * 100) if avg_grade else 50
                
                recommendation = {
                    'teacher_id': teacher_id,
                    'name': name,
                    'current_classes': classes_taught,
                    'performance_score': round(performance_score, 1),
                    'recommended_action': self._get_assignment_recommendation(performance_score, classes_taught)
                }
                recommendations.append(recommendation)
            
            return recommendations
        except Exception as e:
            return []
    
    def _get_assignment_recommendation(self, score, classes):
        if score >= 85:
            return 'Assign to advanced classes or mentorship roles'
        elif score >= 70:
            return 'Maintain current assignments'
        else:
            return 'Recommend professional development'
    
    def predict_fee_payment_plan(self, student_id):
        """Suggest personalized fee payment schedule"""
        try:
            self.cursor.execute('''
                SELECT 
                    SUM(amount_due) as total_due,
                    SUM(amount_paid) as total_paid,
                    SUM(arrears) as total_arrears
                FROM fees
                WHERE student_id = ?
            ''', (student_id,))
            
            result = self.cursor.fetchone()
            if not result or not result[0]:
                return {'recommendation': 'No fees data'}
            
            total_due, total_paid, total_arrears = result
            
            # Get payment history
            self.cursor.execute('''
                SELECT AVG(amount_paid)
                FROM fees
                WHERE student_id = ? AND amount_paid > 0
            ''', (student_id,))
            
            avg_payment = self.cursor.fetchone()[0] or 0
            
            plan = {
                'total_arrears': round(total_arrears, 2),
                'suggested_monthly_payment': round(total_arrears / 6, 2) if total_arrears else 0,
                'historical_average_payment': round(avg_payment, 2),
                'payment_feasibility': 'High' if avg_payment > total_due / 6 else 'Medium' if avg_payment > 0 else 'Low',
                'recommended_schedule': self._generate_payment_schedule(total_arrears)
            }
            
            return plan
        except Exception as e:
            return {'error': str(e)}
    
    def _generate_payment_schedule(self, amount):
        """Generate optimal payment schedule"""
        if amount <= 500:
            return "2-3 months: 2-3 equal installments"
        elif amount <= 1000:
            return "3-4 months: 3-4 equal installments"
        else:
            return "5-6 months: 5-6 equal installments or negotiate with school"
    
    # ==================== FEATURE 5: SMART ATTENDANCE ANALYSIS ====================
    
    def analyze_attendance_patterns(self, student_id):
        """Analyze detailed attendance patterns"""
        try:
            self.cursor.execute('''
                SELECT strftime('%w', date) as day_of_week, COUNT(*) as count,
                       SUM(CASE WHEN present = 1 THEN 1 ELSE 0 END) as present_count
                FROM attendance
                WHERE student_id = ?
                GROUP BY strftime('%w', date)
            ''', (student_id,))
            
            patterns = {}
            days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
            
            for day_num, count, present_count in self.cursor.fetchall():
                day_name = days[int(day_num)]
                rate = (present_count / count * 100) if count > 0 else 0
                patterns[day_name] = {
                    'total_days': count,
                    'present': present_count,
                    'absent': count - present_count,
                    'attendance_rate': round(rate, 1)
                }
            
            # Find problematic day
            worst_day = min(patterns.items(), key=lambda x: x[1]['attendance_rate']) if patterns else None
            
            analysis = {
                'daily_patterns': patterns,
                'worst_performing_day': worst_day[0] if worst_day else None,
                'is_chronic_absentee': self._is_chronic_absentee(student_id),
                'seasonal_trends': self._analyze_seasonal_trends(student_id),
                'subject_specific_absences': self._get_subject_specific_absences(student_id)
            }
            
            return analysis
        except Exception as e:
            return {'error': str(e)}
    
    def _is_chronic_absentee(self, student_id):
        """Check if student is chronically absent"""
        try:
            self.cursor.execute('''
                SELECT COUNT(*), SUM(CASE WHEN present = 1 THEN 1 ELSE 0 END)
                FROM attendance
                WHERE student_id = ?
            ''', (student_id,))
            
            result = self.cursor.fetchone()
            if result and result[0] > 0:
                rate = (result[1] / result[0]) * 100
                return {
                    'is_chronic': rate < 70,
                    'attendance_rate': round(rate, 1),
                    'threshold': 70
                }
            return {'is_chronic': False}
        except:
            return {'is_chronic': False}
    
    def _analyze_seasonal_trends(self, student_id):
        """Analyze seasonal attendance patterns"""
        try:
            self.cursor.execute('''
                SELECT strftime('%m', date) as month, COUNT(*) as count,
                       SUM(CASE WHEN present = 1 THEN 1 ELSE 0 END) as present_count
                FROM attendance
                WHERE student_id = ?
                GROUP BY strftime('%m', date)
            ''', (student_id,))
            
            trends = {}
            months = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                     'July', 'August', 'September', 'October', 'November', 'December']
            
            for month_num, count, present_count in self.cursor.fetchall():
                rate = (present_count / count * 100) if count > 0 else 0
                trends[months[int(month_num)]] = round(rate, 1)
            
            return trends
        except:
            return {}
    
    def _get_subject_specific_absences(self, student_id):
        """Get absence patterns by subject"""
        try:
            # This would require subject field in attendance table
            return {}  # Placeholder for schema enhancement
        except:
            return {}
    
    # ==================== FEATURE 6: FINANCIAL INTELLIGENCE ====================
    
    def predict_fee_defaults(self):
        """ML-based fee default prediction"""
        try:
            # Get training data
            self.cursor.execute('''
                SELECT s.id, 
                       COUNT(DISTINCT f.id) as fee_records,
                       SUM(f.arrears) as total_arrears,
                       AVG(a.present) as attendance_rate,
                       COUNT(DISTINCT a.id) as attendance_records
                FROM students s
                LEFT JOIN fees f ON s.id = f.student_id
                LEFT JOIN attendance a ON s.id = a.student_id
                GROUP BY s.id
            ''')
            
            predictions = []
            for student_id, fee_records, total_arrears, att_rate, att_records in self.cursor.fetchall():
                if fee_records == 0:
                    continue
                
                # Simple risk scoring
                arrear_risk = min(100, (total_arrears / 5000 * 100)) if total_arrears else 0
                att_risk = max(0, (100 - (att_rate * 100))) if att_rate else 50
                
                risk_score = (arrear_risk * 0.6) + (att_risk * 0.4)
                
                if risk_score >= 60:
                    risk_level = 'High'
                elif risk_score >= 35:
                    risk_level = 'Medium'
                else:
                    risk_level = 'Low'
                
                predictions.append({
                    'student_id': student_id,
                    'default_risk_score': round(risk_score, 1),
                    'risk_level': risk_level,
                    'total_arrears': round(total_arrears, 2) if total_arrears else 0,
                    'attendance_factor': round(att_rate * 100, 1) if att_rate else 0
                })
            
            return sorted(predictions, key=lambda x: x['default_risk_score'], reverse=True)
        except Exception as e:
            return []
    
    def calculate_financial_health_score(self, student_id):
        """Comprehensive financial health scoring"""
        try:
            self.cursor.execute('''
                SELECT 
                    COUNT(*) as total_fees,
                    SUM(CASE WHEN arrears = 0 THEN 1 ELSE 0 END) as paid_fees,
                    SUM(arrears) as total_arrears,
                    SUM(amount_due) as total_due
                FROM fees
                WHERE student_id = ?
            ''', (student_id,))
            
            result = self.cursor.fetchone()
            if not result or result[0] == 0:
                return {'score': 100, 'status': 'No fees'}
            
            total, paid, arrears, due = result
            
            # Calculate score (0-100)
            payment_rate = (paid / total * 100) if total > 0 else 0
            arrear_ratio = (arrears / due * 100) if due > 0 else 0
            
            score = (payment_rate * 0.7) - (arrear_ratio * 0.3)
            score = max(0, min(100, score))
            
            if score >= 85:
                status = 'Excellent'
            elif score >= 70:
                status = 'Good'
            elif score >= 50:
                status = 'Fair'
            else:
                status = 'Poor'
            
            return {
                'financial_health_score': round(score, 1),
                'status': status,
                'payment_rate': round(payment_rate, 1),
                'arrear_percentage': round(arrear_ratio, 1),
                'total_arrears': round(arrears, 2)
            }
        except Exception as e:
            return {'error': str(e)}
    
    # ==================== FEATURE 7: TEACHER PERFORMANCE ANALYTICS ====================
    
    def calculate_teacher_effectiveness(self, teacher_id):
        """Calculate comprehensive teacher effectiveness score"""
        try:
            self.cursor.execute('''
                SELECT AVG(g.grade) as avg_student_grade,
                       COUNT(DISTINCT g.student_id) as students_taught,
                       COUNT(DISTINCT g.class_id) as classes_taught
                FROM grades g
                WHERE g.teacher_id = ?
            ''', (teacher_id,))
            
            result = self.cursor.fetchone()
            avg_grade, students, classes = result if result else (0, 0, 0)
            
            # Effectiveness score (0-100)
            grade_score = (avg_grade / 100 * 100) if avg_grade else 50
            
            score = grade_score
            
            recommendations = []
            if score >= 85:
                rating = 'Excellent'
                recommendations.append('Continue current teaching methods')
            elif score >= 75:
                rating = 'Good'
                recommendations.append('Consider professional development for advancement')
            elif score >= 60:
                rating = 'Average'
                recommendations.append('Recommend professional development training')
            else:
                rating = 'Below Average'
                recommendations.append('URGENT: Recommend coaching and mentoring')
            
            return {
                'teacher_id': teacher_id,
                'effectiveness_score': round(score, 1),
                'rating': rating,
                'avg_student_grade': round(avg_grade, 1) if avg_grade else 0,
                'students_taught': students,
                'classes_taught': classes,
                'recommendations': recommendations
            }
        except Exception as e:
            return {'error': str(e)}
    
    def analyze_class_dynamics(self, class_id):
        """Analyze class performance and dynamics"""
        try:
            self.cursor.execute('''
                SELECT COUNT(DISTINCT s.id) as total_students,
                       AVG(g.grade) as avg_grade,
                       MIN(g.grade) as min_grade,
                       MAX(g.grade) as max_grade,
                       COUNT(DISTINCT a.student_id) as students_with_att
                FROM classes c
                LEFT JOIN students s ON c.id = s.class_id
                LEFT JOIN grades g ON s.id = g.student_id
                LEFT JOIN attendance a ON s.id = a.student_id
                WHERE c.id = ?
            ''', (class_id,))
            
            result = self.cursor.fetchone()
            total, avg, min_g, max_g, att_count = result if result else (0, 0, 0, 0, 0)
            
            variance = max_g - min_g if max_g and min_g else 0
            
            return {
                'class_id': class_id,
                'total_students': total,
                'average_grade': round(avg, 1) if avg else 0,
                'grade_range': f"{min_g} - {max_g}" if min_g and max_g else "N/A",
                'performance_variance': round(variance, 1),
                'class_assessment': self._assess_class_performance(avg) if avg else 'No data'
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _assess_class_performance(self, avg_grade):
        if avg_grade >= 85:
            return 'Excellent class performance'
        elif avg_grade >= 75:
            return 'Good class performance'
        elif avg_grade >= 65:
            return 'Satisfactory performance'
        else:
            return 'Needs improvement'
    
    # ==================== FEATURE 8: CLUSTERING & SEGMENTATION ====================
    
    def segment_students_for_intervention(self):
        """Automatically segment students for targeted interventions"""
        try:
            # Get student data
            self.cursor.execute('''
                SELECT s.id, s.name,
                       AVG(g.grade) as avg_grade,
                       COUNT(DISTINCT a.id) as attendance_count,
                       SUM(CASE WHEN a.present = 1 THEN 1 ELSE 0 END) as days_present
                FROM students s
                LEFT JOIN grades g ON s.id = g.student_id
                LEFT JOIN attendance a ON s.id = a.student_id
                GROUP BY s.id
            ''')
            
            data = self.cursor.fetchall()
            if len(data) < 3:
                return {'message': 'Insufficient data for clustering'}
            
            # Prepare features
            X = []
            student_ids = []
            for student_id, name, avg_grade, att_count, days_present in data:
                grade = avg_grade or 50
                att_rate = (days_present / att_count * 100) if att_count and att_count > 0 else 50
                X.append([grade, att_rate])
                student_ids.append((student_id, name))
            
            X = np.array(X)
            
            # K-means clustering
            kmeans = KMeans(n_clusters=min(3, len(data)), random_state=42)
            clusters = kmeans.fit_predict(X)
            
            segmentation = {'High Performers': [], 'Average': [], 'At Risk': []}
            cluster_names = ['High Performers', 'Average', 'At Risk']
            
            for idx, (student_id, name) in enumerate(student_ids):
                cluster = clusters[idx]
                cluster_name = cluster_names[cluster] if cluster < len(cluster_names) else 'Other'
                segmentation[cluster_name].append({
                    'student_id': student_id,
                    'name': name,
                    'cluster': cluster
                })
            
            return segmentation
        except Exception as e:
            return {'error': str(e)}
    
    def identify_learning_style_groups(self):
        """Group similar learners for peer tutoring"""
        try:
            # Would require learning style assessment data
            # This is a placeholder for enhanced schema
            return {'message': 'Learning style assessment data needed'}
        except Exception as e:
            return {'error': str(e)}
    
    def classify_risk_categories(self):
        """Automatically classify students into risk categories"""
        try:
            risk_categories = {'Low': [], 'Medium': [], 'High': []}
            
            dropouts = self.detect_dropout_risk_enhanced()
            for student in dropouts:
                category = student['risk_level']
                if category in risk_categories:
                    risk_categories[category].append({
                        'id': student['id'],
                        'name': student['name'],
                        'score': student['risk_score']
                    })
            
            return risk_categories
        except Exception as e:
            return {'error': str(e)}
    
    # ==================== FEATURE 9: NLP-BASED FEATURES ====================
    
    def generate_automated_feedback(self, student_id):
        """Generate personalized feedback comments"""
        try:
            # Get student data
            grade_pred = self.predict_student_final_grade(student_id)
            study_plan = self.generate_personalized_study_plans(student_id)
            anomalies = self.detect_behavioral_anomalies()
            
            feedback_parts = []
            
            if grade_pred.get('predicted_grade'):
                pred = grade_pred['predicted_grade']
                if pred >= 85:
                    feedback_parts.append(f"Excellent predicted performance at {pred}%. Keep up the outstanding work!")
                elif pred >= 75:
                    feedback_parts.append(f"Good predicted grade of {pred}%. With focused effort, you can reach excellence.")
                elif pred >= 65:
                    feedback_parts.append(f"Predicted grade is {pred}%. Focus on weak areas and seek additional support.")
                else:
                    feedback_parts.append(f"Concerning predicted grade of {pred}%. Urgent intervention needed.")
            
            if study_plan.get('recommendations'):
                feedback_parts.append("Recommendations: " + " ".join(study_plan['recommendations'][:2]))
            
            return {'automated_feedback': " ".join(feedback_parts)}
        except Exception as e:
            return {'error': str(e)}
    
    def generate_parent_communication(self, student_id):
        """Auto-generate professional messages for parents"""
        try:
            self.cursor.execute("SELECT name FROM students WHERE id = ?", (student_id,))
            student_name = self.cursor.fetchone()[0]
            
            grade_pred = self.predict_student_final_grade(student_id)
            
            message = f"Dear Parent/Guardian,\n\n"
            message += f"We are writing to provide an update on {student_name}'s academic progress.\n\n"
            
            if grade_pred.get('predicted_grade'):
                message += f"Predicted Performance: {grade_pred['predicted_grade']}\n"
                message += f"Trend: {grade_pred.get('trend', 'N/A')}\n\n"
                message += f"Recommendation: {grade_pred.get('recommendation', 'Monitor progress')}\n\n"
            
            message += "Please contact us if you would like to discuss your child's progress.\n\n"
            message += "Best regards,\nSchool Management"
            
            return {'parent_message': message}
        except Exception as e:
            return {'error': str(e)}
    
    # ==================== FEATURE 10: TIME SERIES FORECASTING ====================
    
    def forecast_enrollment_trends(self):
        """Forecast future enrollment based on trends"""
        try:
            # Get monthly enrollment history
            self.cursor.execute('''
                SELECT DATE(date_of_admission, 'start of month') as month, COUNT(*) as count
                FROM students
                GROUP BY DATE(date_of_admission, 'start of month')
                ORDER BY month
            ''')
            
            records = self.cursor.fetchall()
            if len(records) < 3:
                return {'message': 'Insufficient historical data'}
            
            months = len(records)
            enrollments = [r[1] for r in records]
            
            # Simple linear trend
            X = np.arange(months).reshape(-1, 1)
            y = np.array(enrollments)
            
            coeffs = np.polyfit(np.arange(months), enrollments, 1)
            
            # Forecast next 3 months
            forecast = []
            for i in range(1, 4):
                pred = np.polyval(coeffs, months + i)
                forecast.append(max(0, int(pred)))
            
            trend = 'Increasing' if coeffs[0] > 0 else 'Decreasing' if coeffs[0] < 0 else 'Stable'
            
            return {
                'current_month_enrollment': enrollments[-1],
                'trend': trend,
                'next_3_months_forecast': forecast,
                'average_monthly_change': round(coeffs[0], 1)
            }
        except Exception as e:
            return {'error': str(e)}
    
    def detect_grade_inflation(self):
        """Detect potential marking anomalies"""
        try:
            self.cursor.execute('''
                SELECT teacher_id, COUNT(*) as grades_given, AVG(grade) as avg_grade,
                       STDDEV(grade) as std_dev
                FROM grades
                GROUP BY teacher_id
                HAVING COUNT(*) > 10
            ''')
            
            anomalies = []
            
            # Get overall statistics
            self.cursor.execute("SELECT AVG(grade), STDDEV(grade) FROM grades")
            overall_avg, overall_std = self.cursor.fetchone()
            
            for teacher_id, count, avg, std in self.cursor.fetchall() or []:
                # Check for unusually high or low averages
                if avg and abs(avg - overall_avg) > (overall_std or 0):
                    anomalies.append({
                        'teacher_id': teacher_id,
                        'grades_given': count,
                        'average_grade': round(avg, 1),
                        'system_average': round(overall_avg, 1),
                        'deviation': round(abs(avg - overall_avg), 1),
                        'concern': 'Grades unusually high' if avg > overall_avg else 'Grades unusually low'
                    })
            
            return anomalies
        except Exception as e:
            return []
    
    def predict_resource_needs(self):
        """Predict resource needs based on trends"""
        try:
            # Get class size distribution
            self.cursor.execute('''
                SELECT COUNT(*) as class_count, SUM(current_students) as total_students
                FROM classes
            ''')
            
            class_count, total_students = self.cursor.fetchone()
            
            # Forecast enrollments
            forecast = self.forecast_enrollment_trends()
            
            recommendations = {
                'current_students': total_students,
                'active_classes': class_count,
                'avg_class_size': round(total_students / class_count, 1) if class_count > 0 else 0,
                'resource_recommendations': []
            }
            
            avg_size = recommendations['avg_class_size']
            if avg_size > 50:
                recommendations['resource_recommendations'].append('Overcrowding: Consider splitting classes or hiring more teachers')
            elif avg_size < 15:
                recommendations['resource_recommendations'].append('Low enrollment: Consider combining classes')
            
            if forecast.get('trend') == 'Increasing':
                recommendations['resource_recommendations'].append('Rising enrollment: Plan for additional classrooms and teachers')
            
            return recommendations
        except Exception as e:
            return {'error': str(e)}


# ==================== INTEGRATION HELPER ====================

def get_all_ai_insights(db_connection):
    """Get comprehensive AI insights summary"""
    ai = AdvancedAIAnalytics(db_connection)
    
    insights = {
        'dropout_risks': ai.detect_dropout_risk_enhanced()[:10],
        'anomalies': ai.detect_behavioral_anomalies()[:10],
        'fee_defaults': ai.predict_fee_defaults()[:10],
        'enrollment_forecast': ai.forecast_enrollment_trends(),
        'resource_needs': ai.predict_resource_needs(),
        'student_segmentation': ai.segment_students_for_intervention()
    }
    
    return insights
