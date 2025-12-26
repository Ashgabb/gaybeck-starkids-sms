from django import forms
from .models import Grade

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'class_assignment', 'term', 'year', 'mark', 'comments']
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 3})
        }
