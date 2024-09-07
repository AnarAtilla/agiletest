import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.users.models import User, Project

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def project(db):  # Добавлено использование фикстуры базы данных
    return Project.objects.create(name='Test Project')

@pytest.fixture
def user(project, db):  # Добавлено использование фикстуры базы данных
    return User.objects.create(
        username='testuser',
        password='password123',
        email='testuser@example.com',
        first_name='Test',
        last_name='User',
        position='Developer',
        phone='1234567890',
        project=project
    )

@pytest.mark.django_db
@pytest.mark.parametrize('user_id, expected_status, expected_message', [
    (1, status.HTTP_200_OK, None),
    (999, status.HTTP_404_NOT_FOUND, 'No User matches the given query.')
])
def test_user_detail(api_client, user, user_id, expected_status, expected_message):
    if user_id == 1:
        url = reverse('user-detail', kwargs={'pk': user.pk})
    else:
        url = reverse('user-detail', kwargs={'pk': user_id})

    response = api_client.get(url)

    assert response.status_code == expected_status
    if expected_message:
        assert response.data['detail'] == expected_message
    else:
        assert response.data['username'] == 'testuser'
        assert response.data['first_name'] == 'Test'
        assert response.data['last_name'] == 'User'
        assert response.data['email'] == 'testuser@example.com'
        assert response.data['phone'] == '1234567890'
        assert response.data['position'] == 'Developer'
        assert response.data['project'] == 'Test Project'
