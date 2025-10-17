from django.test import TestCase
import pytest
from . import services
from .models import Todo

pytestmark = [pytest.mark.django_db]


def test_get_todo_by_slug(todo_test):
    todo_to_get = todo_test
    received_todo = services.get_todo_by_pk_slug(todo_to_get.pk, todo_to_get.slug)
    assert todo_to_get == received_todo


def test_todo_add(user_mikelee):
    data = {'name': 'todo',
            'description': 'text'}      
    services.todo_add(data, user_mikelee)
    assert Todo.objects.count() == 1

@pytest.mark.xfail(reason='ожидаемое падения из за несуществующего todo', strict=True)
def test_todo_del(todo_test):
    todo = todo_test
    services.todo_del(todo.pk, todo.slug)
    assert Todo.objects.get(pk=todo.pk, slug=todo.slug) 


def test_todo_update(todo_test):
    todo_to_update = todo_test
    data = {'name': 'todo',
            'description': 'text'} 
    services.todo_update(todo_to_update.pk, todo_to_update.slug, data)
    todo_to_update = Todo.objects.get(pk=todo_to_update.pk)
    assert todo_to_update.name == data['name'] and \
        todo_to_update.description == data['description']
    
def test_todo_confirm(todo_test):
    todo_to_confirm = todo_test
    todo_to_confirm_pk = todo_to_confirm.pk
    confirmed = services.todo_confirm(todo_to_confirm_pk, todo_to_confirm.slug)
    assert todo_to_confirm_pk == confirmed.pk and confirmed.status == 'confirmed'
