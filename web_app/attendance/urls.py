from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('', views.AttendanceListView.as_view(), name='list'),
    path('create/', views.AttendanceCreateView.as_view(), name='create'),
    path('bulk/', views.BulkAttendanceView.as_view(), name='bulk'),
    path('date/', views.AttendanceByDateView.as_view(), name='by_date'),
    path('date/<str:date>/', views.AttendanceByDateView.as_view(), name='by_date_specific'),
    path('class/<str:class_name>/', views.ClassAttendanceView.as_view(), name='by_class'),
    path('student/<int:student_id>/', views.StudentAttendanceView.as_view(), name='by_student'),
    path('record/<int:pk>/edit/', views.AttendanceEditView.as_view(), name='edit'),
]
