from unittest import mock

from apps.users.choices.positions import Positions  # Импортируйте Enum, если используете
from apps.users.models import User, Project
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.db.models.query import QuerySet

class UserApiTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.project = Project.objects.create(name='Test Project')
        cls.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
            position=Positions.DEVELOPER.name,  # Используйте значение из Enum, если применимо
            phone='1234567890',
            project=cls.project
        )
        cls.user.set_password('password123')
        cls.user.save()

    def test_successful_retrieval_of_user_by_id(self):
        url = reverse('user-detail', kwargs={'pk': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'username')
        self.assertContains(response, 'first_name')
        self.assertContains(response, 'last_name')
        self.assertContains(response, 'email')
        self.assertContains(response, 'phone')
        self.assertContains(response, 'position')
        self.assertContains(response, 'project')

    @mock.patch('apps.users.models.User.objects.all', return_value=User.objects.none())  # Возвращаем пустой QuerySet
    def test_empty_user_list(self, mock_all):
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, [])

    def test_create_user_with_valid_data(self):
        url = reverse('user-register')  # Используем правильный URL для регистрации
        data = {
            'username': 'newuser',
            'password': 'ComplexPass123!',  # Более сложный пароль
            're_password': 'ComplexPass123!',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'position': Positions.DEVELOPER.name,  # Используйте значение из Enum, если применимо
            'phone': '0987654321',
            'project': self.project.id
        }
        response = self.client.post(url, data, format='json')
        print(response.data)  # Вывод данных ответа для отладки
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_with_invalid_data(self):
        url = reverse('user-register')  # Используем правильный URL для регистрации
        data = {
            'username': '',  # Invalid username
            'password': 'password123',
            're_password': 'password123',
            'email': 'invalid-email',  # Invalid email
            'first_name': 'New',
            'last_name': 'User',
            'position': Positions.DEVELOPER.name,  # Используйте значение из Enum, если применимо
            'phone': '0987654321',
            'project': self.project.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        self.assertIn('email', response.data)

    def test_create_user_with_missing_required_data(self):
        url = reverse('user-register')  # Используем правильный URL для регистрации
        data = {
            'username': 'newuser',
            # Missing other required fields
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
        self.assertIn('email', response.data)
        self.assertIn('position', response.data)
