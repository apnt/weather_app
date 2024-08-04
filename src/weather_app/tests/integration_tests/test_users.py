"""Test suite for users endpoints"""

import pytest

from weather_app.tests.config import users_url, user_url, default_post_args
from weather_app.tests.data import users as data
from weather_app.tests.fixtures import auto_login_user
from weather_app.tests.utils import get_auth_header

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
        # test unauthenticated, unauthorized user (simple user + service station user)
        (data.invalid_credentials, 401, None),
        (data.user_credentials, 403, None),
        (data.station0_user_credentials, 403, None),
        # test authorized admin
        (data.admin_credentials, 200, 33),
    ],
)
def test_list_users(auto_login_user, credentials, status_code, total_users):
    client, login_res = auto_login_user()
    auth_header = get_auth_header(access_token=login_res.get("access"))
    response = client.get(users_url, headers=auth_header)
    assert response.status_code == status_code
    assert response.json().get("count") == total_users


@pytest.mark.parametrize(
    "credentials, status_code, query_params, total_users",
    [
        (data.admin_credentials, 200, *data.admin_users_filter),
        (data.admin_credentials, 200, *data.station_users_filter),
        (data.admin_credentials, 200, *data.viewer_users_filter),
    ],
)
def test_filter_users(
    auto_login_user, credentials, status_code, query_params, total_users
):
    client, login_res = auto_login_user()
    auth_header = get_auth_header(access_token=login_res.get("access"))
    response = client.get(users_url, headers=auth_header, data=query_params)
    assert response.status_code == status_code
    assert response.json().get("count") == total_users


@pytest.mark.parametrize(
    "credentials, status_code, email",
    [
        # test unauthenticated, unauthorized user (simple user + sevice station user)
        (data.invalid_credentials, 401, None),
        (data.user_credentials, 403, None),
        (data.station0_user_credentials, 403, None),
        # test authorized admin
        (data.admin_credentials, 200, "user@test.com"),
    ],
)
def test_retrieve_user(auto_login_user, credentials, status_code, email):
    client, login_res = auto_login_user()
    auth_header = get_auth_header(access_token=login_res.get("access"))
    test_user_url = user_url.format(user_uuid=data.user_uuid)
    response = client.get(test_user_url, headers=auth_header)
    assert response.status_code == status_code
    assert response.json().get("email") == email


@pytest.mark.parametrize(
    "credentials, update_user_data, status_code, field_to_test, value",
    [
        # Permission tests - validate auth + permissions
        (data.empty_credentials, data.updated_user_data_valid, 401, None, None),
        (data.invalid_credentials, data.updated_user_data_valid, 401, None, None),
        (data.user_credentials, data.updated_user_data_valid, 403, None, None),
        (data.station0_user_credentials, data.updated_user_data_valid, 403, None, None),
        # Admin tests - validate payload
        (data.admin_credentials, data.updated_user_data_invalid, 400, None, None),
        (
            data.admin_credentials,
            data.updated_user_data_ignored,
            200,
            "is_superuser",
            False,
        ),
        (data.admin_credentials, data.updated_user_data_valid, 200, "is_active", False),
    ],
)
def test_update_user(
    auto_login_user, credentials, update_user_data, status_code, field_to_test, value
):
    client, login_res = auto_login_user()
    auth_header = get_auth_header(access_token=login_res.get("access"))
    test_user_url = user_url.format(user_uuid=data.user_uuid)
    response = client.patch(
        test_user_url, update_user_data, headers=auth_header, **default_post_args
    )
    assert response.status_code == status_code
    if isinstance(field_to_test, tuple):
        to_validate = response.json()
        for f in field_to_test:
            to_validate = to_validate.get(f)
        assert to_validate == value
    else:
        assert response.json().get(field_to_test) == value
