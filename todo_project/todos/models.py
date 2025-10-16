from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Todo(models.Model):
    class StatusChoises(models.TextChoices):
        no_report = 'no_report'
        no_confirm = 'no_confirm'
        confirmed = 'confirmed'
    user = models.ForeignKey(User, related_name='todo', on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64)
    description = models.TextField()
    img = models.ImageField(upload_to='todo_images/', blank=True, null=True)
    publish_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=StatusChoises, default=StatusChoises.no_report)

    class Meta:
        ordering = ['publish_date',]


    def __str__(self):
        return self.name
    

    def get_absolute_url(self):
        return reverse('todos:todo_info', kwargs={'pk': self.pk,
                                     'slug': self.slug,
                                     })
    



class TodoReport(models.Model):
    todo = models.OneToOneField(Todo, related_name='report', on_delete=models.CASCADE)
    description = models.TextField()
    img = models.ImageField(upload_to='todo_images/report', blank=True, null=True)