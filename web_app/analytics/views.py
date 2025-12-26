from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.db.models import Avg, Count, Q, Sum, Max, Min
from datetime import datetime, timedelta
from students.models import Student
from attendance.models import AttendanceRecord
from grading.models import Grade
from fees.models import StudentFee, FeePayment
from .models import AnalyticsReport, StudentAnalytics, ClassAnalytics

class AnalyticsDashboardView(LoginRequiredMixin, View):
    
    def get(self, request):
        # Overall statistics
        total_students = Student.objects.filter(is_active=True).count()
        total_classes = Student.objects.values('class_name').distinct().count()
        
        # Attendance statistics
        today = datetime.today().date()
        today_present = AttendanceRecord.objects.filter(
            date=today, status='P'
        ).count()
        today_absent = AttendanceRecord.objects.filter(
            date=today, status='A'
        ).count()
        
        # Academic statistics
        average_grade = Grade.objects.aggregate(Avg('mark'))['mark__avg'] or 0
        high_performers = Grade.objects.filter(
            mark__gte=80
        ).values('student').distinct().count()
        low_performers = Grade.objects.filter(
            mark__lt=50
        ).values('student').distinct().count()
        
        # Financial statistics
        total_fees = StudentFee.objects.aggregate(Sum('amount_due'))['amount_due__sum'] or 0
        paid_fees = StudentFee.objects.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
        collection_rate = (paid_fees / total_fees * 100) if total_fees > 0 else 0
        
        # Risk students
        at_risk_students = self._get_at_risk_students()[:10]
        
        return JsonResponse({
            'total_students': total_students,
            'total_classes': total_classes,
            'today_present': today_present,
            'today_absent': today_absent,
            'average_grade': round(average_grade, 2),
            'high_performers': high_performers,
            'low_performers': low_performers,
            'total_fees': float(total_fees),
            'total_collected': float(paid_fees),
            'collection_rate': round(collection_rate, 2),
            'at_risk_students': at_risk_students
        })
    
    def _get_at_risk_students(self):
        """Identify students at risk based on multiple factors"""
        risk_students = []
        
        for student in Student.objects.filter(is_active=True)[:100]:  # Limit to avoid timeout
            risk_score = 0
            
            # Attendance risk
            attendance_rate = self._get_attendance_rate(student)
            if attendance_rate < 70:
                risk_score += (70 - attendance_rate) / 10
            
            # Academic risk
            avg_grade = Grade.objects.filter(student=student).aggregate(Avg('mark'))['mark__avg'] or 0
            if avg_grade < 50:
                risk_score += (50 - avg_grade) / 10
            
            # Financial risk
            pending_fees = StudentFee.objects.filter(student=student, is_paid=False).count()
            if pending_fees > 0:
                risk_score += pending_fees
            
            if risk_score > 0:
                risk_students.append({
                    'student': student,
                    'risk_score': risk_score,
                    'attendance_rate': attendance_rate,
                    'average_grade': avg_grade,
                    'pending_fees': pending_fees
                })
        
        return sorted(risk_students, key=lambda x: x['risk_score'], reverse=True)
    
    def _get_attendance_rate(self, student):
        """Calculate student's attendance rate"""
        records = AttendanceRecord.objects.filter(student=student)
        if records.count() == 0:
            return 0
        present = records.filter(status='P').count()
        return (present / records.count()) * 100

