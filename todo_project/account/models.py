from django.db import models
from django.contrib.auth.models import User
import datetime


class profile_info(User):
    user = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE)
    sex = models.TextChoices('M', 'Ж', blank=True) #тут ебаная хуйня
    birthd = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to= 'imgs/profile_photos', blank=True)
    preview = models.TextField(blank=True)

    class Meta:
        ordering = ['first_name']

    def get_age(self):
        days = (datetime.datetime.now() - self.birthd).days
        return days // 365
    