from django.urls import path
from . import views

app_name = 'todos'

urlpatterns = [
    path('<int:pk>/<str:slug>/<str:publish_date>/', views.todo_info, name='todo_info'),
    path('add/', views.todo_add, name='todo_add'),
]