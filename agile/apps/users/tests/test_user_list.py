from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.users.models import User, Project

class UserListTests(APITestCase):
    def setUp(self):
        self.url = reverse('user-list')
        self.project = Project.objects.create(name='Test Project')

    def test_get_user_list(self):
        User.objects.create(
            username='user1',
            password='password123',
            email='user1@example.com',
            first_name='User',
            last_name='One',
            position='Developer',
            project=self.project
        )
        User.objects.create(
            username='user2',
            password='password123',
            email='user2@example.com',
            first_name='User',
            last_name='Two',
            position='Manager',
            project=self.project
        )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertIn('first_name', response.data[0])
        self.assertIn('last_name', response.data[0])
        self.assertIn('position', response.data[0])

    def test_get_user_list_empty(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, [])

