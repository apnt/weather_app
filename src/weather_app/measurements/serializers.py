from decimal import Decimal

from rest_framework import serializers

from weather_app.common import constants
from weather_app.measurements.models import Measurement
from weather_app.stations.models import Station


class BaseStationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Station
        fields = ("uuid", "name")


class UpdateMeasurementSerializer(serializers.ModelSerializer):
    # Allow more decimals to be sent and round to the specified in the database.
    # Sending more than the max digits specified in each field will result in a 400 response.
    temperature = serializers.DecimalField(
        min_value=Decimal(constants.MIN_TEMPERATURE),
        max_value=Decimal(constants.MAX_TEMPERATURE),
        max_digits=10,
        decimal_places=None,
    )
    humidity = serializers.DecimalField(
        min_value=Decimal(constants.MIN_HUMIDITY),
        max_value=Decimal(constants.MAX_HUMIDITY),
        max_digits=10,
        decimal_places=None,
    )
    precipitation = serializers.DecimalField(
        min_value=Decimal(constants.MIN_PRECIPITATION),
        max_value=Decimal(constants.MAX_PRECIPITATION),
        max_digits=8,
        decimal_places=None,
    )
    wind_direction = serializers.DecimalField(
        min_value=Decimal(constants.MIN_WIND_DIRECTION),
        max_value=Decimal(constants.MAX_WIND_DIRECTION),
        max_digits=10,
        decimal_places=None,
    )
    wind_speed = serializers.DecimalField(
        min_value=Decimal(constants.MIN_WIND_SPEED),
        max_value=Decimal(constants.MAX_WIND_SPEED),
        max_digits=10,
        decimal_places=None,
    )

    def validate_temperature(self, temperature):
        return round(temperature, 2)

    def validate_humidity(self, humidity):
        return round(humidity, 2)

    def validate_precipitation(self, precipitation):
        return round(precipitation, 1)

    def validate_wind_direction(self, wind_direction):
        return round(wind_direction, 2)

    def validate_wind_speed(self, wind_speed):
        return round(wind_speed, 2)

    class Meta:
        model = Measurement
        fields = (
            "temperature",
            "humidity",
            "precipitation",
            "wind_direction",
            "wind_speed",
        )


class CreateMeasurementSerializer(UpdateMeasurementSerializer):
    station = serializers.SlugRelatedField(
        many=False, slug_field="uuid", queryset=Station.objects.all(), required=True
    )
    date_captured = serializers.DateTimeField(
        input_formats=constants.VALID_DATETIME_INPUT_FORMATS
    )

    class Meta:
        model = Measurement
        fields = (
            "station",
            "date_captured",
            "temperature",
            "humidity",
            "precipitation",
            "wind_direction",
            "wind_speed",
        )


class MeasurementSerializer(serializers.ModelSerializer):
    station = BaseStationSerializer()

    class Meta:
        model = Measurement
        fields = (
            "uuid",
            "station",
            "date_captured",
            "date_registered",
            "temperature",
            "humidity",
            "precipitation",
            "wind_direction",
            "wind_speed",
        )
