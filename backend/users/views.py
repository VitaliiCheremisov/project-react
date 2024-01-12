from djoser.views import UserViewSet as DjoserViewSet
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from follow.serializers import FollowSerializer


class CustomUserViewSet(DjoserViewSet):
    """Работа c моделью пользователя."""

    def get_permissions(self):
        """Настройка разрешения для эндпоинта /me."""
        if self.action == 'retrieve':
            return [IsAuthenticatedOrReadOnly()]
        return super().get_permissions()

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='subscriptions',
        url_name='subscriptions',
        serializer_class=FollowSerializer
    )
    def subscriptions(self, request):
        """Получение подписок пользователя."""
        queryset = request.user.follower.all()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
