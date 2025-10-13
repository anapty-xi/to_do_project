from django.urls import path
from . import views

app_name = 'todos'

urlpatterns = [
    path('<int:pk>/<str:slug>/', views.todo_info, name='todo_info'),
    path('add/', views.todo_add, name='todo_add'),
    path('delete/<int:pk>/<str:slug>/', views.todo_del, name='todo_del'),
    path('edit/<int:pk>/<str:slug>/', views.todo_edit, name='todo_edit'),
    path('report/add/<int:pk>/<str:slug>/', views.report_add, name='report_add'),
   
]