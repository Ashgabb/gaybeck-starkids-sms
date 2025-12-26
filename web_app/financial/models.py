"""
Financial Management Models
Manages budgets, income, expenses, and cash flow
"""

from django.db import models
from decimal import Decimal
from django.utils import timezone
from datetime import datetime

class BudgetAllocation(models.Model):
    """Budget allocations for different categories"""
    CATEGORY_CHOICES = (
        ('SALARY', 'Salaries & Wages'),
        ('UTILITIES', 'Utilities'),
        ('MAINTENANCE', 'Maintenance & Repairs'),
        ('SUPPLIES', 'Supplies & Materials'),
        ('EQUIPMENT', 'Equipment & Technology'),
        ('TRANSPORTATION', 'Transportation'),
        ('ADMIN', 'Administrative'),
        ('DEVELOPMENT', 'Staff Development'),
        ('BUILDING', 'Building/Infrastructure'),
        ('OTHER', 'Other'),
    )
    
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, unique=True)
    allocated_amount = models.DecimalField(max_digits=15, decimal_places=2)
    year = models.IntegerField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-year', 'category']
        unique_together = ('category', 'year')
    
    def __str__(self):
        return f"{self.get_category_display()} - {self.year} (Ksh {self.allocated_amount})"
    
    @property
    def spent_amount(self):
        """Calculate total spent in this category"""
        return ExpenseRecord.objects.filter(
            category=self.category,
            date__year=self.year
        ).aggregate(total=models.Sum('amount'))['total'] or Decimal('0.00')
    
    @property
    def remaining_amount(self):
        """Calculate remaining budget"""
        return self.allocated_amount - self.spent_amount


class IncomeRecord(models.Model):
    """Track income sources"""
    INCOME_TYPE_CHOICES = (
        ('FEES', 'Student Fees'),
        ('DONATION', 'Donation'),
        ('GRANT', 'Grant/Subsidy'),
        ('SPONSORSHIP', 'Sponsorship'),
        ('INTEREST', 'Interest Income'),
        ('OTHER', 'Other Income'),
    )
    
    income_type = models.CharField(max_length=50, choices=INCOME_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateField(default=timezone.now)
    description = models.TextField()
    reference_number = models.CharField(max_length=100, blank=True)
    recorded_by = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Income Records'
    
    def __str__(self):
        return f"{self.get_income_type_display()} - Ksh {self.amount} ({self.date})"


class ExpenseRecord(models.Model):
    """Track expenses"""
    CATEGORY_CHOICES = (
        ('SALARY', 'Salaries & Wages'),
        ('UTILITIES', 'Utilities'),
        ('MAINTENANCE', 'Maintenance & Repairs'),
        ('SUPPLIES', 'Supplies & Materials'),
        ('EQUIPMENT', 'Equipment & Technology'),
        ('TRANSPORTATION', 'Transportation'),
        ('ADMIN', 'Administrative'),
        ('DEVELOPMENT', 'Staff Development'),
        ('BUILDING', 'Building/Infrastructure'),
        ('OTHER', 'Other'),
    )
    
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateField(default=timezone.now)
    description = models.TextField()
    vendor = models.CharField(max_length=100, blank=True)
    reference_number = models.CharField(max_length=100, blank=True)
    receipt_file = models.FileField(upload_to='expense_receipts/', blank=True, null=True)
    recorded_by = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Expense Records'
    
    def __str__(self):
        return f"{self.get_category_display()} - Ksh {self.amount} ({self.date})"


class MonthlyFinancialSummary(models.Model):
    """Monthly summary of income and expenses"""
    month = models.DateField()  # First day of month
    total_income = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    total_expenses = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    net_balance = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-month']
        unique_together = ('month',)
        verbose_name_plural = 'Monthly Financial Summaries'
    
    def __str__(self):
        return f"Financial Summary - {self.month.strftime('%B %Y')}"
    
    def calculate_summary(self):
        """Calculate financial summary for the month"""
        from django.db.models import Sum
        year = self.month.year
        month = self.month.month
        
        income_sum = IncomeRecord.objects.filter(
            date__year=year,
            date__month=month
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        
        expense_sum = ExpenseRecord.objects.filter(
            date__year=year,
            date__month=month
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        
        self.total_income = income_sum
        self.total_expenses = expense_sum
        self.net_balance = income_sum - expense_sum
        self.save()


class CashFlowProjection(models.Model):
    """Project future cash flow"""
    month = models.DateField()
    projected_income = models.DecimalField(max_digits=15, decimal_places=2)
    projected_expenses = models.DecimalField(max_digits=15, decimal_places=2)
    projected_balance = models.DecimalField(max_digits=15, decimal_places=2)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['month']
        unique_together = ('month',)
    
    def __str__(self):
        return f"Cash Flow Projection - {self.month.strftime('%B %Y')}"
