"""Test suite for stations endpoints"""

import pytest

from weather_app.tests.config import stations_url, station_url, default_post_args
from weather_app.tests.data import stations as data
from weather_app.tests.data.users import (
    empty_credentials,
    invalid_credentials,
    station0_user_credentials,
    user_credentials,
    admin_credentials,
)
from weather_app.tests.fixtures import auto_login_user
from weather_app.tests.utils import get_auth_header

# mark all tests as needing database access
pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "credentials, new_station_data, status_code",
    [
        # Permission tests - validate auth + permissions
        (empty_credentials, data.create_valid_station, 401),
        (invalid_credentials, data.create_valid_station, 401),
        (station0_user_credentials, data.create_valid_station, 403),
        (user_credentials, data.create_valid_station, 403),
        # Admin tests - validate payload
        # Test missing payload fields
        (admin_credentials, data.station_missing_user, 400),
        (admin_credentials, data.station_missing_name, 400),
        (admin_credentials, data.station_missing_latitude, 400),
        (admin_credentials, data.station_missing_longitude, 400),
        # Test invalid fields
        (admin_credentials, data.station_user_already_associated, 400),
        (admin_credentials, data.station_user_is_admin, 400),
        (admin_credentials, data.station_user_is_viewer, 400),
        (admin_credentials, data.station_name_exists, 400),
        (admin_credentials, data.station_too_small_latitude, 400),
        (admin_credentials, data.station_too_large_latitude, 400),
        (admin_credentials, data.station_too_small_longitude, 400),
        (admin_credentials, data.station_too_large_longitude, 400),
        # Test valid data
        (admin_credentials, data.create_valid_station, 201),
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
        (invalid_credentials, 401, None),
        (user_credentials, 200, data.total_station_count),
        (station0_user_credentials, 200, data.total_station_count),
        (admin_credentials, 200, data.total_station_count),
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
        (admin_credentials, 200, *data.lat_range_invalid_values),
        (admin_credentials, 200, *data.lat_range_one_invalid),
        (admin_credentials, 200, *data.lat_range_one_number),
        (admin_credentials, 200, *data.lat_range_valid_brackets),
        (admin_credentials, 200, *data.lat_range_valid_parenth),
        (admin_credentials, 200, *data.lat_range_valid),
        # Test longitude filtering (invalid, notation, valid)
        (admin_credentials, 200, *data.long_range_invalid_values),
        (admin_credentials, 200, *data.long_range_one_invalid),
        (admin_credentials, 200, *data.long_range_one_number),
        (admin_credentials, 200, *data.long_range_valid_brackets),
        (admin_credentials, 200, *data.long_range_valid_parenth),
        (admin_credentials, 200, *data.long_range_valid),
        # Test both
        (admin_credentials, 200, *data.lat_long_combined),
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
        (invalid_credentials, 401, None),
        (user_credentials, 200, data.retrieve_station_name),
        (station0_user_credentials, 200, data.retrieve_station_name),
        (admin_credentials, 200, data.retrieve_station_name),
    ],
)
def test_retrieve_station(auto_login_user, credentials, status_code, name):
    client, login_res = auto_login_user()
    auth_header = get_auth_header(access_token=login_res.get("access"))
    athens_station_url = station_url.format(station_uuid=data.athens_station_uuid)
    response = client.get(athens_station_url, headers=auth_header)
    assert response.status_code == status_code
    assert response.json().get("name") == name


@pytest.mark.parametrize(
    "credentials, update_station_data, status_code, field_to_test, value",
    [
        # Permission tests - validate auth + permissions
        (empty_credentials, data.lat_valid, 401, None, None),
        (invalid_credentials, data.lat_valid, 401, None, None),
        (user_credentials, data.lat_valid, 403, None, None),
        (station0_user_credentials, data.lat_valid, 403, None, None),
        # Admin tests - validate payload
        (admin_credentials, data.lat_too_small, 400, None, None),
        (admin_credentials, data.lat_too_large, 400, None, None),
        (admin_credentials, data.lat_valid, 200, "latitude", 50.0),
        (admin_credentials, data.long_too_small, 400, None, None),
        (admin_credentials, data.long_too_large, 400, None, None),
        (admin_credentials, data.long_valid, 200, "longitude", 50.0),
        (admin_credentials, data.update_name, 200, "name", "Test name"),
        (admin_credentials, data.update_user_admin, 400, None, None),
        (admin_credentials, data.update_user_viewer, 400, None, None),
        (admin_credentials, data.update_user_station_associated, 400, None, None),
        (
            admin_credentials,
            data.update_user_same_as_current,
            200,
            ("user", "uuid"),
            data.station0_user_uuid,
        ),
        (
            admin_credentials,
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
    athens_station_url = station_url.format(station_uuid=data.athens_station_uuid)
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
