from weather_app.common.permissions import IsSuperuser


class UsersPermissions(IsSuperuser):
    """Permissions for the users endpoints"""

    def has_permission(self, request, view):
        # All users, even unauthenticated, can use POST (action "create") to register
        return view.action == "create" or self.user_is_superuser(request)
