from django.urls import path
from . import views

app_name = 'classes'

urlpatterns = [
    # Class URLs
    path('', views.ClassListView.as_view(), name='class_list'),
    path('create/', views.ClassCreateView.as_view(), name='class_create'),
    path('<int:pk>/', views.ClassDetailView.as_view(), name='class_detail'),
    path('<int:pk>/edit/', views.ClassUpdateView.as_view(), name='class_update'),
    
    # Classroom URLs
    path('rooms/', views.ClassRoomListView.as_view(), name='classroom_list'),
    path('rooms/create/', views.ClassRoomCreateView.as_view(), name='classroom_create'),
    path('rooms/<int:pk>/edit/', views.ClassRoomUpdateView.as_view(), name='classroom_update'),
    
    # Performance
    path('performance/', views.ClassPerformanceView.as_view(), name='performance'),
]
