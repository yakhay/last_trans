
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    photo_profile = models.ImageField(upload_to='User_profile', default="User_profile/default_profile.png")
    score = models.IntegerField(default=10)
    win = models.IntegerField(default=0)
    lose = models.IntegerField(default=0)
    ranking = models.IntegerField(default=0)
    total_match = models.IntegerField(default=0)

    def __str__(self):
        return self.username