from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.users.models import User
from apps.habits.models import Habit
from apps.habits.serializers import HabitSerializer


class HabitCreateAPIViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('habits:habit-create')
        self.user = User.objects.create(username='testuser')
        self.client.force_authenticate(user=self.user)

    def test_create_habit(self):
        data = {
            'user': self.user.id,
            'place': 'дом',
            'time': '2023-08-21T12:00:00Z',
            'action': 'попрыгать',
            'pleasant_habit': True,
            'period': 7,
            'reward': 'шото',
            'execution_time': 30,
            'is_public': True
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 1)
        self.assertEqual(Habit.objects.get().user, self.user)


class HabitRetrieveUpdateDestroyViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.habit = Habit.objects.create(
            user=self.user,
            place='дом',
            time='2023-08-21T12:00:00Z',
            action='Exercise',
            pleasant_habit=True,
            period=7,
            execution_time=30,
            is_public=True
        )
        self.url = reverse('habits:habit-retrieve-update-destroy', kwargs={'pk': self.habit.pk})
        self.client.force_authenticate(user=self.user)

    def test_retrieve_habit(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, HabitSerializer(self.habit).data)

    def test_update_habit(self):
        data = {
            'user': self.user.pk,
            'place': 'дома',
            'time': '2023-08-21T12:00:00Z',
            'action': 'попить',
            'pleasant_habit': False,
            'period': 14,
            'execution_time': 60,
            'is_public': False
        }
        response = self.client.put(self.url, data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.place, 'дома')
        self.assertEqual(self.habit.action, 'попить')
        self.assertFalse(self.habit.pleasant_habit)
        self.assertEqual(self.habit.period, 14)
        self.assertEqual(self.habit.execution_time, 60)
        self.assertFalse(self.habit.is_public)

    def test_delete_habit(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)


class HabitPublicListAPIViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('habits:public-list')
        self.user = User.objects.create(username='testuser')
        self.habit1 = Habit.objects.create(
            user=self.user,
            place='Дома',
            time='2023-08-21T12:00:00Z',
            action='анжумання',
            pleasant_habit=True,
            period=7,
            reward='нету',
            execution_time=30,
            is_public=True
        )
        self.habit2 = Habit.objects.create(
            user=self.user,
            place='улица',
            time='2022-01-02T12:00:00Z',
            action='бегать',
            pleasant_habit=False,
            period=14,
            reward='да)',
            execution_time=60,
            is_public=False
        )
        self.client.force_authenticate(user=self.user)

    def test_get_public_habits(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

