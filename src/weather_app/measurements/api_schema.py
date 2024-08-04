"""Configuration for the API Schema generation for measurements endpoints"""

from drf_spectacular.utils import OpenApiParameter

from weather_app.common.constants import VALID_DATE_INPUT_FORMATS
from weather_app.measurements.serializers import MeasurementSerializer

retrieve_measurement = {"description": "Fetches the measurement with the given uuid."}
list_measurements = {
    "description": "Fetches all measurements (paginated).",
    "parameters": [
        OpenApiParameter(
            name="order_by",
            description="Which field to use when ordering the results. By default ascending order is used. "
            "For descending order use a dash before the field e.g. '-date_captured",
            type=str,
            enum=[
                "date_captured",
                "date_registered",
                "temperature",
                "humidity",
                "precipitation",
                "wind_direction",
                "wind_speed",
            ],
        ),
        OpenApiParameter(
            name="date_range",
            description="A range (start-end dates) for filtering by date and time. The two dates "
            f"must be comma-separated. Valid date formats: {VALID_DATE_INPUT_FORMATS}",
        ),
        OpenApiParameter(
            name="date_lte",
            description=f"Filter and fetch only measurements before the given date. "
            f"Valid date formats: {VALID_DATE_INPUT_FORMATS}",
        ),
        OpenApiParameter(
            name="date_gte",
            description=f"Filter and fetch only measurements after the given date. "
            f"Valid date formats: {VALID_DATE_INPUT_FORMATS}",
        ),
        OpenApiParameter(
            name="temp_range",
            description="A range (min-max) for filtering by temperature. "
            "The two float values must be comma-separated.",
        ),
        OpenApiParameter(
            name="temp_lte",
            description="Temperature filtering less than or equal to the given float value.",
        ),
        OpenApiParameter(
            name="temp_gte",
            description="Temperature filtering greater than or equal to the given float value.",
        ),
        OpenApiParameter(
            name="humid_range",
            description="A range (min-max) for filtering by humidity. The two float values must be comma-separated.",
        ),
        OpenApiParameter(
            name="humid_lte",
            description="Humidity filtering less than or equal to the given float value.",
        ),
        OpenApiParameter(
            name="humid_gte",
            description="Humidity filtering greater than or equal to the given float value.",
        ),
        OpenApiParameter(
            name="precip_range",
            description="A range (min-max) for filtering by precipitation. "
            "The two float values must be comma-separated.",
        ),
        OpenApiParameter(
            name="precip_lte",
            description="Precipitation filtering less than or equal to the given float value.",
        ),
        OpenApiParameter(
            name="precip_gte",
            description="Precipitation filtering greater than or equal to the given float value.",
        ),
        OpenApiParameter(
            name="wd_range",
            description="A range (min-max) for filtering by wind direction. "
            "The two float values must be comma-separated.",
        ),
        OpenApiParameter(
            name="wd_lte",
            description="Wind direction filtering less than or equal to the given float value.",
        ),
        OpenApiParameter(
            name="wd_gte",
            description="Wind direction filtering greater than or equal to the given float value.",
        ),
        OpenApiParameter(
            name="ws_range",
            description="A range (min-max) for filtering by wind speed. "
            "The two float values must be comma-separated.",
        ),
        OpenApiParameter(
            name="ws_lte",
            description="Wind speed filtering less than or equal to the given float value.",
        ),
        OpenApiParameter(
            name="ws_gte",
            description="Wind speed filtering greater than or equal to the given float value.",
        ),
        OpenApiParameter(
            name="station",
            description="Filter by one or more stations by their uuid. "
            "In order to filter with multiple stations, their uuids must be comma-separated.",
        ),
    ],
}
create_measurement = {"responses": {201: MeasurementSerializer}}
partial_update_measurement = {"responses": {200: MeasurementSerializer}}
destroy_measurement = {}
