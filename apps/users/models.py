from django.contrib.auth.models import AbstractUser
from django.db import models


NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    tg_name = models.CharField(max_length=255, verbose_name='Имя')
    chat_id = models.CharField(max_length=255, default=None, verbose_name='ID', **NULLABLE)
    REQUIRED_FIELDS = ["email", "tg_name"]
