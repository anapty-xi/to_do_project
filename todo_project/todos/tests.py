import pytest
from . import services
from .models import Todo, TodoReport
from account.models import Profile
from django.urls import reverse


pytestmark = pytest.mark.django_db

@pytest.mark.ServircesTodoTests
def test_get_todo_by_slug(todo_test):
    todo_to_get = todo_test
    received_todo = services.get_todo_by_pk_slug(todo_to_get.pk, todo_to_get.slug)
    assert todo_to_get == received_todo


@pytest.mark.ServircesTodoTests
def test_todo_add(user_test):
    data = {'name': 'todo',
            'description': 'text'}      
    services.todo_add(data, user_test)
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




@pytest.mark.ServircesTodoReportTests
def test_report_add(todo_test):
    data = {'description': 'text'}
    todo = todo_test
    services.report_add(todo.pk, todo.slug, data)
    assert TodoReport.objects.count() == 1

@pytest.mark.ServircesTodoReportTests 
def test_report_edit(report_test):
    report = report_test
    todo_pk = report.todo.pk
    todo_slug = report.todo.slug
    data = {'description': 'text'}
    services.report_edit(todo_pk, todo_slug, data)
    assert TodoReport.objects.get(pk=report.pk).description == data['description']





@pytest.mark.TodosResponseTests
def test_homepage(client, django_user_model):
    username = 'test'
    password = '1111'
    user = django_user_model.objects.create_user(username=username, password=password)
    client.force_login(user)
    Profile.objects.create(user=user)
    services.todo_add({'name': 'test', 'description': 'text'}, user)
    todo = Todo.objects.get(name='test')
    response = client.get(reverse('todos:todo_info', kwargs={'pk': todo.pk,
                                                                'slug': todo.slug}))
    assert response.status_code == 200 and response.context['current_todo'] == todo and \
        response.context['is_user_todo'] == True
    
@pytest.mark.TodosResponseTests
def test_todo_add(client, django_user_model):
    username = 'test'
    password = '1111'
    user = django_user_model.objects.create_user(username=username, password=password)
    client.force_login(user)
    Profile.objects.create(user=user)
    response = client.post(reverse('todos:todo_add'),{'name': 'test', 'description': 'text'})
    assert response.status_code == 302

@pytest.mark.TodosResponseTests
def test_todo_del(client, todo_test, user_test):
    client.force_login(user_test)
    response = client.get(reverse('todos:todo_del', 
                          kwargs={'pk': todo_test.pk, 'slug': todo_test.slug}))
    assert Todo.objects.count() == 0 and response.status_code == 302

@pytest.mark.TodosResponseTests
def test_todo_edit(client, todo_test, user_test):
    client.force_login(user_test)
    response = client.post(reverse('todos:todo_edit', 
                                   kwargs={'pk': todo_test.pk, 'slug': todo_test.slug}),
                                   {'name': 'new_name', 'description': 'new_text'})
    assert response.status_code == 302

@pytest.mark.TodosResponseTests
def test_report_add(client, todo_test, user_test):
    client.force_login(user_test)
    response = client.post(reverse('todos:report_add', 
                                   kwargs={'pk': todo_test.pk, 'slug': todo_test.slug}),
                                   {'name': 'new_name', 'description': 'new_text'})
    assert response.status_code == 302

@pytest.mark.TodosResponseTests
def test_report_edit(client, user_test, todo_test, report_test):
    client.force_login(user_test)
    report = report_test
    response_get = client.get(reverse('todos:report_edit', kwargs={'pk': todo_test.pk, 'slug': todo_test.slug}))
    response_post = client.post(reverse('todos:report_edit', 
                                   kwargs={'pk': todo_test.pk, 'slug': todo_test.slug}),
                                   {'name': 'new_name', 'description': 'new_text'})
    assert response_post.status_code == 302 and response_get.status_code == 200

@pytest.mark.TodosResponseTests
def test_todo_confirm(client, todo_test, user_test):
    client.force_login(user_test)
    response = response = client.post(reverse('todos:todo_confirm', 
                                   kwargs={'pk': todo_test.pk, 'slug': todo_test.slug}))
    assert response.status_code == 302
                   
   