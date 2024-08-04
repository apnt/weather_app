from django.utils import timezone

from weather_app.common import constants
from weather_app.tests.data.stations import (
    athens_station_uuid,
    thess_station_uuid,
    invalid_station_uuid,
)
from weather_app.tests.utils import create_missing_dict, get_random_string

# Measurement filtering test data (filter params + filter counts)
# Station filtering
total_measurements_count = 240
random_string_station_filtering = [{"station": get_random_string}, 0]
invalid_station_filtering = [{"station": invalid_station_uuid}, 0]
one_station_filtering = [{"station": athens_station_uuid}, 24]
multiple_stations_filtering = [
    {
        "station": ",".join(
            [athens_station_uuid, thess_station_uuid, invalid_station_uuid]
        )
    },
    48,
]

# Date filtering
start_date = "03/05/2024 12:00:00"
end_date = "03/05/2024 15:00:00"
earlier_end_date = "03/05/2024 03:00:00"
no_measurements_date_early = "01/05/2024 12:00:00"
no_measurements_date_late = "04/05/2024 12:00:00"
invalid_date_range_filtering = [{"date_range": "test,test"}, 0]
invalid_date_range_one_date = [{"date_range": f"{start_date}"}, 0]
end_date_earlier_than_start = [{"date_range": f"{start_date, earlier_end_date}"}, 0]
date_range_filtering = [{"date_range": f"{start_date},{end_date}"}, 30]
invalid_date_lte_filtering = [{"date_lte": "test"}, 0]
early_date_lte_filtering = [{"date_lte": no_measurements_date_early}, 0]
date_lte_filtering = [{"date_lte": start_date}, 120]
invalid_date_gte_filtering = [{"date_gte": "test"}, 0]
late_date_gte_filtering = [{"date_gte": no_measurements_date_late}, 0]
date_gte_filtering = [{"date_gte": start_date}, 120]

# Combined filtering
combined_filtering = [{"station": athens_station_uuid, "date_gte": start_date}, 12]

# Measurements test values
temp_too_small = {"temperature": constants.MIN_TEMPERATURE - 0.1}
temp_too_large = {"temperature": constants.MAX_TEMPERATURE + 0.1}
temp_valid = {"temperature": 50.0}
humidity_too_small = {"humidity": constants.MIN_HUMIDITY - 0.1}
humidity_too_large = {"humidity": constants.MAX_HUMIDITY + 0.1}
humidity_valid = {"humidity": 50.0}
precipitation_too_small = {"precipitation": constants.MIN_PRECIPITATION - 0.1}
precipitation_too_large = {"precipitation": constants.MAX_PRECIPITATION + 0.1}
precipitation_valid = {"precipitation": 5.0}
wd_too_small = {"wind_direction": constants.MIN_WIND_DIRECTION - 0.1}
wd_too_large = {"wind_direction": constants.MAX_WIND_DIRECTION + 0.1}
wd_valid = {"wind_direction": 50.0}
ws_too_small = {"wind_speed": constants.MIN_WIND_SPEED - 0.1}
ws_too_large = {"wind_speed": constants.MAX_WIND_SPEED + 0.1}
ws_valid = {"wind_speed": 7.0}

# Measurement creation test data
current_date = timezone.now()
create_valid_measurement = {
    "station": athens_station_uuid,
    "date_captured": current_date.strftime(constants.VALID_DATETIME_INPUT_FORMATS[0]),
    "temperature": 10.0,
    "humidity": 30.0,
    "precipitation": 30.0,
    "wind_direction": 30.0,
    "wind_speed": 30.0,
}
measurement_non_associated_station = dict(
    create_valid_measurement, station=thess_station_uuid
)
measurement_empty_data = {}
measurement_missing_station = create_missing_dict(create_valid_measurement, "station")
measurement_missing_date = create_missing_dict(
    create_valid_measurement, "date_captured"
)
measurement_missing_temp = create_missing_dict(create_valid_measurement, "temperature")
measurement_missing_humid = create_missing_dict(create_valid_measurement, "humidity")
measurement_missing_precip = create_missing_dict(
    create_valid_measurement, "precipitation"
)
measurement_missing_wd = create_missing_dict(create_valid_measurement, "wind_direction")
measurement_missing_ws = create_missing_dict(create_valid_measurement, "wind_speed")
measurement_invalid_station = dict(
    create_valid_measurement, station=invalid_station_uuid
)
measurement_invalid_date = dict(create_valid_measurement, date_captured="TODO")  # TODO
measurement_temp_too_small = dict(create_valid_measurement, **temp_too_small)
measurement_temp_too_large = dict(create_valid_measurement, **temp_too_large)
measurement_humid_too_small = dict(create_valid_measurement, **humidity_too_small)
measurement_humid_too_large = dict(create_valid_measurement, **humidity_too_large)
measurement_precip_too_small = dict(create_valid_measurement, **precipitation_too_small)
measurement_precip_too_large = dict(create_valid_measurement, **precipitation_too_large)
measurement_wd_too_small = dict(create_valid_measurement, **wd_too_small)
measurement_wd_too_large = dict(create_valid_measurement, **wd_too_large)
measurement_ws_too_small = dict(create_valid_measurement, **ws_too_small)
measurement_ws_too_large = dict(create_valid_measurement, **ws_too_large)

# Date formats
valid_date_formats_data = [
    dict(
        create_valid_measurement,
        date_captured=current_date.strftime(df),
    )
    for df in constants.VALID_DATETIME_INPUT_FORMATS
]
invalid_date_format_no_tz = dict(
    create_valid_measurement,
    date_captured=current_date.strftime("%Y-%m-%dT%H:%M:%S.%f"),
)
invalid_date_format_no_time = dict(
    create_valid_measurement, date_captured=current_date.strftime("%Y-%m-%d")
)

# Retrieve measurement - this is a measurement from thess station
selected_measurement_uuid = "054fb2f9-aecf-4a8c-a3dd-890144cf0b28"

# Update measurement test data
update_valid_measurement = {
    "temperature": 20.0,
    "humidity": 50.0,
    "precipitation": 2.3,
    "wind_direction": 45.8,
    "wind_speed": 7.6,
}
update_station = {"station": athens_station_uuid}
update_date = {
    "date_captured": current_date.strftime(constants.VALID_DATETIME_INPUT_FORMATS[0])
}
date_before_update = "2024-05-03T15:00:00.433000Z"
