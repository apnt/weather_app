from weather_app.common.filters import RangeFilter


class LatitudeRangeFilter(RangeFilter):
    field = "latitude"
    query_param = "lat_range"


class LongitudeRangeFilter(RangeFilter):
    field = "longitude"
    query_param = "long_range"
