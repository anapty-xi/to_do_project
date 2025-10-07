from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import sys
sys.path.append('..')
from todos.models import todo

@login_required
def homepage(requset):
    todos = todo.objects.all()
    return render(requset, 'homepage/homepage.html', {'todos': todos})
