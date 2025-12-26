from django.contrib import admin
from .models import TimeSlot, ClassTimetable, Homework, Lesson, ClassRemark

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_time', 'end_time', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']

@admin.register(ClassTimetable)
class ClassTimetableAdmin(admin.ModelAdmin):
    list_display = ['class_assignment', 'day', 'time_slot', 'room', 'is_active']
    list_filter = ['day', 'is_active']
    search_fields = ['class_assignment__class_name', 'room']

@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ['title', 'class_assignment', 'due_date', 'status']
    list_filter = ['status', 'due_date']
    search_fields = ['title', 'class_assignment__class_name']

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['topic', 'class_assignment', 'lesson_date', 'duration_minutes']
    list_filter = ['lesson_date']
    search_fields = ['topic', 'class_assignment__class_name']

@admin.register(ClassRemark)
class ClassRemarkAdmin(admin.ModelAdmin):
    list_display = ['class_assignment', 'remark_date', 'teacher']
    list_filter = ['remark_date']
    search_fields = ['class_assignment__class_name', 'remark_text']
