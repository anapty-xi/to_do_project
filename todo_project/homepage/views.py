from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def homepage(requset):
    todos = todo.objects.all()
    return render(requset, 'homepage/homepage.html', {'todos': todos})
