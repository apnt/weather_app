from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from weather_app.auth.authentications import JWTBearerAuthentication
from weather_app.common.mixins import CustomCreateModelMixin, CustomUpdateModelMixin
from weather_app.common.paginations import BasePagination
from weather_app.stations import api_schema
from weather_app.stations import filters
from weather_app.stations.models import Station
from weather_app.stations.permissions import StationsPermissions
from weather_app.stations.serializers import (
    StationSerializer,
    UpdateOrCreateStationSerializer,
)


@extend_schema_view(
    list=extend_schema(**api_schema.list_stations),
    retrieve=extend_schema(**api_schema.retrieve_station),
    create=extend_schema(**api_schema.create_station),
    partial_update=extend_schema(**api_schema.partial_update_station),
    destroy=extend_schema(**api_schema.destroy_station),
)
class StationViewSet(
    GenericViewSet,
    ListModelMixin,
    RetrieveModelMixin,
    CustomCreateModelMixin,
    CustomUpdateModelMixin,
):
    queryset = Station.objects.select_related("user").all()
    authentication_classes = (JWTBearerAuthentication,)
    permission_classes = (StationsPermissions,)
    pagination_class = BasePagination
    serializer_class = StationSerializer
    response_serializer_class = StationSerializer
    lookup_field = "uuid"
    http_method_names = ["get", "post", "patch", "delete"]

    # filtering and ordering
    filter_backends = [
        SearchFilter,
        OrderingFilter,
        filters.LatitudeRangeFilter,
        filters.LatitudeLessThanFilter,
        filters.LatitudeGreaterThanFilter,
        filters.LongitudeRangeFilter,
        filters.LongitudeLessThanFilter,
        filters.LongitudeGreaterThanFilter,
    ]
    search_fields = ["name"]
    ordering_fields = ["date_created", "latitude", "longitude", "name"]
    ordering = ["date_created"]

    def get_serializer_class(self):
        return {
            "create": UpdateOrCreateStationSerializer,
            "partial_update": UpdateOrCreateStationSerializer,
        }.get(self.action, self.serializer_class)

    def get_response_serializer(self, instance):
        return self.response_serializer_class(
            instance, context=self.get_serializer_context()
        )
