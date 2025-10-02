from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm, ProfileInfoForm
from django.contrib.auth.models import User
from .models import user_info
from django.core.exceptions import ValidationError




def login_view(request):
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


def profile_info(requset):
    user = requset.user
    if requset.method == 'POST':
        form = ProfileInfoForm(requset.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user_unfo_obj = user_info.objects.get(user_id=user.id)
            user_unfo_obj.sex = cd['sex']
    else:
        form = ProfileInfoForm()
    return render(requset, 'profile_info.html', {'form': form, 'user': user})


