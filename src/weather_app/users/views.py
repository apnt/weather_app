from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from weather_app.auth.authentications import JWTBearerAuthentication
from weather_app.common.mixins import CustomCreateModelMixin, CustomUpdateModelMixin
from weather_app.common.paginations import BasePagination
from weather_app.users import api_schema
from weather_app.users.filters import UserTypeFilter
from weather_app.users.models import User
from weather_app.users.permissions import UsersPermissions
from weather_app.users.serializers import (
    UserSerializer,
    CreateUserSerializer,
    UpdateUserSerializer,
)


@extend_schema(tags=["users"])
@extend_schema_view(
    list=extend_schema(**api_schema.list_users),
    retrieve=extend_schema(**api_schema.retrieve_user),
    create=extend_schema(**api_schema.create_user),
    partial_update=extend_schema(**api_schema.update_user),
)
class UserViewSet(
    GenericViewSet,
    ListModelMixin,
    RetrieveModelMixin,
    CustomCreateModelMixin,
    CustomUpdateModelMixin,
):
    queryset = User.objects.all()
    authentication_classes = (JWTBearerAuthentication,)
    permission_classes = (UsersPermissions,)
    pagination_class = BasePagination
    serializer_class = UserSerializer
    response_serializer_class = UserSerializer
    lookup_field = "uuid"
    http_method_names = ["get", "post", "patch"]

    # filtering and ordering
    filter_backends = [SearchFilter, OrderingFilter, UserTypeFilter]
    search_fields = ["email"]
    ordering_fields = ["date_joined", "last_login", "email"]
    ordering = ["date_joined"]

    def get_serializer_class(self):
        return {
            "create": CreateUserSerializer,
            "partial_update": UpdateUserSerializer,
        }.get(self.action, self.serializer_class)

    def get_response_serializer(self, instance):
        return self.response_serializer_class(
            instance, context=self.get_serializer_context()
        )
