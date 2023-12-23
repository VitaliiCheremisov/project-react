from rest_framework import exceptions, permissions


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


class IsAuthenticatedOrDelete(permissions.BasePermission):
    """Разрешение на удаление только авторизованному."""
    def has_permission(self, request, view):
        if request.method == 'DELETE':
            return True
        if request.user and request.user.is_authenticated:
            return True
        raise exceptions.AuthenticationFailed('Неавторизован')
