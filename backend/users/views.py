from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from djoser.views import UserViewSet as DjoserViewSet

from recipes.paginators import CustomPaginator
from recipes.serializers import FollowSerializer


class CustomUserViewSet(DjoserViewSet):
    """Работа c моделью пользователя."""

    pagination_class = CustomPaginator

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
