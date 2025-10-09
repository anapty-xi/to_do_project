from django.shortcuts import render,redirect
from .forms import FriendSearchForm
from django.contrib.auth.models import User
import sys
from django.urls import reverse
sys.path.append('..')
from account.models import UserProxy, user_info



def friends_search(request):
    user_queryset = {}
    user_friends = user_info.objects.get(user_id=request.user).friends.all()
    if request.method == 'POST':
        form = FriendSearchForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user_queryset = UserProxy.objects.filter(username__startswith=cd['username']).exclude(username=request.user.username)
    else:
        form = FriendSearchForm()
    return render(request, 'friend_search.html', {'form': form, 'user_queryset': user_queryset, 'user_friends': user_friends})


def friend_add(request, pk, username):
    friend = User.objects.get(pk=pk, username=username)
    current_user_profile = user_info.objects.get(user_id=request.user)
    current_user_profile.friends.add(friend)
    return redirect(reverse('homepage:homepage'))
