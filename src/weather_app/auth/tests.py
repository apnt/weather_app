"""Test suite for auth endpoints"""

import pytest

from weather_app.common.tests import data
from weather_app.common.tests.config import auth_url, default_post_args
from weather_app.common.tests.fixtures import auto_login_user
from weather_app.common.tests.utils import get_random_string

# mark all tests as needing database access
pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "credentials, status_code",
    [
        (data.empty_credentials, 400),  # test empty credentials
        (data.missing_email_credentials, 400),  # test missing email credentials
        (data.missing_password_credentials, 400),  # test missing password credentials
        (data.invalid_credentials, 401),  # test invalid credentials
        (data.admin_credentials, 200),  # test valid credentials admin
        (data.user_credentials, 200),  # test valid credentials user
        (data.station0_user_credentials, 200),  # test valid credentials station0
        (data.station1_user_credentials, 200),  # test valid credentials station1
    ],
)
def test_login(client, credentials, status_code):
    response = client.post(auth_url, credentials, **default_post_args)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "refresh_token, status_code",
    [
        (None, 400),  # test no refresh token
        (get_random_string(), 400),  # test invalid refresh token
        (data.expired_refresh_token_admin, 400),  # test expired refresh token for admin
        (data.expired_refresh_token_user, 400),  # test expired refresh token for user
        (
            data.expired_refresh_token_station,
            400,
        ),  # test expired refresh token for station user
    ],
)
def test_refresh_invalid(client, refresh_token, status_code):
    request_body = {"refresh": refresh_token} if refresh_token is not None else {}
    response = client.patch(auth_url, request_body, **default_post_args)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "credentials, status_code",
    [
        (data.admin_credentials, 200),  # test valid credentials admin
        (data.user_credentials, 200),  # test valid credentials user
        (data.station0_user_credentials, 200),  # test valid credentials station
    ],
)
def test_refresh_valid(auto_login_user, credentials, status_code):
    client, login_res = auto_login_user()
    request_body = {"refresh": login_res.get("refresh")}
    refresh_res = client.patch(auth_url, request_body, **default_post_args)
    assert refresh_res.status_code == status_code
