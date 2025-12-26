from django import forms
from .models import Teacher, ClassAssignment


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['user', 'employee_id', 'subject', 'qualifications', 'hire_date', 'is_active']
        widgets = {
            'hire_date': forms.DateInput(attrs={'type': 'date'}),
            'qualifications': forms.Textarea(attrs={'rows': 4}),
        }


class ClassAssignmentForm(forms.ModelForm):
    class Meta:
        model = ClassAssignment
        fields = ['teacher', 'class_name', 'subject', 'year', 'semester']
        widgets = {
            'year': forms.NumberInput(attrs={'min': 2020, 'max': 2030}),
        }
