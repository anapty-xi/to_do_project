from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from .models import profile_info




def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('/')
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
                profile_info.objects.create(id=user.id)            
                return redirect('/')

    else:
        form = RegisterForm()
    return render(request, 'authentication/register.html', {'form': form})

