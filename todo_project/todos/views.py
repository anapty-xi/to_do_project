from django.shortcuts import render,redirect
from .forms import TodoAddAndEditForm, ReportAddForm
from django.urls import reverse
from . import services
from django.contrib.auth.decorators import login_required
from datetime import datetime
from account.services import get_user_by_pk_username



@login_required
def todo_info(request, pk, slug):

    '''подробная иформация о ToDo'''

    current_todo = services.get_todo_by_pk_slug(pk, slug)
    is_user_todo = False
    if current_todo in request.user.todo.all():
        is_user_todo = True
    return render(request, 'todo_info.html', {'current_todo': current_todo, 'is_user_todo': is_user_todo})


@login_required
def todo_add(request):

    '''создание ToDo'''

    user = request.user
    if request.method == 'POST':
        form = TodoAddAndEditForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            services.todo_add(cd, user)
            return redirect(reverse('account:profile_info'))
    else:
        form = TodoAddAndEditForm()
    return render(request, 'todo_add.html', {'form': form})


@login_required
def todo_del(request, pk, slug):

    '''удаление ToDo'''

    services.todo_del(pk, slug)
    return redirect(reverse('account:profile_info'))


@login_required
def todo_edit(request, pk, slug):

    '''изсенение ToDo'''

    todo_to_edit = services.get_todo_by_pk_slug(pk, slug)
    if request.method == 'POST':
        form = TodoAddAndEditForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            services.todo_update(pk, slug, cd)

            return redirect(reverse('todos:todo_info', kwargs={'pk': pk,
                                                                'slug': slug}))
    else:
        form = TodoAddAndEditForm(initial={'name': todo_to_edit.name,
                                            'description': todo_to_edit.description})
    return render(request, 'todo_edit.html', {'form': form})


@login_required
def report_add(request, pk, slug):

    '''создание отчета'''

    current_todo = services.get_todo_by_pk_slug(pk, slug)
    if request.method == 'POST':
        form = ReportAddForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            services.report_add(pk, slug, cd)
            services.todo_change_status(pk, slug, status='no_confirm')
            
            return redirect(current_todo.get_absolute_url())
    else:
        form = ReportAddForm()
    return render(request, 'report_add.html', {'form': form})


@login_required
def report_edit(request, pk, slug):

    '''изменение отчета'''

    current_todo = services.get_todo_by_pk_slug(pk, slug)
    if request.method == 'POST':
        form = ReportAddForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            services.report_edit(pk, slug, cd)
            return redirect(current_todo.get_absolute_url())
    else:
        form = ReportAddForm(initial={'description': current_todo.report.description })
    return render(request, 'report_add.html', {'form': form})


@login_required
def todo_confirm(requset, pk, slug):

    '''подтверждение ToDo и отправка письма о подтверждении'''

    todo = services.todo_change_status(pk, slug, status='confirmed')
    services.your_todo_has_confirmed_mail(todo.user.email,
                                          todo.user.username,
                                          todo.name)
    return redirect(todo.get_absolute_url())


@login_required
def friends_reminder(request):

    '''отправка писем всем друзьям пользователя с просьбой создать ToDO'''

    user = request.user
    friends = services.get_user_friends(user)
    services.friends_reminder_mail(user, friends)
    emails_amount = friends.count()
    now = datetime.now()
    return render(request, 'friends_reminder.html', {'emails_amount': emails_amount, 'now': now})

@login_required
def friend_reminder(request, pk, username):

    '''отправка письма конкретному другу с просьбой создать ToDO'''

    user = request.user
    friend = get_user_by_pk_username(pk, username)
    services.friends_reminder_mail(user, [friend.email])
    now = datetime.now()
    return render(request, 'friends_reminder.html', {'now': now})
