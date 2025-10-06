from django.db import models
from django.contrib.auth.models import User
import datetime
from django.conf import settings
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

class user_info(models.Model):
    class SexChoises(models.TextChoices):
        male = 'М', ('male')
        female = 'Ж', ('female')
        default = '-', ('default')   

    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    sex = models.CharField(max_length=1, choices=SexChoises, default=SexChoises.default)
    birthd = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to=settings.MEDIA_ROOT, blank=True)



    preview = models.TextField(blank=True)

    class Meta:
        ordering = ['birthd']

    def get_age(self):
        days = (datetime.datetime.now() - self.birthd).days
        return days // 365
    