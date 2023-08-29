from django_celery_beat.models import PeriodicTask, IntervalSchedule


class AddTask:
    """ Добавление задачи и интервала в БД """
    def __init__(self, every='ONE_DAY', name='no_name'):
        """
        :param every: принимает текст(количество дней), переводит в количество int
        :param name: Имя новой задачи и id рассылки
        """
        every_dict: dict = {
            'ONE_DAY': 1,
            'TWO_DAYS': 2,
            'THREE_DAYS': 3,
            'FOUR_DAYS': 4,
            'FIVE_DAYS': 5,
            'SIX_DAYS': 6,
            'SEVEN_DAYS': 7
        }

        schedule, created = IntervalSchedule.objects.get_or_create(
            every=every_dict[every],
            period=IntervalSchedule.DAYS,
        )

        # Если запись существует, обновляет ее, иначе создает
        if PeriodicTask.objects.filter(name=name):
            obj_task = PeriodicTask.objects.get(name=name)
            obj_task.interval = schedule
            obj_task.save()
        else:
            PeriodicTask.objects.create(
                interval=schedule,
                name=name,
                task='habits.tasks.mailing_telegram_task'
            )