class StudentAnalyticsView(LoginRequiredMixin, View):
    
    def get(self, request, student_id):
        student = get_object_or_404(Student, pk=student_id)
        
        # Attendance metrics
        attendance_records = AttendanceRecord.objects.filter(student=student)
        total_attendance = attendance_records.count()
        present_count = attendance_records.filter(status='P').count()
        absent_count = attendance_records.filter(status='A').count()
        late_count = attendance_records.filter(status='L').count()
        
        attendance_rate = (present_count / total_attendance * 100) if total_attendance > 0 else 0
        
        # Academic metrics
        grades = Grade.objects.filter(student=student)
        average_mark = grades.aggregate(Avg('mark'))['mark__avg'] or 0
        highest_mark = grades.aggregate(max=Max('mark'))['max'] or 0
        lowest_mark = grades.aggregate(min=Min('mark'))['min'] or 0
        
        # Financial metrics
        fees = StudentFee.objects.filter(student=student)
        total_fees = fees.aggregate(Sum('amount_due'))['amount_due__sum'] or 0
        paid_fees = fees.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
        
        return JsonResponse({
            'student': {
                'id': student.id,
                'name': student.name,
                'registration': student.registration_number,
                'class': student.class_name
            },
            'attendance': {
                'present': present_count,
                'absent': absent_count,
                'late': late_count,
                'total': total_attendance,
                'rate': round(attendance_rate, 2)
            },
            'academics': {
                'average_mark': round(average_mark, 2),
                'highest_mark': int(highest_mark) if highest_mark else 0,
                'lowest_mark': int(lowest_mark) if lowest_mark else 0,
                'total_grades': grades.count()
            },
            'fees': {
                'total_fees': float(total_fees),
                'paid_fees': float(paid_fees),
                'pending_fees': float(total_fees - paid_fees),
                'payment_rate': round((paid_fees / total_fees * 100) if total_fees > 0 else 0, 2)
            }
        })

class ClassAnalyticsView(LoginRequiredMixin, View):
    
    def get(self, request, class_name):
        students = Student.objects.filter(class_name=class_name, is_active=True)
        
        # Attendance statistics
        today = datetime.today().date()
        today_present = AttendanceRecord.objects.filter(
            student__in=students, date=today, status='P'
        ).count()
        today_attendance_rate = (today_present / students.count() * 100) if students.count() > 0 else 0
        
        # Academic statistics
        grades = Grade.objects.filter(student__in=students)
        average_grade = grades.aggregate(Avg('mark'))['mark__avg'] or 0
        high_performers = grades.filter(mark__gte=80).count()
        low_performers = grades.filter(mark__lt=50).count()
        
        return JsonResponse({
            'class_name': class_name,
            'total_students': students.count(),
            'today_present': today_present,
            'today_attendance_rate': round(today_attendance_rate, 2),
            'average_grade': round(average_grade, 2),
            'high_performers': high_performers,
            'low_performers': low_performers
        })

class AnalyticsReportsView(LoginRequiredMixin, ListView):
    model = AnalyticsReport
    template_name = 'analytics/reports_list.html'
    context_object_name = 'reports'
    paginate_by = 25
    
    def get_queryset(self):
        return AnalyticsReport.objects.all().order_by('-created_at')

class ExportAnalyticsView(LoginRequiredMixin, View):
    
    def post(self, request, *args, **kwargs):
        from django.http import HttpResponse
        import csv
        
        export_type = request.POST.get('export_type')
        
        if export_type == 'attendance':
            return self._export_attendance(request)
        elif export_type == 'grades':
            return self._export_grades(request)
        elif export_type == 'fees':
            return self._export_fees(request)
        
        return JsonResponse({'error': 'Invalid export type'}, status=400)
    
    def _export_attendance(self, request):
        from django.http import HttpResponse
        import csv
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="attendance.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Student', 'Registration', 'Class', 'Date', 'Status'])
        
        for record in AttendanceRecord.objects.all():
            writer.writerow([
                record.student.name,
                record.student.registration_number,
                record.class_name,
                record.date,
                record.status
            ])
        
        return response
    
    def _export_grades(self, request):
        from django.http import HttpResponse
        import csv
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="grades.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Student', 'Registration', 'Subject', 'Mark', 'Grade', 'Term', 'Year'])
        
        for grade in Grade.objects.select_related('class_assignment'):
            writer.writerow([
                grade.student.name,
                grade.student.registration_number,
                grade.class_assignment.subject if grade.class_assignment else 'N/A',
                grade.mark,
                grade.grade_letter,
                grade.term,
                grade.year
            ])
        
        return response
    
    def _export_fees(self, request):
        from django.http import HttpResponse
        import csv
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="fees.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Student', 'Registration', 'Fee Type', 'Amount Due', 'Paid', 'Balance'])
        
        for fee in StudentFee.objects.all():
            writer.writerow([
                fee.student.name,
                fee.student.registration_number,
                fee.fee_type.name if fee.fee_type else 'N/A',
                fee.amount_due,
                fee.amount_paid,
                fee.amount_pending
            ])
        
        return response
