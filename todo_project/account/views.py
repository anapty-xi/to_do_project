from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm, ProfileInfoForm
from django.contrib.auth.models import User
from .models import user_info
from django.core.exceptions import ValidationError

import sys
sys.path.append('..')
from todos.models import todo




def login_view(request):

    '''вход пользователя в аккаунт'''

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('/homepage')
            else:
                form.add_error(field=None, error=ValidationError('неверный логин или пароль'))
    else:
        form = LoginForm()
    return render(request, 'authentication/login.html', {'form': form})



def register_view(request):

    '''регистарция пользователя'''

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password1'] == form.cleaned_data['password2']:
                User.objects.create_user(username=form.cleaned_data['username'], email=form.cleaned_data['email'],
                                        password=form.cleaned_data['password1'])
                user = User.objects.get(username=form.cleaned_data['username'])
                user_info.objects.create(user_id=user)

                return redirect('/account/login')

    else:
        form = RegisterForm()
    return render(request, 'authentication/register.html', {'form': form})



def profile_info(request):

    '''страница с информацией профиля'''
    
    user = request.user
    user_todos = todo.objects.filter(user_id=user.id)
    return render(request, 'account/profile_info.html', {'user': user, 'user_todos': user_todos})




def profile_info_edit(request):
    
    '''страница для изменения информации об аккаунте'''
    user = request.user
    if request.method == 'POST':
        form = ProfileInfoForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            
            User.objects.filter(id=user.id).update(username=cd['username'],
                                                email=cd['email'])
            user_info.objects.filter(user_id=user.id).update(photo=cd['photo'],
                                                  sex=cd['sex'],
                                                  birthd=cd['birthd'],
                                                  preview=cd['preview'],
                                                  )
                                                  
            a = user_info.objects.get(user_id=user.id)
            a.photo = cd['photo']
            a.save()
            return redirect('/account/profile_info')
        
    else:
        form = ProfileInfoForm(initial={
            'username': user.username,
            'email': user.email,
            'birthd': user.user_info.birthd,
            'sex': user.user_info.sex,
            'preview': user.user_info.preview,
            'photo': user.user_info.photo,
        })
                                        
    return render(request, 'account/profile_info_edit.html', {'form': form})



def another_profile_info(request, pk, username):
    user = User.objects.get(pk=pk, username=username)
    user_todos = todo.objects.filter(user_id=user)
    return render(request, 'account/another_profile_info.html', {'user': user, 'user_todos': user_todos})




