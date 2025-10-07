from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class todo(models.Model):
    user_id = models.ForeignKey(User, related_name='todo', on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64)
    description = models.TextField()
    img = models.ImageField(upload_to='todo_images/', blank=True, null=True)
    publish_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['publish_date',]


    def __str__(self):
        return self.name
    

    def get_absolute_url(self):
        return reverse('todos', kwargs={'pk': self.pk,
                                     'slug': self.slug,
                                     'publish_date': self.publish_date})