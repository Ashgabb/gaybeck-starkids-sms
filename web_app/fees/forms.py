from django import forms
from .models import StudentFee, FeePayment

class StudentFeeForm(forms.ModelForm):
    class Meta:
        model = StudentFee
        fields = ['fee_type', 'term', 'year', 'amount_due', 'due_date']

class FeePaymentForm(forms.ModelForm):
    class Meta:
        model = FeePayment
        fields = ['amount', 'payment_method', 'reference_number', 'notes']
