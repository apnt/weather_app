from django.urls import path

from weather_app.auth.views import AuthView

urlpatterns = [
    path("auth/", AuthView.as_view(), name="authenticate"),
]
