from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Avg, Q, Sum
from datetime import datetime, timedelta
from students.models import Student
from teachers.models import Teacher
from attendance.models import AttendanceRecord
from fees.models import StudentFee, FeePayment
from grading.models import Grade

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Core statistics
        context['total_students'] = Student.objects.filter(is_active=True).count()
        context['total_teachers'] = Teacher.objects.filter(is_active=True).count()
        context['total_classes'] = Student.objects.filter(is_active=True).values('class_name').distinct().count()
        
        # Attendance statistics for today
        today = datetime.today().date()
        today_records = AttendanceRecord.objects.filter(date=today)
        context['today_present'] = today_records.filter(status='P').count()
        context['today_absent'] = today_records.filter(status='A').count()
        context['today_late'] = today_records.filter(status='L').count()
        
        # Calculate attendance summary
        if today_records.count() > 0:
            context['today_attendance_rate'] = (context['today_present'] / today_records.count()) * 100
        else:
            context['today_attendance_rate'] = 0
        
        # Fee statistics
        total_fees = StudentFee.objects.aggregate(Sum('amount_due'))['amount_due__sum'] or 0
        paid_fees = StudentFee.objects.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
        pending_fees = StudentFee.objects.filter(is_paid=False).count()
        
        context['pending_fees'] = pending_fees
        context['total_fees_pending'] = total_fees - paid_fees
        context['total_fees_amount'] = total_fees
        context['total_fees_collected'] = paid_fees
        context['collection_rate'] = (paid_fees / total_fees * 100) if total_fees > 0 else 0
        
        # Academic performance statistics
        grades = Grade.objects.all()
        context['avg_grade'] = round(grades.aggregate(Avg('mark'))['mark__avg'] or 0, 1)
        context['high_achievers'] = grades.filter(mark__gte=80).count()
        context['struggling_students'] = Grade.objects.filter(
            mark__lt=50
        ).values('student').distinct().count()
        
        # Recent activities
        context['recent_students'] = Student.objects.all().order_by('-id')[:5]
        context['recent_grades'] = Grade.objects.all().order_by('-id')[:10]
        context['recent_payments'] = FeePayment.objects.all().order_by('-payment_date')[:10]
        
        # Attendance trend (last 7 days)
        last_7_days = datetime.today().date() - timedelta(days=7)
        context['attendance_trend'] = AttendanceRecord.objects.filter(
            date__gte=last_7_days
        ).values('date').annotate(
            present=Count('id', filter=Q(status='P')),
            absent=Count('id', filter=Q(status='A'))
        ).order_by('date')
        
        # At-risk students
        context['at_risk_students'] = self._get_at_risk_students()[:5]
        
        # Role-based customization
        if user.is_teacher():
            # Teacher dashboard
            context['assigned_classes'] = 5  # Placeholder
            context['my_students'] = 120  # Placeholder
        elif user.is_accountant():
            # Accountant dashboard
            context['monthly_target'] = 50000  # Placeholder
            context['this_month_collected'] = 35000  # Placeholder
        
        return context
    
    def _get_at_risk_students(self):
        """Identify students at risk"""
        risk_students = []
        
        for student in Student.objects.filter(is_active=True)[:50]:
            risk_factors = 0
            
            # Check attendance
            attendance = AttendanceRecord.objects.filter(student=student)
            if attendance.count() > 0:
                present_rate = attendance.filter(status='P').count() / attendance.count()
                if present_rate < 0.7:
                    risk_factors += 1
            
            # Check grades
            grades = Grade.objects.filter(student=student)
            if grades.count() > 0:
                avg_grade = grades.aggregate(Avg('mark'))['mark__avg']
                if avg_grade < 50:
                    risk_factors += 1
            
            # Check fees
            fees = StudentFee.objects.filter(student=student, is_paid=False)
            if fees.count() > 0:
                risk_factors += 1
            
            if risk_factors > 0:
                risk_students.append({
                    'student': student,
                    'risk_factors': risk_factors
                })
        
        return sorted(risk_students, key=lambda x: x['risk_factors'], reverse=True)
