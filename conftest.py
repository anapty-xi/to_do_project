import pytest
from django.contrib.auth.models import User
from PIL import Image
import datetime
from todos.models import Todo, TodoReport
from unidecode import unidecode
from django.utils.text import slugify

@pytest.fixture
def user_factory(db):
    def create_user(
            username: str,
            password: str = '11',
            first_name: str = 'foo',
            last_name: str = 'bar',
            email: str = 'foo@bar.com',
            is_staff: bool = False,
            is_superuser: bool = False,
            is_active: bool = True
    ):
        user = User.objects.create(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=is_active,
        )
        return user
    
    return create_user


@pytest.fixture
def user_mikelee(db, user_factory):
    return user_factory('mikelee')



@pytest.fixture
def todo_factory(db):
    def create_todo(
            user: User,
            name: str,
            slug: str = None,
            description: str = 'some text',
            img: Image = None,
            publish_date: datetime.date = datetime.date.today(),
            status: str = 'no_report'
    ):
        if not slug:
            slug = slugify(unidecode(name))
        todo = Todo.objects.create(
            user=user,
            name=name,
            slug=slug,
            description=description,
            img=img,
            publish_date=publish_date,
            status=status
        )
        return todo
    return create_todo

@pytest.fixture
def todo_test(db, todo_factory, user_mikelee):
    return todo_factory(user=user_mikelee, name='test-todo')