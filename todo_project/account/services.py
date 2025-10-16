from django.contrib.auth.models import User
from .models import Profile
import todos
from todos.models import Todo
from django.contrib.auth import authenticate, login, logout



def get_user_by_pk_username(pk, username):
    return User.objects.get(pk=pk, username=username)


'''логика работы с аккаунтом'''

def user_auth(request, cd):
    username = cd['username']
    password = cd['password']
    return authenticate(request, username=username, password=password)


def user_logout(request):
    logout(request)


def user_login(request, user):
    login(request, user)

def user_register(cd):
    User.objects.create_user(username=cd['username'], email=cd['email'],
                            password=cd['password1'])
    Profile.objects.create(user=User.objects.get(username=cd['username']))



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
    user_profile.photo = cd['photo']
    user_profile.save()


    


