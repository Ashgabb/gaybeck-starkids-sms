from django.contrib import admin
from .models import AttendanceRecord

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'status', 'recorded_by')
    list_filter = ('date', 'status', 'class_name')
    search_fields = ('student__name', 'student__registration_number')
    date_hierarchy = 'date'
