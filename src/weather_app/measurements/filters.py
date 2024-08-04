import logging

from rest_framework.filters import BaseFilterBackend

from weather_app.common.filters import (
    FloatRangeFilter,
    SingleFloatFilter,
    DateRangeFilter,
    SingleDateFilter,
)
from weather_app.common.utils import is_valid_uuid
from weather_app.stations.models import Station

logger = logging.getLogger(__name__)


class StationFilter(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        queried_stations = request.query_params.get("station")
        if queried_stations is not None:
            cleared_stations = [
                station.strip() for station in queried_stations.split(",")
            ]
            valid_stations = [
                station for station in cleared_stations if is_valid_uuid(station)
            ]
            stations = Station.objects.filter(uuid__in=valid_stations)
            if len(stations) > 0:
                queryset = queryset.filter(station__in=stations)
            else:
                queryset = queryset.none()
        return queryset


class TemperatureRangeFilter(FloatRangeFilter):
    field = "temperature"
    query_param = "temp_range"


class TemperatureLessThanFilter(SingleFloatFilter):
    gte = False
    field = "temperature"
    query_param = "temp_lte"


class TemperatureGreaterThanFilter(SingleFloatFilter):
    gte = True
    field = "temperature"
    query_param = "temp_gte"


class HumidityRangeFilter(FloatRangeFilter):
    field = "humidity"
    query_param = "humid_range"


class HumidityLessThanFilter(SingleFloatFilter):
    gte = False
    field = "humidity"
    query_param = "humid_lte"


class HumidityGreaterThanFilter(SingleFloatFilter):
    gte = True
    field = "humidity"
    query_param = "humid_gte"


class PrecipitationRangeFilter(FloatRangeFilter):
    field = "precipitation"
    query_param = "precip_range"


class PrecipitationLessThanFilter(SingleFloatFilter):
    gte = False
    field = "precipitation"
    query_param = "precip_lte"


class PrecipitationGreaterThanFilter(SingleFloatFilter):
    gte = True
    field = "precipitation"
    query_param = "precip_gte"


class WindDirectionRangeFilter(FloatRangeFilter):
    field = "wind_direction"
    query_param = "wd_range"


class WindDirectionLessThanFilter(SingleFloatFilter):
    gte = False
    field = "wind_direction"
    query_param = "wd_lte"


class WindDirectionGreaterThanFilter(SingleFloatFilter):
    gte = True
    field = "wind_direction"
    query_param = "wd_gte"


class WindSpeedRangeFilter(FloatRangeFilter):
    field = "wind_speed"
    query_param = "ws_range"


class WindSpeedLessThanFilter(SingleFloatFilter):
    gte = False
    field = "wind_speed"
    query_param = "ws_lte"


class WindSpeedGreaterThanFilter(SingleFloatFilter):
    gte = True
    field = "wind_speed"
    query_param = "ws_gte"


class DateCapturedRangeFilter(DateRangeFilter):
    field = "date_captured"
    query_param = "date_range"


class DateCapturedBeforeFilter(SingleDateFilter):
    gte = False
    field = "date_captured"
    query_param = "date_lte"


class DateCapturedAfterFilter(SingleDateFilter):
    gte = True
    field = "date_captured"
    query_param = "date_gte"
