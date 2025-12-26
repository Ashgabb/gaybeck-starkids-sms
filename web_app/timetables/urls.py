from django.urls import path
from . import views

app_name = 'timetables'

urlpatterns = [
    # Timetable URLs
    path('', views.TimetableListView.as_view(), name='timetable_list'),
    path('create/', views.TimetableCreateView.as_view(), name='timetable_create'),
    path('<int:pk>/edit/', views.TimetableUpdateView.as_view(), name='timetable_update'),
    path('<int:pk>/delete/', views.TimetableDeleteView.as_view(), name='timetable_delete'),
    
    # Homework URLs
    path('homework/', views.HomeworkListView.as_view(), name='homework_list'),
    path('homework/create/', views.HomeworkCreateView.as_view(), name='homework_create'),
    path('homework/<int:pk>/', views.HomeworkDetailView.as_view(), name='homework_detail'),
    path('homework/<int:pk>/edit/', views.HomeworkUpdateView.as_view(), name='homework_update'),
    
    # Lesson URLs
    path('lessons/', views.LessonListView.as_view(), name='lesson_list'),
    path('lessons/create/', views.LessonCreateView.as_view(), name='lesson_create'),
    path('lessons/<int:pk>/', views.LessonDetailView.as_view(), name='lesson_detail'),
    path('lessons/<int:pk>/edit/', views.LessonUpdateView.as_view(), name='lesson_update'),
]
