from django.db import models
from config import settings
from django.utils.translation import gettext_lazy as _


class Place(models.Model):
    """ Модель места """
    name = models.CharField(max_length=100, verbose_name='Место выполнения привычки')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Место'
        verbose_name_plural = 'Места'


class Action(models.Model):
    """ Модель описание действия """
    name = models.CharField(max_length=150, verbose_name='Описание действия')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Действие'
        verbose_name_plural = 'Действия'


class Award(models.Model):
    """ Модель вознаграждение """
    name = models.CharField(max_length=150, verbose_name='Вознаграждение за выполнение привычки')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Вознаграждение'
        verbose_name_plural = 'Вознаграждения'


class FrequencyStatus(models.TextChoices):
    """ Класс описание статуса периодичности """
    ONE_DAY = 'ONE_DAY'
    TWO_DAYS = 'TWO_DAYS'
    THREE_DAYS = 'THREE_DAYS'
    FOUR_DAYS = 'FOUR_DAYS'
    FIVE_DAYS = 'FIVE_DAYS'
    SIX_DAYS = 'SIX_DAYS'
    SEVEN_DAYS = 'SEVEN_DAYS'


class Habit(models.Model):
    """ Модель привычки """
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Владелец'
    )
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Место выполнения привычки'
    )
    time_habit = models.TimeField(verbose_name='Время выполнения привычки')
    action = models.ForeignKey(
        Action,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Описание действия'
    )
    is_pleasant_habit = models.BooleanField(default=False, verbose_name='Приятная привычка')
    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Полезная привычка, которая не является приятной'
    )
    frequency_habit = models.CharField(
        max_length=10,
        choices=FrequencyStatus.choices,
        default=FrequencyStatus.ONE_DAY,
        verbose_name='Периодичность'
    )
    award = models.ForeignKey(
        Award,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Вознаграждение за выполнение привычки'
    )
    time_to_complete = models.SmallIntegerField(verbose_name='Время на выполнение привычки')
    is_publicity = models.BooleanField(default=False, verbose_name='Признак публичности')

    def __str__(self):
        return f'{self.action}'

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
