from django.conf.urls import include
from django.urls import re_path
from rest_framework import routers

from weather_app.measurements.views import MeasurementViewSet

router = routers.DefaultRouter()
router.register(r"measurements", MeasurementViewSet, basename="users")

urlpatterns = [
    re_path(r"", include(router.urls)),
]
