from django.db import models
from django.contrib.auth.models import User


class friend(models.Model):
    user_id = models.ForeignKey(User, related_name='friend', on_delete=models.CASCADE)


    def __str__(self):
        return self.user_id.username
