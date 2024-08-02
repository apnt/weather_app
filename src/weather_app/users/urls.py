from django.conf.urls import include
from django.urls import re_path
from rest_framework import routers

from weather_app.users.views import UserViewSet

router = routers.DefaultRouter()
router.register(r"users", UserViewSet, basename="users")

urlpatterns = [
    re_path(r"", include(router.urls)),
]
