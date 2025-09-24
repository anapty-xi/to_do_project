from django.db import models
from django.contrib.auth.models import User
import datetime


class profile_info(User):

    sex = models.TextChoices('M', 'Ж')
    birthd = models.DateField
    photo = models.ImageField(upload_to= 'imgs/profile_photos')
    preview = models.TextField

    class Meta:
        ordering = ['first_name']

    def get_age(self):
        days = (datetime.datetime.now() - self.birthd).days
        return days // 365
    