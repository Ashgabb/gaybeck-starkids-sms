from django.urls import path
from . import views

app_name = 'teachers'

urlpatterns = [
    path('', views.TeacherListView.as_view(), name='list'),
    path('create/', views.TeacherCreateView.as_view(), name='create'),
    path('<int:pk>/', views.TeacherDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.TeacherUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.TeacherDeleteView.as_view(), name='delete'),
    path('assignments/', views.ClassAssignmentListView.as_view(), name='assignments'),
    path('assignments/create/', views.ClassAssignmentCreateView.as_view(), name='assignment_create'),
    path('assignments/<int:pk>/edit/', views.ClassAssignmentUpdateView.as_view(), name='assignment_edit'),
]
