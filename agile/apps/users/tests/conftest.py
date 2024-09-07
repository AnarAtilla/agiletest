import pytest
from django.contrib.auth import get_user_model
from apps.users.models import Project

@pytest.fixture
def user(db):
    return get_user_model().objects.create_user(
        username='testuser',
        password='password123',
        email='testuser@example.com'
    )

@pytest.fixture
def project(db):
    return Project.objects.create(name='Test Project')
