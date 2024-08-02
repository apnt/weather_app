"""Configuration for the API Schema generation for authentication endpoints"""

from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)


login = {
    "request": TokenObtainPairSerializer,
    "responses": {200: TokenObtainPairSerializer},
}
refresh = {"request": TokenRefreshSerializer}
