import pytest
from django.contrib.auth.models import User
from PIL import Image
import datetime
from todos.models import Todo, TodoReport
from unidecode import unidecode
from django.utils.text import slugify
from account.models import Profile
from friends.models import Friendship

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
def user_test(db, user_factory):
    return user_factory('mikelee')

@pytest.fixture
def friend_test(db, user_factory, user_test):
    return user_factory('friend')





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
def todo_test(db, todo_factory, user_test):
    return todo_factory(user=user_test, name='test-todo')

@pytest.fixture
def todo_friend_test(db, todo_factory, friend_test):
    return todo_factory(user=friend_test, name='friend-todo')




@pytest.fixture
def report_factory(db):
    def report_create(
            todo: Todo,
            description: str = 'some text',
            img: Image = None
    ):
        report = TodoReport.objects.create(
            todo=todo,
            description=description,
            img=img
        )
        return report
    return report_create

@pytest.fixture
def report_test(db, todo_test, report_factory):
    return report_factory(todo=todo_test)




@pytest.fixture
def profile_factory(db):
    def profile_create(
            user: User,
            sex: str = '-',
            birthd: datetime.date = datetime.date.today(),
            photo: Image = None,
            preview: str = 'text',
    ):
        profile = Profile.objects.create(
            user=user,
            sex=sex,
            birthd=birthd,
            photo=photo,
            preview=preview,
        )
        return profile
    return profile_create

@pytest.fixture
def profile_test_user(db, profile_factory, user_test):
    return profile_factory(user=user_test)

@pytest.fixture
def profile_test_friend(db, profile_factory, friend_test):
    return profile_factory(user=friend_test)
        

def pytest_configure(config):
    config.addinivalue_line(
        "markers", "ServircesTodoTests"
    )
    config.addinivalue_line(
    "markers", "ServircesTodoReportTests"
    )
    config.addinivalue_line(
    "markers", "TodosResponseTests"
    )
    config.addinivalue_line(
    "markers", "HomepageServiceTests"
    )
    config.addinivalue_line(
    "markers", "HomepageResponseTests"
    )