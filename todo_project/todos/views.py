from django.shortcuts import render,redirect
from .models import todo, TodoReport
from .forms import TodoAddAndEditForm, ReportAddForm
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode



def todo_info(request, pk, slug):
    current_todo = todo.objects.get(pk=pk,
                                    slug=slug,
                                    )
    return render(request, 'todo_info.html', {'current_todo': current_todo})


def todo_add(request):
    user = request.user
    if request.method == 'POST':
        form = TodoAddAndEditForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            todo.objects.create(user_id=user,
                                name=cd['name'],
                                slug=slugify(unidecode(cd['name'])),
                                description=cd['description'])
            return redirect('/account/profile_info/')
    else:
        form = TodoAddAndEditForm()
    return render(request, 'todo_add.html', {'form': form})


def todo_del(request, pk, slug):
    todo_for_del = todo.objects.get(pk=pk, slug=slug)
    todo_for_del.delete()
    return redirect(reverse('account:profile_info'))


def todo_edit(request, pk, slug):
    if request.method == 'POST':
        form = TodoAddAndEditForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            todo.objects.filter(pk=pk, slug=slug).update(name=cd['name'],
                                                      description=cd['description'],
                                                      )
            return redirect(reverse('todos:todo_info', kwargs={'pk': pk,
                                                              'slug': slug}))
    else:
        todo_to_edit = todo.objects.get(pk=pk, slug=slug)
        form = TodoAddAndEditForm(initial={'name': todo_to_edit.name,
                                            'description': todo_to_edit.description})
    return render(request, 'todo_edit.html', {'form': form})



def report_add(request, pk, slug):
    current_todo = todo.objects.get(pk=pk, slug=slug)
    if request.method == 'POST':
        form = ReportAddForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            report = TodoReport(description = cd['description'])
            report.todo = current_todo
            report.save()
            return redirect(current_todo.get_absolute_url())
    else:
        form = ReportAddForm()
    return render(request, 'report_add.html', {'form': form})



def report_edit(request, pk, slug):
    current_todo = todo.objects.get(pk=pk, slug=slug)
    if request.method == 'POST':
        form = ReportAddForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            report = TodoReport.objects.get(todo=current_todo)
            report.description = cd['description']
            report.save()
            return redirect(current_todo.get_absolute_url())
    else:
        form = ReportAddForm(initial={'description': current_todo.report.description })
    return render(request, 'report_add.html', {'form': form})
