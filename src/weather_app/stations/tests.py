"""Test suite for stations endpoints"""

import pytest

from weather_app.common.tests import data
from weather_app.common.tests.config import stations_url, station_url, default_post_args
from weather_app.common.tests.fixtures import auto_login_user
from weather_app.common.tests.utils import get_auth_header

# mark all tests as needing database access
pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "credentials, new_station_data, status_code",
    [
        # Permission tests - validate auth + permissions
        (data.empty_credentials, data.create_valid_station, 401),
        (data.invalid_credentials, data.create_valid_station, 401),
        (data.station0_user_credentials, data.create_valid_station, 403),
        (data.user_credentials, data.create_valid_station, 403),
        # Admin tests - validate payload
        # Test missing payload fields
        (data.admin_credentials, data.station_missing_user, 400),
        (data.admin_credentials, data.station_missing_name, 400),
        (data.admin_credentials, data.station_missing_latitude, 400),
        (data.admin_credentials, data.station_missing_longitude, 400),
        # Test invalid fields
        (data.admin_credentials, data.station_user_already_associated, 400),
        (data.admin_credentials, data.station_user_is_admin, 400),
        (data.admin_credentials, data.station_user_is_viewer, 400),
        (data.admin_credentials, data.station_name_exists, 400),
        (data.admin_credentials, data.station_too_small_latitude, 400),
        (data.admin_credentials, data.station_too_large_latitude, 400),
        (data.admin_credentials, data.station_too_small_longitude, 400),
        (data.admin_credentials, data.station_too_large_longitude, 400),
        # Test valid data
        (data.admin_credentials, data.create_valid_station, 201),
    ],
)
def test_create_station(auto_login_user, credentials, new_station_data, status_code):
    client, login_res = auto_login_user()
    auth_header = get_auth_header(access_token=login_res.get("access"))
    response = client.post(
        stations_url, new_station_data, headers=auth_header, **default_post_args
    )
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "credentials, status_code, total_stations",
    [
        # Test listing stations - auth + permission + functionality
        (data.invalid_credentials, 401, None),
        (data.user_credentials, 200, 10),
        (data.station0_user_credentials, 200, 10),
        (data.admin_credentials, 200, 10),
    ],
)
def test_list_stations(auto_login_user, credentials, status_code, total_stations):
    client, login_res = auto_login_user()
    auth_header = get_auth_header(access_token=login_res.get("access"))
    response = client.get(stations_url, headers=auth_header)
    assert response.status_code == status_code
    assert response.json().get("count") == total_stations


@pytest.mark.parametrize(
    "credentials, status_code, query_params, total_stations",
    [
        # Test latitude filtering (invalid, notation, valid)
        (data.admin_credentials, 200, {"lat_range": "test,test"}, 0),
        (data.admin_credentials, 200, {"lat_range": "test"}, 0),
        (data.admin_credentials, 200, {"lat_range": "38,"}, 0),
        (data.admin_credentials, 200, {"lat_range": "38"}, 0),
        (data.admin_credentials, 200, {"lat_range": "[38,40]"}, 4),
        (data.admin_credentials, 200, {"lat_range": "(38,40)"}, 4),
        (data.admin_credentials, 200, {"lat_range": "38,40"}, 4),
        # Test longitude filtering (invalid, notation, valid)
        (data.admin_credentials, 200, {"long_range": "test,test"}, 0),
        (data.admin_credentials, 200, {"long_range": "test"}, 0),
        (data.admin_credentials, 200, {"long_range": "21.5,"}, 0),
        (data.admin_credentials, 200, {"long_range": "21.5"}, 0),
        (data.admin_credentials, 200, {"long_range": "[21.5,25.0]"}, 6),
        (data.admin_credentials, 200, {"long_range": "(21.5,25.0)"}, 6),
        (data.admin_credentials, 200, {"long_range": "21.5,25.0"}, 6),
        # Test both
        (
            data.admin_credentials,
            200,
            {"lat_range": "38,40", "long_range": "21.5,25.0"},
            3,
        ),
    ],
)
def test_filter_stations(
    auto_login_user, credentials, status_code, query_params, total_stations
):
    client, login_res = auto_login_user()
    auth_header = get_auth_header(access_token=login_res.get("access"))
    response = client.get(stations_url, headers=auth_header, data=query_params)
    assert response.status_code == status_code
    assert response.json().get("count") == total_stations


