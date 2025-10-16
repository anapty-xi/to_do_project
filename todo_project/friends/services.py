from account.models import UserProxy, Profile
import todos
from .models import Friendship
from django.contrib.auth.models import User







def user_friends_with_gau(request):
    '''отображение профилей друзей на UserProxy, так как друзья храняться как экземпляры Profile,
    а метод get_absolute_url описан в прокси модели UserProxy'''
    return list(map(lambda x: UserProxy.objects.get(username=x.user.username)
                                , request.user.profile.friends.all()))



def search_queryset(request, cd):
    '''проводит простой поиск по принципу "вернуть если объект начинается с"  '''
    return UserProxy.objects.filter(username__startswith=cd['username']).exclude(username=request.user.username)



def friend_add(request, pk, username):
    '''Friendship хранит экземпляры Profile так что получаем их для текущего юзера и друга'''
    friend = User.objects.get(pk=pk, username=username).profile
    current_user_profile = Profile.objects.get(user=request.user)
    relation = Friendship(friend_1=current_user_profile, friend_2=friend)
    relation.save()



def friend_delete(request, pk, username):
    friend_for_delete = User.objects.get(pk=pk, username=username).profile
    request.user.profile.friends.remove(friend_for_delete)