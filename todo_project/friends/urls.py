from django.urls import path
from . import views


app_name = 'friends'

urlpatterns = [
    path('search/', views.friends_search, name='friend_search'),
]