"""Test suite for users endpoints"""

import pytest

from weather_app.common.tests import data
from weather_app.common.tests.config import users_url, user_url, default_post_args
from weather_app.common.tests.fixtures import auto_login_user
from weather_app.common.tests.utils import get_auth_header

# mark all tests as needing database access
pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "new_user_data, status_code",
    [
        (data.new_user_empty_data, 400),  # test empty data
        (data.new_user_missing_email_data, 400),  # test missing email
        (data.new_user_missing_password_data, 400),  # test missing password
        (data.new_user_existing_email_data, 400),  # test existing email (invalid)
        (data.new_user_valid_data, 201),  # test valid registration
    ],
)
def test_register_user(client, new_user_data, status_code):
    response = client.post(users_url, new_user_data, **default_post_args)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "credentials, status_code, total_users",
    [
        (data.invalid_credentials, 401, None),  # test unauthenticated
        (data.user_credentials, 403, None),  # test unauthorized user (simple user)
        (
            data.station0_credentials,
            403,
            None,
        ),  # test unauthorized user (service station user)
        (data.admin_credentials, 200, 32),  # test authorized admin
    ],
)
def test_list_users(auto_login_user, credentials, status_code, total_users):
    client, login_res = auto_login_user()
    auth_header = get_auth_header(access_token=login_res.get("access"))
    response = client.get(users_url, headers=auth_header)
    assert response.status_code == status_code
    assert response.json().get("count") == total_users


@pytest.mark.parametrize(
    "credentials, status_code, email",
    [
        (data.invalid_credentials, 401, None),  # test unauthenticated
        (data.user_credentials, 403, None),  # test unauthorized user (simple user)
        (
            data.station0_credentials,
            403,
            None,
        ),  # test unauthorized user (service station user)
        (data.admin_credentials, 200, "user@test.com"),  # test authorized admin
    ],
)
def test_retrieve_user(auto_login_user, credentials, status_code, email):
    client, login_res = auto_login_user()
    auth_header = get_auth_header(access_token=login_res.get("access"))
    user1_url = user_url.format(user_uuid=data.user_uuid)
    response = client.get(user1_url, headers=auth_header)
    assert response.status_code == status_code
    assert response.json().get("email") == email
