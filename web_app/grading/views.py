from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q, Avg, Count
from students.models import Student
from .models import Grade
from .forms import GradeForm

class GradeListView(LoginRequiredMixin, ListView):
    model = Grade
    template_name = 'grading/grade_list.html'
    context_object_name = 'grades'
    paginate_by = 50
    
    def get_queryset(self):
        queryset = Grade.objects.select_related('student')
        search = self.request.GET.get('search', '')
        term_filter = self.request.GET.get('term', '')
        subject_filter = self.request.GET.get('subject', '')
        
        if search:
            queryset = queryset.filter(
                Q(student__name__icontains=search) |
                Q(student__registration_number__icontains=search) |
                Q(subject__icontains=search)
            )
        
        if term_filter:
            queryset = queryset.filter(term=term_filter)
        
        if subject_filter:
            queryset = queryset.filter(class_assignment__subject=subject_filter)
        
        return queryset.order_by('-year', '-term', 'student__name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['term_choices'] = Grade.TERM_CHOICES
        context['subjects'] = Grade.objects.values_list('class_assignment__subject', flat=True).distinct()
        return context

class StudentGradeView(LoginRequiredMixin, ListView):
    template_name = 'grading/student_grades.html'
    context_object_name = 'grades'
    paginate_by = 50
    
    def get_queryset(self):
        student = get_object_or_404(Student, pk=self.kwargs['student_id'])
        return student.grades.all().order_by('-year', '-term')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = get_object_or_404(Student, pk=self.kwargs['student_id'])
        context['student'] = student
        
        # Calculate statistics
        grades = student.grades.all()
        context['average_mark'] = grades.aggregate(Avg('mark'))['mark__avg'] or 0
        context['total_subjects'] = grades.values('class_assignment__subject').distinct().count()
        
        # Grade distribution
        context['grade_distribution'] = {
            'A': grades.filter(mark__gte=90).count(),
            'B': grades.filter(mark__gte=80, mark__lt=90).count(),
            'C': grades.filter(mark__gte=70, mark__lt=80).count(),
            'D': grades.filter(mark__gte=60, mark__lt=70).count(),
            'F': grades.filter(mark__lt=60).count(),
        }
        
        return context

class GradeCreateView(LoginRequiredMixin, CreateView):
    model = Grade
    form_class = GradeForm
    template_name = 'grading/grade_form.html'
    success_url = reverse_lazy('grading:list')
    
    def form_valid(self, form):
        # Optional: Set recorded_by if you want to track who entered grades
        return super().form_valid(form)

class GradeEditView(LoginRequiredMixin, UpdateView):
    model = Grade
    form_class = GradeForm
    template_name = 'grading/grade_form.html'
    success_url = reverse_lazy('grading:list')

class GradeDeleteView(LoginRequiredMixin, DeleteView):
    model = Grade
    template_name = 'grading/grade_confirm_delete.html'
    success_url = reverse_lazy('grading:list')

class ClassGradesView(LoginRequiredMixin, ListView):
    template_name = 'grading/class_grades.html'
    context_object_name = 'grades'
    paginate_by = 100
    
    def get_queryset(self):
        class_name = self.kwargs['class_name']
        term = self.kwargs.get('term')
        year = self.kwargs.get('year')
        
        queryset = Grade.objects.filter(student__class_name=class_name).select_related('student')
        
        if term:
            queryset = queryset.filter(term=term)
        
        if year:
            queryset = queryset.filter(year=year)
        
        return queryset.order_by('student__name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['class_name'] = self.kwargs['class_name']
        context['term'] = self.kwargs.get('term')
        context['year'] = self.kwargs.get('year')
        
        # Class statistics
        grades = self.get_queryset()
        context['class_average'] = grades.aggregate(Avg('mark'))['mark__avg'] or 0
        context['class_highest'] = grades.aggregate(Avg('mark'))['mark__max'] or 0
        context['class_lowest'] = grades.aggregate(Avg('mark'))['mark__min'] or 0
        
        return context

class BulkGradeUploadView(LoginRequiredMixin, CreateView):
    template_name = 'grading/bulk_upload.html'
    
    def post(self, request, *args, **kwargs):
        # Handle CSV or bulk upload
        term = request.POST.get('term')
        year = request.POST.get('year')
        subject = request.POST.get('subject')
        csv_file = request.FILES.get('csv_file')
        
        if csv_file:
            import csv
            stream = csv.reader(csv_file.stream.decode('utf8').splitlines())
            
            for row in stream:
                try:
                    registration_number = row[0]
                    mark = int(row[1])
                    comments = row[2] if len(row) > 2 else ''
                    
                    student = Student.objects.get(registration_number=registration_number)
                    Grade.objects.create(
                        student=student,
                        subject=subject,
                        mark=mark,
                        term=term,
                        year=year,
                        comments=comments
                    )
                except (Student.DoesNotExist, ValueError, IndexError):
                    continue
        
        return redirect('grading:list')
