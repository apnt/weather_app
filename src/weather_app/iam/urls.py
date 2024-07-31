from django.conf.urls import include
from django.urls import path
from django.urls import re_path
from rest_framework import routers

from weather_app.iam.auth.views import AuthView
from weather_app.iam.users.views import UserViewSet

router = routers.DefaultRouter()
router.register(r"users", UserViewSet, basename="users")

urlpatterns = [
    re_path(r"", include(router.urls)),
    path("auth/", AuthView.as_view(), name="authenticate"),
]
