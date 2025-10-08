from django.shortcuts import render
from .models import friend
from .forms import FriendSearchForm
from django.contrib.auth.models import User
import sys
sys.path.append('..')
from account.models import UserProxy


def friends_search(request):
    user_queryset = {}
    if request.method == 'POST':
        form = FriendSearchForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user_queryset = UserProxy.objects.filter(username__startswith=cd['username'])
    else:
        form = FriendSearchForm()
    return render(request, 'friend_search.html', {'form': form, 'user_queryset': user_queryset})
