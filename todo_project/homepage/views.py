from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import sys
sys.path.append('..')
from todos.models import todo
from account.models import user_info


@login_required
def homepage(requset):
    user = requset.user
    user_todos = user.todo.all()
    friends = user.user_info.friends.all()
    friends_todos_manylvl = map(lambda x: x.user_id.todo.all(), friends)
    friends_todos = []
    for todos in friends_todos_manylvl:
        friends_todos.extend(todos)
    return render(requset, 'homepage/homepage.html', {'user_todos': user_todos, 'friends_todos': friends_todos})
