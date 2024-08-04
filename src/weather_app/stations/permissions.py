from weather_app.common.permissions import IsSuperuser


class StationsPermissions(IsSuperuser):
    """Permissions for the stations endpoints"""

    def has_permission(self, request, view):
        # All authenticated users, can use GET (actions "list" and "retrieve) to see available stations
        return (
            self.user_is_authenticated(request)
            if view.action in {"list", "retrieve"}
            else self.user_is_superuser(request)
        )
