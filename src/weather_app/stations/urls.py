from django.conf.urls import include
from django.urls import re_path
from rest_framework import routers

from weather_app.stations.views import StationViewSet

router = routers.DefaultRouter()
router.register(r"stations", StationViewSet, basename="users")

urlpatterns = [
    re_path(r"", include(router.urls)),
]
