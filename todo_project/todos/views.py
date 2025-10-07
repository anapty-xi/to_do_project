from django.shortcuts import render,redirect
from .models import todo
from .forms import TodoAddForm



def todo_info(request, pk, slug, publish_date):
    current_todo = todo.objects.get(pk=pk,
                                    slug=slug,
                                    publish_date=publish_date)
    return render(request, 'todo_info.html', {'current_todo': current_todo})


def todo_add(request):
    user = request.user
    if request.method == 'POST':
        form = TodoAddForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            todo.objects.create(user_id=user,
                                name=cd['name'],
                                description=cd['description'])
            return redirect('/account/profile_info/')
    else:
        form = TodoAddForm()
    return render(request, 'todo_add.html', {'form': form})