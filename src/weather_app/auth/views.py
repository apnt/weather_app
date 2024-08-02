from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from weather_app.auth.api_schema import login, refresh
from weather_app.auth.serializers import CustomTokenObtainPairSerializer


class AuthView(GenericAPIView):
    """View that implements the user authentication (login and token refresh)"""

    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        """
        if self.request.method == "PATCH":
            return TokenRefreshSerializer
        return CustomTokenObtainPairSerializer

    @extend_schema(**login)
    def post(self, request, *args, **kwargs):
        """
        User login with email and password.
        In case of success, returns a 200 response with the access and refresh tokens.
        """
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError:
            return Response(
                {"message": "Token is not valid."}, status=status.HTTP_400_BAD_REQUEST
            )
        except ValueError:  # for example if we have wrong signing and verifying keys
            return Response(
                {"message": "Error in token."}, status=status.HTTP_400_BAD_REQUEST
            )

        response = Response(serializer.validated_data, status=status.HTTP_200_OK)
        return response

    @extend_schema(**refresh)
    def patch(self, request, *args, **kwargs):
        """
        Refresh access token and return it.
        In case of success, returns a 200 response with the new access token.
        """
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError:
            return Response(
                {"message": "Token is not valid."}, status=status.HTTP_400_BAD_REQUEST
            )
        except ValueError:  # for example if we have wrong signing and verifying keys
            return Response(
                {"message": "Error in token."}, status=status.HTTP_400_BAD_REQUEST
            )

        response = Response(serializer.validated_data, status=status.HTTP_200_OK)
        return response
