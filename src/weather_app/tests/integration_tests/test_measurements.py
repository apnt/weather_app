"""Test suite for stations endpoints"""

import pytest

from weather_app.tests.config import (
    measurements_url,
    measurement_url,
    default_post_args,
)
from weather_app.tests.data import measurements as data
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
    "credentials, measurement_data, status_code",
    [
        # Permission tests - validate auth + permissions
        (empty_credentials, data.create_valid_measurement, 401),
        (invalid_credentials, data.create_valid_measurement, 401),
        (user_credentials, data.create_valid_measurement, 403),
        # Station user - can only create measurements for the associated station
        (station0_user_credentials, data.create_valid_measurement, 201),
        (station0_user_credentials, data.measurement_non_associated_station, 400),
        # Admin tests - validate payload
        # Test missing payload fields
        (admin_credentials, data.measurement_missing_station, 400),
        (admin_credentials, data.measurement_missing_date, 400),
        (admin_credentials, data.measurement_missing_temp, 400),
        (admin_credentials, data.measurement_missing_humid, 400),
        (admin_credentials, data.measurement_missing_precip, 400),
        (admin_credentials, data.measurement_missing_wd, 400),
        (admin_credentials, data.measurement_missing_ws, 400),
        # Test invalid fields
        (admin_credentials, data.measurement_invalid_station, 400),
        (admin_credentials, data.measurement_temp_too_small, 400),
        (admin_credentials, data.measurement_temp_too_large, 400),
        (admin_credentials, data.measurement_humid_too_small, 400),
        (admin_credentials, data.measurement_humid_too_large, 400),
        (admin_credentials, data.measurement_precip_too_small, 400),
        (admin_credentials, data.measurement_precip_too_large, 400),
        (admin_credentials, data.measurement_wd_too_small, 400),
        (admin_credentials, data.measurement_wd_too_large, 400),
        (admin_credentials, data.measurement_ws_too_small, 400),
        (admin_credentials, data.measurement_ws_too_large, 400),
        # Test valid data
        (admin_credentials, data.create_valid_measurement, 201),
        # Test date formats
        *[
            (admin_credentials, df_data, 201)
            for df_data in data.valid_date_formats_data
        ],
        (admin_credentials, data.invalid_date_format_no_tz, 400),
        (admin_credentials, data.invalid_date_format_no_time, 400),
    ],
)
def test_create_measurement(
    auto_login_user, credentials, measurement_data, status_code
):
    client, login_res = auto_login_user()
    auth_header = get_auth_header(access_token=login_res.get("access"))
    response = client.post(
        measurements_url, measurement_data, headers=auth_header, **default_post_args
    )
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "credentials, status_code, total_measurements",
    [
        # Test listing measurements - auth + permission + functionality
        (invalid_credentials, 401, None),
        (user_credentials, 200, data.total_measurements_count),
        (station0_user_credentials, 200, data.total_measurements_count),
        (admin_credentials, 200, data.total_measurements_count),
    ],
)
def test_list_measurements(
    auto_login_user, credentials, status_code, total_measurements
):
    client, login_res = auto_login_user()
    auth_header = get_auth_header(access_token=login_res.get("access"))
    response = client.get(measurements_url, headers=auth_header)
    assert response.status_code == status_code
    assert response.json().get("count") == total_measurements


@pytest.mark.parametrize(
    "credentials, status_code, query_params, total_measurements",
    [
        # Test measurement filtering (invalid, notation, valid)
        (admin_credentials, 200, *data.random_string_station_filtering),
        (admin_credentials, 200, *data.invalid_station_filtering),
        (admin_credentials, 200, *data.one_station_filtering),
        (admin_credentials, 200, *data.multiple_stations_filtering),
        # Test date captured filtering (invalid, notation, valid)
        (admin_credentials, 200, *data.invalid_date_range_filtering),
        (admin_credentials, 200, *data.invalid_date_range_one_date),
        (admin_credentials, 200, *data.end_date_earlier_than_start),
        (admin_credentials, 200, *data.date_range_filtering),
        (admin_credentials, 200, *data.invalid_date_lte_filtering),
        (admin_credentials, 200, *data.early_date_lte_filtering),
        (admin_credentials, 200, *data.date_lte_filtering),
        (admin_credentials, 200, *data.invalid_date_gte_filtering),
        (admin_credentials, 200, *data.late_date_gte_filtering),
        (admin_credentials, 200, *data.date_gte_filtering),
        # Test both
        (admin_credentials, 200, *data.combined_filtering),
    ],
)
def test_filter_measurements(
    auto_login_user, credentials, status_code, query_params, total_measurements
):
    client, login_res = auto_login_user()
    auth_header = get_auth_header(access_token=login_res.get("access"))
    response = client.get(measurements_url, headers=auth_header, data=query_params)
    assert response.status_code == status_code
    assert response.json().get("count") == total_measurements


