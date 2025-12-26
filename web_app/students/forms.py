from django import forms
from .models import Student, StudentDocument

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'name', 'registration_number', 'date_of_birth', 'gender', 'email', 'phone',
            'address', 'class_name', 'guardian_name', 'guardian_phone', 'guardian_email', 'photo', 'is_active'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

class StudentDocumentForm(forms.ModelForm):
    class Meta:
        model = StudentDocument
        fields = ['document_type', 'file']
