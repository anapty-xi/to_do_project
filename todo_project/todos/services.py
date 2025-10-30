from django.core.mail import EmailMessage
from .models import Todo, TodoReport
from django.utils.text import slugify
from unidecode import unidecode
from django.contrib.auth.models import User


def get_user_friends(user):
    return user.profile.friends.all()




'''отправка электронных писем'''

def your_todo_has_confirmed_mail(user_email, username, todo_name):
    subject = 'Ваше Todo подтверждено!'
    body = f'Пользователь {username} подтвердил ваше ToDo {todo_name}. Хорошая работа'
    email = EmailMessage(
        subject,
        body,
        to=[user_email],
    )
    email.send(fail_silently=False)


def friends_reminder_mail(user, friends):
    subject = 'Время распланировать свой день'
    body = f'Пользователь {user.username} заметил отсутствие ваших ToDO! Есть минутка записать задачи?'
    try:
        friends = [friend.user.email for friend in friends]
    except: pass
    email = EmailMessage(
        subject,
        body,
        to=friends,
    )
    email.send(fail_silently=False)

        



'''операции с ToDo'''

def get_todo_by_pk_slug(pk, slug):
    return Todo.objects.get(pk=pk, slug=slug)


def todo_add(cd, user):
     Todo.objects.create(user=user,
                         name=cd['name'],
                         slug=slugify(unidecode(cd['name'])),
                         description=cd['description'])


def todo_del(pk, slug):
    todo = get_todo_by_pk_slug(pk, slug)
    todo.delete()


def todo_update(pk, slug, cd):
    todo = get_todo_by_pk_slug(pk, slug)
    todo.name = cd['name']
    todo.description = cd['description']
    todo.save()

def todo_change_status(pk, slug, status):
     todo = get_todo_by_pk_slug(pk, slug)
     todo.status = status
     todo.save()
     return todo







'''операции с TodoReport'''
def report_add(pk, slug, cd):
    todo = get_todo_by_pk_slug(pk, slug)
    report = TodoReport(description = cd['description'])
    report.todo = todo
    report.save()
    


def report_edit(pk, slug, cd):
    report = TodoReport.objects.get(todo=get_todo_by_pk_slug(pk, slug))
    report.description = cd['description']
    report.save()