@pytest.mark.parametrize(
    "credentials, status_code, uuid",
    [
        # Test retrieving - auth + permission + functionality
        (invalid_credentials, 401, None),
        (user_credentials, 200, data.selected_measurement_uuid),
        (station0_user_credentials, 200, data.selected_measurement_uuid),
        (admin_credentials, 200, data.selected_measurement_uuid),
    ],
)
def test_retrieve_measurement(auto_login_user, credentials, status_code, uuid):
    client, login_res = auto_login_user()
    auth_header = get_auth_header(access_token=login_res.get("access"))
    selected_measurement_url = measurement_url.format(
        measurement_uuid=data.selected_measurement_uuid
    )
    response = client.get(selected_measurement_url, headers=auth_header)
    assert response.status_code == status_code
    assert response.json().get("uuid") == uuid


@pytest.mark.parametrize(
    "credentials, update_measurement_data, status_code, field_to_test, value",
    [
        # Permission tests - validate auth + permissions
        (empty_credentials, data.temp_valid, 401, None, None),
        (invalid_credentials, data.temp_valid, 401, None, None),
        (user_credentials, data.temp_valid, 403, None, None),
        (station0_user_credentials, data.temp_valid, 403, None, None),
        # Admin tests - validate payload
        (admin_credentials, data.temp_too_small, 400, None, None),
        (admin_credentials, data.temp_too_large, 400, None, None),
        (admin_credentials, data.temp_valid, 200, "temperature", 50.0),
        (admin_credentials, data.humidity_too_small, 400, None, None),
        (admin_credentials, data.humidity_too_large, 400, None, None),
        (admin_credentials, data.humidity_valid, 200, "humidity", 50.0),
        (admin_credentials, data.precipitation_too_small, 400, None, None),
        (admin_credentials, data.precipitation_too_large, 400, None, None),
        (admin_credentials, data.precipitation_valid, 200, "precipitation", 5.0),
        (admin_credentials, data.wd_too_small, 400, None, None),
        (admin_credentials, data.wd_too_large, 400, None, None),
        (admin_credentials, data.wd_valid, 200, "wind_direction", 50.0),
        (admin_credentials, data.ws_too_small, 400, None, None),
        (admin_credentials, data.ws_too_large, 400, None, None),
        (admin_credentials, data.ws_valid, 200, "wind_speed", 7.0),
        # These fields cannot be changed
        (
            admin_credentials,
            data.update_station,
            200,
            ("station", "uuid"),
            data.thess_station_uuid,
        ),
        (
            admin_credentials,
            data.update_date,
            200,
            "date_captured",
            data.date_before_update,
        ),
    ],
)
def test_update_measurement(
    auto_login_user,
    credentials,
    update_measurement_data,
    status_code,
    field_to_test,
    value,
):
    client, login_res = auto_login_user()
    auth_header = get_auth_header(access_token=login_res.get("access"))
    selected_measurement_url = measurement_url.format(
        measurement_uuid=data.selected_measurement_uuid
    )
    response = client.patch(
        selected_measurement_url,
        update_measurement_data,
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
        # Test retrieving - auth + permission + functionality
        (invalid_credentials, 401),
        (user_credentials, 403),
        (station0_user_credentials, 403),
        (admin_credentials, 204),
    ],
)
def test_delete_measurement(auto_login_user, credentials, status_code):
    client, login_res = auto_login_user()
    auth_header = get_auth_header(access_token=login_res.get("access"))
    selected_measurement_url = measurement_url.format(
        measurement_uuid=data.selected_measurement_uuid
    )
    response = client.delete(selected_measurement_url, headers=auth_header)
    assert response.status_code == status_code
