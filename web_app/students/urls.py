from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('', views.StudentListView.as_view(), name='list'),
    path('create/', views.StudentCreateView.as_view(), name='create'),
    path('<int:pk>/', views.StudentDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.StudentEditView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.StudentDeleteView.as_view(), name='delete'),
    path('<int:student_pk>/documents/', views.StudentDocumentListView.as_view(), name='documents'),
    path('<int:student_pk>/documents/add/', views.StudentDocumentCreateView.as_view(), name='document_add'),
    path('document/<int:pk>/delete/', views.StudentDocumentDeleteView.as_view(), name='document_delete'),
]
