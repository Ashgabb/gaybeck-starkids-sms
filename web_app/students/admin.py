from django.contrib import admin
from .models import Student, StudentDocument

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'registration_number', 'class_name', 'is_active', 'admission_date')
    list_filter = ('class_name', 'is_active', 'admission_date')
    search_fields = ('name', 'registration_number', 'email')
    fieldsets = (
        ('Personal Information', {'fields': ('name', 'registration_number', 'date_of_birth', 'gender', 'email', 'phone')}),
        ('Address', {'fields': ('address',)}),
        ('Class Information', {'fields': ('class_name', 'admission_date', 'is_active')}),
        ('Guardian Information', {'fields': ('guardian_name', 'guardian_phone', 'guardian_email')}),
        ('Photo', {'fields': ('photo',)}),
    )

@admin.register(StudentDocument)
class StudentDocumentAdmin(admin.ModelAdmin):
    list_display = ('student', 'document_type', 'uploaded_at')
    list_filter = ('document_type', 'uploaded_at')
    search_fields = ('student__name', 'document_type')
