import pytest

from weather_app.common.tests.config import auth_url, default_post_args


@pytest.fixture
def auto_login_user(client, credentials):
    def auto_login():
        response = client.post(auth_url, credentials, **default_post_args)
        return client, response.json()

    return auto_login
