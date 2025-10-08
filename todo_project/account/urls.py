from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('profile_info/', views.profile_info, name='profile_info'),
    path('profile_info_edit/', views.profile_info_edit, name='profile_info_edit'),
    path('<int:pk>/<str:username>/', views.another_profile_info, name='another_profile_info'),
]