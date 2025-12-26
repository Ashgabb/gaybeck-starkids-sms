"""Grading App Models"""

from django.db import models
from students.models import Student
from teachers.models import ClassAssignment
from django.core.validators import MinValueValidator, MaxValueValidator

class Grade(models.Model):
    TERM_CHOICES = (('1', 'Term 1'), ('2', 'Term 2'), ('3', 'Term 3'))
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    class_assignment = models.ForeignKey(ClassAssignment, on_delete=models.CASCADE, related_name='grades')
    term = models.CharField(max_length=1, choices=TERM_CHOICES)
    year = models.IntegerField()
    mark = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    comments = models.TextField(blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('student', 'class_assignment', 'term', 'year')
        ordering = ['-year', '-term']
    
    def __str__(self):
        return f"{self.student.name} - {self.class_assignment.subject}: {self.mark}/100"
    
    @property
    def grade_letter(self):
        """Convert numeric grade to letter grade"""
        if self.mark >= 90:
            return 'A'
        elif self.mark >= 80:
            return 'B'
        elif self.mark >= 70:
            return 'C'
        elif self.mark >= 60:
            return 'D'
        else:
            return 'F'
