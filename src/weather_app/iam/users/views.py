from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from weather_app.common.paginations import BasePagination
from weather_app.iam.auth.authentications import JWTBearerAuthentication
from weather_app.iam.models import User
from weather_app.iam.users.api_schema import list_users, create_user, retrieve_user
from weather_app.iam.users.permissions import UsersPermissions
from weather_app.iam.users.serializers import UserSerializer, CreateUserSerializer


@extend_schema(tags=["users"])
@extend_schema_view(
    list=extend_schema(**list_users), retrieve=extend_schema(**retrieve_user)
)
class UserViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin):
    queryset = User.objects.all()
    authentication_classes = (JWTBearerAuthentication,)
    permission_classes = (UsersPermissions,)
    pagination_class = BasePagination
    serializer_class = UserSerializer
    response_serializer_class = UserSerializer
    lookup_field = "uuid"

    # filtering and ordering
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["email"]
    ordering_fields = ["date_joined", "last_login", "email"]
    ordering = ["date_joined"]

    def get_serializer_class(self):
        return {"create": CreateUserSerializer}.get(self.action, self.serializer_class)

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

    def perform_create(self, serializer):
        return serializer.save()
