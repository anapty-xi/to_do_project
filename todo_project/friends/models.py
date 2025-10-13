from django.db import models
import sys
sys.path.append('..')
from account.models import user_info


class Friendship(models.Model):
    friend_1 = models.ForeignKey(user_info, related_name='friend1', on_delete=models.CASCADE)
    friend_2 = models.ForeignKey(user_info, related_name='friend2', on_delete=models.CASCADE)




