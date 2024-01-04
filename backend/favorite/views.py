from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ValidationError

from recipes.models import Recipe

from .models import Favorite
from .serializers import FavoriteSerializer


class FavoriteViewSet(viewsets.ModelViewSet):
    """Работа с избранными рецептами."""

    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        """Добавление рецепта в избранное."""
        serializer.save(user=self.request.user,
                        recipe=Recipe.objects.get(id=self.kwargs['id']))

    def get_serializer(self, *args, **kwargs):
        """Изменение данных из запроса."""
        data = {'user': self.request.user.id, 'recipe': self.kwargs['id']}
        kwargs['data'] = data
        return super().get_serializer(*args, **kwargs)

    def get_object(self):
        """Получение объекта для удаления."""
        recipe = get_object_or_404(Recipe, id=self.kwargs['id'])
        queryset = Favorite.objects.filter(
            user=self.request.user,
            recipe__id=recipe.id
        )
        if not queryset:
            raise ValidationError('Рецепта не существует.')
        return queryset.first()
