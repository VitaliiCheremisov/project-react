from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or request.user \
            and request.user.is_staff


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Разрешения для автора записи."""
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class IsAutheticatedOrReadOnlyOrIsMe(permissions.BasePermission):
    """Разрешение для эндпоинта /me."""

    def has_permission(self, request, view):
        if view.action == 'me':
            return request.user.is_authenticated
        else:
            return (request.method in permissions.SAFE_METHODS
                    or request.user.is_authenticated)
