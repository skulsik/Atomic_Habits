from rest_framework.serializers import ValidationError


class TimeToCompleteValidator:
    """ Проверка поля, на ввод времени, не более 120 секунд и не меньше 0 """
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        time_to_complete = int((value).get(self.field))
        if time_to_complete > 120 or time_to_complete < 0:
            raise ValidationError('Разрешено вводить, не более 120 секунд. Отрицательные значения так же запрещены.')


class ChoosingRelatedOrRewardHabit:
    """ Исключение одновременного выбора связанной привычки и указания вознаграждения """
    def __init__(self, fields):
        self.related_habit = fields[0]
        self.award = fields[1]

    def __call__(self, value):
        related_habit = value.get(self.related_habit)
        award = value.get(self.award)
        if related_habit and award:
            raise ValidationError(
                'Нельзя одновременно выбирать связанную привычку и вознаграждение, выберите что то одно.'
            )


class CheckingForPleasantHabit:
    """ Связанная привычка не может ссылаться на приятную """
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        is_pleasant_habit = value.get(self.field)
        if is_pleasant_habit:
            if is_pleasant_habit.is_pleasant_habit:
                raise ValidationError(
                    'Нельзя указывать приятную привычку, укажите полезную.'
                )


class NoRelatedHabitNoAward:
    """ Приятная привычка не может иметь связанную и вознаграждение """

    def __init__(self, fields):
        self.is_pleasant_habit = fields[0]
        self.related_habit = fields[1]
        self.award = fields[2]

    def __call__(self, value):
        is_pleasant_habit = value.get(self.is_pleasant_habit)
        related_habit = value.get(self.related_habit)
        award = value.get(self.award)
        if is_pleasant_habit:
            if related_habit or award:
                raise ValidationError(
                    'Приятная привычка не может иметь связанную и вознаграждение.'
                )
