from django.db import models
from django.contrib.auth.models import User
import datetime
from django.urls import reverse

class user_info(models.Model):
    class SexChoises(models.TextChoices):
        male = 'М', ('male')
        female = 'Ж', ('female')
        default = '-', ('default')   

    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    sex = models.CharField(max_length=1, choices=SexChoises, default=SexChoises.default)
    birthd = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='user_images/', blank=True, null=True)
    preview = models.TextField(blank=True)
    friends = models.ManyToManyField('self', through='friends.Friendship', symmetrical=True)

    class Meta:
        ordering = ['birthd']

    def get_age(self):
        days = (datetime.datetime.now() - self.birthd).days
        return days // 365
    



class UserProxy(User):

    class Meta:
        proxy = True

    def get_absolute_url(self):
        return reverse('account:another_profile_info', kwargs={'pk': self.pk,
                                                              'username': self.username})
    


    