from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User
from django.contrib.auth.hashers import make_password

class UserTests(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password=make_password("testpassword123")  # Создаем пользователя с зашифрованным паролем
        )
        self.user2 = User.objects.create(
            first_name="Jane",
            last_name="Doe",
            email="jane.doe@example.com",
            password=make_password("testpassword456")
        )
        self.list_create_url = reverse('user-list-create')
        self.detail_url = reverse('user-detail', kwargs={'id': self.user1.id})

    def test_get_users(self):
        # Тестирование получения списка пользователей
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_user(self):
        # Тестирование создания нового пользователя
        data = {
            'first_name': 'Alice',
            'last_name': 'Smith',
            'email': 'alice.smith@example.com',
            'password': 'securepassword'
        }
        response = self.client.post(self.list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)

    def test_create_user_invalid_data(self):
        # Тестирование создания пользователя с некорректными данными
        data = {
            'first_name': '',
            'last_name': 'Smith',
            'email': 'alice.smith@example.com',
            'password': 'securepassword'
        }
        response = self.client.post(self.list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_user_detail(self):
        # Тестирование получения данных о конкретном пользователе
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user1.email)

    def test_update_user(self):
        # Тестирование обновления данных пользователя
        data = {'first_name': 'UpdatedName'}
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.first_name, 'UpdatedName')

    def test_delete_user(self):
        # Тестирование удаления пользователя
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 1)
