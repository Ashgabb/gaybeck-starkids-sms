from django.contrib import admin
from .models import Grade

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_assignment', 'term', 'mark', 'grade_letter', 'recorded_at')
    list_filter = ('term', 'year', 'class_assignment__subject', 'recorded_at')
    search_fields = ('student__name', 'class_assignment__subject')
    readonly_fields = ('recorded_at', 'grade_letter')
    fieldsets = (
        ('Student & Subject', {'fields': ('student', 'class_assignment')}),
        ('Grade Information', {'fields': ('term', 'year', 'mark', 'grade_letter')}),
        ('Comments', {'fields': ('comments',), 'classes': ('wide',)}),
        ('Recorded', {'fields': ('recorded_at',), 'classes': ('collapse',)}),
    )
