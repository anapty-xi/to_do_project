from django.shortcuts import render,redirect
from .forms import FriendSearchForm
from django.urls import reverse
from . import services



def friends_search(request):
    '''страница для поиска новых и отображения имеющихся друзей'''
    search_queryset = []
    user_friends = services.user_friends_with_gau(request)
    if request.method == 'POST':
        form = services.form_post(request, FriendSearchForm)
        cd = form.cleaned_data
        search_queryset = services.search_queryset(request, cd)
    else:
        form = FriendSearchForm()
    return render(request, 'friend_search.html', {'form': form, 'user_queryset': search_queryset, 'user_friends': user_friends})



def friend_add(request, pk, username):
    services.friend_add(request, pk, username)
    return redirect(reverse('friends:friends_search'))



def friend_delete(request, pk, username):
    services.friend_delete(request, pk, username)
    return redirect(reverse('friends:friends_search'))
