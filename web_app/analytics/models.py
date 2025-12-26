"""Analytics App Services - AI/ML Analytics"""

from django.db import models
from students.models import Student
from attendance.models import AttendanceRecord
from fees.models import StudentFee
from grading.models import Grade
from django.db.models import Avg, Count, Q
from datetime import datetime, timedelta

# ML imports moved to functions to avoid import errors
ML_AVAILABLE = False

class AnalyticsReport(models.Model):
    REPORT_TYPES = (
        ('ATTENDANCE', 'Attendance Analysis'),
        ('PERFORMANCE', 'Performance Analysis'),
        ('FINANCIAL', 'Financial Analysis'),
        ('RISK', 'Risk Assessment'),
    )
    
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    data = models.JSONField()
    generated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-generated_at']
    
    def __str__(self):
        return f"{self.get_report_type_display()} - {self.generated_at}"

class StudentAnalytics:
    """Analytics service for student insights"""
    
    @staticmethod
    def get_attendance_risk(student_id):
        """Identify students at attendance risk"""
        student = Student.objects.get(id=student_id)
        thirty_days_ago = datetime.now().date() - timedelta(days=30)
        
        records = AttendanceRecord.objects.filter(
            student=student,
            date__gte=thirty_days_ago
        )
        
        total = records.count()
        if total == 0:
            return {'risk': 'NONE', 'score': 0}
        
        present = records.filter(Q(status='P') | Q(status='L')).count()
        attendance_rate = (present / total) * 100
        
        if attendance_rate < 75:
            return {'risk': 'HIGH', 'score': attendance_rate}
        elif attendance_rate < 85:
            return {'risk': 'MEDIUM', 'score': attendance_rate}
        else:
            return {'risk': 'LOW', 'score': attendance_rate}
    
    @staticmethod
    def get_academic_performance(student_id):
        """Get student academic performance summary"""
        student = Student.objects.get(id=student_id)
        grades = Grade.objects.filter(student=student)
        
        if not grades.exists():
            return {'average': 0, 'trend': 'NO_DATA', 'performance': 'UNGRADED'}
        
        avg_grade = grades.aggregate(avg=Avg('mark'))['avg']
        
        if avg_grade >= 80:
            performance = 'EXCELLENT'
        elif avg_grade >= 70:
            performance = 'GOOD'
        elif avg_grade >= 60:
            performance = 'SATISFACTORY'
        else:
            performance = 'NEEDS_IMPROVEMENT'
        
        return {
            'average': round(avg_grade, 1),
            'performance': performance,
            'total_grades': grades.count()
        }
    
    @staticmethod
    def get_financial_status(student_id):
        """Get student fee payment status"""
        student = Student.objects.get(id=student_id)
        fees = StudentFee.objects.filter(student=student)
        
        total_due = sum(f.amount_due for f in fees)
        total_paid = sum(f.amount_paid for f in fees)
        
        return {
            'total_due': float(total_due),
            'total_paid': float(total_paid),
            'balance': float(total_due - total_paid),
            'payment_rate': (total_paid / total_due * 100) if total_due > 0 else 0
        }

class ClassAnalytics:
    """Analytics service for class-level insights"""
    
    @staticmethod
    def get_class_statistics(class_name):
        """Get comprehensive class statistics"""
        students = Student.objects.filter(class_name=class_name, is_active=True)
        
        stats = {
            'total_students': students.count(),
            'avg_attendance': 0,
            'avg_grade': 0,
            'total_fees_due': 0,
            'total_fees_paid': 0,
        }
        
        if students.count() == 0:
            return stats
        
        # Calculate averages
        attendance_records = AttendanceRecord.objects.filter(
            student__in=students
        )
        if attendance_records.exists():
            present_count = attendance_records.filter(
                Q(status='P') | Q(status='L')
            ).count()
            stats['avg_attendance'] = (present_count / attendance_records.count() * 100) if attendance_records.count() > 0 else 0
        
        grades = Grade.objects.filter(student__in=students)
        if grades.exists():
            stats['avg_grade'] = grades.aggregate(avg=Avg('mark'))['avg'] or 0
        
        fees = StudentFee.objects.filter(student__in=students)
        stats['total_fees_due'] = float(sum(f.amount_due for f in fees))
        stats['total_fees_paid'] = float(sum(f.amount_paid for f in fees))
        
        return stats
