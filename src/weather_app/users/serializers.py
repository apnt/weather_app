from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from weather_app.users.models import User


class CreateUserSerializer(serializers.ModelSerializer):

    def validate_email(self, email):
        # Normalize the email address by lowercasing it
        return email.lower()

    def validate_password(self, password):
        # Hash password for saving in DB
        return make_password(password)

    class Meta:
        model = User
        fields = ("email", "password")


class UpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("is_active",)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "uuid",
            "email",
            "is_superuser",
            "is_service_station",
            "is_active",
            "date_joined",
            "last_login",
        )
