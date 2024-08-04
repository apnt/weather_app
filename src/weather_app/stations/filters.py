from weather_app.common.filters import FloatRangeFilter, SingleFloatFilter


class LatitudeRangeFilter(FloatRangeFilter):
    field = "latitude"
    query_param = "lat_range"


class LatitudeLessThanFilter(SingleFloatFilter):
    gte = False
    field = "latitude"
    query_param = "lat_lte"


class LatitudeGreaterThanFilter(SingleFloatFilter):
    gte = True
    field = "latitude"
    query_param = "lat_gte"


class LongitudeRangeFilter(FloatRangeFilter):
    field = "longitude"
    query_param = "long_range"


class LongitudeLessThanFilter(SingleFloatFilter):
    gte = False
    field = "longitude"
    query_param = "long_lte"


class LongitudeGreaterThanFilter(SingleFloatFilter):
    gte = True
    field = "longitude"
    query_param = "long_gte"