@pytest.mark.parametrize(
    "credentials, status_code, name",
    [
        # Test retrieving - auth + permission + functionality
        (data.invalid_credentials, 401, None),
        (data.user_credentials, 200, "Athens station"),
        (data.station0_user_credentials, 200, "Athens station"),
        (data.admin_credentials, 200, "Athens station"),
    ],
)
def test_retrieve_station(auto_login_user, credentials, status_code, name):
    client, login_res = auto_login_user()
    auth_header = get_auth_header(access_token=login_res.get("access"))
    athens_station_url = station_url.format(station_uuid=data.athens_station)
    response = client.get(athens_station_url, headers=auth_header)
    assert response.status_code == status_code
    assert response.json().get("name") == name


@pytest.mark.parametrize(
    "credentials, update_station_data, status_code, field_to_test, value",
    [
        # Permission tests - validate auth + permissions
        (data.empty_credentials, data.update_latitude_valid, 401, None, None),
        (data.invalid_credentials, data.update_latitude_valid, 401, None, None),
        (data.user_credentials, data.update_latitude_valid, 403, None, None),
        (data.station0_user_credentials, data.update_latitude_valid, 403, None, None),
        # Admin tests - validate payload
        (data.admin_credentials, data.update_latitude_too_small, 400, None, None),
        (data.admin_credentials, data.update_latitude_too_large, 400, None, None),
        (data.admin_credentials, data.update_latitude_valid, 200, "latitude", 50.0),
        (data.admin_credentials, data.update_longitude_too_small, 400, None, None),
        (data.admin_credentials, data.update_longitude_too_large, 400, None, None),
        (data.admin_credentials, data.update_longitude_valid, 200, "longitude", 50.0),
        (data.admin_credentials, data.update_name, 200, "name", "Test name"),
        (data.admin_credentials, data.update_user_admin, 400, None, None),
        (data.admin_credentials, data.update_user_viewer, 400, None, None),
        (data.admin_credentials, data.update_user_station_associated, 400, None, None),
        (
            data.admin_credentials,
            data.update_user_same_as_current,
            200,
            ("user", "uuid"),
            data.station0_user_uuid,
        ),
        (
            data.admin_credentials,
            data.update_user_valid,
            200,
            ("user", "uuid"),
            data.test_station_user_uuid,
        ),
    ],
)
def test_update_station(
    auto_login_user, credentials, update_station_data, status_code, field_to_test, value
):
    client, login_res = auto_login_user()
    auth_header = get_auth_header(access_token=login_res.get("access"))
    athens_station_url = station_url.format(station_uuid=data.athens_station)
    response = client.patch(
        athens_station_url,
        update_station_data,
        headers=auth_header,
        **default_post_args
    )
    assert response.status_code == status_code
    if isinstance(field_to_test, tuple):
        to_validate = response.json()
        for f in field_to_test:
            to_validate = to_validate.get(f)
        assert to_validate == value
    else:
        assert response.json().get(field_to_test) == value


@pytest.mark.parametrize(
    "credentials, status_code",
    [
        # Test auth + permission + functionality
        (data.invalid_credentials, 401),
        (data.user_credentials, 403),
        (data.station0_user_credentials, 403),
        (data.admin_credentials, 204),
    ],
)
def test_delete_station(auto_login_user, credentials, status_code):
    client, login_res = auto_login_user()
    auth_header = get_auth_header(access_token=login_res.get("access"))
    athens_station_url = station_url.format(station_uuid=data.athens_station)
    response = client.delete(athens_station_url, headers=auth_header)
    assert response.status_code == status_code
