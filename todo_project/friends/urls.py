from django.urls import path
from . import views


app_name = 'friends'

urlpatterns = [
    path('search/', views.friends_search, name='friends_search'),
    path('add/<int:pk>/<str:username>/', views.friend_add, name='friend_add'),
    path('delete/<int:pk>/<str:username>/', views.friend_delete, name='friend_delete'),
]