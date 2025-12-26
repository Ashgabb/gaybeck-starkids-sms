"""
Financial Management Views
Handle budget, income, expenses, and cash flow
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Sum, Q
from datetime import datetime, date, timedelta
from decimal import Decimal
from .models import BudgetAllocation, IncomeRecord, ExpenseRecord, MonthlyFinancialSummary, CashFlowProjection

class FinancialDashboardView(LoginRequiredMixin, TemplateView):
    """Financial management dashboard"""
    template_name = 'financial/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()
        year = today.year
        
        # Current year financial data
        income_total = IncomeRecord.objects.filter(date__year=year).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
        expense_total = ExpenseRecord.objects.filter(date__year=year).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
        
        context['year'] = year
        context['total_income'] = income_total
        context['total_expenses'] = expense_total
        context['net_balance'] = income_total - expense_total
        context['budget_items'] = BudgetAllocation.objects.filter(year=year)
        context['recent_income'] = IncomeRecord.objects.order_by('-date')[:10]
        context['recent_expenses'] = ExpenseRecord.objects.order_by('-date')[:10]
        
        return context


class BudgetListView(LoginRequiredMixin, ListView):
    """View budget allocations"""
    model = BudgetAllocation
    template_name = 'financial/budget_list.html'
    context_object_name = 'budgets'
    paginate_by = 20
    
    def get_queryset(self):
        year = self.request.GET.get('year')
        if year:
            return BudgetAllocation.objects.filter(year=year).order_by('category')
        current_year = date.today().year
        return BudgetAllocation.objects.filter(year=current_year).order_by('category')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['years'] = BudgetAllocation.objects.values_list('year', flat=True).distinct().order_by('-year')
        return context


class BudgetCreateView(LoginRequiredMixin, CreateView):
    """Create budget allocation"""
    model = BudgetAllocation
    template_name = 'financial/budget_form.html'
    fields = ['category', 'allocated_amount', 'year', 'notes']
    success_url = reverse_lazy('financial:budget_list')


class BudgetUpdateView(LoginRequiredMixin, UpdateView):
    """Update budget allocation"""
    model = BudgetAllocation
    template_name = 'financial/budget_form.html'
    fields = ['category', 'allocated_amount', 'year', 'notes']
    success_url = reverse_lazy('financial:budget_list')


class IncomeListView(LoginRequiredMixin, ListView):
    """View income records"""
    model = IncomeRecord
    template_name = 'financial/income_list.html'
    context_object_name = 'income_records'
    paginate_by = 30
    
    def get_queryset(self):
        queryset = IncomeRecord.objects.all()
        income_type = self.request.GET.get('type')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        
        if income_type:
            queryset = queryset.filter(income_type=income_type)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        return queryset.order_by('-date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['income_types'] = IncomeRecord.INCOME_TYPE_CHOICES
        context['total_income'] = IncomeRecord.objects.aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
        return context


class IncomeCreateView(LoginRequiredMixin, CreateView):
    """Record income"""
    model = IncomeRecord
    template_name = 'financial/income_form.html'
    fields = ['income_type', 'amount', 'date', 'description', 'reference_number']
    success_url = reverse_lazy('financial:income_list')
    
    def form_valid(self, form):
        form.instance.recorded_by = self.request.user.email
        return super().form_valid(form)


class IncomeUpdateView(LoginRequiredMixin, UpdateView):
    """Update income record"""
    model = IncomeRecord
    template_name = 'financial/income_form.html'
    fields = ['income_type', 'amount', 'date', 'description', 'reference_number']
    success_url = reverse_lazy('financial:income_list')


class ExpenseListView(LoginRequiredMixin, ListView):
    """View expense records"""
    model = ExpenseRecord
    template_name = 'financial/expense_list.html'
    context_object_name = 'expense_records'
    paginate_by = 30
    
    def get_queryset(self):
        queryset = ExpenseRecord.objects.all()
        category = self.request.GET.get('category')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        
        if category:
            queryset = queryset.filter(category=category)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        return queryset.order_by('-date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ExpenseRecord.CATEGORY_CHOICES
        context['total_expenses'] = ExpenseRecord.objects.aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
        return context


class ExpenseCreateView(LoginRequiredMixin, CreateView):
    """Record expense"""
    model = ExpenseRecord
    template_name = 'financial/expense_form.html'
    fields = ['category', 'amount', 'date', 'description', 'vendor', 'reference_number', 'receipt_file']
    success_url = reverse_lazy('financial:expense_list')
    
    def form_valid(self, form):
        form.instance.recorded_by = self.request.user.email
        return super().form_valid(form)


class ExpenseUpdateView(LoginRequiredMixin, UpdateView):
    """Update expense record"""
    model = ExpenseRecord
    template_name = 'financial/expense_form.html'
    fields = ['category', 'amount', 'date', 'description', 'vendor', 'reference_number', 'receipt_file']
    success_url = reverse_lazy('financial:expense_list')


class FinancialReportView(LoginRequiredMixin, TemplateView):
    """Generate financial reports"""
    template_name = 'financial/report.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = self.request.GET.get('year') or date.today().year
        
        # Income and expense by category
        income_by_type = IncomeRecord.objects.filter(
            date__year=year
        ).values('income_type').annotate(total=Sum('amount')).order_by('-total')
        
        expense_by_category = ExpenseRecord.objects.filter(
            date__year=year
        ).values('category').annotate(total=Sum('amount')).order_by('-total')
        
        context['year'] = year
        context['income_by_type'] = income_by_type
        context['expense_by_category'] = expense_by_category
        context['total_income'] = sum(item['total'] for item in income_by_type)
        context['total_expenses'] = sum(item['total'] for item in expense_by_category)
        
        return context
