"""Attendance App Models"""

from django.db import models
from students.models import Student
from teachers.models import Teacher
from datetime import date

class AttendanceRecord(models.Model):
    STATUS_CHOICES = (
        ('P', 'Present'),
        ('A', 'Absent'),
        ('L', 'Late'),
        ('E', 'Excused'),
    )
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    class_name = models.CharField(max_length=50)
    date = models.DateField(default=date.today)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    recorded_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('student', 'date', 'class_name')
        ordering = ['-date']
        verbose_name_plural = 'Attendance Records'
    
    def __str__(self):
        return f"{self.student.name} - {self.date} ({self.get_status_display()})"
