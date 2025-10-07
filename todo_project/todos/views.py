from django.shortcuts import render
from .models import todo



def todo_info(request, pk, slug, publish_date):
    current_todo = todo.objects.get(pk=pk,
                                    slug=slug,
                                    publish_date=publish_date)
    return render(request, 'todo_info.html', {'current_todo': current_todo})