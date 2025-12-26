from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Student, StudentDocument
from .forms import StudentForm, StudentDocumentForm

class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'
    paginate_by = 25
    
    def get_queryset(self):
        queryset = Student.objects.filter(is_active=True)
        search = self.request.GET.get('search', '')
        class_filter = self.request.GET.get('class', '')
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | 
                Q(registration_number__icontains=search) |
                Q(guardian_contact__icontains=search)
            )
        
        if class_filter:
            queryset = queryset.filter(class_name=class_filter)
        
        return queryset.order_by('class_name', 'name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['class_filter'] = self.request.GET.get('class', '')
        context['classes'] = Student.objects.values_list('class_name', flat=True).distinct()
        return context

class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('students:list')

class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = 'students/student_detail.html'
    context_object_name = 'student'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.get_object()
        context['documents'] = student.documents.all()
        context['fees'] = student.fees.all()
        context['grades'] = student.grades.all()
        context['attendance_records'] = student.attendance_records.all()[:10]
        return context

class StudentEditView(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    
    def get_success_url(self):
        return reverse_lazy('students:detail', kwargs={'pk': self.object.pk})

class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = 'students/student_confirm_delete.html'
    success_url = reverse_lazy('students:list')

class StudentDocumentListView(LoginRequiredMixin, ListView):
    template_name = 'students/document_list.html'
    context_object_name = 'documents'
    paginate_by = 25
    
    def get_queryset(self):
        student = get_object_or_404(Student, pk=self.kwargs['student_pk'])
        return student.documents.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student'] = get_object_or_404(Student, pk=self.kwargs['student_pk'])
        return context

class StudentDocumentCreateView(LoginRequiredMixin, CreateView):
    model = StudentDocument
    fields = ['document_type', 'document_file', 'upload_date']
    template_name = 'students/document_form.html'
    
    def form_valid(self, form):
        student = get_object_or_404(Student, pk=self.kwargs['student_pk'])
        form.instance.student = student
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('students:documents', kwargs={'student_pk': self.kwargs['student_pk']})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student'] = get_object_or_404(Student, pk=self.kwargs['student_pk'])
        return context

class StudentDocumentDeleteView(LoginRequiredMixin, DeleteView):
    model = StudentDocument
    template_name = 'students/document_confirm_delete.html'
    
    def get_success_url(self):
        return reverse_lazy('students:documents', kwargs={'student_pk': self.object.student.pk})
    form_class = StudentDocumentForm
    template_name = 'students/document_form.html'
    
    def form_valid(self, form):
        form.instance.student = get_object_or_404(Student, pk=self.kwargs['student_pk'])
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('students:documents', kwargs={'student_pk': self.kwargs['student_pk']})
