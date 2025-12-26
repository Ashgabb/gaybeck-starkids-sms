"""
Timetable App Models
Manages class schedules, timetables, and lesson planning
"""

from django.db import models
from teachers.models import Teacher, ClassAssignment
from django.core.validators import MinValueValidator, MaxValueValidator

class TimeSlot(models.Model):
    """Define time slots for the school day"""
    name = models.CharField(max_length=50)  # e.g., "Period 1", "Morning Session"
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['start_time']
    
    def __str__(self):
        return f"{self.name} ({self.start_time} - {self.end_time})"


class ClassTimetable(models.Model):
    """Define timetable entries for a class"""
    DAY_CHOICES = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    )
    
    class_assignment = models.ForeignKey(ClassAssignment, on_delete=models.CASCADE, related_name='timetable_entries')
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.PROTECT)
    room = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('class_assignment', 'day', 'time_slot')
        ordering = ['day', 'time_slot__start_time']
    
    def __str__(self):
        return f"{self.class_assignment.class_name} - {self.day} at {self.time_slot.name}"


class Homework(models.Model):
    """Homework assignments for classes"""
    STATUS_CHOICES = (
        ('ASSIGNED', 'Assigned'),
        ('SUBMITTED', 'Submitted'),
        ('GRADED', 'Graded'),
    )
    
    class_assignment = models.ForeignKey(ClassAssignment, on_delete=models.CASCADE, related_name='homework')
    title = models.CharField(max_length=200)
    description = models.TextField()
    assigned_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ASSIGNED')
    file_attachment = models.FileField(upload_to='homework_attachments/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-due_date']
    
    def __str__(self):
        return f"{self.class_assignment.class_name} - {self.title}"
    
    @property
    def is_overdue(self):
        from datetime import date
        return date.today() > self.due_date


class Lesson(models.Model):
    """Lesson plans and lesson topics"""
    class_assignment = models.ForeignKey(ClassAssignment, on_delete=models.CASCADE, related_name='lessons')
    topic = models.CharField(max_length=200)
    description = models.TextField()
    objectives = models.TextField(blank=True)
    teaching_materials = models.TextField(blank=True)
    lesson_date = models.DateField()
    duration_minutes = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(1440)])
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-lesson_date']
    
    def __str__(self):
        return f"{self.class_assignment.class_name} - {self.topic} ({self.lesson_date})"


class ClassRemark(models.Model):
    """Teacher remarks and observations for a class"""
    class_assignment = models.ForeignKey(ClassAssignment, on_delete=models.CASCADE, related_name='remarks')
    remark_date = models.DateField(auto_now_add=True)
    remark_text = models.TextField()
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-remark_date']
    
    def __str__(self):
        return f"{self.class_assignment.class_name} - {self.remark_date}"
