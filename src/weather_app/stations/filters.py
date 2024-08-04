from weather_app.common.filters import FloatRangeFilter


class LatitudeRangeFilter(FloatRangeFilter):
    field = "latitude"
    query_param = "lat_range"


class LongitudeRangeFilter(FloatRangeFilter):
    field = "longitude"
    query_param = "long_range"
