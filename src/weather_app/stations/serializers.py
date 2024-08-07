from decimal import Decimal

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from weather_app.common import constants
from weather_app.stations.models import Station
from weather_app.users.models import User


class BaseUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("uuid", "email", "is_service_station", "is_active")


class UpdateOrCreateStationSerializer(serializers.ModelSerializer):
    # Allow more decimals to be sent and round to the specified in the database.
    # Sending more than the max digits specified in each field will result in a 400 response.
    latitude = serializers.DecimalField(
        min_value=Decimal(constants.MIN_LATITUDE),
        max_value=Decimal(constants.MAX_LATITUDE),
        max_digits=20,
        decimal_places=None,
    )
    longitude = serializers.DecimalField(
        min_value=Decimal(constants.MIN_LONGITUDE),
        max_value=Decimal(constants.MAX_LONGITUDE),
        max_digits=20,
        decimal_places=None,
    )
    user = serializers.SlugRelatedField(
        many=False, slug_field="uuid", queryset=User.objects.all(), required=True
    )

    def validate_user(self, user):
        if self.instance is not None and self.instance.user == user:
            return user

        if user.is_service_station is False:
            raise ValidationError(
                "Only service station users can be associated with a station.",
                code="invalid",
            )
        if Station.objects.filter(user_id=user.id).exists():
            raise ValidationError(
                "This user is already associated with a station. "
                "A service station user can be associated with exactly one station.",
                code="invalid",
            )
        return user

    def validate_latitude(self, latitude):
        return round(latitude, 6)

    def validate_longitude(self, longitude):
        return round(longitude, 6)

    class Meta:
        model = Station
        fields = ("name", "longitude", "latitude", "user")


class StationSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer()

    class Meta:
        model = Station
        fields = (
            "uuid",
            "name",
            "latitude",
            "longitude",
            "date_created",
            "user",
        )
