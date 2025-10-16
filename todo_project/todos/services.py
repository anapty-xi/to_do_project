from django.core.mail import EmailMessage
from .models import Todo, TodoReport
from django.utils.text import slugify
from unidecode import unidecode



def your_todo_has_confirmed_mail(user_email, username, todo_name):
    subject = 'Ваше Todo подтверждено!'
    body = 'Пользователь {} подтвердил ваше ToDo {}. Хорошая работа'.format(username, todo_name)
    email = EmailMessage(
        subject,
        body,
        to=[user_email],
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

def todo_confirm(pk, slug):
     todo = get_todo_by_pk_slug(pk, slug)
     todo.status = 'confirmed'
     todo.save()
     return todo







'''операции с репортами ToDo'''
def report_add(pk, slug, cd):
    todo = get_todo_by_pk_slug(pk, slug)
    todo.status = 'no_confirm'
    todo.save()

    report = TodoReport(description = cd['description'])
    report.todo = todo
    report.save()


def report_edit(pk, slug, cd):
    report = TodoReport.objects.get(todo=get_todo_by_pk_slug(pk, slug))
    report.description = cd['description']
    report.save()


