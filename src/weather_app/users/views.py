from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from weather_app.auth.authentications import JWTBearerAuthentication
from weather_app.common.paginations import BasePagination
from weather_app.users.api_schema import list_users, create_user, retrieve_user
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
    list=extend_schema(**list_users), retrieve=extend_schema(**retrieve_user)
)
class UserViewSet(
    GenericViewSet,
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
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

    @extend_schema(**create_user)
    def create(self, request, *args, **kwargs):
        """Registers a new user."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response_serializer = self.get_response_serializer(instance)
        return Response(
            response_serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @extend_schema(**create_user)
    def partial_update(self, request, *args, **kwargs):
        """Registers a new user."""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        response_serializer = self.get_response_serializer(instance)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        return serializer.save()

    def perform_update(self, serializer):
        return serializer.save()
