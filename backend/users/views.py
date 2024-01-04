from djoser.views import UserViewSet as DjoserViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from recipes.serializers import FollowSerializer


class CustomUserViewSet(DjoserViewSet):
    """Работа c моделью пользователя."""

    def get_permissions(self):
        """Настройка разрешения для эндпоинта /me."""
        if self.action == 'me':
            return [IsAuthenticated()]
        return super().get_permissions()

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='subscriptions',
        url_name='subscriptions'
    )
    def subscriptions(self, request):
        """Получение подписок пользователя."""
        queryset = request.user.follower.all()
        page = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            page,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
