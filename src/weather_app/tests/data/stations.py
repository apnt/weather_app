from weather_app.common import constants
from weather_app.tests.data.users import (
    admin_uuid,
    user_uuid,
    station0_user_uuid,
    station1_user_uuid,
    test_station_user_uuid,
)
from weather_app.tests.utils import create_missing_dict

# Station filtering test data (filter params + filter counts)
total_station_count = 10
lat_range_invalid_values = [{"lat_range": "test,test"}, 0]
lat_range_one_invalid = [{"lat_range": "test"}, 0]
lat_range_one_number = [{"lat_range": "38,"}, 0]
lat_range_valid_brackets = [{"lat_range": "[38,40]"}, 4]
lat_range_valid_parenth = [{"lat_range": "(38,40)"}, 4]
lat_range_valid = [{"lat_range": "38,40"}, 4]
long_range_invalid_values = [{"long_range": "test,test"}, 0]
long_range_one_invalid = [{"long_range": "test"}, 0]
long_range_one_number = [{"long_range": "21.5,"}, 0]
long_range_valid_brackets = [{"long_range": "[21.5,25.0]"}, 6]
long_range_valid_parenth = [{"long_range": "(21.5,25.0)"}, 6]
long_range_valid = [{"long_range": "21.5,25.0"}, 6]
lat_long_combined = [{"lat_range": "38,40", "long_range": "21.5,25.0"}, 3]

# Station retrieval
retrieve_station_name = "Athens station"

# Station test values
lat_too_small = {"latitude": constants.MIN_LATITUDE - 0.1}
lat_too_large = {"latitude": constants.MAX_LATITUDE + 0.1}
lat_valid = {"latitude": 50.0}
long_too_small = {"longitude": constants.MIN_LONGITUDE - 0.1}
long_too_large = {"longitude": constants.MAX_LONGITUDE + 0.1}
long_valid = {"longitude": 50.0}

# Station creation test data
invalid_station_uuid = "4d0d1904-c182-497e-9368-8d75e6cbda87"
athens_station_uuid = "7bcb4778-244f-4fbe-946b-565eb8cb2a2d"
thess_station_uuid = "44bebc5d-721c-4a2f-86e1-3c20dd1a2314"
create_valid_station = {
    "user": test_station_user_uuid,
    "name": "Test station",
    "latitude": 10.0,
    "longitude": 30.0,
}
create_station_empty_data = {}
station_missing_user = create_missing_dict(create_valid_station, "user")
station_missing_name = create_missing_dict(create_valid_station, "name")
station_missing_latitude = create_missing_dict(create_valid_station, "latitude")
station_missing_longitude = create_missing_dict(create_valid_station, "longitude")
station_user_already_associated = dict(create_valid_station, user=station0_user_uuid)
station_user_is_admin = dict(create_valid_station, user=admin_uuid)
station_user_is_viewer = dict(create_valid_station, user=user_uuid)
station_name_exists = dict(create_valid_station, name="Athens station")
station_too_small_latitude = dict(create_valid_station, **lat_too_small)
station_too_large_latitude = dict(create_valid_station, **lat_too_large)
station_too_small_longitude = dict(create_valid_station, **long_too_small)
station_too_large_longitude = dict(create_valid_station, **long_too_large)

# Station update test data
update_name = {"name": "Test name"}
update_user_admin = {"user": admin_uuid}
update_user_viewer = {"user": user_uuid}
update_user_station_associated = {"user": station1_user_uuid}
update_user_same_as_current = {"user": station0_user_uuid}
update_user_valid = {"user": test_station_user_uuid}
