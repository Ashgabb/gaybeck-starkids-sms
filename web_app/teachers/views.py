from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q, Count
from .models import Teacher, ClassAssignment
from .forms import TeacherForm, ClassAssignmentForm

class TeacherListView(LoginRequiredMixin, ListView):
    model = Teacher
    template_name = 'teachers/teacher_list.html'
    context_object_name = 'teachers'
    paginate_by = 25
    
    def get_queryset(self):
        queryset = Teacher.objects.select_related('user').filter(is_active=True)
        search = self.request.GET.get('search', '')
        subject_filter = self.request.GET.get('subject', '')
        
        if search:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(employee_id__icontains=search)
            )
        
        if subject_filter:
            queryset = queryset.filter(subject=subject_filter)
        
        return queryset.order_by('user__last_name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['subjects'] = Teacher.objects.values_list('subject', flat=True).distinct()
        return context

class TeacherDetailView(LoginRequiredMixin, DetailView):
    model = Teacher
    template_name = 'teachers/teacher_detail.html'
    context_object_name = 'teacher'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher = self.get_object()
        context['classes'] = ClassAssignment.objects.filter(teacher=teacher)
        return context

class TeacherCreateView(LoginRequiredMixin, CreateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'teachers/teacher_form.html'
    success_url = reverse_lazy('teachers:list')

class TeacherUpdateView(LoginRequiredMixin, UpdateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'teachers/teacher_form.html'
    
    def get_success_url(self):
        return reverse_lazy('teachers:detail', kwargs={'pk': self.object.pk})

class TeacherDeleteView(LoginRequiredMixin, DeleteView):
    model = Teacher
    template_name = 'teachers/teacher_confirm_delete.html'
    success_url = reverse_lazy('teachers:list')

class ClassAssignmentListView(LoginRequiredMixin, ListView):
    model = ClassAssignment
    template_name = 'teachers/assignment_list.html'
    context_object_name = 'assignments'
    paginate_by = 50

class ClassAssignmentCreateView(LoginRequiredMixin, CreateView):
    model = ClassAssignment
    form_class = ClassAssignmentForm
    template_name = 'teachers/assignment_form.html'
    success_url = reverse_lazy('teachers:assignments')

class ClassAssignmentUpdateView(LoginRequiredMixin, UpdateView):
    model = ClassAssignment
    form_class = ClassAssignmentForm
    template_name = 'teachers/assignment_form.html'
    success_url = reverse_lazy('teachers:assignments')
