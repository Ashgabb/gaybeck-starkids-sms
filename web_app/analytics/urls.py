from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('dashboard/', views.AnalyticsDashboardView.as_view(), name='dashboard'),
    path('student/<int:student_id>/', views.StudentAnalyticsView.as_view(), name='student'),
    path('class/<str:class_name>/', views.ClassAnalyticsView.as_view(), name='class'),
    path('reports/', views.AnalyticsReportsView.as_view(), name='reports'),
    path('export/', views.ExportAnalyticsView.as_view(), name='export'),
]
