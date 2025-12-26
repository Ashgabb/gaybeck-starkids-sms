from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q, Count
from datetime import datetime, timedelta
from students.models import Student
from .models import AttendanceRecord
from .forms import AttendanceForm

class AttendanceListView(LoginRequiredMixin, ListView):
    model = AttendanceRecord
    template_name = 'attendance/attendance_list.html'
    context_object_name = 'records'
    paginate_by = 50
    
    def get_queryset(self):
        queryset = AttendanceRecord.objects.select_related('student')
        search = self.request.GET.get('search', '')
        date_from = self.request.GET.get('date_from', '')
        date_to = self.request.GET.get('date_to', '')
        status_filter = self.request.GET.get('status', '')
        
        if search:
            queryset = queryset.filter(
                Q(student__name__icontains=search) |
                Q(student__registration_number__icontains=search)
            )
        
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        
        if date_to:
            queryset = queryset.filter(date__lte=date_to)
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset.order_by('-date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['status_choices'] = AttendanceRecord.STATUS_CHOICES
        context['today'] = datetime.today().date()
        return context

class AttendanceByDateView(LoginRequiredMixin, ListView):
    template_name = 'attendance/attendance_by_date.html'
    context_object_name = 'records'
    paginate_by = 100
    
    def get_queryset(self):
        if 'date' in self.kwargs:
            date = datetime.strptime(self.kwargs['date'], '%Y-%m-%d').date()
        else:
            date = datetime.today().date()
        return AttendanceRecord.objects.filter(date=date).select_related('student')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'date' in self.kwargs:
            context['date'] = self.kwargs['date']
        else:
            context['date'] = datetime.today().date()
        return context

class ClassAttendanceView(LoginRequiredMixin, ListView):
    template_name = 'attendance/class_attendance.html'
    context_object_name = 'records'
    paginate_by = 50
    
    def get_queryset(self):
        return AttendanceRecord.objects.filter(
            class_name=self.kwargs['class_name']
        ).select_related('student').order_by('-date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['class_name'] = self.kwargs['class_name']
        
        # Calculate attendance statistics
        records = self.get_queryset()
        total = records.count()
        present = records.filter(status='P').count()
        absent = records.filter(status='A').count()
        
        context['total_records'] = total
        context['present_count'] = present
        context['absent_count'] = absent
        context['attendance_rate'] = (present / total * 100) if total > 0 else 0
        
        return context

class StudentAttendanceView(LoginRequiredMixin, ListView):
    template_name = 'attendance/student_attendance.html'
    context_object_name = 'records'
    paginate_by = 50
    
    def get_queryset(self):
        return AttendanceRecord.objects.filter(
            student_id=self.kwargs['student_id']
        ).order_by('-date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = get_object_or_404(Student, pk=self.kwargs['student_id'])
        context['student'] = student
        
        # Calculate attendance statistics
        records = self.get_queryset()
        total = records.count()
        present = records.filter(status='P').count()
        absent = records.filter(status='A').count()
        late = records.filter(status='L').count()
        
        context['total_records'] = total
        context['present_count'] = present
        context['absent_count'] = absent
        context['late_count'] = late
        context['attendance_rate'] = (present / total * 100) if total > 0 else 0
        
        return context

class AttendanceEditView(LoginRequiredMixin, UpdateView):
    model = AttendanceRecord
    fields = ['status', 'notes']
    template_name = 'attendance/attendance_form.html'
    success_url = reverse_lazy('attendance:list')

class AttendanceCreateView(LoginRequiredMixin, CreateView):
    model = AttendanceRecord
    fields = ['student', 'class_name', 'date', 'status', 'notes']
    template_name = 'attendance/attendance_form.html'
    success_url = reverse_lazy('attendance:list')
    
    def form_valid(self, form):
        form.instance.recorded_by = self.request.user
        return super().form_valid(form)

class BulkAttendanceView(LoginRequiredMixin, CreateView):
    template_name = 'attendance/bulk_attendance.html'
    
    def post(self, request, *args, **kwargs):
        class_name = request.POST.get('class_name')
        date = request.POST.get('date')
        
        students = Student.objects.filter(class_name=class_name, is_active=True)
        
        for student in students:
            status = request.POST.get(f'attendance_{student.id}', 'A')
            notes = request.POST.get(f'notes_{student.id}', '')
            
            AttendanceRecord.objects.update_or_create(
                student=student,
                date=date,
                class_name=class_name,
                defaults={
                    'status': status,
                    'notes': notes,
                    'recorded_by': request.user
                }
            )
        
        return redirect('attendance:list')
