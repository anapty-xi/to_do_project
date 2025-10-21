from django.shortcuts import render, redirect, HttpResponse
from .forms import RegisterForm, LoginForm, ProfileInfoForm
from django.core.exceptions import ValidationError
from django.urls import reverse
from . import services
import sys
sys.path.append('..')



def login_view(request):

    '''вход пользователя в аккаунт'''

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = services.user_auth(cd)
            if user:
                services.user_login(request, user)
                return redirect('/homepage')
            else:
                form.add_error(field=None, error=ValidationError('неверный логин или пароль'))
    else:
        form = LoginForm()
    return render(request, 'authentication/login.html', {'form': form})



def logout_view(request):
    services.user_logout(request)
    return redirect(reverse('account:login'))



def register_view(request):
    '''регистарция пользователя, создание экземпляра User и связанного с ним Profile'''
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            services.user_register(cd)
            return redirect('/account/login')
    else:
        form = RegisterForm()
    return render(request, 'authentication/register.html', {'form': form})



def profile_info(request):
    '''страница с информацией профиля'''
    user = request.user
    user_todos = services.get_user_todos(user)
    return render(request, 'account/profile_info.html', {'user': user, 'user_todos': user_todos})




def profile_info_edit(request):
    '''страница для изменения информации об аккаунте'''
    user = request.user
    if request.method == 'POST':
        form = ProfileInfoForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data  
            services.user_profile_update_user_model(request, cd)
            services.user_profile_update_profile_model(request, cd)
            return redirect('/account/profile_info')

        
    else:
        form = ProfileInfoForm(initial={
            'username': user.username,
            'email': user.email,
            'birthd': user.profile.birthd,
            'sex': user.profile.sex,
            'preview': user.profile.preview,
            'photo': user.profile.photo,
        })
                                        
    return render(request, 'account/profile_info_edit.html', {'form': form})



def another_profile_info(request, pk, username):
    '''профиль другого пользователя, его ToDo, и проверка является ли он другом текущего пользователя'''   
    user = services.get_user_by_pk_username(pk, username)
    friend_add_flag = True
    if user.profile in services.get_user_friends(request.user):
        friend_add_flag = False
    user_todos = services.get_user_todos(user)
    return render(request, 'account/another_profile_info.html', {'user': user, 'user_todos': user_todos, 'friend_add_flag': friend_add_flag})




