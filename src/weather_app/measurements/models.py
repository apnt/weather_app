from uuid import uuid4

from django.db import models

from weather_app.stations.models import Station


class Measurement(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid4)
    date_captured = models.DateTimeField()
    date_registered = models.DateTimeField(auto_now_add=True)
    station = models.ForeignKey(
        Station,
        on_delete=models.PROTECT,
        related_name="measurements",
        related_query_name="measurement",
    )

    # Degrees Celsius
    temperature = models.DecimalField(max_digits=5, decimal_places=2)

    # Percentage
    humidity = models.DecimalField(max_digits=5, decimal_places=2)

    # mm
    precipitation = models.DecimalField(max_digits=5, decimal_places=1)

    # Degrees clockwise from north where 0/360 is the wind from the north
    wind_direction = models.DecimalField(max_digits=5, decimal_places=2)

    # m/s
    wind_speed = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.station.name} - {self.date_captured}"

    @property
    def temp_fahrenheit(self):
        return self.temperature * (9 / 5) + 32

    @property
    def temp_kelvin(self):
        return self.temperature + 273

    class Meta:
        ordering = ("date_captured",)
        unique_together = ("station", "date_captured")
