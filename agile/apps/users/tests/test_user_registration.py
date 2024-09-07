import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.users.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def existing_user():
    return User.objects.create_user(
        username='existinguser',
        password='password123',
        email='existinguser@example.com',
        first_name='Existing',
        last_name='User',
        position='Developer'
    )


@pytest.mark.django_db
def test_register_user_success(api_client):
    url = reverse('user-register')
    response = api_client.post(
        url,
        {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'position': 'PROGRAMMER',
            'password': 'testpassword123',
            're_password': 'testpassword123'
        },
        format='json'
    )
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_register_user_validation_errors(api_client, existing_user):
    url = reverse('user-register')

    # Invalid email
    data = {
        'username': 'newuser',
        'password': 'password123',
        're_password': 'password123',
        'email': 'invalidemail',
        'first_name': 'New',
        'last_name': 'User',
        'position': 'Developer'
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'email' in response.data

    # Duplicate username
    data = {
        'username': 'existinguser',
        'password': 'password123',
        're_password': 'password123',
        'email': 'newemail@example.com',
        'first_name': 'New',
        'last_name': 'User',
        'position': 'Developer'
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'username' in response.data
