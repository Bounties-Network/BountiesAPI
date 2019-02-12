from rest_framework import permissions


class AuthenticationPermission(permissions.BasePermission):
    message = 'Unauthorized'

    def has_permission(self, request, view):
        return request.is_logged_in


class UserIDMatches(permissions.BasePermission):
    message = 'Unauthorized'

    def has_permission(self, request, view):
        public_address = view.kwargs.get('public_address', -1)

        if request.current_user:
            return request.current_user.public_address == public_address.lower()
        return False


class IsSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.current_user


class UserObjectPermissions(permissions.BasePermission):
    message = 'Unauthorized'

    def has_object_permission(self, request, view, obj):
        return obj.user == request.current_user


class ApplicantPermissions(permissions.BasePermission):
    message = 'Unauthorized'

    def has_object_permission(self, request, view, obj):
        return obj.bounty.user == request.current_user
