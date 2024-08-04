from uuid import uuid4

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone

from weather_app.users.management.managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    uuid = models.UUIDField(unique=True, default=uuid4)
    email = models.EmailField(unique=True, blank=False, null=False)
    is_superuser = models.BooleanField(default=False)
    is_service_station = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    # Set custom manager
    objects = CustomUserManager()

    # Set field used as username
    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_superuser

    class Meta:
        ordering = ("date_joined",)
