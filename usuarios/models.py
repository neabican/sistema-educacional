from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

class CustomUser(AbstractUser):
  email = models.EmailField(unique=True)

  def __str__(self):
    return self.email