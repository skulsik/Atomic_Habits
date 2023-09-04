from django.contrib import admin

from habits.models import *


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'owner',
        'place',
        'time_habit',
        'action',
        'is_pleasant_habit',
        'related_habit',
        'frequency_habit',
        'award',
        'time_to_complete',
        'is_publicity'
    )
