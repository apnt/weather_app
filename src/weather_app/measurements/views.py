from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.filters import OrderingFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet

from weather_app.auth.authentications import JWTBearerAuthentication
from weather_app.common.mixins import CustomCreateModelMixin, CustomUpdateModelMixin
from weather_app.common.paginations import BasePagination
from weather_app.measurements import api_schema
from weather_app.measurements import filters
from weather_app.measurements.models import Measurement
from weather_app.measurements.permissions import MeasurementsPermissions
from weather_app.measurements.serializers import (
    MeasurementSerializer,
    CreateMeasurementSerializer,
    UpdateMeasurementSerializer,
)


@extend_schema_view(
    list=extend_schema(**api_schema.list_measurements),
    retrieve=extend_schema(**api_schema.retrieve_measurement),
    create=extend_schema(**api_schema.create_measurement),
    partial_update=extend_schema(**api_schema.partial_update_measurement),
    destroy=extend_schema(**api_schema.destroy_measurement),
)
class MeasurementViewSet(
    GenericViewSet,
    ListModelMixin,
    RetrieveModelMixin,
    CustomCreateModelMixin,
    CustomUpdateModelMixin,
    DestroyModelMixin,
):
    queryset = Measurement.objects.select_related("station").all()
    authentication_classes = (JWTBearerAuthentication,)
    permission_classes = (MeasurementsPermissions,)
    pagination_class = BasePagination
    serializer_class = MeasurementSerializer
    response_serializer_class = MeasurementSerializer
    lookup_field = "uuid"
    http_method_names = ["get", "post", "patch", "delete"]

    # filtering and ordering
    filter_backends = [
        OrderingFilter,
        filters.StationFilter,
        filters.DateCapturedRangeFilter,
        filters.DateCapturedBeforeFilter,
        filters.DateCapturedAfterFilter,
        filters.TemperatureRangeFilter,
        filters.TemperatureLessThanFilter,
        filters.TemperatureGreaterThanFilter,
        filters.HumidityRangeFilter,
        filters.HumidityLessThanFilter,
        filters.HumidityGreaterThanFilter,
        filters.PrecipitationRangeFilter,
        filters.PrecipitationLessThanFilter,
        filters.PrecipitationGreaterThanFilter,
        filters.WindDirectionRangeFilter,
        filters.WindDirectionLessThanFilter,
        filters.WindDirectionGreaterThanFilter,
        filters.WindSpeedRangeFilter,
        filters.WindSpeedLessThanFilter,
        filters.WindSpeedGreaterThanFilter,
    ]
    ordering_fields = [
        "date_captured",
        "date_registered",
        "temperature",
        "humidity",
        "precipitation",
        "wind_direction",
        "wind_speed",
    ]
    ordering = ["date_captured"]

    def get_serializer_class(self):
        return {
            "create": CreateMeasurementSerializer,
            "partial_update": UpdateMeasurementSerializer,
        }.get(self.action, self.serializer_class)

    def get_response_serializer(self, instance):
        return self.response_serializer_class(
            instance, context=self.get_serializer_context()
        )
