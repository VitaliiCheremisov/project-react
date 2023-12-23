from rest_framework import permissions
from rest_framework.exceptions import NotAuthenticated


class IsAuthenticatedOrIsMe(permissions.BasePermission):
    """Специальный пермишн для djoser."""

    def has_permission(self, request, view):
        if (request.path == '/api/users/me/'
                and not request.user.is_authenticated):
            raise NotAuthenticated
        return (request.user and request.user.is_authenticated
                or request.path.startswith('/api/users/'))
