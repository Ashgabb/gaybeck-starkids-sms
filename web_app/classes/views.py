"""
Class Management Views
Handle classes, classrooms, and class metrics
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Count, Avg, Q
from datetime import datetime, date
from decimal import Decimal
from .models import ClassInfo, ClassRoom, ClassPerformanceMetrics
from students.models import Student
from attendance.models import AttendanceRecord
from grading.models import Grade

class ClassListView(LoginRequiredMixin, ListView):
    """List all classes"""
    model = ClassInfo
    template_name = 'classes/class_list.html'
    context_object_name = 'classes'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = ClassInfo.objects.all()
        level = self.request.GET.get('level')
        year = self.request.GET.get('year')
        
        if level:
            queryset = queryset.filter(level=level)
        if year:
            queryset = queryset.filter(year=year)
        
        return queryset.order_by('level', 'name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['levels'] = ClassInfo.objects.values_list('level', flat=True).distinct()
        context['years'] = ClassInfo.objects.values_list('year', flat=True).distinct().order_by('-year')
        return context


class ClassCreateView(LoginRequiredMixin, CreateView):
    """Create new class"""
    model = ClassInfo
    template_name = 'classes/class_form.html'
    fields = ['name', 'level', 'stream', 'class_teacher', 'capacity', 'year']
    success_url = reverse_lazy('classes:class_list')


class ClassUpdateView(LoginRequiredMixin, UpdateView):
    """Update class information"""
    model = ClassInfo
    template_name = 'classes/class_form.html'
    fields = ['name', 'level', 'stream', 'class_teacher', 'capacity', 'year', 'is_active']
    success_url = reverse_lazy('classes:class_list')


class ClassDetailView(LoginRequiredMixin, DetailView):
    """View class details with students and metrics"""
    model = ClassInfo
    template_name = 'classes/class_detail.html'
    context_object_name = 'class_info'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        class_obj = self.get_object()
        
        # Get students in class
        context['students'] = Student.objects.filter(
            class_name=class_obj.name,
            is_active=True
        ).order_by('name')
        
        # Get attendance rate
        today = date.today()
        month_start = today.replace(day=1)
        attendance_records = AttendanceRecord.objects.filter(
            class_name=class_obj.name,
            date__gte=month_start,
            date__lte=today
        )
        
        if attendance_records.exists():
            present_count = attendance_records.filter(status='P').count()
            context['attendance_rate'] = round((present_count / attendance_records.count()) * 100, 2)
        else:
            context['attendance_rate'] = 0
        
        # Get average grade
        grades = Grade.objects.filter(
            student__class_name=class_obj.name
        )
        if grades.exists():
            context['average_grade'] = round(grades.aggregate(Avg('mark'))['mark__avg'], 2)
        else:
            context['average_grade'] = 0
        
        return context


class ClassRoomListView(LoginRequiredMixin, ListView):
    """List all classrooms"""
    model = ClassRoom
    template_name = 'classes/classroom_list.html'
    context_object_name = 'classrooms'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = ClassRoom.objects.all()
        room_type = self.request.GET.get('type')
        
        if room_type:
            queryset = queryset.filter(room_type=room_type)
        
        return queryset.order_by('name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room_types'] = ClassRoom._meta.get_field('room_type').choices
        return context


class ClassRoomCreateView(LoginRequiredMixin, CreateView):
    """Create new classroom"""
    model = ClassRoom
    template_name = 'classes/classroom_form.html'
    fields = ['name', 'room_type', 'capacity', 'has_projector', 'has_air_conditioning', 'condition', 'last_maintenance_date', 'notes']
    success_url = reverse_lazy('classes:classroom_list')


class ClassRoomUpdateView(LoginRequiredMixin, UpdateView):
    """Update classroom information"""
    model = ClassRoom
    template_name = 'classes/classroom_form.html'
    fields = ['name', 'room_type', 'capacity', 'has_projector', 'has_air_conditioning', 'condition', 'last_maintenance_date', 'notes', 'is_active']
    success_url = reverse_lazy('classes:classroom_list')


class ClassPerformanceView(LoginRequiredMixin, TemplateView):
    """View class performance metrics"""
    template_name = 'classes/class_performance.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all classes with performance
        classes = ClassInfo.objects.filter(is_active=True).select_related('performance_metrics')
        class_metrics = []
        
        for cls in classes:
            students = Student.objects.filter(class_name=cls.name, is_active=True)
            
            # Calculate attendance
            attendance_records = AttendanceRecord.objects.filter(class_name=cls.name)
            attendance_rate = 0
            if attendance_records.exists():
                present = attendance_records.filter(status='P').count()
                attendance_rate = round((present / attendance_records.count()) * 100, 2)
            
            # Calculate average grade
            grades = Grade.objects.filter(student__class_name=cls.name)
            avg_grade = 0
            if grades.exists():
                avg_grade = round(grades.aggregate(Avg('mark'))['mark__avg'], 2)
            
            class_metrics.append({
                'class': cls,
                'student_count': students.count(),
                'attendance_rate': attendance_rate,
                'average_grade': avg_grade,
            })
        
        context['class_metrics'] = class_metrics
        return context
