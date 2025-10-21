import pytest
from . import services
from .models import Friendship
from account.models import UserProxy
from django.urls import reverse

class fake_request:
    def __init__(self, user):
        self.user = user


@pytest.mark.FriendsServicesTests
def test_user_friends_with_gau(profile_test_user, profile_test_friend):
    Friendship.objects.create(friend_1=profile_test_user, friend_2=profile_test_friend)
    userprixy_friends = services.user_friends_with_gau(fake_request(profile_test_user.user))
    assert userprixy_friends == [UserProxy.objects.get(username=profile_test_friend.user.username)]

@pytest.mark.FriendsServicesTests
def test_search_queryset(profile_test_user, profile_test_friend):
    Friendship.objects.create(friend_1=profile_test_user, friend_2=profile_test_friend)
    data = {'username': 'fr'}
    queryset = services.search_queryset(fake_request(profile_test_user.user), data)
    assert list(queryset) == [UserProxy.objects.get(username=profile_test_friend.user.username)]

@pytest.mark.FriendsServicesTests
def test_friend_add(profile_test_user, profile_test_friend):
    services.friend_add(fake_request(profile_test_user.user), profile_test_friend.user.pk, profile_test_friend.user.username)
    assert Friendship.objects.count() == 1

@pytest.mark.FriendsServicesTests
def test_friend_delete(profile_test_user, profile_test_friend):
    Friendship.objects.create(friend_1=profile_test_user, friend_2=profile_test_friend)
    services.friend_delete(fake_request(profile_test_user.user), profile_test_friend.user.pk, profile_test_friend.user.username)
    assert Friendship.objects.count() == 0




@pytest.mark.FriendsResponseTests
def test_friends_search(client, profile_test_user, profile_test_friend):
    client.force_login(profile_test_user.user)
    Friendship.objects.create(friend_1=profile_test_user, friend_2=profile_test_friend)
    response = client.post(reverse('friends:friends_search'), {'username': 'friend'})
    assert response.status_code == 200

@pytest.mark.FriendsResponseTests
def test_friend_add(client, profile_test_user, profile_test_friend):
    client.force_login(profile_test_user.user)
    Friendship.objects.create(friend_1=profile_test_user, friend_2=profile_test_friend)
    response = client.get(reverse('friends:friend_add', 
                                  kwargs={'pk': profile_test_friend.user.pk,
                                          'username': profile_test_friend.user.username}))
    assert response.status_code == 302

@pytest.mark.FriendsResponseTests
def test_friend_delete(client, profile_test_user, profile_test_friend):
    client.force_login(profile_test_user.user)
    Friendship.objects.create(friend_1=profile_test_user, friend_2=profile_test_friend)
    response = client.get(reverse('friends:friend_delete', 
                                  kwargs={'pk': profile_test_friend.user.pk,
                                          'username': profile_test_friend.user.username}))
    assert response.status_code == 302