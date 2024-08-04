"""Configuration for the API Schema generation for stations endpoints"""

from drf_spectacular.utils import OpenApiParameter

from weather_app.stations.serializers import StationSerializer

list_stations = {
    "description": "Fetches all stations (paginated).",
    "parameters": [
        OpenApiParameter(
            name="order_by",
            description="Which field to use when ordering the results. By default ascending order is used. "
            "For descending order use a dash before the field e.g. '-name'",
            type=str,
            enum=["date_created", "latitude", "longitude", "name"],
        ),
        OpenApiParameter(
            name="search",
            description="A search term that is used to find matches in the name field.",
            type=str,
        ),
        OpenApiParameter(
            name="lat_range",
            description="A range (min-max) for filtering by latitude. The two float values must be comma-separated.",
        ),
        OpenApiParameter(
            name="lat_lte",
            description="Latitude filtering less than or equal to the given float value.",
        ),
        OpenApiParameter(
            name="lat_gte",
            description="Latitude filtering greater than or equal to the given float value.",
        ),
        OpenApiParameter(
            name="long_range",
            description="A range (min-max) for filtering by longitude. The two float values must be comma-separated.",
        ),
        OpenApiParameter(
            name="long_lte",
            description="Longitude filtering less than or equal to the given float value.",
        ),
        OpenApiParameter(
            name="long_gte",
            description="Longitude filtering greater than or equal to the given float value.",
        ),
    ],
}
retrieve_station = {"description": "Fetches the station with the given uuid."}
create_station = {"responses": {201: StationSerializer}}
partial_update_station = {"responses": {200: StationSerializer}}
