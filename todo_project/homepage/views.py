from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import services
from datetime import datetime


@login_required
def homepage(requset):

    '''отображения главной страницы с собстенными ToDo и ToDo друзей'''

    user = requset.user
    user_todos = services.get_user_todos(user)
    friends_todos = services.get_friends_todos(user)
    now = datetime.now()
    return render(requset, 'homepage/homepage.html', {'user_todos': user_todos, 'friends_todos': friends_todos, 'now': now})
