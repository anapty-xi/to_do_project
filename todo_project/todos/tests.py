from django.test import TestCase
import pytest
from . import services
from .models import Todo, TodoReport


pytestmark = pytest.mark.django_db

@pytest.mark.ServircesTodoTests
def test_get_todo_by_slug(todo_test):
    todo_to_get = todo_test
    received_todo = services.get_todo_by_pk_slug(todo_to_get.pk, todo_to_get.slug)
    assert todo_to_get == received_todo


@pytest.mark.ServircesTodoTests
def test_todo_add(user_mikelee):
    data = {'name': 'todo',
            'description': 'text'}      
    services.todo_add(data, user_mikelee)
    assert Todo.objects.count() == 1


@pytest.mark.ServircesTodoTests
@pytest.mark.xfail(reason='ожидаемое падения из за несуществующего todo', strict=True)
def test_todo_del(todo_test):
    todo = todo_test
    services.todo_del(todo.pk, todo.slug)
    assert Todo.objects.get(pk=todo.pk, slug=todo.slug) 

@pytest.mark.ServircesTodoTests
def test_todo_update(todo_test):
    todo_to_update = todo_test
    data = {'name': 'todo',
            'description': 'text'} 
    services.todo_update(todo_to_update.pk, todo_to_update.slug, data)
    todo_to_update = Todo.objects.get(pk=todo_to_update.pk)
    assert todo_to_update.name == data['name'] and \
        todo_to_update.description == data['description']

@pytest.mark.ServircesTodoTests 
def test_todo_change_status(todo_test):
    todo_to_change_status = todo_test
    todo_to_change_status_pk = todo_to_change_status.pk
    status = 'no_confirm'
    changed = services.todo_change_status(todo_to_change_status_pk, todo_to_change_status.slug, status=status)
    assert todo_to_change_status_pk == changed.pk and changed.status == status






def test_report_add(todo_test):
    data = {'description': 'text'}
    todo = todo_test
    services.report_add(todo.pk, todo.slug, data)
    assert TodoReport.objects.count() == 1


def test_report_edit(report_test):
    report = report_test
    todo_pk = report.todo.pk
    todo_slug = report.todo.slug
    data = {'description': 'text'}
    services.report_edit(todo_pk, todo_slug, data)
    assert TodoReport.objects.get(pk=report.pk).description == data['description']


