from django.db import models

from apps.users.models import User

NULLABLE = {'blank': True, 'null': True}


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    place = models.CharField(max_length=50, verbose_name='Место')
    time = models.DateTimeField(verbose_name='Время старта')
    action = models.CharField(max_length=50, verbose_name='Действие')
    pleasant_habit = models.BooleanField(default=False, verbose_name='Приятная привычка', **NULLABLE)
    related_habit = models.ForeignKey('Habit', on_delete=models.SET_NULL, verbose_name='Связанная привычка', **NULLABLE)
    period = models.IntegerField(default=1, verbose_name='Периодичность', **NULLABLE)
    reward = models.CharField(max_length=50, verbose_name='Награда', **NULLABLE)
    execution_time = models.IntegerField(verbose_name='Время на выполнение', **NULLABLE)
    is_public = models.BooleanField(default=False, verbose_name='Публичный')

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
