from rest_framework import serializers

from habits.models import Habit
from habits.validators import TimeToCompleteValidator, ChoosingRelatedOrRewardHabit, CheckingForPleasantHabit, \
    NoRelatedHabitNoAward
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email'
        ]


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = [
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
        ]

        validators = [
            TimeToCompleteValidator(field='time_to_complete'),
            ChoosingRelatedOrRewardHabit(fields=['related_habit', 'award']),
            CheckingForPleasantHabit(field='related_habit'),
            NoRelatedHabitNoAward(fields=['is_pleasant_habit', 'related_habit', 'award'])
        ]
