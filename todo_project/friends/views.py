from django.shortcuts import render,redirect
from .forms import FriendSearchForm
from django.contrib.auth.models import User
import sys
from django.urls import reverse
sys.path.append('..')
from account.models import UserProxy, user_info
from .models import Friendship
from itertools import chain



def friends_search(request):
    user_queryset = {}
    current_user_profile = user_info.objects.get(user_id=request.user)
    user_friends_profieles = current_user_profile.friends.all()
    user_friends = []
    for user_profile in user_friends_profieles:
        user_friends = list(chain(user_friends, UserProxy.objects.filter(username=user_profile.user_id.username)))


    if request.method == 'POST':
        form = FriendSearchForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user_queryset = UserProxy.objects.filter(username__startswith=cd['username']).exclude(username=request.user.username)
    else:
        form = FriendSearchForm()
    return render(request, 'friend_search.html', {'form': form, 'user_queryset': user_queryset, 'user_friends': user_friends})


def friend_add(request, pk, username):
    friend = user_info.objects.get(user_id=User.objects.get(pk=pk, username=username))
    current_user_profile = user_info.objects.get(user_id=request.user)
    rel = Friendship(friend_1=current_user_profile, friend_2=friend)
    rel.save()
    return redirect(reverse('friends:friends_search'))


def friend_delete(request, pk, username):
    delete_friend = User.objects.get(pk=pk, username=username).user_info
    request.user.user_info.friends.remove(delete_friend)
    return redirect(reverse('friends:friends_search'))
