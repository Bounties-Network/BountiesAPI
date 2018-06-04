from rest_framework import permissions

class AuthenticationPermission(permissions.BasePermission):
    message = 'Unauthorized'

    def has_permission(self, request, view):
        return request.is_logged_in


class UserIDMatches(permissions.BasePermission):
    message = 'Unauthorized'

    def has_permission(self, request, view):
        user_id = view.kwargs.get('user_id', -1)

        if request.current_user:
            return request.current_user.id == int(user_id)
        return False


class UserObjectPermissions(permissions.BasePermission):
    message = 'Unauthorized'

    def has_object_permission(self, request, view, obj):
        return obj.user == request.current_user
