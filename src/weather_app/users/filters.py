from rest_framework.filters import BaseFilterBackend


class UserTypeFilter(BaseFilterBackend):
    """Filtering by user type (admin, service_station, viewer)"""

    def filter_queryset(self, request, queryset, view):
        valid_user_types_queries = {
            "admin": {"is_superuser": True},
            "service_station": {"is_service_station": True},
            "viewer": {"is_superuser": False, "is_service_station": False},
        }
        user_type = request.query_params.get("user_type")
        if user_type is not None:
            filter_query = valid_user_types_queries.get(user_type, None)
            if filter_query is not None:
                return queryset.filter(**filter_query)
            return queryset.none()
        return queryset
