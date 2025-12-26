from django.contrib import admin
from .models import FeeType, StudentFee, FeePayment

@admin.register(FeeType)
class FeeTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'is_active')
    list_filter = ('is_active', 'created_at')

@admin.register(StudentFee)
class StudentFeeAdmin(admin.ModelAdmin):
    list_display = ('student', 'fee_type', 'term', 'amount_due', 'amount_paid', 'is_paid')
    list_filter = ('term', 'year', 'is_paid')
    search_fields = ('student__name', 'student__registration_number')

@admin.register(FeePayment)
class FeePaymentAdmin(admin.ModelAdmin):
    list_display = ('student_fee', 'amount', 'payment_method', 'payment_date')
    list_filter = ('payment_method', 'payment_date')
    search_fields = ('student_fee__student__name',)
