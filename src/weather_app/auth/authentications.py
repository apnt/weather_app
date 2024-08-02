from django.contrib.auth import get_user_model
from drf_spectacular.contrib.rest_framework_simplejwt import SimpleJWTScheme
from rest_framework import authentication
from rest_framework.request import Request
from rest_framework_simplejwt.exceptions import (
    TokenError,
    InvalidToken,
    AuthenticationFailed,
)
from rest_framework_simplejwt.settings import api_settings


class JWTBearerAuthentication(authentication.BaseAuthentication):
    """Authentication using JWT with Bearer token in the Authorization header"""

    auth_header = "Authorization"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.user_model = get_user_model()

    def authenticate(self, request: Request):
        """
        Authenticates a request using its Authorization header.
        Returns None if authentication fails.
        """
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        return self.get_user(validated_token), validated_token

    def get_header(self, request):
        """Extracts the header containing the JWT from the given request"""
        return request.META.get(api_settings.AUTH_HEADER_NAME)

    @staticmethod
    def get_raw_token(header):
        """Extracts an unvalidated JWT from the given authorization header value."""
        parts = header.split()

        if len(parts) == 0:
            # Empty AUTHORIZATION header sent
            return None

        if parts[0] not in api_settings.AUTH_HEADER_TYPES:
            # Assume the header does not contain a JSON web token
            return None

        if len(parts) != 2:
            raise AuthenticationFailed(
                "Authorization header must contain two space-delimited values",
                code="bad_authorization_header",
            )

        return parts[1]

    @staticmethod
    def get_validated_token(raw_token):
        """Validates an encoded jwt and returns a validated token wrapper object."""
        messages = []
        for AuthToken in api_settings.AUTH_TOKEN_CLASSES:
            try:
                return AuthToken(raw_token)
            except TokenError as e:
                messages.append(
                    {
                        "token_class": AuthToken.__name__,
                        "token_type": AuthToken.token_type,
                        "message": e.args[0],
                    }
                )

        raise InvalidToken(
            {
                "detail": "Given token not valid for any token type",
                "messages": messages,
            }
        )

    def get_user(self, validated_token):
        """Attempts to find and return a user using the given validated token."""
        user_model = get_user_model()
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            raise InvalidToken("Token contained no recognizable user identification")

        try:
            user = user_model.objects.get(**{api_settings.USER_ID_FIELD: user_id})
        except user_model.DoesNotExist:
            raise AuthenticationFailed("User not found", code="user_not_found")

        return user


class JWTBearerAuthenticationScheme(SimpleJWTScheme):
    """Authentication Scheme used for the API Schema generation."""

    target_class = JWTBearerAuthentication
    name = "JWT Bearer Authentication"
