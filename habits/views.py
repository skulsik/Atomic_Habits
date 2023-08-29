from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from habits.models import Habit
from habits.paginators import HabitPaginator
from habits.permissions import IsOwner
from habits.serializers import UserSerializer, HabitSerializer
from services.celery_beat import AddTask


class UserCreateAPIView(CreateAPIView):
    """ Создание пользователя """
    serializer_class = UserSerializer


class HabitCreateAPIView(CreateAPIView):
    """ Создание привычки """
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """ Запись пользователя в поле владельца """
        habit = serializer.save()
        habit.owner = self.request.user
        habit.save()

        # Получает количество дней(период)
        every = habit.frequency_habit
        # Получает id для последующей передачи в задачу(в задаче id = имя задачи)
        name_id = habit.pk
        print(every)

        # Добавление задачи в БД
        AddTask(every=every, name=name_id)


class HabitUpdateAPIView(UpdateAPIView):
    """ Обновление привычки """
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class HabitDeleteAPIView(DestroyAPIView):
    """ Удаление привычки """
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class HabitUserListAPIView(ListAPIView):
    """ Список привычек авторизованного пользователя """
    serializer_class = HabitSerializer
    pagination_class = HabitPaginator
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        queryset = Habit.objects.filter(owner=self.request.user)
        return queryset


class HabitPublicListAPIView(ListAPIView):
    """ Список привычек открытых для публичного просмотра """
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Habit.objects.filter(is_publicity=True)
        return queryset
