"""Configuration for the API Schema generation for users' endpoints"""

from drf_spectacular.utils import OpenApiParameter

from weather_app.users.serializers import UserSerializer

list_users = {
    "description": "Fetches all users (paginated).",
    "parameters": [
        OpenApiParameter(
            name="order_by",
            description="Which field to use when ordering the results. By default ascending order is used. "
            "For descending order use a dash before the field e.g. '-email'",
            type=str,
            enum=["date_joined", "last_login", "email"],
        ),
        OpenApiParameter(
            name="search",
            description="A search term that is used to find matches in the email field.",
            type=str,
        ),
        OpenApiParameter(
            name="user_type",
            description="A user type to filter the results.",
            type=str,
            enum=["admin", "service_station", "viewer"],
        ),
    ],
}
retrieve_user = {"description": "Fetches the user with the given uuid."}
create_user = {"responses": {201: UserSerializer}}
partial_update_user = {"responses": {200: UserSerializer}}
