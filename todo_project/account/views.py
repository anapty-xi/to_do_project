from django.shortcuts import render, redirect, HttpResponse
from .forms import RegisterForm, LoginForm, ProfileInfoForm, ResetPasswordForm, FortgotPasswordForm
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from . import services
from django.contrib.auth.models import User
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


@login_required
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


@login_required
def profile_info(request):
    '''страница с информацией профиля'''
    user = request.user
    user_todos = services.get_user_todos(user)
    return render(request, 'account/profile_info.html', {'user': user, 'user_todos': user_todos})



@login_required
def profile_info_edit(request):
    '''страница для изменения информации об аккаунте'''
    user = request.user
    if request.method == 'POST':
        form = ProfileInfoForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data 
            error_dict = {}
            error_dict['username'] = User.objects.exclude(pk=user.pk).filter(username=cd['username'])
            error_dict['email'] =  User.objects.exclude(pk=user.pk).filter(email=cd['email'])
            if len(error_dict['username']) == 0 and len(error_dict['email']) == 0:
                services.user_profile_update_user_model(request, cd)
                services.user_profile_update_profile_model(request, cd)
                return redirect('/account/profile_info')
            else:
                if len(error_dict['username']) == 0:
                    form.add_error(field='username', error=ValidationError('Логин уже занят'))
                elif len(error_dict['email']) == 0:
                    form.add_error(field='email', error=ValidationError('Почта уже привязана к другому аккаунту'))

        
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


@login_required
def another_profile_info(request, pk, username):
    '''профиль другого пользователя, его ToDo, и проверка является ли он другом текущего пользователя'''   
    user = services.get_user_by_pk_username(pk, username)
    friend_add_flag = True
    if user.profile in services.get_user_friends(request.user):
        friend_add_flag = False
    user_todos = services.get_user_todos(user)
    return render(request, 'account/another_profile_info.html', {'user': user, 'user_todos': user_todos, 'friend_add_flag': friend_add_flag})


@login_required
def reset_password_email(request):
    token = PasswordResetTokenGenerator()
    token = token.make_token(request.user)
    services.reset_password_email(request.user, token)
    return render(request, 'account/reset_email_sent.html')


def reset_password_proccess(request, token):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = request.user
            user.set_password(cd['password1'])
            user.save()
            flag = 'success'
    else:
        try:
            checker = PasswordResetTokenGenerator()
            if checker.check_token(user=request.user, token=token):
                flag = 'get'
            else:
                flag = 'token-fail'
            
        except:
            flag = 'anon'
        form = ResetPasswordForm()
    return render(request, 'account/reset_password.html', {'form': form, 'flag': flag})
    
def forgot_password(request):
    if request.method == 'POST':
        form = FortgotPasswordForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.get(email=cd['email'])
            token = PasswordResetTokenGenerator()
            token = token.make_token(user)
            services.reset_password_email(user, token)
            return render(request, 'account/reset_email_sent.html')
    else:
        form = FortgotPasswordForm()
    return render(request, 'account/forgot_password.html', {'form': form})
