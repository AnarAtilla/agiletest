import os
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from rest_framework.test import APIClient
from apps.users.models import User, Project

# Получение абсолютного пути к файлу feature
feature_file_path = os.path.join(os.path.dirname(__file__), 'features', 'user_api.feature')

# Загрузка сценариев из файла feature
scenarios(feature_file_path)

# Фикстуры
@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def project(db):
    return Project.objects.create(name='Test Project')

@pytest.fixture
def user(project, db):
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

# Определения шагов
@given('a user exists with ID "1"')
def step_given_user_exists(user):
    pass

@given('no user exists with ID "9999"')
def step_given_no_user_exists(db):
    User.objects.filter(id=9999).delete()

@when(parsers.parse('I send a GET request to "{url}"'))
def step_when_send_get_request(api_client, url):
    pytest.response = api_client.get(url)

@then(parsers.parse('I should receive a response with status code "{status_code}"'))
def step_then_should_receive_status_code(status_code):
    assert pytest.response.status_code == int(status_code), (
        f"Expected status code {status_code}, but got {pytest.response.status_code}"
    )

@then(parsers.parse('the response should contain the field "{field}"'))
def step_then_response_contains_field(field):
    response_data = pytest.response.json()
    assert field in response_data, f"Field '{field}' not found in response"

@then('the response should contain the message "No User matches the given query."')
def step_then_response_contains_error_message():
    response_data = pytest.response.json()
    assert response_data.get('detail') == "No User matches the given query.", (
        f"Expected error message 'No User matches the given query.', but got '{response_data.get('detail')}'"
    )

@then(parsers.parse('the response should contain the following user details:'))
def step_then_response_contains_user_details(pytestbdd_table):
    expected_data = {row['field']: row['value'] for row in pytestbdd_table}
    response_data = pytest.response.json()

    for key, value in expected_data.items():
        assert key in response_data, f"Field '{key}' not found in response"
        assert str(response_data[key]) == value, (
            f"Expected '{key}' to be '{value}', but got '{response_data[key]}'"
        )
