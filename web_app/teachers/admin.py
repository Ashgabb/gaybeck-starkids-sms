from django.contrib import admin
from .models import Teacher, ClassAssignment

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id', 'subject', 'hire_date', 'is_active')
    list_filter = ('subject', 'is_active', 'hire_date')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'employee_id')

@admin.register(ClassAssignment)
class ClassAssignmentAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'class_name', 'subject', 'year')
    list_filter = ('year', 'class_name', 'subject')
    search_fields = ('teacher__user__first_name', 'class_name')
