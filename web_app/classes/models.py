"""
Class Management Models
Manages classes, streams, and class information
"""

from django.db import models
from teachers.models import Teacher

class ClassInfo(models.Model):
    """Information about classes offered"""
    name = models.CharField(max_length=100, unique=True)  # e.g., "Form 1A", "Grade 3B"
    level = models.CharField(max_length=50)  # e.g., "Primary", "Secondary"
    stream = models.CharField(max_length=50, blank=True)  # e.g., "Science", "Arts"
    class_teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='classes_teaching')
    capacity = models.IntegerField(default=50)
    year = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['level', 'name']
        unique_together = ('name', 'year')
        verbose_name_plural = 'Classes'
    
    def __str__(self):
        return f"{self.name} ({self.year})"
    
    @property
    def student_count(self):
        """Get count of active students in class"""
        from students.models import Student
        return Student.objects.filter(class_name=self.name, is_active=True).count()
    
    @property
    def available_seats(self):
        """Get available seats in class"""
        return self.capacity - self.student_count


class ClassRoom(models.Model):
    """Physical classroom information"""
    name = models.CharField(max_length=100, unique=True)  # e.g., "Room A1", "Lab 1"
    room_type = models.CharField(max_length=50, choices=[
        ('CLASSROOM', 'Classroom'),
        ('LAB', 'Laboratory'),
        ('COMPUTER_LAB', 'Computer Lab'),
        ('LIBRARY', 'Library'),
        ('MULTI_PURPOSE', 'Multi-purpose'),
    ])
    capacity = models.IntegerField(default=50)
    has_projector = models.BooleanField(default=False)
    has_air_conditioning = models.BooleanField(default=False)
    condition = models.CharField(max_length=50, choices=[
        ('EXCELLENT', 'Excellent'),
        ('GOOD', 'Good'),
        ('FAIR', 'Fair'),
        ('NEEDS_REPAIR', 'Needs Repair'),
    ], default='GOOD')
    last_maintenance_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Class Rooms'
    
    def __str__(self):
        return f"{self.name} ({self.get_room_type_display()})"


class ClassPerformanceMetrics(models.Model):
    """Track performance metrics for a class"""
    class_info = models.OneToOneField(ClassInfo, on_delete=models.CASCADE, related_name='performance_metrics')
    average_attendance_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    average_grade = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    discipline_incidents = models.IntegerField(default=0)
    academic_performance_trend = models.CharField(max_length=50, choices=[
        ('IMPROVING', 'Improving'),
        ('STABLE', 'Stable'),
        ('DECLINING', 'Declining'),
    ], default='STABLE')
    last_calculated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Performance Metrics - {self.class_info.name}"
