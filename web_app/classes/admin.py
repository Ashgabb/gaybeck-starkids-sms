from django.contrib import admin
from .models import ClassInfo, ClassRoom, ClassPerformanceMetrics

@admin.register(ClassInfo)
class ClassInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'stream', 'class_teacher', 'capacity', 'year', 'is_active']
    list_filter = ['level', 'year', 'is_active']
    search_fields = ['name', 'stream']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(ClassRoom)
class ClassRoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'room_type', 'capacity', 'condition', 'is_active']
    list_filter = ['room_type', 'condition', 'is_active']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(ClassPerformanceMetrics)
class ClassPerformanceMetricsAdmin(admin.ModelAdmin):
    list_display = ['class_info', 'average_attendance_rate', 'average_grade', 'academic_performance_trend']
    list_filter = ['academic_performance_trend']
    readonly_fields = ['last_calculated']
