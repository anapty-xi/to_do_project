from django.db import models
from django.contrib.auth.models import User
import datetime


class profile_info(User):
    class SexChoises(models.TextChoices):
        male = 'М', ('male')
        female = 'Ж', ('female')
        default = '-', ('defailt')

    
    sex = models.CharField(max_length=1, choices=SexChoises, default=SexChoises.default)
    birthd = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to= 'imgs/profile_photos', blank=True)
    preview = models.TextField(blank=True)

    class Meta:
        ordering = ['first_name']

    def get_age(self):
        days = (datetime.datetime.now() - self.birthd).days
        return days // 365
    