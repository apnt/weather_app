from uuid import uuid4

from django.conf import settings
from django.db import models


class Station(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, primary_key=False
    )
    uuid = models.UUIDField(unique=True, default=uuid4)
    name = models.CharField(unique=True, max_length=50)
    latitude = models.DecimalField(max_digits=8, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    date_created = models.DateTimeField(auto_now_add=True)

    @property
    def is_active(self):
        return self.user.is_active

    class Meta:
        ordering = ("name",)
