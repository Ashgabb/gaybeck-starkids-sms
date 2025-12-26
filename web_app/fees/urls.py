from django.urls import path
from . import views

app_name = 'fees'

urlpatterns = [
    path('', views.StudentFeeListView.as_view(), name='list'),
    path('create/', views.StudentFeeCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.StudentFeeUpdateView.as_view(), name='edit'),
    path('student/<int:student_id>/', views.StudentFeeDetailView.as_view(), name='student_detail'),
    path('<int:fee_id>/payment/create/', views.FeePaymentCreateView.as_view(), name='payment_create'),
    path('payments/', views.FeePaymentListView.as_view(), name='payment_list'),
    path('statistics/', views.FeeStatisticsView.as_view(), name='statistics'),
]
