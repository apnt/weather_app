from weather_app.common.permissions import IsSuperuser


class MeasurementsPermissions(IsSuperuser):
    """Permissions for the measurements endpoints"""

    def has_permission(self, request, view):
        # All authenticated users, can use GET (actions "list" and "retrieve) to see available measurements
        if view.action in {"list", "retrieve"}:
            return self.user_is_authenticated(request)
        if view.action in {"create"}:
            return self.user_is_authenticated(request) and (
                self.user_is_superuser(request) or request.user.is_service_station
            )
        return self.user_is_superuser(request)
