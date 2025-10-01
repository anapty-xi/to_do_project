from django.db import models
from django.contrib.auth.models import User
import datetime


class user_info(models.Model):
    class SexChoises(models.TextChoices):
        male = 'М', ('male')
        female = 'Ж', ('female')
        default = '-', ('defailt')

    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    sex = models.CharField(max_length=1, choices=SexChoises, default=SexChoises.default)
    birthd = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to= 'imgs/profile_photos', blank=True)
    preview = models.TextField(blank=True)

    class Meta:
        ordering = ['birthd']

    def get_age(self):
        days = (datetime.datetime.now() - self.birthd).days
        return days // 365
    