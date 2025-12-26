"""
Timetables Views
Handle timetable management, homework, and lessons
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from datetime import datetime, timedelta
from .models import TimeSlot, ClassTimetable, Homework, Lesson, ClassRemark
from teachers.models import ClassAssignment
from students.models import Student

class TimetableListView(LoginRequiredMixin, ListView):
    """Display timetables for a class"""
    model = ClassTimetable
    template_name = 'timetables/timetable_list.html'
    context_object_name = 'timetables'
    paginate_by = 50
    
    def get_queryset(self):
        queryset = ClassTimetable.objects.all()
        class_name = self.request.GET.get('class')
        if class_name:
            queryset = queryset.filter(class_assignment__class_name=class_name)
        return queryset.select_related('class_assignment', 'time_slot')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['classes'] = ClassAssignment.objects.values_list('class_name', flat=True).distinct()
        return context


class TimetableCreateView(LoginRequiredMixin, CreateView):
    """Create a new timetable entry"""
    model = ClassTimetable
    template_name = 'timetables/timetable_form.html'
    fields = ['class_assignment', 'day', 'time_slot', 'room', 'notes']
    success_url = reverse_lazy('timetables:timetable_list')


class TimetableUpdateView(LoginRequiredMixin, UpdateView):
    """Update timetable entry"""
    model = ClassTimetable
    template_name = 'timetables/timetable_form.html'
    fields = ['class_assignment', 'day', 'time_slot', 'room', 'notes', 'is_active']
    success_url = reverse_lazy('timetables:timetable_list')


class TimetableDeleteView(LoginRequiredMixin, DeleteView):
    """Delete timetable entry"""
    model = ClassTimetable
    template_name = 'timetables/timetable_confirm_delete.html'
    success_url = reverse_lazy('timetables:timetable_list')


class HomeworkListView(LoginRequiredMixin, ListView):
    """Display homework assignments"""
    model = Homework
    template_name = 'timetables/homework_list.html'
    context_object_name = 'homework_list'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Homework.objects.all().select_related('class_assignment')
        status = self.request.GET.get('status')
        class_name = self.request.GET.get('class')
        overdue_only = self.request.GET.get('overdue')
        
        if status:
            queryset = queryset.filter(status=status)
        if class_name:
            queryset = queryset.filter(class_assignment__class_name=class_name)
        if overdue_only:
            from datetime import date
            queryset = queryset.filter(due_date__lt=date.today(), status='ASSIGNED')
        
        return queryset.order_by('-due_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['classes'] = ClassAssignment.objects.values_list('class_name', flat=True).distinct()
        context['statuses'] = Homework.STATUS_CHOICES
        return context


class HomeworkCreateView(LoginRequiredMixin, CreateView):
    """Create new homework"""
    model = Homework
    template_name = 'timetables/homework_form.html'
    fields = ['class_assignment', 'title', 'description', 'due_date', 'file_attachment']
    success_url = reverse_lazy('timetables:homework_list')


class HomeworkUpdateView(LoginRequiredMixin, UpdateView):
    """Update homework"""
    model = Homework
    template_name = 'timetables/homework_form.html'
    fields = ['class_assignment', 'title', 'description', 'due_date', 'status', 'file_attachment']
    success_url = reverse_lazy('timetables:homework_list')


class HomeworkDetailView(LoginRequiredMixin, DetailView):
    """View homework details"""
    model = Homework
    template_name = 'timetables/homework_detail.html'
    context_object_name = 'homework'


class LessonListView(LoginRequiredMixin, ListView):
    """Display lessons"""
    model = Lesson
    template_name = 'timetables/lesson_list.html'
    context_object_name = 'lessons'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Lesson.objects.all().select_related('class_assignment')
        class_name = self.request.GET.get('class')
        if class_name:
            queryset = queryset.filter(class_assignment__class_name=class_name)
        return queryset.order_by('-lesson_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['classes'] = ClassAssignment.objects.values_list('class_name', flat=True).distinct()
        return context


class LessonCreateView(LoginRequiredMixin, CreateView):
    """Create new lesson"""
    model = Lesson
    template_name = 'timetables/lesson_form.html'
    fields = ['class_assignment', 'topic', 'description', 'objectives', 'teaching_materials', 'lesson_date', 'duration_minutes', 'notes']
    success_url = reverse_lazy('timetables:lesson_list')


class LessonUpdateView(LoginRequiredMixin, UpdateView):
    """Update lesson"""
    model = Lesson
    template_name = 'timetables/lesson_form.html'
    fields = ['class_assignment', 'topic', 'description', 'objectives', 'teaching_materials', 'lesson_date', 'duration_minutes', 'notes']
    success_url = reverse_lazy('timetables:lesson_list')


class LessonDetailView(LoginRequiredMixin, DetailView):
    """View lesson details"""
    model = Lesson
    template_name = 'timetables/lesson_detail.html'
    context_object_name = 'lesson'
