from django.contrib import admin
from .models import BudgetAllocation, IncomeRecord, ExpenseRecord, MonthlyFinancialSummary, CashFlowProjection

@admin.register(BudgetAllocation)
class BudgetAllocationAdmin(admin.ModelAdmin):
    list_display = ['category', 'year', 'allocated_amount']
    list_filter = ['year']
    search_fields = ['category']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(IncomeRecord)
class IncomeRecordAdmin(admin.ModelAdmin):
    list_display = ['income_type', 'amount', 'date', 'recorded_by']
    list_filter = ['income_type', 'date']
    search_fields = ['description', 'reference_number']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(ExpenseRecord)
class ExpenseRecordAdmin(admin.ModelAdmin):
    list_display = ['category', 'amount', 'date', 'vendor', 'recorded_by']
    list_filter = ['category', 'date']
    search_fields = ['description', 'vendor', 'reference_number']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(MonthlyFinancialSummary)
class MonthlyFinancialSummaryAdmin(admin.ModelAdmin):
    list_display = ['month', 'total_income', 'total_expenses', 'net_balance']
    list_filter = ['month']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(CashFlowProjection)
class CashFlowProjectionAdmin(admin.ModelAdmin):
    list_display = ['month', 'projected_income', 'projected_expenses', 'projected_balance']
    list_filter = ['month']
    readonly_fields = ['created_at', 'updated_at']
