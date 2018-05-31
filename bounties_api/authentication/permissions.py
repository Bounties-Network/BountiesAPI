from rest_framework import permissions

class AuthenticationPermission(permissions.BasePermission):
    message = 'Unauthorized'

    def has_permission(self, request, view):
        return request.is_logged_in


class UserIDMatches(permissions.BasePermission):
    message = 'Unauthorized'

    def has_permission(self, request, view):
        if request.GET:
            user_id = request.GET.get('user_id', None)
        if request.POST:
            user_id = request.POST.get('user_id', None)

        return bool(user_id)


class UserObjectPermissions(permissions.BasePermission):
    message = 'Unauthorized'

    def has_object_permissions(self, request, view, obj):
        return obj.user == request.current_user