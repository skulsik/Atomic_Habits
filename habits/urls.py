from django.urls import path

from habits.apps import HabitsConfig
from habits.views import UserCreateAPIView, HabitCreateAPIView, HabitUpdateAPIView, HabitDeleteAPIView, \
    HabitUserListAPIView, HabitPublicListAPIView

app_name = HabitsConfig.name

urlpatterns = [
    path('user/create/', UserCreateAPIView.as_view(), name='user_create'),

    path('habit/create/', HabitCreateAPIView.as_view(), name='habit_create'),
    path('habit/update/<int:pk>/', HabitUpdateAPIView.as_view(), name='habit_update'),
    path('habit/delete/<int:pk>/', HabitDeleteAPIView.as_view(), name='habit_delete'),
    path('habit/user/', HabitUserListAPIView.as_view(), name='user_habit_list'),
    path('habit/public/', HabitPublicListAPIView.as_view(), name='public_habit_list'),
]
