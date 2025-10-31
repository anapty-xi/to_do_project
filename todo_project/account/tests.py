import pytest
from . import services
from django.contrib.auth.models import User
from .models import Profile
from friends.models import Friendship
import datetime
from django.urls import reverse
from io import BytesIO
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class fake_request:
    def __init__(self, user):
        self.user = user

'''получение user'''

@pytest.mark.AccountServicesTests
def test_get_user_by_pk_username(user_test):
    user = user_test
    found_user = services.get_user_by_pk_username(user.pk, user.username)
    assert user == found_user

@pytest.mark.AccountServicesTests
def test_get_user_by_email(user_test):
    user = user_test
    found_user = services.get_user_by_email(user.email)
    assert user == found_user

@pytest.mark.AccountServicesTests
def test_get_user_by_pk(user_test):
    user = user_test
    found_user = services.get_user_by_pk(user.pk)
    assert user == found_user

'''логика работы с аккаунтом'''

@pytest.mark.AccountServicesTests
def test_user_auth(user_test: User):
    data = {'username': user_test.username, 'password': '11'}
    user = services.user_auth(data)
    assert user

@pytest.mark.django_db
@pytest.mark.AccountServicesTests
def test_user_register():
    data = {'username': 'test', 'email': 'test@test.ru', 'password1': '11'}
    services.user_register(data)
    assert User.objects.get(username=data['username']) and Profile.objects.get(user__username=data['username'])

@pytest.mark.AccountServicesTests
def test_make_token(user_test: User):
    token = services.make_token(user_test)
    assert PasswordResetTokenGenerator().check_token(user_test, token)

'''возврат атрибутов связных моделей с User'''

@pytest.mark.AccountServicesTests
def test_get_user_todos(user_test, todo_test):
    user = user_test
    todo = todo_test
    queryset = services.get_user_todos(user)
    assert list(queryset) == [todo]

@pytest.mark.AccountServicesTests
def test_get_user_friends(profile_test_user, profile_test_friend):
    Friendship.objects.create(friend_1=profile_test_user, friend_2=profile_test_friend)
    queryset = services.get_user_friends(profile_test_user.user)
    assert list(queryset) == [profile_test_friend]

'''обновления профиля для моделей User И Profile'''

@pytest.mark.AccountServicesTests
def test_user_profile_update_user_model(user_test):
    user_pk = user_test.pk
    data = {'username': 'us', 'email': 'new@email.com'}
    services.user_profile_update_user_model(fake_request(user_test), data)
    updated_user = User.objects.get(pk=user_pk)
    assert updated_user.username == data['username'] and updated_user.email == data['email']

@pytest.mark.AccountServicesTests
def test_user_profile_update_profile_model(profile_test_user):
    user_pk = profile_test_user.pk
    data = {'sex': 'М', 'birthd': datetime.datetime.now().date(), 'preview': 'test', 'photo': None}
    services.user_profile_update_profile_model(fake_request(profile_test_user.user), data)
    updated_profile = Profile.objects.get(pk=user_pk)
    assert updated_profile.sex == data['sex'] and updated_profile.birthd == data['birthd'] \
        and updated_profile.preview == data['preview']
    





@pytest.mark.AccountResponseTests
def test_login_view(client, user_test):
    data = {'username': user_test.username, 'password': '11'}
    response = client.post(reverse('account:login'), data)
    assert response.status_code == 302

@pytest.mark.AccountResponseTests
@pytest.mark.django_db
def test_register_view(client):
    data = {'username': 'test', 'email': 'test@test.ru', 'password1': '11', 'password2': '11'}
    response = client.post(reverse('account:register'), data)
    assert response.status_code == 302

@pytest.mark.AccountResponseTests
def test_profile_info(client, profile_test_user):
    client.force_login(profile_test_user.user)
    response = client.get(reverse('account:profile_info'))
    assert response.status_code == 200

