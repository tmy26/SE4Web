from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=20, blank=False, unique=True)
    email = models.EmailField(blank=False)
    
    def __str__(self) -> str:
        return self.username