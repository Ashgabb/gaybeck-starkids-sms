from django.urls import path
from . import views

app_name = 'grading'

urlpatterns = [
    path('', views.GradeListView.as_view(), name='list'),
    path('create/', views.GradeCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.GradeEditView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.GradeDeleteView.as_view(), name='delete'),
    path('student/<int:student_id>/', views.StudentGradeView.as_view(), name='student_grades'),
    path('class/<str:class_name>/', views.ClassGradesView.as_view(), name='class_grades'),
    path('bulk-upload/', views.BulkGradeUploadView.as_view(), name='bulk_upload'),
]
