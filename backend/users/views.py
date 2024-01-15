from djoser.views import UserViewSet as DjoserViewSet
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from follow.serializers import FollowSerializer


class CustomUserViewSet(DjoserViewSet):
    """Работа c моделью пользователя."""

    def get_permissions(self):
        """Настройка разрешения."""
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
        self.queryset = request.user.follower.all()
        return self.list(request)
