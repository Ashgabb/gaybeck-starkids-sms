"""Teachers App Models"""

from django.db import models
from accounts.models import User

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    employee_id = models.CharField(max_length=50, unique=True)
    subject = models.CharField(max_length=100)
    qualifications = models.TextField(blank=True)
    hire_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['user__first_name']
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.subject})"

class ClassAssignment(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='class_assignments')
    class_name = models.CharField(max_length=50)
    subject = models.CharField(max_length=100)
    semester = models.CharField(max_length=20)
    year = models.IntegerField()
    assigned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('teacher', 'class_name', 'subject', 'year')
    
    def __str__(self):
        return f"{self.teacher.user.get_full_name()} - {self.class_name} ({self.subject})"
