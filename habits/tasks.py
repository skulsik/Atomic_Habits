import json
import os
from datetime import *

import requests
from django.core.mail import send_mail

from config import settings
from config.celery import app
from habits.models import Habit


@app.task(bind=True)
def mailing_telegram_task(self, **kwargs):
    print('---------- working task start ---------------')

    # Получает объект (c info) планировщика, который запускает task
    periodic_task_info = self.request.properties

    # Получает объект рассылки, которая создала планировщика
    id = int(periodic_task_info['periodic_task_name'])
    object_habit = Habit.objects.get(id=id)

    # Получает время начало рассылки и время сейчас
    time_begin = object_habit.time_habit
    time_now = datetime.now().time()

    # Если пришло время запускать задачу
    if time_now > time_begin:
        # Телеграм бот
        # Токен
        token = os.getenv('HABIT_BOT_API')
        # Метод API
        method = 'sendMessage'
        # добавить мой ид в модель, прочитать ид и вставить
        telegram_id = object_habit.owner.telegram_id
        # Текст для отправки сообщения
        award = ''
        if object_habit.award:
            award = f'Вознаграждение: {object_habit.award}.'
        text_bot = f'Выполни: {object_habit.action}.\nМесто: {object_habit.place}.\nВремя на выполнение: {object_habit.time_to_complete} секунд.{award}'

        response = requests.post(
            url=f'https://api.telegram.org/bot{token}/{method}',
            data={'chat_id': telegram_id, 'text': text_bot}
        ).json()
