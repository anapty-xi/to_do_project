from django.urls import path
from . import views


app_name = 'friends'

urlpatterns = [
    path('search/', views.friends_search, name='friend_search'),
    path('<int:pk>/<str:username>/', views.friend_add, name='friend_add'),
]