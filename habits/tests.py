from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from habits.models import Habit, Place, Action, Award
from users.models import User


class UserTestCase(APITestCase):
    def setUp(self) -> None:
        pass

    def test_create_user(self):
        """ Тест создания пользователя """
        data = {
            "email": 'tets@test.ru',
            "password": 'qwerty'
        }
        # Отправка запроса
        response = self.client.post(
            '/user/create/',
            data=data
        )

        # Проверка на создание
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        # Проверка на полученные данные
        self.assertEqual(
            response.json(),
            {'email': 'tets@test.ru'}
        )


class HabitsTestCase(APITestCase):
    def setUp(self):
        # Создает пользователя
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='tets@test.ru',
            password='qwerty'
        )
        self.client.force_authenticate(user=self.user)

        # Создает место
        self.place = Place.objects.create(
            name='Дома'
        )

        # Создает действие
        self.action = Action.objects.create(
            name='Отжимания от пола'
        )

        # Создает вознаграждение
        self.award = Award.objects.create(
            name='Попить воды'
        )

        # Создает привычку
        self.habit = Habit.objects.create(
            owner=self.user,
            place=self.place,
            time_habit='22:22:56',
            action=self.action,
            is_pleasant_habit=True,
            frequency_habit='SEVEN_DAYS',
            time_to_complete=100,
            is_publicity=True
        )

    def test_create_habit(self):
        """ Тест создание привычки """
        data = {
            "place": 1,
            "time_habit": "22:22:56",
            "action": 1,
            "is_pleasant_habit": "True",
            "frequency_habit": "FIVE_DAYS",
            "time_to_complete": 90,
            "is_publicity": "False"
        }
        # Отправка запроса
        response = self.client.post(
            '/habit/create/',
            data=data
        )

        # Проверка на создание
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        # Проверка на полученные данные
        self.assertEqual(
            response.json(),
            {'id': 2, 'owner': 1, 'place': 1, 'time_habit': '22:22:56', 'action': 1, 'is_pleasant_habit': True,
             'related_habit': None, 'frequency_habit': 'FIVE_DAYS', 'award': None, 'time_to_complete': 90,
             'is_publicity': False}
        )

    def test_update_habit(self):
        """ Тест обновление привычки """
        data = {
            "frequency_habit": "ONE_DAY",
            "time_to_complete": 60
        }
        # Отправка запроса
        response = self.client.patch(
            '/habit/update/4/',
            data=data
        )

        # Проверка на создание
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        # Проверка на полученные данные
        self.assertEqual(
            response.json(),
            {'id': 4, 'owner': 3, 'place': 3, 'time_habit': '22:22:56', 'action': 3, 'is_pleasant_habit': True,
             'related_habit': None, 'frequency_habit': 'ONE_DAY', 'award': None, 'time_to_complete': 60,
             'is_publicity': True}
        )

    def test_delete_habit(self):
        """ Тест удаления привычки """
        # Отправка запроса
        response = self.client.delete(
            '/habit/delete/3/'
        )

        # Проверка на удаление
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_view_list_user_habits(self):
        """ Тест получение списка привычек авторизованного пользователя """
        response = self.client.get(
            '/habit/user/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_view_list_public_habits(self):
        """ Тест получение списка привычек публичных """
        response = self.client.get(
            '/habit/public/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
