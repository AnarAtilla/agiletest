import pytest
from django.contrib.auth import get_user_model
from apps.users.models import Project

@pytest.fixture
def project(db):
    return Project.objects.create(name='Test Project')

@pytest.fixture
def user(project, db):
    return get_user_model().objects.create_user(
        username='testuser',
        password='password123',
        email='testuser@example.com',
        first_name='Test',
        last_name='User',
        position='Developer',
        phone='1234567890',
        project=project
    )
