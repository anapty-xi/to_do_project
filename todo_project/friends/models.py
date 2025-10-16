from django.db import models
from account.models import Profile


class Friendship(models.Model):
    friend_1 = models.ForeignKey(Profile, related_name='friend1', on_delete=models.CASCADE)
    friend_2 = models.ForeignKey(Profile, related_name='friend2', on_delete=models.CASCADE)


 