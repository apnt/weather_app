from weather_app.common.permissions import IsSuperuser


class StationsPermissions(IsSuperuser):
    """Permissions for the stations endpoints"""

    def has_permission(self, request, view):
        # All users, even unauthenticated, can use GET
        # (actions "list" and "retrieve) to see available stations
        return view.action in {"list", "retrieve"} or self.user_is_superuser(request)
