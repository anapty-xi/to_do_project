import pytest
from . import services
from django.contrib.auth.models import User
from todos.models import Todo
from friends.models import Friendship
from django.urls import reverse

pytestmark = pytest.mark.django_db

@pytest.mark.HomepageServiceTests
def test_get_user_todos(user_test, todo_test):
    user = user_test
    todo = todo_test
    services.get_user_todos(user)
    assert user.todo.all().count() == 1

@pytest.mark.HomepageServiceTests
def test_get_friends_todos(profile_test_user, profile_test_friend, todo_friend_test):
    user = profile_test_user
    friend = profile_test_friend
    rel = Friendship(friend_1=user, friend_2=friend)
    rel.save()
    friend_todo = todo_friend_test
    queryset = services.get_friends_todos(user.user)
    assert Todo.objects.get(user=friend.user) == queryset[0]



@pytest.mark.HomepageResponseTests
def test_homepage(client, profile_test_user, todo_test):
    client.force_login(profile_test_user.user)
    todo = todo_test
    response = client.get(reverse('homepage:homepage'))
    assert response.status_code == 200 and response.context['user_todos'][0] == todo

