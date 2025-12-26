from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q, Sum, Count
from students.models import Student
from .models import StudentFee, FeePayment, FeeType
from .forms import FeePaymentForm

class StudentFeeListView(LoginRequiredMixin, ListView):
    model = StudentFee
    template_name = 'fees/fee_list.html'
    context_object_name = 'fees'
    paginate_by = 25
    
    def get_queryset(self):
        queryset = StudentFee.objects.select_related('student', 'fee_type')
        search = self.request.GET.get('search', '')
        status_filter = self.request.GET.get('status', '')
        
        if search:
            queryset = queryset.filter(
                Q(student__name__icontains=search) |
                Q(student__registration_number__icontains=search)
            )
        
        if status_filter == 'paid':
            queryset = queryset.filter(is_paid=True)
        elif status_filter == 'pending':
            queryset = queryset.filter(is_paid=False)
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['total_pending'] = StudentFee.objects.filter(is_paid=False).aggregate(
            Sum('amount_due')
        )['amount_due__sum'] or 0
        return context

class StudentFeeDetailView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = 'fees/student_fee_detail.html'
    context_object_name = 'student'
    pk_url_kwarg = 'student_id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.get_object()
        context['fees'] = student.fees.all()
        context['payments'] = FeePayment.objects.filter(student_fee__student=student)
        context['total_amount'] = student.fees.aggregate(Sum('amount_due'))['amount_due__sum'] or 0
        context['total_paid'] = FeePayment.objects.filter(
            student_fee__student=student
        ).aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
        context['balance'] = context['total_amount'] - context['total_paid']
        return context

class FeePaymentCreateView(LoginRequiredMixin, CreateView):
    model = FeePayment
    form_class = FeePaymentForm
    template_name = 'fees/payment_form.html'
    
    def form_valid(self, form):
        student_fee = get_object_or_404(StudentFee, pk=self.kwargs['fee_id'])
        form.instance.student_fee = student_fee
        form.instance.recorded_by = self.request.user.email
        return super().form_valid(form)
    
    def get_success_url(self):
        student_fee = get_object_or_404(StudentFee, pk=self.kwargs['fee_id'])
        return reverse_lazy('fees:student_detail', kwargs={'student_id': student_fee.student.id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student_fee'] = get_object_or_404(StudentFee, pk=self.kwargs['fee_id'])
        return context

class FeePaymentListView(LoginRequiredMixin, ListView):
    model = FeePayment
    template_name = 'fees/payment_list.html'
    context_object_name = 'payments'
    paginate_by = 50
    
    def get_queryset(self):
        queryset = FeePayment.objects.select_related('student_fee__student')
        search = self.request.GET.get('search', '')
        method_filter = self.request.GET.get('method', '')
        
        if search:
            queryset = queryset.filter(
                Q(student_fee__student__name__icontains=search) |
                Q(student_fee__student__registration_number__icontains=search)
            )
        
        if method_filter:
            queryset = queryset.filter(payment_method=method_filter)
        
        return queryset.order_by('-payment_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['payment_methods'] = FeePayment.PAYMENT_METHOD_CHOICES
        context['total_collected'] = FeePayment.objects.aggregate(
            Sum('amount_paid')
        )['amount_paid__sum'] or 0
        return context

class StudentFeeCreateView(LoginRequiredMixin, CreateView):
    model = StudentFee
    fields = ['student', 'fee_type', 'amount', 'due_date']
    template_name = 'fees/fee_form.html'
    success_url = reverse_lazy('fees:list')

class StudentFeeUpdateView(LoginRequiredMixin, UpdateView):
    model = StudentFee
    fields = ['amount', 'due_date', 'is_paid']
    template_name = 'fees/fee_form.html'
    success_url = reverse_lazy('fees:list')

class FeeStatisticsView(LoginRequiredMixin, ListView):
    template_name = 'fees/statistics.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Calculate statistics
        total_fees = StudentFee.objects.aggregate(Sum('amount_due'))['amount_due__sum'] or 0
        paid_fees = FeePayment.objects.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
        pending_fees = StudentFee.objects.filter(is_paid=False).aggregate(
            Sum('amount_due')
        )['amount_due__sum'] or 0
        
        context['total_fees'] = total_fees
        context['paid_fees'] = paid_fees
        context['pending_fees'] = pending_fees
        context['collection_rate'] = (paid_fees / total_fees * 100) if total_fees > 0 else 0
        
        # By payment method
        context['by_method'] = FeePayment.objects.values('payment_method').annotate(
            count=Count('id'),
            total=Sum('amount_paid')
        )
        
        # By class
        context['by_class'] = StudentFee.objects.values('student__class_name').annotate(
            count=Count('id'),
            total=Sum('amount'),
            paid=Sum('amount') - Sum('amount') * 0  # Simplified
        )
        
        return context
