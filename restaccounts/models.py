from django.db import models
from django.contrib.auth.models import AbstractUser


class ExtendedUser(AbstractUser):
    name = models.CharField(max_length=250, default='Name')
    image = models.ImageField(upload_to='profile/', default='profile/none/no-img.jpg')
    tel = models.CharField(max_length=400, default=0)

    def __str__(self):
        return self.username
