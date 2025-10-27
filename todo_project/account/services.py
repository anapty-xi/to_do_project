from django.contrib.auth.models import User
from .models import Profile
from todos.models import Todo
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage



def get_user_by_pk_username(pk, username):
    return User.objects.get(pk=pk, username=username)


'''логика работы с аккаунтом'''

def user_auth(cd):
    username = cd['username']
    password = cd['password']
    return authenticate(username=username, password=password)


def user_logout(request):
    logout(request)


def user_login(request, user):
    login(request, user)

def user_register(cd):
    User.objects.create_user(username=cd['username'], email=cd['email'],
                            password=cd['password1'])
    Profile.objects.create(user=User.objects.get(username=cd['username']))

def reset_password_email(user: User, token: PasswordResetTokenGenerator):
    subject = f'Изменита пораль аккаунта {user.username}'
    link = f'http://127.0.0.1:8000/account/reset/{user.pk}/{token}/'
    body = f'Пожалуйста, воспользуйтесь ссылкой для изменения пароля {link}'
    email = EmailMessage(
        subject,
        body,
        to=[user.email],
    )
    email.send(fail_silently=False)




'''возврат атрибутов связных моделей с User'''

def get_user_todos(user):
    return Todo.objects.filter(user=user)

def get_user_friends(user):
    return user.profile.friends.all()


'''обновления профиля для моделей User И Profile'''

def user_profile_update_user_model(request, cd):
    User.objects.filter(id=request.user.id).update(username=cd['username'],
                                                email=cd['email'])
    
def user_profile_update_profile_model(request, cd):
    Profile.objects.filter(user=request.user).update(sex=cd['sex'],
                                                birthd=cd['birthd'],
                                                preview=cd['preview'],
                                                )
    user_profile = Profile.objects.get(user=request.user)
    if cd['photo']:
        user_profile.photo = cd['photo']
        user_profile.save()


    


