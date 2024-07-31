import json

from django.http import HttpResponse
from rest_framework import status


def health_check_view(request):
    """Simple view for checking health status."""
    return HttpResponse(
        json.dumps({"status": "ok"}),
        status=status.HTTP_200_OK,
        content_type="application/json",
    )
