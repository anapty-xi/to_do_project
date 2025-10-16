from django.test import TestCase
import pytest
from . import services
from .models import Todo
from django.contrib.auth.models import User


@pytest.fixture
def user_add():
    return User.objects.create(username='test', password='11')

@pytest.mark.django_db
def test_add_todo(user_add):
    cd = {'name': 'test', 'description': 'test too'}
    services.todo_add(cd, user_add)
    assert Todo.objects.count() == 1