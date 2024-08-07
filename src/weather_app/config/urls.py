"""
URL configuration for weather_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from weather_app.config.views import health_check_view

urlpatterns = [
    path("api/v1/ping/", health_check_view),
    path("api/v1/admin/", admin.site.urls),
    # API Schema endpoints
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    # API Schema UIs endpoints
    path(
        "api/v1/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/v1/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    # Users urls
    path("api/v1/", include("weather_app.users.urls")),
    # Auth endpoints
    path("api/v1/", include("weather_app.auth.urls")),
    # Stations endpoints
    path("api/v1/", include("weather_app.stations.urls")),
    # Measurements endpoints
    path("api/v1/", include("weather_app.measurements.urls")),
]