@pytest.mark.AccountResponseTests
def test_profile_info_edit(client, profile_test_user):
    with open(r'C:\pch_projects\to_do_project\todo_project\static\user_placeholder.png', 'rb') as photo:
        photo_bites = photo.read()
        photo_io = BytesIO(photo_bites)
        photo_io.name = 'user_placeholder.png'
        data = {'username': 'us', 'email': 'email@test.ru', 'sex': 'male', 
                'birthd': datetime.datetime.now().date(), 'preview': 'test', 
                'photo': photo_io}
        client.force_login(profile_test_user.user)
        response = client.post(reverse('account:profile_info_edit'), data)
        assert response.status_code == 302


@pytest.mark.AccountResponseTests
def test_another_profile_info(client, profile_test_user, profile_test_friend):
    client.force_login(profile_test_user.user)
    user = profile_test_friend
    response = client.get(reverse('account:another_profile_info', kwargs={'pk': user.user.pk,
                                                                          'username': user.user.username}))
    assert response.status_code == 200    

@pytest.mark.AccountResponseTests
def test_reset_password_email(client, user_test):
    client.force_login(user_test)
    response = client.get(reverse('account:reset_password_email'))
    assert response.status_code == 200
                                        
@pytest.mark.AccountResponseTests
def test_reset_password_proccess_get(client, user_test):
    client.force_login(user_test)
    token = services.make_token(user_test)
    response = client.get(reverse('account:reset_password_proccess', kwargs={'pk': user_test.pk,
                                                                          'token': token}))
    template = [template.name for template in response.templates][0]
    assert response.status_code == 200 and template == 'account/reset_password_get.html'

@pytest.mark.AccountResponseTests
def test_reset_password_proccess_post(client, user_test):
    client.force_login(user_test)
    token = services.make_token(user_test)
    data = {'password1': '11', 'password2': '11'}
    response = client.post(reverse('account:reset_password_proccess', kwargs={'pk': user_test.pk,
                                                                          'token': token}), data)
    template = [template.name for template in response.templates][0]
    assert response.status_code == 200 and template == 'account/reset_password_success.html'

@pytest.mark.AccountResponseTests
def test_reset_password_proccess_token_fail_get(client, user_test):
    client.force_login(user_test)
    token = services.make_token(user_test)
    data = {'password1': '11', 'password2': '11'}
    client.post(reverse('account:reset_password_proccess', kwargs={'pk': user_test.pk,
                                                                          'token': token}), data)
    response = client.get(reverse('account:reset_password_proccess', kwargs={'pk': user_test.pk,
                                                                          'token': token}))
    template = [template.name for template in response.templates][0]
    assert response.status_code == 200 and template == 'account/reset_password_token_fail.html'

@pytest.mark.AccountResponseTests
def test_reset_password_proccess_token_fail_post(client, user_test):
    client.force_login(user_test)
    token = services.make_token(user_test)
    data = {'password1': '11', 'password2': '11'}
    client.post(reverse('account:reset_password_proccess', kwargs={'pk': user_test.pk,
                                                                          'token': token}), data)
    response = client.post(reverse('account:reset_password_proccess', kwargs={'pk': user_test.pk,
                                                                          'token': token}), data)
    template = [template.name for template in response.templates][0]
    assert response.status_code == 200 and template == 'account/reset_password_token_fail.html'


@pytest.mark.AccountResponseTests
def test_forgot_password_post(client, user_test):
    client.force_login(user_test)
    data = {'email': user_test.email}
    response = client.post(reverse('account:forgot_password'), data)
    template = [template.name for template in response.templates][0]
    assert response.status_code == 200 and template == 'account/reset_email_sent.html'

@pytest.mark.AccountResponseTests
def test_forgot_password_get(client, user_test):
    client.force_login(user_test)
    data = {'email': user_test.email}
    response = client.get(reverse('account:forgot_password'))
    template = [template.name for template in response.templates][0]
    assert response.status_code == 200 and template == 'account/forgot_password.html'